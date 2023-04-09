from flask_app.app import app
from flask_app.database.db import db, init_db
from flask_app.database.db_models import User

# Подготоваливаем контекст и создаём таблицы
init_db(app)
app.app_context().push()
db.create_all()

# Insert-запросы
admin = User(login='admin', password='password')
db.session.add(admin)
db.session.commit()

# Select-запросы
User.query.all()
User.query.filter_by(login='admin').first()