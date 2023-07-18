from cinechek import db, app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import MoviesAndSeries
from helpers import recover_image, delete_file, GameForm
import time


@app.route('/')
def index():
    list = MoviesAndSeries.query.order_by(MoviesAndSeries.id)
    return render_template('lista.html', title='Filmes e Séries', movie_and_series=list)


@app.route('/new')
def new():
    form = GameForm()
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    else:
        return render_template('new.html', title="Novos Filmes e Séries", form=form)


@app.route('/create', methods=['POST', ])
def create():
    form = GameForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    name = form.name.data
    duration = form.duration.data
    local = form.local.data

    movie_or_serie = MoviesAndSeries.query.filter_by(name=name).first()

    if movie_or_serie:
        flash('Filme ou série já existente!')
        return redirect(url_for('index'))

    new_movie_or_serie = MoviesAndSeries(name=name, duration=duration, local=local)
    db.session.add(new_movie_or_serie)
    db.session.commit()

    file = request.files['file']
    if file:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        file.save(f'{upload_path}/cover{new_movie_or_serie.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('edit', id=id)))
    movie_or_serie = MoviesAndSeries.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = movie_or_serie.name
    form.duration.data = movie_or_serie.duration
    form.local.data = movie_or_serie.local
    cover = recover_image(id)
    return render_template(
        'edit.html', title="Editando Filmes e Séries", movie_or_serie=movie_or_serie, cover=cover, form=form)


@app.route('/update', methods=['POST', ])
def update():
    form = GameForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('new'))

    movie_or_serie = MoviesAndSeries.query.filter_by(id=request.form['id']).first()
    movie_or_serie.name = form.name.data
    movie_or_serie.duration = form.duration.data
    movie_or_serie.local = form.local.data

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


@app.route('/uploads/<name_file>')
def image(name_file):
    return send_from_directory('uploads', name_file)
