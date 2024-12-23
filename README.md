*Clone the repository*
```bash
git clone https://github.com/kodzhsilv/RESTful-API-Project.git
cd RESTful-API-Project
```

 *Create virtual environment*
```bash
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
```

*Required packages*
```bash
pip install alembic sqlalchemy fastapi uvicorn databases pymysql
```

*Create database (bash)*
```bash
mysql -u root -p
CREATE DATABASE car_api;
EXIT;
```


*Configure MySQL credentials*
```bash
*config/db.py*
DATABASE_URL = "mysql+pymysql://<your_mysql_user>:<your_mysql_password>@localhost:3306/car_api"

*alembic.ini*
sqlalchemy.url = mysql+pymysql://<your_mysql_user>:<your_mysql_password>@localhost/car_api
```


*Run migration/create tables for car_api*
```bash
alembic upgrade head
```


*Start the API*
```bash
 uvicorn main:app --host 127.0.0.1 --port 8088 --reload
```
