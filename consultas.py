import pandas as pd
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='airbnb'
)

def feed_query(conn):
    df = pd.read_sql(""" 
        SELECT 
            H.nome AS host, 
            L.Rua AS local, 
            P.NotaReviews AS nota, 
            P.Preco AS preço, 
            P.Imagem AS imagem_casa,
            P.ID_Postagem  -- Inclui o ID_Postagem para realizar o filtro depois
        FROM 
            Postagem AS P
        JOIN 
            host_ AS H ON P.ID_Host = H.ID_Host
        JOIN 
            residencia AS R ON P.ID_Postagem = R.ID_Postagem
        JOIN 
            local_ AS L ON R.ID_Residencia = L.ID_Residencia
    """, conn)

    return df


def filter_nota(nota, conn):
    query_ids = f"""
    SELECT P.ID_Postagem
    FROM Postagem AS P
    WHERE P.NotaReviews > {nota}
    """
    ids_filtrados = pd.read_sql_query(query_ids, conn)
    return ids_filtrados

def filter_preco(preco, conn):
    query_ids = f"""
    SELECT P.ID_Postagem
    FROM Postagem AS P
    WHERE P.Preco < {preco}
    """
    ids_filtrados = pd.read_sql_query(query_ids, conn)
    return ids_filtrados


'''
def prop_por_hosts():

def review_por_postagem():

def preco_local_comodidade():

def preco_():

def hosts_todas_maior_que_95():
'''