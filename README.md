## Phonepe Pulse (2018-2022) Data_Analysis

This is Streamlit web app for analysing and visualizing Phonepe Pulse Data(2018-2022).The unstructured pluse data are cloned and transformed to structure data. Then,the structure data are stored in AWS RDS Mysql database.

Web App is - [Live](https://balajeerjs-phonepe-pulse-data-analysis-main-rht4p9.streamlit.app/)

## Tech Stack

**Language:** Python\
**Libraries:** plotly, pandas,mysql-connector-python\
**SQL Database:**: AWS RDS MySQL\
**GUI Framework:** Streamlit

## Storing and Fetching  data in AWS RDS MySQL Database

The Pulse data are stored and fetched using **mysql-connector-python** python library.

## Visualizing Data

The Pulse data are visualized using **plotly** python library.

## Creating the UI

 **Streamlit framework** is used for creating the GUI for Phonepe Pulse data analysis .It is used to create dropdown and diplaying results.

## Database Configuration

Please replace with  your own **Username**,**Password**,**AWS Endpoint** and **Database** string in **sqlconnect.py** file while running the code in your local machine.

![image](https://user-images.githubusercontent.com/116367662/224826762-2916bfa4-a1b1-465e-89c8-94c3a8fda690.png)


## Command to run

**Clone from Phonepe Pulse repository** --->python clone.py [Note: create a new folder in current working directory as per repo_name variable value in clone.py]\
**To create table and insert data to datbase** --->python sql.py [Note:Replace all path variables in sql.py as per your working directory path]\
**To start web app** --> streamlit run main.py

## How app works ?

The app  has 3 sections 

**1. TRANSACTION ANALYSIS**\
    In this section, Transaction Counts are visualized for payment mode, districts, and India in each year.from 2018-2022\
**2. USER BASE ANALYSIS**\
    In this section, Registered User Counts are visualized for states, districts, and India in each year.from 2018-2022\
**3. TOP TRANSACTION & USER ANALYSIS**\
    In this section, Top 3 Transaction Counts and Registered User Counts are visualized for states and  districts in each year.from 2018-2022

## Reference docs
 - [Streamlit docs](https://docs.streamlit.io/)
 
## My Linkedin Post
- [LinkedIn Post](https://www.linkedin.com/posts/rjs-balajee-389a8215a_python-dataengineering-aws-activity-7041175210158432256-jaS2?utm_source=share&utm_medium=member_desktop)
