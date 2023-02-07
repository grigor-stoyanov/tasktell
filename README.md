# Tasktell
This was my first SoftUni graduation project for the Python Course Path. Its meant to showcase my skills
in Django Web Framework and Python. It is a project-manager application aimed to make tracking of projects
and tasks between a group of people simpler.


## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Status](#status)
* [Inspiration](#inspiration)
* [Other](#other)

## General Info
**Create** or **join** new projects trough the interface or via a **invite link** sent asynchronously by the app. Manage members and **roles** between projects. **Add, remove or track** new tasks on your project in a to-do list fashion and track your project **completion**. Communicate with members of your project in **real time**. Built on Django using **Class Based** Views and Templates with **Bootstrap**. Not supported for mobile.

The project also contains **form validation** for each form input(register,login,create project), **unit tests** covering different edge-cases for the main and auth apps and **error handling** of certain edge cases between users and members of project model and registered models to the base django admin pannel.

It is salso **configured** for deployment on Heroku with .env, cloudinary support and .procfile


## Features
* All CRUD Operations
* Custom User Model
* Form Generation with Bootsrap front-end Design
* Complex Relational Database with Different User Roles
* Asynchronous Email Function for Users
* Real Time Messaging Function between Users
* Heroku Deployment Configuration with Environment Variables


## Technologies
* [Bootstrap 5](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
* [Django 4](https://docs.djangoproject.com/en/4.0/)  
* [Celery 5.2](https://docs.celeryq.dev/en/stable/)
* [Channels 3](https://channels.readthedocs.io/en/3.x/)


## Screenshots
![image](https://user-images.githubusercontent.com/76039296/217268932-ec6f4714-c39b-4dde-9f99-94b7756e6058.png)
![image](https://user-images.githubusercontent.com/76039296/217269329-9991773b-b52b-4842-ba20-c3c7e40575cc.png)
![image](https://user-images.githubusercontent.com/76039296/217269439-7a6067e6-e152-4049-9140-fb8652663ce7.png)
![image](https://user-images.githubusercontent.com/76039296/217269816-93c48359-e9d5-4d92-b2b7-9192a27b3d63.png)


## Setup

Clone repo(```git clone https://github.com/grigor-stoyanov/tasktell```)

### Prerequesites
Set up a virtual environment
* venv(```python -m venv .venv```)

Linux(```source .venv/bin/activate```)  
Windows(```.venv/Scripts activate```)

Install Docker to compose database configuration or add your own configuration urself.
* [Docker](https://docs.docker.com/) - Once you have cloned the repository you can use the docker-compose.yml from base folder(```docker-compose up```)

### Installation
1. Install Dependencies(```pip install -r requirements.txt```)  
2. Clone database schema(```python -m manage migrate```)  
3. Run application(```python -m manage runserver```)
> **Note** You might want to add your your own configurations(if any) for database and email host in the .env file


## Status
Project is completed and no further improvements are planned as of now.


## Inspiration
App frontend and main functions mostly inspired by [Trello](https://trello.com/en)


## Other
| ![image](https://user-images.githubusercontent.com/76039296/217279449-93faa114-667a-4183-96cb-60d5393da610.png) |
|-|
[Linkedin](https://www.linkedin.com/feed/)