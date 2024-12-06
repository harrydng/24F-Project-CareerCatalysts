# Database Files Folder Explanation

The `database-files` folder contains all the SQL scripts required to set up, initialize, and maintain the database for the TalentTrail web application. Each file serves a specific purpose in ensuring the proper functionality and data structure of the app.

## Files and Their Purposes

1. **`00_talenttrail.sql`**  
   This file contains the foundational database schema creation script(DDL). It defines the structure of tables, relationships, and primary/foreign keys for the TalentTrail application.

2. **`02_talenttrail-data.sql`**  
   This file includes scripts for populating the database with instances. It adds roles, skills, projects, certifications, users, and other relevant entries to the corresponding tables.

3. **`03_add_to_talenttrail.sql`**  
   This file contains additional data inserts or updates that extend the database with more specific entries, such as predefined job postings, student profiles, and activity logs to support advanced use cases.

To reset and reinitialize the database, simply start the database service by running:

```bash
docker compose up db -d
```
---
