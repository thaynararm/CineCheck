from cinechek import db


class Users(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(20), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class MoviesAndSeries(db.Model):
    __tablename__ = 'movies_and_series'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(30), nullable=False)
    local = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
