# crm-sample
A CRM database with FrontEnd  

A customer relationship management web application as mini project for Databases and Web Tech Courses of 5th Semester.  
**Database**  MySQL  
**Backend**   Django  

## Installation

We assume that Python 3 and MySQL is already installed.
Since the backend is of MySQL, make sure that MySQL server 
is configured.

- Clone this repo.
- Create a virtualenv. `python3 -m venv <name>`
- Source it. `source <name>/bin/activate`
- Install requirements. `pip install -r requirements.txt`
- In case the above step fails, do the following to resolve
mySQL error: `sudo apt-get install libmysqlclient-dev`
- Apply migrations. `python3 manage.py migrate`
- Run the server. `python manage.py runserver`