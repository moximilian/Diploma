# Tutors Hub

**Made entierly by Maxim Syrov in 2025**

Originaly this project started as a Final Qualifying Work from Moscow Polytech Univercity,
Specialty is Corporate information technology

## Description:

Build your timetable, manage your groups, connect with pupils. Made spicificly for teacher's and tutor's needs!

## Backend

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white) 3.11
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white) 0.136.1
- ![SqlAlchemy](https://img.shields.io/badge/SQLAlchemy-306998?logo=python&logoColor=white) 2.0.49
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 14.4-alpine
- ![Docker](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white) 3.8
- ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) 1.19.3


## Frontend

- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript) ES2023
- ![Vue](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D) 3.5.13

## Project table of contents

- /src/backend - Server side src
- /src/frontend - Client side src
- /docs - Documentation
- /examples - Usage examples

## Functionality:

- User registration (manually or via OAUth 2)
- User authentication
- Editing own data
- Deleting account
- Storing authentication session, log out when the session expires
- Creating, searching, editing, and deleting participant groups
- Join open groups
- Send a request to join closed groups
- Leave a group
- Create a group invitation link
- Creating, editing, searching, and deleting slots
- Joining (booking) a slot
- Viewing personal attendance statistics for various activities with filters
- Viewing attendance statistics for an entire group or a specific activity
- Viewing personal schedule of planned activities (as both organizer and participant)
- Tracking attendance, payments, and other attributes for each activity
- Sending notifications about rescheduling activities

## Set up and run

`cd src` - move to working direcroty

`docker-compose --env-file .env up` - Build all images and run containers

API will be avaliable at `8000` port

Client side will be avaliable at `localhost:1024`, made possible by NGINX
