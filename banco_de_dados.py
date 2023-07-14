import mysql.connector
from mysql.connector import errorcode


print("Conectando...")
try:
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='065Karla030*'
    )

except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')

      else:
            print(err)


cursor = mydb.cursor()

cursor.execute("DROP DATABASE IF EXISTS `cinecheck`;")

cursor.execute("CREATE DATABASE `cinecheck`;")

cursor.execute("USE `cinecheck`;")

# criando tabelas
TABLES = {}
TABLES['movies_and_series'] = ('''
      CREATE TABLE `movies_and_series` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `duration` varchar(40) NOT NULL,
      `local` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `password` varchar(25) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      table_sql = TABLES[table_name]
      try:
            print('Criando tabela {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
      ("Thay Rodrigues", "Thay", "fitdance"),
      ("Maria Eduarda", "Duda", "enfermagem"),
      ("Livia Vitoria", "Livia", "rosa")
]
cursor.executemany(user_sql, users)

cursor.execute('select * from cinecheck.users')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo filmes e series
movies_and_series_sql = 'INSERT INTO movies_and_series (name, duration, local) VALUES (%s, %s, %s)'
movies_and_series = [
    ('Cosmos', '1 temporada', 'Disney+'),
    ('A Rainha do Sul', '5 temporadas', 'Netflix'),
    ('Um Sonho de Liberdade', '2 horas e 22 minutos', 'HBO'),
]
cursor.executemany(movies_and_series_sql, movies_and_series)

cursor.execute('select * from cinecheck.movies_and_series')
print(' -------------  Filmes e Series:  -------------')
for movies_and_series in cursor.fetchall():
    print(movies_and_series[1])

# commitando se não nada tem efeito
mydb.commit()

cursor.close()
mydb.close()