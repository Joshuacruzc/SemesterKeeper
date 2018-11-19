from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '018121e405b67ca8f60e44614ef2a60b'
POSTGRES = {
    'user': 'skipster_server',
    'pw': 'babilonia',
    'db': 'semester_keeper_db',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)
ma = Marshmallow(app)
db.init_app(app)

from semester_keeper import routes