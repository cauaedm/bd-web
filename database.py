import pymysql
import pandas as pd

# Estabelecendo a conexão com o MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='airbnb'
)

# Utilizando pandas para executar a consulta SQL e criar um DataFrame
df = pd.read_sql("SELECT * FROM avalia", conn)

# Exibindo o DataFrame
print(df)

# Fechando a conexão
conn.close()
