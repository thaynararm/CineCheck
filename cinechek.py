from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'fitdance'


class Users:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password


user1 = Users('Thaynara', 'Thay', 'fitdance')
user2 = Users('Maria Eduarda', 'Duda', 'helo')
user3 = Users('Livia', 'Livinha', 'rosa')

nicknames = {user1.nickname: user1,
             user2.nickname: user2,
             user3.nickname: user3}

passwords = {user1.password: user1,
             user2.password: user2,
             user3.password: user3}


class MoviesAndSeries:
    def __init__(self, name, duration, local):
        self.name: str = name
        self.duration: str = duration
        self.local: str = local


serie1 = MoviesAndSeries('Cosmos', '1 temporada', 'Disney+')
serie2 = MoviesAndSeries('A Rainha do Sul', '5 temporadas', 'Netflix')
movie1 = MoviesAndSeries('Um Sonho de Liberdade', '2 horas e 22 minutos', 'HBO')
list = [serie1, serie2, movie1]


@app.route('/')
def index():
    return render_template('lista.html', title='Filmes e Séries', movie_and_series=list)


@app.route('/new')
def new():
    if 'logged_in_user' not in session or session['logged_in_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    else:
        return render_template('new.html', title="Novos Filmes e Séries")


@app.route('/create', methods=['POST', ])
def create():
    name = request.form['nome']
    duration = request.form['duracao']
    local = request.form['local']
    new_movie_or_serie = MoviesAndSeries(name, duration, local)
    list.append(new_movie_or_serie)
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
    next_page = request.form['next']

    if request.form['user'] in nicknames:
        user = nicknames[request.form['user']]
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
