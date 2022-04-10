# Polling tool and feedback uploader.

## Simple application to learn how to connect REST API to MongoDB in Python 3.9.6.

User can create, read, update or delete question with answers.   
User also can answer to any question that already exists in database.  
Application allows user to perform CRUD operations on feedback forms, where one can share opinion.

## How to run

To run this application on docker containers you need to run "docker-compose up --build".

To run this application locally:

- install Python in version 3.9.6,
- in project directory use command 'pip install -r requirements.txt',
- in project directory use command 'python main.py'.

MongoDB has to be available on localhost:27017 (use command 'docker-compose up db' to create MongoDB
container).

## Documentation

To access Swagger head to "http://localhost:8000/docs"
