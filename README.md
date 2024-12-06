# Talent Trail
Team: CarrerCatalysts
Contributed Members: Harry Duong, Arnav Rathore, Yuvraj Kapoor, Sean Issac

## Our Project

NEED TO ADD MORE ==================================

## User Roles, Access, and Control

Currently our project is split up among 4 roles - Student, Advisor, Employer, and The System Administration.

## Project Components

Currently, there are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory

### Setting Up

1. Make a new File in `api ` folder named `.env` based on the `.env.template` file.
1. Start the docker containers. 

## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 

### Getting Started with the RBAC 

1. The pages are organized by Role.  Pages that start with a `2` are related to the *System Administration* role.  Pages that start with a `6` are related to the *Employer* role.  Pages that start with a `7` are related to The *Advisor* role. And, pages that start with a `8` are related to The *Student* role 