# Talent Trail
Team: CarrerCatalysts
Contributed Members: Harry Duong, Arnav Rathore, Yuvraj Kapoor, Sean Issac

## Our Project

TalentTrail is a data-driven platform that empowers Northeastern University students 
to explore personalized career pathways with unprecedented clarity. 
TalentTrail delivers curated recommendations for classes, projects, and job opportunities 
tailored to each user’s career aspirations by collecting and analyzing data 
on students' majors, minors, skills, and interests. 
    
Traditional career platforms lack the ability to integrate academic planning with personal interests
in a way that feels engaging and intuitive—this is where TalentTrail excels.
    
Our primary users include students, employers, co-op advisors/decision-makers, and system administrators. 
Key features include a personalized career discovery pathway, 
an advanced job search tool that matches students with roles based on personality tags, 
and a gamified experience where students earn badges and climb leaderboards by achieving career milestones. 
    
TalentTrail bridges the gap between education and employment, 
transforming career planning into a proactive, personalized journey.

## User Roles, Access, and Control

Currently our project is split up among 4 roles - Student, Advisor, Employer, and The System Administration.

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Flask, Python
- **Database:** SQL (managed using DataGrip)
- **Containerization:** Docker

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
