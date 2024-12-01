import sqlite3
import pandas as pd

conn = sqlite3.connect("meu_banco.db")

def filter_nota(nota, db_path):
    conn = sqlite3.connect(db_path)

    query = f"SELECT * FROM minha_tabela WHERE nota > {nota}"

    df = pd.read_sql_query(query, conn)
    
    return df

def filter_local(local, db_path):
    conn = sqlite3.connect(db_path)

    query = f"SELECT * FROM minha_tabela WHERE local LIKE %{local}%"

    df = pd.read_sql_query(query, conn)
    
    return df

'''
def prop_por_hosts():

def review_por_postagem():

def preco_local_comodidade():

def preco_():

def hosts_todas_maior_que_95():
'''


