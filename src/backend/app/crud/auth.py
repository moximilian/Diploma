
"""
Logic to work with DB
"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as m
from schemas import UserCreate, UserLogin, UserOut, Token
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from crud.base import BaseCRUD
import api.exceptions as exc
from database import get_db
from jose import JWTError, jwt
from env_constants import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, BASE_URL
import typing as t

import bcrypt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f'/{BASE_URL}/auth/login', auto_error=False)
ALGORITHM = 'HS256'


async def authorised_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserOut:
    """Dependency by which access is guaranteed only to authorised users.
    Token should be placed in Authoruisation Header of any request that requires authorised access.

    Example of Header placement: `Authorization: 'Bearer <your JWT token>'`

    Args:
        `token` (str): JWT access token from headers

    Returns:
        Authorised user

    Raises:
        AuthorisationError: If provided token is mismatched or provided login does not exist

    """
    print(token)
    if Authorisation(db)._is_token_revoked(token):
        raise exc.AuthorisationError('Token is expired. Log in again')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise exc.AuthorisationError('Could not validate credentials')
    except (JWTError, AttributeError):
        raise exc.AuthorisationError('Provided token is invalid')
    user = Authorisation(db)._get_user_by_login(username)
    if user is None:
        raise exc.AuthorisationError('Could not validate credentials')
    return user


class Authorisation(BaseCRUD):
    def __init__(self, db: Session):
        super().__init__(db, m.User)

    def register(self, body: UserCreate) -> UserOut:
        """Register user.

        Args:
            `body` (UserCreate): User data for creation

        Returns:
            New registered user

        Raises:
            exc.ValidationError
        """
        login = body.get('login')
        existing_user = self._get_user_by_login(login)
        if (existing_user):
            raise exc.ValidationEror(
                message='Username already registered', field='login')

        password = body.get('password')
        password_confirm = body.get('password_confirm')
        if (password != password_confirm):
            raise exc.ValidationEror(
                message='Passwords do not match', field='password_confirm')

        hashed_password = self._hash_password(password)

        added_image = self._add_image(body)

        new_user = m.User(name=body.get('name'),
                          surname=body.get('surname'),
                          last_name=body.get('last_name', ''),
                          login=login,
                          password=hashed_password,
                          photo_id=added_image.get('id')
                          )
        new_user = self._save_to_db(new_user)
        return new_user

    def _add_image(self, body: UserCreate) -> t.Union[dict, m.Image]:
        """Add provided image to images table

        Args:
            `body` (UserCreate): request body

        Returns:
            Dict if provided image is empty. \n
            m.Image created in db for save in users
        """
        image_name = body.get('image_name', None)
        if not image_name:
            return {'id': None}

        new_image = m.Image(image_name=image_name,
                            image_data=body.get('image_data', b''))
        return self._save_to_db(new_image)

    def _hash_password(self, password: str) -> str:
        """Hash password with bcrypt module.

        Args:
            password (str): plain password from request.

        Returns:
            hashed_password (str): hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def login(self, auth_creds: UserLogin) -> Token:
        """Authorise user. Create JWT token for future access.

        Args:
            `auth_creds` (UserLogin): Credentials for authorisation

        Returns:
            Token for future access

        Raises:
            ValidationEror if db does not have user with provided login
        """
        user = self._verify_token(
            auth_creds.get('login'), auth_creds.get('password')
        )
        if not user:
            raise exc.ValidationEror(field=['login', 'password'])

        # self._change_failed_attempt(user, 0)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={'sub': user.login}, expires_delta=access_token_expires
        )
        return {'access_token': access_token, 'token_type': 'bearer', 'user_id': user.get('id')}

    def _verify_token(self, username: str, password: str) -> t.Union[UserOut, bool]:
        """Verify if user exists and given password match one in db.

        Args:
            `username` (str): login for auth.
            `password` (str): plain password for auth check.

        Returns:
            False if there is no such user or passwords do not match. \n
            User if one exists.
        """
        user = self._get_user_by_login(username)
        if not user or not self._verify_password(password, user.get('password')):
            return False
        return user

    # def _change_failed_attempt(self, user: m.User, new_count) -> m.User:
    #     """Add failed attempt to user

    #     Args:
    #         user (m.User): current user

    #     Returns:
    #         user (m.User): current user
    #     """
    #     # Make base function
    #     user = self.db.update(m.User).where(m.User.id == user.id ).values(failed_attempts_count=new_count)
    #     self.db.commit()
    #     self.db.refresh(user)
    #     return user

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify plain password's hash matches one in db.

        Args:
            plain_password (str): plain password from request
            hashed_password (str): hash of plain password stored in db

        Returns:
            bool Result of match
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def _get_user_by_login(self, login: str) -> t.Optional[t.Union[UserOut, None]]:
        """Get user by login.

        Args:
            login (str): Login by which search will be run.

        Returns:
            m.User if one exists with provided login else None.
        """
        return self.db.query(m.User).where(
            and_(m.User.login == login, m.User.is_deleted == False)).first()

    def _create_access_token(self, data, expires_delta: timedelta):
        """Create and encode JWT token for future access.

        Args:
            data: login by which jwt check authorisation.
            expires_delta: duration of time by which token is valid.
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def logout(self, token: Token) -> dict:
        """Logout from current session

        Args:
            token (Token): Token to be resttricted
        """
        revoked_token = m.RevokedToken(token=token.access_token)
        self.db.add(revoked_token)
        self.db.commit()
        return {"message": "Successfully logged out"}

    def _is_token_revoked(self, access_token: str) -> bool:
        """Checks if token is revoked.

        Args:
            access_token (str): Token access_token

        Returns:
            bool if token is revoked or not
        """
        return self.db.query(m.RevokedToken).filter(m.RevokedToken.token == access_token).first() is not None
