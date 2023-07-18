from cinechek import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Users
from helpers import  UserForm
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    form = UserForm()
    if request.args.get('next') is None:
        return render_template('login.html', title='Filmes e Séries', next=url_for('other'), form=form)
    else:
        next = request.args.get('next')
        return render_template('login.html', title='Filmes e Séries', next=next, form=form)


@app.route('/other')
def other():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))


@app.route('/authenticate', methods=['POST', ])
def authenticate():
    #if not form.validate_on_submit():
        #return redirect(url_for('login'))
    form = UserForm(request.form)
    user = Users.query.filter_by(nickname=form.nickname.data).first()
    next_page = request.form['next']

    if user is not None:
        password = check_password_hash(user.password, form.password.data)
        if password:
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
