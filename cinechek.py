from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '{SGBD}://{user}:{password}@{host}:{port}/{database}'.format(
    SGBD='mysql+mysqlconnector',
    user='root',
    password='065Karla030*',
    host='localhost',
    port='3306',
    database='cinecheck'
    )

db = SQLAlchemy(app)

app.secret_key = 'fitdance'


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


@app.route('/')
def index():
    list = MoviesAndSeries.query.order_by(MoviesAndSeries.id)
    return render_template('lista.html', title='Filmes e Séries', movie_and_series=list)


@app.route('/new')
def new():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    else:
        return render_template('new.html', title="Novos Filmes e Séries")


@app.route('/create', methods=['POST', ])
def create():

    name = request.form['name']
    duration = request.form['duration']
    local = request.form['local']

    movie_or_serie = MoviesAndSeries.query.filter_by(name=name).first()

    if movie_or_serie:
        flash('Filme ou série já existente!')
        return redirect(url_for('index'))

    new_movie_or_serie = MoviesAndSeries(name=name, duration=duration, local=local)
    db.session.add(new_movie_or_serie)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/other')
def other():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route('/login')
def login():
    if request.args.get('next') is None:
        return render_template('login.html', title='Filmes e Séries', next=url_for('other'))
    else:
        next = request.args.get('next')
        return render_template('login.html', title='Filmes e Séries', next=next)


@app.route('/authenticate', methods=['POST', ])
def authenticate():
    user = Users.query.filter_by(nickname=request.form['user']).first()
    next_page = request.form['next']

    if user:
        if request.form['password'] == user.password:
            session['logged_in_user'] = user.nickname
            flash(user.nickname + ' logado com sucesso!')
            return redirect(next_page)
        else:
            flash('Usuário e/ou senha inválidos!')
            return redirect(next_page)
    else:
        flash('Usuário e/ou senha inválidos!')
        return redirect(next_page)


@app.route('/logout')
def logout():
    session['logged_in_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


app.run(debug=True)
