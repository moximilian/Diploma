FROM python:3.12

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

COPY *.env /app/

RUN pip install pipenv

RUN pipenv install --ignore-pipfile

COPY ./app /app/

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
