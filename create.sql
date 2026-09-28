
-- SQL file to input commands to create tables and view 

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(30) NOT NULL,
    user_lastname VARCHAR(30) NOT NULL,
    country VARCHAR(50) NOT NULL,
    birth_day VARCHAR(2) NOT NULL,
    birth_month VARCHAR(15) NOT NULL,
    birth_year VARCHAR(4) NOT NULL,
    email varchar(50) NOT NULL,
    passwrd TEXT NOT NULL,
    ncourses INTEGER DEFAULT 0
);

CREATE TABLE courses (
    course_id VARCHAR(4) NOT NULL PRIMARY KEY,
    course_name VARCHAR(50),
    course_description TEXT NOT NULL,
    participants INTEGER DEFAULT 0 
);

CREATE TABLE user_courses (
    id INTEGER AUTO_INCREMENT,
    course_id VARCHAR(4) NOT NULL,
    course_name VARCAHR(50),
    email varchar(50) NOT NULL,
    date_enrolled DATETIME DEFAULT CURRENT_TIMESTAMP,
    progress VARCHAR(10) DEFAULT 0,
    enrolled BINARY,
    PRIMARY KEY (id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);


-- Command to insert the courses couse into the database

INSERT INTO courses (course_id, course_name, course_description) VALUES (
    "O001", "MS Excel", "This course offers the basics to learning Microsoft Excel, some of the most important functions and every aspect that is available to users. Here, you will learn to use tables, graphs and mucho more." 
);

INSERT INTO courses (course_id, course_name, course_description) VALUES (
    "P001", "Python", "In this Python course you will learn the basics of programming and specially one of the most powerfull programming languages there is: Python. You will make basic programs and learn how to use Python for data analysis." 
);

INSERT INTO courses (course_id, course_name, course_description) VALUES (
    "J001", "Java", "In this Java course you will learn the basics of the Java programming language, as well as build simple projects." 
);

-- Command to modify tables if neccesary

ALTER TABLE courses ADD url1 TEXT;
ALTER TABLE courses ADD url2 TEXT;
ALTER TABLE courses ADD url3 TEXT;

-- Command to insert urls to DB

UPDATE courses SET url1 = "https://www.youtube.com/embed/mMv6OSuitWw?si=6gRsyxtpNvkBSt4w", url2 = "https://www.youtube.com/embed/b093aqAZiPU?si=6U1H1HLZ1hIlUP7h", url3 = "https://www.youtube.com/embed/rfscVS0vtbw?si=POfI5lp3ZF_krwDc" WHERE course_name = "Python";
UPDATE courses SET url1 = "https://www.youtube.com/embed/0tdlR1rBwkM?si=yjSlbZODZMcaZYtB", url2 = "https://www.youtube.com/embed/LgXzzu68j7M?si=4jc6kiG5hhaCKtS0", url3 = "https://www.youtube.com/embed/Vl0H-qTclOg?si=Bc2NPuuEXN8_plkm" WHERE course_name = "MS Excel";
UPDATE courses SET url1 = "https://www.youtube.com/embed/RRubcjpTkks?si=ajb3n2I2EKDwkaWX", url2 = "https://www.youtube.com/embed/eIrMbAQSU34?si=E5-QXUadSt1os8cR", url3 = "https://www.youtube.com/embed/A74TOX803D0?si=Oar2922e019ET2Vd" WHERE course_name = "Java";