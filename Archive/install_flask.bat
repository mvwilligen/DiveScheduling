@echo on

call C:\Data\Python\DiveScheduling\Export2Website.bat start_python_session

pip install virtualenv
python -m venv env
call venv\Scripts\activate.bat

py -m ensurepip --default-pip

pip install flask 
pip install flask-sqlalchemy
pip install flask-wtf
pip install email_validator
pip install flask_bcrypt
pip install flask_login
rem source: https://flask-login.readthedocs.io/en/latest/
pip install flask-login
pip install python-dotenv
pip install Flask-Mailman
