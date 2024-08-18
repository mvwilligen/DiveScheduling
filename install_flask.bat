pip install flask 
pip install flask-sqlalchemy

from homepage import app, db
with app.app_context():
    db.create_all()

