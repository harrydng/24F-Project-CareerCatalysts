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
       ('repo2', 'Calculator app made using JavaFX', 'Calculator App'),
       ('repo3', 'E-commerce platform built with Django', 'E-Commerce Platform'),
       ('repo4', 'Weather forecasting app using OpenWeather API', 'Weather App'),
       ('repo5', 'Portfolio website built with React.js', 'Portfolio Website'),
       ('repo6', 'Library management system using Spring Boot', 'Library Management System'),
       ('repo7', 'Real-time chat application with WebSocket', 'Chat Application'),
       ('repo8', 'Task management app with Flask and SQLite', 'Task Manager'),
       ('repo9', 'Expense tracker using Vue.js and Firebase', 'Expense Tracker'),
       ('repo10', 'AI-based spam email classifier with Python', 'Spam Classifier'),
       ('repo11', 'Health monitoring app using IoT devices', 'Health Monitor App'),
       ('repo12', 'Online exam portal built with Angular', 'Online Exam Portal'),
       ('repo13', 'Food delivery system with Node.js and MongoDB', 'Food Delivery System'),
       ('repo14', 'Blogging platform with Ruby on Rails', 'Blogging Platform'),
       ('repo15', 'Image gallery with infinite scrolling using React.js', 'Image Gallery'),
       ('repo16', 'Online bookstore using PHP and MySQL', 'Online Bookstore'),
       ('repo17', 'Music recommendation system with TensorFlow', 'Music Recommender'),
       ('repo18', 'Fitness tracker app with React Native', 'Fitness Tracker'),
       ('repo19', 'Virtual reality game built using Unity', 'VR Game'),
       ('repo20', 'News aggregator using Python and BeautifulSoup', 'News Aggregator'),
       ('repo21', 'Personal finance dashboard with Django', 'Finance Dashboard'),
       ('repo22', 'Stock market prediction app with R', 'Stock Prediction App');


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
       ('Web Development', 'Experienced in building responsive web applications.'),
       ('Java Programming', 'Skilled in Java for object-oriented programming and backend development.'),
       ('Data Analysis', 'Expertise in analyzing and visualizing data using tools like Pandas and Matplotlib.'),
       ('Machine Learning', 'Proficient in building predictive models using Scikit-Learn and TensorFlow.'),
       ('Database Management', 'Experienced in designing and managing databases with MySQL and PostgreSQL.'),
       ('Cloud Computing', 'Familiar with deploying applications using AWS and Azure.'),
       ('DevOps', 'Knowledge of CI/CD pipelines and containerization tools like Docker and Kubernetes.'),
       ('Cybersecurity', 'Understanding of security protocols and penetration testing.'),
       ('JavaScript', 'Experienced in creating interactive web interfaces using JavaScript.'),
       ('React.js', 'Skilled in building component-based web applications using React.js.'),
       ('Node.js', 'Proficient in developing server-side applications with Node.js.'),
       ('C++ Programming', 'Experienced in C++ for competitive programming and system-level development.'),
       ('API Development', 'Skilled in building RESTful APIs with Flask and Django.'),
       ('UI/UX Design', 'Proficient in creating user-friendly designs using Figma and Adobe XD.'),
       ('Mobile App Development', 'Experience in building cross-platform mobile apps with React Native.'),
       ('Artificial Intelligence', 'Knowledge of AI algorithms and their applications in problem-solving.'),
       ('Networking', 'Understanding of network protocols and configuration.'),
       ('Big Data', 'Proficient in working with large datasets using Apache Spark and Hadoop.'),
       ('Project Management', 'Skilled in managing projects using Agile methodologies.'),
       ('Communication Skills', 'Strong written and verbal communication skills for collaboration.'),
       ('Leadership', 'Experience in leading teams and managing tasks effectively.');


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
VALUES  ('jdoe', 'jdoe@example.com', 1, 'John', 'Michael', 'Doe', 'hashed_password_1', 1),
        ('asmith', 'asmith@example.com', 1, 'Anna', NULL, 'Smith', 'hashed_password_2', 1),
       -- student
        ('JDoe', 'JD@gmail.com', 1, 'John', NULL, 'Doe', 'password', 2),
        ('water_bottle', 'waterbottle@gmail.com', 1, 'Water', NULL, 'Bottle', 'password', 2),
        ('jsmith', 'jsmith@gmail.com', 1, 'John', NULL, 'Smith', 'password123', 2),
        ('mbrown', 'mbrown@gmail.com', 1, 'Mary', NULL, 'Brown', 'password123', 2),
        ('albert_einstein', 'einstein@gmail.com', 1, 'Albert', NULL, 'Einstein', 'password', 2),
        ('jdoe123', 'jdoe123@gmail.com', 1, 'Jane', NULL, 'Doe', 'securepass', 2),
        ('pstar', 'pstar@gmail.com', 1, 'Patrick', NULL, 'Star', 'mypassword', 2),
        ('superman', 'superman@gmail.com', 1, 'Clark', NULL, 'Kent', 'krypton123', 2),
        ('brucewayne', 'wayne@gmail.com', 1, 'Bruce', NULL, 'Wayne', 'batcave', 2),
        ('peter_parker', 'spiderman@gmail.com', 1, 'Peter', NULL, 'Parker', 'spidey123', 2),
        ('thor_odinson', 'thor@gmail.com', 1, 'Thor', NULL, 'Odinson', 'mjolnir', 2),
        ('tonystark', 'ironman@gmail.com', 1, 'Tony', NULL, 'Stark', 'arcreactor', 2),
        ('harrypotter', 'harry@gmail.com', 1, 'Harry', NULL, 'Potter', 'expelliarmus', 2),
        ('hermionegranger', 'hermione@gmail.com', 1, 'Hermione', NULL, 'Granger', 'hogwarts', 2),
        ('ronweasley', 'ron@gmail.com', 1, 'Ron', NULL, 'Weasley', 'chesschamp', 2),
        ('frodo_baggins', 'frodo@gmail.com', 1, 'Frodo', NULL, 'Baggins', 'ringbearer', 2),
        ('aragorn', 'aragorn@gmail.com', 1, 'Aragorn', NULL, 'Elessar', 'anduril', 2),
        ('legolas', 'legolas@gmail.com', 1, 'Legolas', NULL, 'Greenleaf', 'arrow123', 2),
        ('gandalf', 'gandalf@gmail.com', 1, 'Gandalf', NULL, 'Grey', 'you_shall_not_pass', 2),
        ('samwise', 'sam@gmail.com', 1, 'Samwise', NULL, 'Gamgee', 'loyalfriend', 2),
        ('natasha', 'natasha@gmail.com', 1, 'Natasha', NULL, 'Romanoff', 'widowpass', 2),
        ('steverogers', 'cap@gmail.com', 1, 'Steve', NULL, 'Rogers', 'shield123', 2),
        ('hulk', 'hulk@gmail.com', 1, 'Bruce', NULL, 'Banner', 'smash', 2),
        ('drstrange', 'strange@gmail.com', 1, 'Stephen', NULL, 'Strange', 'slingring', 2),
        ('blackpanther', 'panther@gmail.com', 1, 'T\Challa', NULL, 'Black Panther', 'wakanda', 2),
        ('scarletwitch', 'scarlet@gmail.com', 1, 'Wanda', NULL, 'Maximoff', 'chaosmagic', 2),
        ('hawkeye', 'hawkeye@gmail.com', 1, 'Clint', NULL, 'Barton', 'archery123', 2),
        ('antman', 'antman@gmail.com', 1, 'Scott', NULL, 'Lang', 'quantumrealm', 2),
        ('groot', 'iamgroot@gmail.com', 1, 'I', NULL, 'Am Groot', 'iamgroot', 2),
        ('rocket', 'rocket@gmail.com', 1, 'Rocket', NULL, 'Raccoon', 'blasters', 2),
        ('gamora', 'gamora@gmail.com', 1, 'Gamora', NULL, 'ZenWhoberi', 'nebula123', 2),
        ('starlord', 'starlord@gmail.com', 1, 'Peter', NULL, 'Quill', 'mixtape', 2),
        ('drax', 'drax@gmail.com', 1, 'Drax', NULL, 'The Destroyer', 'invisible', 2),
        ('vision', 'vision@gmail.com', 1, 'Vision', NULL, 'Synthetic', 'mindstone', 2);



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
       (4, '2003-01-02', 'Data Science', NULL, 2022, 2),
       (5, '2003-02-03', 'Cybersecurity', NULL, 2024,2),
       (6, '2000-01-02', 'Computer Science', 'Environmental Studies', 2025,1);


SELECT *
FROM student_profile;


-- 4) student_skills instances
INSERT INTO student_skills(nuid, skillId)
VALUES (3, 1),
       (4, 2),
       (3,2),
       (3,3),
       (3,4),
       (3,5),
       (3,6),
       (3,7),
       (3,8),
       (3,9),
       (4,9),
       (4,10),
       (5,10),
       (5,11),
       (5,12);

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
       (4, 2, 'Good Student', 2);


SELECT *
FROM student_reports;


-- 25) Job Application Instances


INSERT INTO job_applications(jobId, nuId)
VALUES (1, 3),
       (2, 4);


SELECT *
FROM job_applications;


-- 26) Student_profile_jobs Instances
INSERT INTO student_projects(nuid, projectid)
VALUES (3, 1),
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
       (4, 2);


SELECT *
FROM student_badges;
