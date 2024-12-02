import pandas as pd
import streamlit as st
import pymysql

from consultas import filter_nota
from consultas import feed_query
from consultas import filter_preco

# Conexão com o banco de dados
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='airbnb'
)

# Consulta SQL inicial (sem o JOIN)
df = feed_query(conn)

# Configuração das abas do Streamlit
tab = st.radio("Escolha uma aba", ["Feed", "Analytics"], index=0, horizontal=True)

# Aba Feed
if tab == "Feed":
    st.title("Feed")

    # Filtros de pesquisa
    st.subheader("Filtrar Publicações")

    # Filtro para local
    local_filter = st.selectbox("Escolha um local", ["Todos"] + df['local'].unique().tolist())

    # Filtro para nota
    nota_filter = st.slider("Escolha a nota mínima", 0.0, 5.0, 0.0)
    
    preco_min = float(df['preço'].min())
    preco_max = float(df['preço'].max())

    # Filtro para preço
    preco_filter = st.slider("Escolha o preço máximo", preco_min, preco_max, preco_max)


    # Filtrando o DataFrame com base nos filtros
    filtered_df = df
    
    if local_filter != "Todos":
        filtered_df = filtered_df[filtered_df['local'] == local_filter]

    # Se a nota for maior que 0, usamos o filter_nota para pegar os IDs filtrados
    if nota_filter > 0.0:
        ids_filtrados_nota = filter_nota(nota_filter, conn)
        filtered_df = filtered_df[filtered_df['ID_Postagem'].isin(ids_filtrados_nota['ID_Postagem'])]

    # Se o preço for maior que o mínimo, usamos o filter_preco para pegar os IDs filtrados
    if preco_filter < preco_max:
        ids_filtrados_preco = filter_preco(preco_filter, conn)
        filtered_df = filtered_df[filtered_df['ID_Postagem'].isin(ids_filtrados_preco['ID_Postagem'])]

    # CSS para estilização
    st.markdown(
        """
        <style>
        .div-box {
            display: flex;
            align-items: center;
            background-color: #333333;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            color: white;
            font-family: Arial, sans-serif;
        }
        .div-box img.host-img {
            max-width: 80px;
            border-radius: 50%;
            margin-right: 20px;
        }
        .info {
            flex: 1;
            margin-right: 20px;
        }
        .images {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .images img {
            max-width: 250px;
            height: auto;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Mostrar publicações filtradas
    if filtered_df.empty:
        st.write("Nenhuma publicação encontrada para os filtros selecionados.")
    else:
        # Exibindo cada publicação
        for _, row in filtered_df.iterrows():
            st.markdown(
                f"""
                <div class="div-box">
                    <div class="info">
                        <h3>Postagem</h3>
                        <p><strong>Host:</strong> {row['host']}</p>
                        <p><strong>Local:</strong> {row['local']}</p>
                        <p><strong>Nota:</strong> {row['nota']} ⭐</p>
                        <p><strong>Preço:</strong> {row['preço']}</p>
                    </div>
                    <div class="images">
                        <img src="{row['imagem_casa']}" alt="Foto da Casa">
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")  # Linha divisória entre publicações

# Aba Analytics
elif tab == "Analytics":
    st.title("Analytics")

    # Exemplo de conteúdo na aba de Analytics (gráfico, resumo, etc.)
    st.subheader("Aqui vai ser a aba com as 5 consultas que a gente já tem")
    
    # Gráfico simples de notas usando Streamlit
    st.bar_chart(df['nota'])

    st.subheader("Resumo dos Preços")
    st.write(df['preço'].value_counts())
