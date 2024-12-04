CREATE DATABASE IF NOT EXISTS talentTrail;
USE talentTrail;
SHOW TABLES;


 
-- Skill Table
CREATE TABLE IF NOT EXISTS skills
(
    name        VARCHAR(100),
    skillId     INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT
);

 
CREATE TABLE IF NOT EXISTS badge
(
    badgeId   INT AUTO_INCREMENT PRIMARY KEY,
    badgeName VARCHAR(50)
);

 
-- Project Table
CREATE TABLE IF NOT EXISTS projects
(
    projectId     INT AUTO_INCREMENT PRIMARY KEY,
    gitRepository TEXT,
    description   TEXT,
    name          VARCHAR(50) NOT NULL
);


 
-- Certification Table
CREATE TABLE IF NOT EXISTS certifications
(
    name            TEXT,
    certificationId INT AUTO_INCREMENT PRIMARY KEY
);


 
-- Courses
CREATE TABLE IF NOT EXISTS courses
(
    courseName   VARCHAR(100),
    description  TEXT,
    courseNumber INT,
    courseId     INT AUTO_INCREMENT PRIMARY KEY
);

 
-- System Metrics
CREATE TABLE IF NOT EXISTS metrics
(
    metricId     INT AUTO_INCREMENT PRIMARY KEY,
    errorRate    DECIMAL(5, 2),                      -- (0.00 to 100.00)
    serverLoad   DECIMAL(5, 2),                      -- (0.00 to 100.00)
    responseTime FLOAT,                              -- Response time in milliseconds (e.g., 123.45)
    createdAt    TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time the metric was recorded
);

 
-- Alert
CREATE TABLE IF NOT EXISTS alert
(
    alertId  INT AUTO_INCREMENT PRIMARY KEY,
    messages TEXT NOT NULL,
    priority INT  NOT NULL,
    title    TEXT NOT NULL
);

 
-- Role
CREATE TABLE IF NOT EXISTS role
(
    roleName VARCHAR(50) NOT NULL,
    roleId   INT AUTO_INCREMENT PRIMARY KEY
);

 
-- User
CREATE TABLE IF NOT EXISTS user
(
    userId        INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL,
    email         VARCHAR(320) NOT NULL,
    status        BOOL DEFAULT 1,
    firstName     VARCHAR(50)  NOT NULL,
    middleName    VARCHAR(50),
    lastName      VARCHAR(50)  NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    roleId        INT          NOT NULL,
    FOREIGN KEY (roleId) REFERENCES role (roleId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Advisor
CREATE TABLE IF NOT EXISTS advisor_profile
(
    advisorId  INT PRIMARY KEY,
    department VARCHAR(100),

    FOREIGN KEY (advisorId) REFERENCES user (userId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
CREATE TABLE IF NOT EXISTS admin_profile
(
    adminId INT PRIMARY KEY,
    FOREIGN KEY (adminId) REFERENCES user (userId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Employer
CREATE TABLE IF NOT EXISTS employer_profile
(
    employerId  INT PRIMARY KEY,
    description TEXT,
    link        TEXT,

    FOREIGN KEY (employerId) REFERENCES user (userId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Student Table
CREATE TABLE IF NOT EXISTS student_profile
(
    nuId      INT PRIMARY KEY,
    dob       DATE NOT NULL,
    major     VARCHAR(50),
    minor     VARCHAR(50),
    year      INT(4),
    advisorId INT,
    FOREIGN KEY (advisorId) REFERENCES advisor_profile (advisorId)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (nuId) REFERENCES user (userId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Student and courses bridge table
CREATE TABLE IF NOT EXISTS student_courses
(
    nuId     INT,
    courseId INT,
    PRIMARY KEY (nuId, courseId),
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId) ON DELETE CASCADE,
    FOREIGN KEY (courseId) REFERENCES courses (courseId) ON DELETE CASCADE
);

 
-- Job Posting
CREATE TABLE IF NOT EXISTS job_posting
(
    jobId          INT AUTO_INCREMENT PRIMARY KEY,
    position       VARCHAR(100),
    description    TEXT,
    createdAt      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    pay            DECIMAL(10, 2),
    timePeriod     VARCHAR(255),
    positionType   VARCHAR(50), -- Intern, coop, full-time
    employmentType VARCHAR(50), -- Full-time, Part-time
    workLocation   VARCHAR(50), -- Remote, On-site
    employerId     INT,
    isActive       BOOL     DEFAULT 1,

    FOREIGN KEY (employerId) REFERENCES employer_profile (employerId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Student and skills bridge table
CREATE TABLE IF NOT EXISTS student_skills
(
    nuId    INT,
    skillId INT,
    PRIMARY KEY (nuId, skillId),
    FOREIGN KEY (nuId) REFERENCES student_profile (nuid) ON DELETE CASCADE,
    FOREIGN KEY (skillId) REFERENCES skills (skillId) ON DELETE CASCADE
);

 
-- Activity Log
CREATE TABLE IF NOT EXISTS activity_log
(
    logId       INT AUTO_INCREMENT PRIMARY KEY,
    alertId     INT,
    createdAt   DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    adminId     INT,
    metricId    INT,
    FOREIGN KEY (metricId) REFERENCES metrics (metricId)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (adminId) REFERENCES admin_profile (adminId)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (alertId) REFERENCES alert (alertId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
-- Student Reports
CREATE TABLE IF NOT EXISTS student_reports
(
    reportId  INT AUTO_INCREMENT PRIMARY KEY,
    nuId      INT,
    advisorId INT,
    notes     TEXT,
    status    BOOL DEFAULT 1,
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (advisorId) REFERENCES advisor_profile (advisorId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
CREATE TABLE IF NOT EXISTS job_applications
(
    jobId INT,
    nuId  INT,
    PRIMARY KEY (jobId, nuId),
    FOREIGN KEY (jobId) REFERENCES job_posting (jobId) ON DELETE CASCADE,
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId) ON DELETE CASCADE
);

-- Job posting and skills bridge table
CREATE TABLE IF NOT EXISTS job_posting_skills
(
    jobId   INT,
    skillId INT,
    PRIMARY KEY (jobId, skillId),
    FOREIGN KEY (jobId) REFERENCES job_posting (jobId) ON DELETE CASCADE,
    FOREIGN KEY (skillId) REFERENCES skills (skillId) ON DELETE CASCADE
);

 
CREATE TABLE IF NOT EXISTS student_badges
(
    nuId    INT,
    badgeId INT,
    PRIMARY KEY (nuId, badgeId),
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId) ON DELETE CASCADE,
    FOREIGN KEY (badgeId) REFERENCES badge (badgeId) ON DELETE CASCADE
);

 
-- Student Profile and projects Bridge table
CREATE TABLE IF NOT EXISTS student_projects
(
    nuId      INT,
    projectId INT,
    PRIMARY KEY (nuId, projectId),
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId) ON DELETE CASCADE,
    FOREIGN KEY (projectId) REFERENCES projects (projectId) ON DELETE CASCADE
);

 
-- Personality Table
CREATE TABLE IF NOT EXISTS personalities
(
    description   TEXT,
    personalityId INT AUTO_INCREMENT PRIMARY KEY,
    interests     TEXT,
    softSkills    TEXT,
    leadership    TEXT,
    nuId          INT,

    FOREIGN KEY (nuId) REFERENCES student_profile (nuId)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

 
CREATE TABLE IF NOT EXISTS student_certifications
(
    nuId            INT,
    certificationId INT,
    PRIMARY KEY (nuId, certificationId),
    FOREIGN KEY (nuId) REFERENCES student_profile (nuId) ON DELETE CASCADE,
    FOREIGN KEY (certificationId) REFERENCES certifications (certificationId) ON DELETE CASCADE
);
