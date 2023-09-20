# TmyRestApiApp

### 1. Clone the github repo in you local computer using
```
git clone https://github.com/nguepigit2020/TmyRestApiApp.git
```
### 2. Move to the project directory using
```
cd tmyRestApiApp
```

### 3. Requirement installations ##
To run this, make sure to install all the requirements by:

```
pip install requirements.txt
```
### 4. After sucesfully installed the requirements, you can run the app by:
```
python3 app.py
```
#### All installed package version are in the requirements.txt file , also you can setup a virtual environement before installing the requirements. 

### 5. To create the database, stay in the root of the project and run the following commands:
```
export FLASK_APP=app.py
```
```
flask shell
```
```
>>> from app import db
>>> db.create_all()
>>> exit()
```
### At this step you app can receive and send the request.
