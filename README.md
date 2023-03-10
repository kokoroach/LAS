# LAS
NDKC Library Attendance System

A. PREPARATION
Ready the pre-prequisite for local development

1. Install the following:
    - Docker Desktop
    - gitbash (or CLI of your choice)
    - python3.10

2. Create your python virtual env
    - python3 -m venv /path/to/new/virtual/environment

3. Activate environment:
    - (for Windows):
        `source /path/to/new/virtual/environment/Scripts/activate`
    - (for Linux/Mac):
        `source /path/to/new/virtual/environment/bin/activate`

4. Install the python requirements
    - pip3 install -r requirements.txt


B. Prepate Data for Import
We will prepare student data for import later

1. Convert the *.xlsx file to .csv and Ensure that header is at row 0
2. Save it within project folder. Recommen data project dir is `/student_data`


C. Setup Docker

1. Build images*
    - `docker-compose up --build`
*NOTE: Should only be done on (a) project init or (b) whenever this is any change in docker-related files. Else, proceed to 2

2. Up existing images
    - `docker-compose up`


D. Setup Admin

1. Create superuser based off the .env file (to be given separately)
    - `docker ps`
    - `docker exec -it <CONTAINER_ID> sh`
    - `python manage.py createsuperuser`

2. Log-in to Django Admin Panel
    - localhost:8080/admin

3. Verify that no users/students exists
    - Visit Students, Users, Attendances


E. Load Users

1. Load users that was processed from (B)
    - `docker ps`
    - `docker exec -it <CONTAINER_ID> sh`
    
    if you've used the recommended student_data path, the use:
    - `python manage.py load_users student_data/<FILE_NAME>`
    else
    -  `python manage.py load_users <CSV_DATA_PATH>`

2. Log-in to Django Admin Panel
    - localhost:8080/admin

3. Verify that users/students are added
    - Visit Students, Users


F. Export Data
1. GOTO Django Admin Panel
    - localhost:8080/admin
2. Goto specific Django Admin Model
3. Click Export


G. Stopping Image
1. CTRL+C or CMD+C
2. Make the image is stopped
3. Else, run `docker compose down`
