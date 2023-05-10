# NDKC Library Attendance System

## A. Installation
Since the system is a Dockerized Python/Django application, we need to prepare the following requisite for the development environment to work.

1. We need to install the following:
    - Docker Desktop (version as of writing is [v4.17.1](https://www.docker.com/products/docker-desktop/))
    - [gitbash](https://git-scm.com/downloads)  (or shell of your choice)
    - [python 3.10](https://www.python.org/downloads/)

2. (Optional) To support debugging of apps an a standalone or isolated environment, we may also create a virtual environment (or virtual env)
```
python3 -m venv </path/to/virtual/environment>
```

3. (Optional) To activate the virtual environment, we will run the following commands:
    - Windows: `source </path/to/virtual/environment>/Scripts/activate`
    - Linux/Mac: `source </path/to/virtual/environment>/bin/activate`

4. (Optional) With the virtual activated, install the application libraries
```
pip3 install -r requirements.txt
```

5. Note that the set-up above is already provided in `Dockerfile.local` file for the docker image.


## B. Setup Docker Container

1. We nedd to build the docker containers defined in `docker-compose.yml` file and run the image based from it. We do this by executing the commands:
```
docker-compose up --build
```
Note: This step should only be done on (a) project initital set-up or (b) whenever this is any change in docker-refereced files like `requirements.txt` and `Dockerfile`

2. If we are only building the image with no change as mentioned in (B1), we can simply run: 
```
docker-compose up
```


## C. Setup Admin

1. In order to create a superuser based, we can create on by going into the image and run createsuperuser command
```
docker ps
docker exec -it <CONTAINER_ID> sh
python manage.py createsuperuser
```

2. Log-in to Django Admin Panel
```
localhost:8080/admin
```

3. Verify that no users/students exists
    - Visit Students, Users, Attendances


## D. Prepate Data for Import
We will prepare student data for import later in step `E`.

1. The system expects a `.csv` file, so `.xlsx`or other format will need to be 'transformed' to `.csv`.
2. Ensure that the `.csv` file contains the following headers:
>NO,ID No.,Student Name,Sex,Program,Major,Year
3. Save it within project folder. Recommended data project directory is `/student_data`


## E. Load Users

1. Load users that was processed from (B)
```
docker ps
docker exec -it <CONTAINER_ID> sh
```
if you've used the recommended student_data path, the use:
```
python manage.py load_users student_data/<FILE_NAME> --level={und,grd,shs}
```
else
```
python manage.py load_users <CSV_DATA_PATH> --level={und,grd,shs}
```

where levels are,
und = undergraduate; grd = graduate; and shs = senior high school 

2. Log-in to Django Admin Panel
    - localhost:8080/admin

3. Verify that users/students are added
    - Visit Students, Users


## F. Export Data
1. Goto Django Admin Panel
```
localhost:8080/admin
```
2. Goto specific Django Admin Model
3. Click Export


## G. Stopping Image
1. CTRL+C or CMD+C
2. Make the image is stopped
3. Else, run `docker compose down`


## OTHER INFO:

Django uses MVC~ish (Model-View-Controller), which can be mapped in the project as:

1. MODEL. Interface to the DB
 - exists in: attendance\models.py
 - data migration in: attendance\migrations

2. VIEW. The UI Logic
 - exists in: attendance\templates\attendance

3. CONTROLLER: Interface between View and the App
 - exists in: attendance\views.py
 - Admin: attendance\admin.py 

SEE:
https://data-flair.training/blogs/django-architecture/#:~:text=MVC%20Pattern%20in%20Django%20Structure,to%20organize%20in%20the%20database.
