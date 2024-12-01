import sqlite3
import pandas as pd

conn = sqlite3.connect("meu_banco.db")

query = "SELECT * FROM minha_tabela"
df = pd.read_sql_query(query, conn)

