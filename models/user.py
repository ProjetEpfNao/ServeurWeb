

def create_user_class(db):
    class User(db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(256))
        password = db.Column(db.String(256))
    return User
