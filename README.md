DormitoryDrive
===============

Requirements
----------------
* python3
* ffmpeg

How to setup
---------------
In DormitoryDrive root directory, command below
```
virtualenv env  
source ./env/bin/activate  
pip install -r requirements.txt  
python init_db.py
```

How to run Debug server
------------------------
In DormitoryDrive root directory, command below
```
python app.py
```
then access to localhost:5000

How to run Release server
--------------------------
In DormitoryDrive root directory, command below
```
foreman start
```
then access to localhost:5000
