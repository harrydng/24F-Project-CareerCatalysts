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
1. Clone the repository in bash
2. cd into the repository
3. Make a new File in `api ` folder named `.env` based on the `.env.template` file.
4. Start the docker containers. 

## Controlling the Containers

- `docker compose build` to build all the containers
- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them.
  


## Getting Started with the RBAC 

1. The pages are organized by Role.  Pages that start with a `2` are related to the *System Administration* role.  Pages that start with a `6` are related to the *Employer* role.  Pages that start with a `7` are related to The *Advisor* role. And, pages from `83` onwards are related to The *Student* role

## Database User ID Ranges

In our database, the `userId` is structured to correspond to specific user profiles. The ranges are defined as follows:

- **Admin Profiles:** `userId` from **1 to 40**
- **Advisor Profiles:** `userId` from **41 to 80**
- **Employer Profiles:** `userId` from **81 to 120**
- **Student Profiles:** `userId` from **121 to 160**

### Important Note:
- When referencing primary keys (`pk`) related to specific user profiles, ensure the `userId` falls within the appropriate range for the respective profile type.
- For example, if working with a **Student Profile**, use a `userId` between **121 and 160**. Similarly, follow the same convention for Admin, Advisor, and Employer profiles.

