use crawl_job;
show tables;
drop table if exists job_detail;
create table job_detail (
    id int unsigned not null auto_increment primary key,
    crawl_date datetime,
    title varchar(500) not null,
    href varchar(500),
    main_text text not null,
    salary varchar(50),    
    skill_tag varchar(500),
    sector varchar(200),
    newbie boolean,
    career varchar(50),
    deadline date,
    company_name varchar(100),
    company_address varchar(500),
    platform varchar(100),
    logo_image varchar(500)
) DEFAULT CHARSET=utf8mb4;
desc job_detail;
select * from job_detail;

CREATE TABLE resume (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        mongo_key VARCHAR(100) NOT NULL, 
        PRIMARY KEY (id)
)
CREATE TABLE jobskill (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        name VARCHAR(200), 
        PRIMARY KEY (id)
)
CREATE TABLE jobsector (
        id INTEGER NOT NULL AUTO_INCREMENT, 
        name VARCHAR(200), 
        PRIMARY KEY (id)
)
CREATE TABLE user (
        id CHAR(32) NOT NULL, 
        auth VARCHAR(100), 
        email VARCHAR(255) NOT NULL, 
        nickname VARCHAR(100) NOT NULL, 
        main_resume_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (email), 
        FOREIGN KEY(main_resume_id) REFERENCES resume (id)
)
CREATE TABLE skills_sector (
        job_skill_id INTEGER, 
        job_sector_id INTEGER, 
        FOREIGN KEY(job_skill_id) REFERENCES jobsector (id), 
        FOREIGN KEY(job_sector_id) REFERENCES jobskill (id)
)