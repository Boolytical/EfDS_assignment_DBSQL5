# Essentials for Data Science (Relational DBs,
SQL, ORM): Group assignment 2021/22

By Marios Chritoforides, Luise Gummi, Iliana Kleovoulou , Vivianne, Esmee and Felix Kapulla

*** 
For this assignment the SQLAlchemy version 1.4 Object Relational Mapper framework for the classes representing the database tables is used. The provided files contain the framework to create the relational database GradeDB. The database is initialized with some random content. By means of the Python access class GradeDB (within `gradedb.py`) and its methods, database tables and relations between tables are maintained. 
***

## Descriptions of the files
***
* `gradedb.py`           This file contains the main class GradeDB. Creating an object of this class provides access to work with and maintain the database. The class contains methods that allow to adjust and maintain the database.   
* `schema.pdf`        This file displays the relational schema of the database with all its tables and relations between tables. Furthermore, attributes of primary keys of each table are listed.
* `create.sql`            This file contains SQL-code to create the tables of the database, relations between tables are implemented as well as triggers that fire when certain events within the databes occur. All this is based on the relational schema.     
* `schema.py`  This file contains SQLAlchemy description of the database tables and relationships between tables. Among others, declarative mapping is used to define basic units of data storage and connection between two mapped classes are constructed via relationship().
* `random_init.ipynb`  Notebook that initializes the Database (document create) with random data 
* `student_summary.ipynb`            This file contains a notebook  which will represent some general information about students such as total grades for the reports, evaluation and whether submitted reports are pending. Each corresponding student can be identified by Studentid.
* `student_details.ipynb`   This jupyter notebook shows all details from the database which was created for the corresponding student. Each student can be identified just like "student_summary" file, using a studentid.
* `teacher_summary.ipynb`   This file contains summary information for the teacher. Grouped by tasks it lists total numbers of students assigned to a task, already submitted solutions, whether an evaluation still has to be made etc.

***

## Packages that need to be installed
***
- `names`
- `random`
- `string`
- `sqlite3`
- `pandas`
- `numpy`
- `sqlalchemy `
- `sqlalchemy.orm`
- `sqlalchemy.sql`
- `random_word`
***


## Additional comments
***

***


