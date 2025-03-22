import pandas as pd
import sqlite3
import random
import datetime
import pdb
import os

def criarBD():
  conn = sqlite3.connect('streaming.db')
  cursor = conn.cursor()

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS filmes (
      id INTEGER PRIMARY KEY,
      titulo VARCHAR,
      genero VARCHAR,
      diretor VARCHAR,
      ano_lancamento INTEGER
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS series (
      id INTEGER PRIMARY KEY,
      titulo VARCHAR,
      genero VARCHAR,
      criador VARCHAR,
      ano_lancamento INTEGER,
      temporadas INTEGER
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
      id INTEGER PRIMARY KEY,
      nome VARCHAR,
      idade INTEGER,
      plano VARCHAR
    )
  ''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS visualizacoes (
      usuario_id INTEGER,
      conteudo_id INTEGER,
      tipo_conteudo VARCHAR,
      data_visualizacao DATE,
      FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')
  conn.commit()
  conn.close()

criarBD()

filmes = [
    ('A Origem', 'Ficção Científica', 'Christopher Nolan', 2010),
    ('O Poderoso Chefão', 'Drama', 'Francis Ford Coppola', 1972),
    ('Pulp Fiction', 'Crime', 'Quentin Tarantino', 1994),
    ('Interestelar', 'Ficção Científica', 'Christopher Nolan', 2014),
    ('O Senhor dos Anéis: A Sociedade do Anel', 'Fantasia', 'Peter Jackson', 2001),
    ('Clube da Luta', 'Drama', 'David Fincher', 1999),
    ('Cidade de Deus', 'Crime', 'Fernando Meirelles', 2002),
    ('A Lista de Schindler', 'Drama', 'Steven Spielberg', 1993),
    ('Parasita', 'Drama', 'Bong Joon-ho', 2019),
    ('O Cavaleiro das Trevas', 'Ação', 'Christopher Nolan', 2008),
    ('De Volta para o Futuro', 'Aventura', 'Robert Zemeckis', 1985),
    ('Matrix', 'Ficção Científica', 'The Wachowskis', 1999),
    ('Um Sonho de Liberdade', 'Drama', 'Frank Darabont', 1994),
    ('O Silêncio dos Inocentes', 'Suspense', 'Jonathan Demme', 1991),
    ('A Viagem de Chihiro', 'Animação', 'Hayao Miyazaki', 2001)
  ]
series = [
    ('Breaking Bad', 'Drama', 'Vince Gilligan', 2008, 5),
    ('Game of Thrones', 'Fantasia', 'David Benioff', 2011, 8),
    ('Stranger Things', 'Ficção Científica', 'The Duffer Brothers', 2016, 4),
    ('The Crown', 'Drama', 'Peter Morgan', 2016, 6),
    ('The Mandalorian', 'Ficção Científica', 'Jon Favreau', 2019, 3),
    ('Friends', 'Comédia', 'David Crane', 1994, 10),
    ('The Office', 'Comédia', 'Greg Daniels', 2005, 9),
    ('Sherlock', 'Crime', 'Mark Gatiss', 2010, 4),
    ('Black Mirror', 'Ficção Científica', 'Charlie Brooker', 2011, 5),
    ('Peaky Blinders', 'Crime', 'Steven Knight', 2013, 6),
    ('The Witcher', 'Fantasia', 'Lauren Schmidt Hissrich', 2019, 3),
    ('La Casa de Papel', 'Crime', 'Álex Pina', 2017, 5),
    ('Squid Game', 'Drama', 'Hwang Dong-hyuk', 2021, 1),
    ('The Queen\'s Gambit', 'Drama', 'Scott Frank', 2020, 1),
    ('Succession', 'Drama', 'Jesse Armstrong', 2018, 4)
]

usuarios = []
planos = ['Básico', 'Padrão', 'Premium']

for i in range(1, 101):
    nome = f'Usuário {i}'
    idade = random.randint(18, 70)
    plano = random.choice(planos)
    usuarios.append((nome, idade, plano))

visualizacoes = []

for usuario_id in range(1, 101):
    for _ in range(random.randint(5, 20)):  # Cada usuário assiste de 5 a 20 conteúdos
        conteudo_id = random.randint(1, 30)  # Conteúdo pode ser filme ou série
        tipo_conteudo = random.choice(['Filme', 'Serie'])
        data_visualizacao = datetime.date(random.randint(2022, 2023), random.randint(1, 12), random.randint(1, 28))
        visualizacoes.append((usuario_id, conteudo_id, tipo_conteudo, str(data_visualizacao)))

def inserirFilmes(filmes):
  conn = sqlite3.connect('streaming.db')
  cursor = conn.cursor()
  cursor.executemany('INSERT INTO filmes (titulo, genero, diretor, ano_lancamento) VALUES (?, ?, ?, ?)', filmes)
  conn.commit()
  conn.close()

def insereSeries(series):
  conn = sqlite3.connect('streaming.db')
  cursor = conn.cursor()
  cursor.executemany('INSERT INTO series (titulo, genero, criador, ano_lancamento, temporadas) VALUES (?, ?, ?, ?, ?)', series)
  conn.commit()
  conn.close()

def inserirUsuarios(usuarios):
  conn = sqlite3.connect('streaming.db')
  cursor = conn.cursor()
  cursor.executemany('INSERT INTO usuarios (nome, idade, plano) VALUES (?, ?, ?)', usuarios)
  conn.commit()
  conn.close()

def inserirVisualizacoes(visualizacoes):
  conn = sqlite3.connect('streaming.db')
  cursor = conn.cursor()
  cursor.executemany('INSERT INTO visualizacoes (usuario_id, conteudo_id, tipo_conteudo, data_visualizacao) VALUES (?, ?, ?, ?)', visualizacoes)
  conn.commit()
  conn.close()

def conectaBD():
  return sqlite3.connect('streaming.db')
def executaConsulta(conn, consulta, parametros=()):
  cursor = conn.cursor()
  cursor.execute(consulta, parametros)
  return cursor.fetchall()

def filmesMaisAssistidos(genero):
  conn = conectaBD()
  consulta = '''SELECT Filmes.titulo
    FROM Filmes
    JOIN Visualizacoes ON Filmes.id = Visualizacoes.conteudo_id
    WHERE Filmes.genero = ? AND Visualizacoes.tipo_conteudo = 'Filme'
    GROUP BY Filmes.titulo
    ORDER BY COUNT(*) DESC
    LIMIT 5;
  ''' # The comment is moved outside the SQL query string

  resultados = executaConsulta(conn, consulta, (genero,))
  conn.close()
  return [resultado[0] for resultado in resultados]

inserirFilmes(filmes)
insereSeries(series)
inserirUsuarios(usuarios)
inserirVisualizacoes(visualizacoes)

print('Os filmes mais assistidos são: ', filmesMaisAssistidos('Drama'))

def mediaIdadeUsuarios():
  conn = sqlite3.connect('streaming.db')
  consulta = '''SELECT AVG(Usuarios.idade)
    FROM Usuarios
    JOIN Visualizacoes ON Usuarios.id = Visualizacoes.usuario_id
    JOIN Series ON Visualizacoes.conteudo_id = Series.id
    WHERE Series.genero = 'Drama' AND Visualizacoes.tipo_conteudo = 'Serie';  '''
  cursor = conn.cursor()
  cursor.execute(consulta)
  resultado = cursor.fetchone()
  conn.close()
  return resultado[0]
print('A média de idade dos usuários que assistiram a séries de drama é: ', mediaIdadeUsuarios())

def criadoresSeriesLancados():
  conn = sqlite3.connect('streaming.db')
  consulta = '''SELECT Series.criador
    FROM Series
    JOIN Visualizacoes ON Series.id = Visualizacoes.conteudo_id
    WHERE Visualizacoes.tipo_conteudo = 'Serie' AND Series.ano_lancamento >= datetime('now', '-1 year')
    GROUP BY Series.criador
    HAVING COUNT(*) > 2;'''
  cursor = conn.cursor()
  cursor.execute(consulta)
  resultados = cursor.fetchall()
  conn.close()
  return [resultado[0] for resultado in resultados]
print('Os criadores de séries que lançaram mais de 2 séries no último ano são: ', criadoresSeriesLancados())

def planoMaispopular():
  conn = sqlite3.connect('streaming.db')
  consulta = '''SELECT Usuarios.plano, COUNT(Usuarios.plano) AS quantidade
    FROM Usuarios
    GROUP BY Usuarios.plano
    ORDER BY quantidade DESC
    LIMIT 1;'''
  cursor = conn.cursor()
  cursor.execute(consulta)
  resultado = cursor.fetchone()
  conn.close()
  return resultado[0]
print('O plano mais popular é: ', planoMaispopular())

def deletarBD():
  try:
    os.remove('streaming.db')
    print("Banco de dados 'streaming.db' deletado com sucesso.")
  except FileNotFoundError:
    print("O banco de dados 'streaming.db' não existe.")

deletarBD()
