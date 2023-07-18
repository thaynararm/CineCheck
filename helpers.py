import os
from cinechek import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class GameForm(FlaskForm):
    name = StringField('Nome do Filme ou Série', validators=[DataRequired(), Length(min=1, max=50)])
    duration = StringField('Duração do Filme ou Série', validators=[DataRequired(), Length(min=1, max=40)])
    local = StringField('Onde assistir o Filme ou Série', validators=[DataRequired(), Length(min=1, max=20)])
    save = SubmitField('Salvar')


class UserForm(FlaskForm):
    nickname = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=1, max=8)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=1, max=25)])
    save = SubmitField('Login')


def recover_image(id):
    for name_file in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in name_file:
            return name_file

    return 'capa_padrao.jpg'


def delete_file(id):
    file = recover_image(id)
    if file != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
