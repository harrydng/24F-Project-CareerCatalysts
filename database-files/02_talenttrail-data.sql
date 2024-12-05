USE talentTrail;
-- 20) Role Instances


INSERT INTO role(roleName)
VALUES ('Co-op Advisor'),
       ('Student');


INSERT INTO role(roleName)
VALUES ('Employer'),
       ('Systems Admin');


SELECT *
FROM role;


-- 10) Projects Instances


INSERT INTO projects(gitRepository, description, name)
VALUES ('repo1', 'Twitter Sentiment Analysis', 'Sentiment Analysis'),
       ('repo2', 'Calculator app made using JavaFX', 'Calculator App');


SELECT *
FROM projects;


-- 12) Certifications Instances


INSERT INTO certifications(name)
VALUES ('AWS Cloud Practitioner'),
       ('Google Data Analytics');


SELECT *
FROM certifications;

-- 5) Skill Instances


INSERT INTO skills (name, description)
VALUES ('Python Programming', 'Proficient in Python for data analysis and development.'),
       ('Web Development', 'Experienced in building responsive web applications.');

SELECT *
FROM skills;


-- 6) Badges Instances


INSERT INTO badge(badgeName)
VALUES ( 'Data Wizard'),
       ('Web Dev GOAT');


SELECT *
FROM badge;


-- 1) User Instances
-- advisor
INSERT INTO user (username, email, status, firstName, middleName, lastName, password_hash, roleId)
VALUES ('jdoe', 'jdoe@example.com', 1, 'John', 'Michael', 'Doe', 'hashed_password_1', 1),
       ('asmith', 'asmith@example.com', 1, 'Anna', NULL, 'Smith', 'hashed_password_2', 1),
       -- student
       ('Arnav619', 'arnavrathore619@gmail.com', 1, 'Arnav', NULL, 'Rathore', 'password', 2),
       ('water_bottle', 'waterbottle@gmail.com', 1, 'Water', NULL, 'Bottle', 'password', 2),
       ('Sean123', 'sean123@gmail.com', 1, 'Sean', 'Narula', 'Isaac', 'password', 2);


-- admin
INSERT INTO user (username, email, status, firstName, middleName, lastName, password_hash, roleId)
VALUES ('DiscordMod', 'Admin1@gmail.com', 1, 'Jonathan', NULL, 'Joestar', 'password', 4),
       ('Mod2', 'Admin2@gmail.com', 1, 'Joseph', NULL, 'Joestar', 'password', 4);


-- employer
INSERT INTO user(username, email, status, firstName, middleName, lastName, password_hash, roleId)
VALUES ('Emp1', 'Google@gmail.com', 1, 'Sundar', NULL, 'Pichai', 'password', 3),
       ('Emp2', 'Apple@email.com', 1, 'Tim', NULL, 'Cook', 'password', 3);


SELECT *
FROM user;


-- 2) Advisor Instances
INSERT INTO advisor_profile (advisorId, department)
VALUES (1, 'Computer Science Department'),
       (2, 'Mechanical Engineering Department');


SELECT *
FROM advisor_profile;


-- 3) Student Profile Instances
INSERT INTO student_profile (nuId, dob, major, minor, year, advisorId)
VALUES (3, '2002-12-05', 'Computer Science', 'Mathematics', 2021, 1),
       (5, '2003-07-10', 'Mech E', 'DS', 2025, 1),
       (4, '2003-01-02', 'Data Science', NULL, 2022, 2);


SELECT *
FROM student_profile;


-- 4) student_skills instances
INSERT INTO student_skills(nuid, skillId)
VALUES (3, 1),
       (5, 2),
       (4, 2);


SELECT *
FROM student_skills;


-- 8) Admin Profile instances


INSERT INTO admin_profile(adminId)
VALUES (5),
       (6);


SELECT *
FROM admin_profile;


-- 9) Employer Profile Instances


INSERT INTO employer_profile(employerId, description, link)
VALUES (7, 'It is google', 'google.com'),
       (8, 'It is apple', 'apple.com');


SELECT * FROM employer_profile;


-- 13) Student_Certification Instances


INSERT INTO student_certifications(nuid, certificationid)
VALUES (3, 1),
       (5, 1),
       (4, 1);


INSERT INTO student_certifications(nuid, certificationid)
VALUES (3, 2);


SELECT *
FROM student_certifications;


-- 14) Courses Instances


INSERT INTO courses(courseName, description, courseNumber)
VALUES ('OOD', 'Learn Object Oriented Programming and Design Patters', 3500),
       ('Database Design', 'Learn SQL', 3200);


SELECT *
FROM courses;


-- 15) Student_courses Instances


INSERT INTO student_courses(nuId, courseId)
VALUES (3, 1),
       (5, 2),
       (4, 2);


SELECT *
FROM student_courses;


-- 16) Job Posting Instances


INSERT INTO job_posting(position, description, pay, timePeriod, positionType,
                        employmentType, workLocation, employerId, isActive)
VALUES ('Software Engineering', 'Description1', 25.00, 'July to December', 'Full Stack SWE', 'Co-op',
        'Remote', 7, 1),
       ('Financial Analyst','Description2', 69.00, 'July to December', 'Assocaite ML Engineer',
         'Full Time', 8, 8, 1);


SELECT *
from job_posting;


-- 18) Alert Instances


INSERT INTO alert(messages, priority, title)
VALUES ('Warning 1', 1, 'Big warning'),
       ('Warning 2', 2, 'Smaller Warning');

SELECT *
FROM alert;

-- 17) Activity Log Instances


INSERT INTO activity_log(alertId, description)
VALUES (1, 'Activity 1'),
       (2, 'Activity 2');


SELECT *
FROM activity_log;

-- 11) Personalities Instances


INSERT INTO personalities(description, interests, softSkills, leadership, nuId)
VALUES ('Active Listener, patient, and good communicator', 'Design Process',
        'Presenting and writing', 'Strong', 3),
       ('Fast Reader and quick Coder', 'Building Web Apps', 'Teamwork', 'Very Strong', 4);


SELECT *
FROM personalities;

-- 19) System Metrics Instances


INSERT INTO metrics(errorRate, serverLoad, responseTime)
VALUES (2.55, 5.22, 1.0),
       (3.11, 4.11, 5.6);


SELECT *
FROM metrics;

-- 23) Student Reports Instances


INSERT INTO student_reports(nuId, advisorId, notes, status)
VALUES (3, 1, 'Great Student', 1),
       (5, 1, NULL, 1),
       (4, 2, 'Good Student', 2);


SELECT *
FROM student_reports;


-- 25) Job Application Instances


INSERT INTO job_applications(jobId, nuId)
VALUES (1, 3),
       (1, 5),
       (2, 4);


SELECT *
FROM job_applications;


-- 26) Student_profile_jobs Instances
INSERT INTO student_projects(nuid, projectid)
VALUES (3, 1),
       (5, 1),
       (4, 2);


SELECT *
FROM student_projects;


-- 27 Job_Posting_skills Instances
INSERT INTO job_posting_skills(jobId, skillId)
VALUES (1, 1),
       (2, 2);


SELECT *
FROM job_posting_skills;


-- 28 Student_Badges Instances
INSERT INTO student_badges(nuid, badgeid)
VALUES (3, 1),
       (5, 1),
       (4, 2);


SELECT *
FROM student_badges;
