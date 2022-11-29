**Project description:**
This project is to design data modeling with Postgres.The objective is to build ETL pipeline using python which includes defining fact and dimentional tables for a star schema and transferring the datasets into these tables. 

Context on data files: 
- song dataset file and log dataset file to be processed
- song dataset contains information on songs and its artists
- log dataset contains information on users listening to songs



**Database design:**

<b>Fact Table</b>
songplays: records on the songs played by the user

<b>Dimension Tables</b>
users: users in the app, columns: user_id, first_name, last_name, gender, level

songs: songs in music database, columns: song_id, title, artist_id, year, duration

artists: artists in music database , columns: artist_id, name, location, latitude, longitude

time: timestamps of records in songplays broken down into specific units, columns:start_time, hour, day, week, month, year, weekday


**ETL Process:**
This section describes the processing of the logs and creating different tables so that analytical queries can be run on them. It also describes, which directories have what kind of data and how are you extracting and transforming it.

- load song_data files to create songs and artists dimensional tables
- load log_data files to create time, users dimensional tables and songplays fact table


**Project Repository files:**

- test.ipynb displays the first few rows of each table to check your database.
- create_tables.py drops and creates the tables. 
- etl.ipynb reads and processes a single file from song_data and log_data and loads the data into the tables. This notebook contains detailed instructions on the ETL process for each of the tables. to test each component in the etl.py file
- etl.py reads and processes files from song_data and log_data and loads them into your tables. 
- sql_queries.py contains all your sql queries, and is imported into the last three files above.

**How To Run the Project:**
- 1. run create_tables.py
- 2. run etl.py
-  note: other files are designed for test purpose
