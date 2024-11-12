FROM python:3.9

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --ignore-pipfile

COPY . /app

EXPOSE 8000

CMD ["pipenv", "run", "python", "main.py"]