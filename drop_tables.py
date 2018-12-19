from semester_keeper.models import db

db.session.commit()
db.drop_all()
db.create_all()
