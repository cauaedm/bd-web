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
    WHERE P.NotaReviews >= {nota}
    """
    ids_filtrados = pd.read_sql_query(query_ids, conn)
    return ids_filtrados

def filter_preco(preco, conn):
    query_ids = f"""
    SELECT P.ID_Postagem
    FROM Postagem AS P
    WHERE P.Preco <= {preco}
    """
    ids_filtrados = pd.read_sql_query(query_ids, conn)
    return ids_filtrados


def prop_por_hosts(conn):

    query = '''
    SELECT 
    h.ID_Host,
    h.Nome AS Nome_Host,
    COUNT(r.ID_Residencia) AS Numero_De_Propriedades
    FROM
    Host_ h JOIN Postagem p ON h.ID_Host = p.ID_Host
    JOIN Residencia r ON p.ID_Postagem = r.ID_Postagem
    GROUP BY h.ID_Host
    ORDER BY Numero_De_Propriedades Desc;
    '''
    
    view = pd.read_sql_query(query, conn)
    return view

def filtrar_local(latitude, longitude, conn):
    # Considerando que você tem uma boa faixa para filtrar
    faixa_latitude = 0.0012517801528474997  # Aproximadamente 100 metros
    faixa_longitude = 0.0009457516108255461  # Aproximadamente 100 metros

    query_ids = f""" 
        SELECT 
            P.ID_Postagem,
            (ABS(L.Latitude - {latitude}) + ABS(L.Longitude - {longitude})) AS distancia
        FROM 
            Postagem AS P
        JOIN 
            residencia AS R ON P.ID_Postagem = R.ID_Postagem
        JOIN 
            local_ AS L ON R.ID_Residencia = L.ID_Residencia
        WHERE 
            (L.Latitude - {latitude}) < {faixa_latitude} AND 
            (L.Longitude - {longitude}) < {faixa_longitude}
        ORDER BY 
            distancia ASC
    """
    ids_filtrados = pd.read_sql_query(query_ids, conn)
    return ids_filtrados

def reviews_por_post(conn):
    query = '''SELECT 
        p.Nome AS Nome_Postagem,
        COUNT(a.ID_Review) AS Numero_De_Reviews
    FROM 
        Postagem as p
    LEFT JOIN 
        Avalia as a on p.ID_Postagem = a.ID_Postagem
    GROUP BY p.ID_Postagem, p.Nome
    ORDER BY Numero_De_Reviews DESC;'''
    
    view = pd.read_sql_query(query, conn)
    return view


def preco_local_comodidade(conn):
    query = '''
    SELECT 
        p.ID_Postagem AS ID_Postagem,
        p.Preco AS Preco,
        r.TipoDePropriedade AS Tipo_Propriedade,
        r.Comodidades AS Comodidades,
        l.Cidade AS Cidade,
        l.Rua AS Rua
    FROM 
        Postagem p
    JOIN 
        Residencia r ON p.ID_Postagem = r.ID_Postagem
    JOIN 
        Local_ l ON r.ID_Residencia = l.ID_Residencia
    ORDER BY 
        p.ID_Postagem;
    '''
    
    view = pd.read_sql_query(query, conn)
    return view

def comodo_media(conn):

    '''
    Mostrar preços e quantidade de quartos e banheiros de postagens sobre residências que possuem mais banheiros e quartos que a média.
    (SUBCONSULTA ANINHADA)
    '''

    query = '''
    SELECT 
        p.ID_Postagem, 
        p.Preco,
        r.Quartos,
        r.Banheiros 
    FROM 
        Postagem p 
    JOIN 
        Residencia r ON p.ID_Postagem = r.ID_Postagem 
    WHERE 
        r.Quartos > (SELECT AVG(r2.Quartos) FROM Residencia r2) AND 
        r.Banheiros > (SELECT AVG(r2.Banheiros) FROM Residencia r2);
    '''
    
    view = pd.read_sql_query(query, conn)
    return view

def host_95(conn):
    '''
    Consultar Hosts com todas as postagens possuindo nota maior que 95 (SUBCONSULTA ANINHADA)
    '''

    query = '''
    SELECT
        h.ID_Host,
        h.Nome 
    FROM 
        Host_ h 
    WHERE NOT EXISTS (
            SELECT 1 
            FROM 
                Postagem p 
            JOIN 
                Host_ h2 ON p.ID_Host = h2.ID_Host 
            WHERE 
                h2.ID_Host = h.ID_Host AND p.NotaReviews <= 95 );
    '''
    
    view = pd.read_sql_query(query, conn)
    return view
