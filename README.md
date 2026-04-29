# Tutors Hub

**Made entierly by Maxim Syrov in 2025**

Originaly this project started as a Final Qualifying Work from Moscow Polytech Univercity,
Specialty is Corporate information technology

## Description:

Build your timetable, manage your groups, connect with pupils. Made spicificly for teacher's and tutor's needs!

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

Docker version >= 3.8

`cd src` - move to working direcroty

`docker-compose --env-file .env up` - Build all images and run containers

API will be avaliable at `8000` port

Client side will be avaliable at `localhost:1024`, made possible by NGINX
