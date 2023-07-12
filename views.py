from cinechek import db, app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Users, MoviesAndSeries
from helpers import recover_image, delete_file
import time


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

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/cover{new_movie_or_serie.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    movie_or_serie = MoviesAndSeries.query.filter_by(id=id).first()
    cover = recover_image(id)
    return render_template('edit.html', title="Editando Filmes e Séries", movie_or_serie=movie_or_serie, cover=cover)


@app.route('/update', methods=['POST', ])
def update():
    movie_or_serie = MoviesAndSeries.query.filter_by(id=request.form['id']).first()
    movie_or_serie.name = request.form['name']
    movie_or_serie.duration = request.form['duration']
    movie_or_serie.local = request.form['local']

    db.session.add(movie_or_serie)
    db.session.commit()

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    delete_file(movie_or_serie.id)
    file.save(f'{upload_path}/cover{movie_or_serie.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    else:
        MoviesAndSeries.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Filme/Série deletado com sucesso!')
        return redirect(url_for('index'))


@app.route('/login')
def login():
    if request.args.get('next') is None:
        return render_template('login.html', title='Filmes e Séries', next=url_for('other'))
    else:
        next = request.args.get('next')
        return render_template('login.html', title='Filmes e Séries', next=next)


@app.route('/other')
def other():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


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


@app.route('/uploads/<name_file>')
def image(name_file):
    return send_from_directory('uploads', name_file)