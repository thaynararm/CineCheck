import os
from cinechek import app


def recover_image(id):
    for name_file in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in name_file:
            return name_file

    return 'capa_padrao.jpg'


def delete_file(id):
    file = recover_image(id)
    if file != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
