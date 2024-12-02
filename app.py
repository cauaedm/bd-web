import pandas as pd
import streamlit as st
import pymysql
import altair as alt
import plotly.express as px

import folium
from streamlit_folium import st_folium

from consultas import *

st.set_page_config(
    page_title="Goats do BD",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

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

    if "last_clicked" not in st.session_state:
        st.session_state["last_clicked"] = None

    def button_clicked(button_name):
        st.session_state["last_clicked"] = button_name

    
    # Filtro para nota
    nota_filter = st.slider("Escolha a nota mínima", 0.0, 100.0, 0.0)
    
    preco_min = float(df['preço'].min())
    preco_max = float(df['preço'].max())

    # Filtro para preço
    preco_filter = st.slider("Escolha o preço máximo", preco_min, preco_max, preco_max)
    filtered_df = df


    if st.button("Filtrar por regiao") or (st.session_state["last_clicked"] == "Filtrar por regiao"):
        button_clicked(button_name="Filtrar por regiao")

        # Criar o mapa interativo de Boston
        boston_map = folium.Map(location=[42.308103483524164, -71.11291662888864], zoom_start=12)  # Boston latitude e longitude

        # Exibir o mapa interativo e capturar a localização clicada
        mapa_interativo = st_folium(boston_map, width=1500, height=500)


        if mapa_interativo.get('last_clicked'):
            button_clicked(button_name="Mapa iterativo")

            latitude = mapa_interativo['last_clicked']['lat']
            longitude = mapa_interativo['last_clicked']['lng']
            
            # Mostrar as coordenadas no Streamlit
            st.write(f"Coordenadas selecionadas: Latitude: {latitude}, Longitude: {longitude}")

            # Usar essas coordenadas para filtrar as publicações
            ids_filtrados_local = filtrar_local(latitude, longitude, conn)
            filtered_df = filtered_df[filtered_df['ID_Postagem'].isin(ids_filtrados_local['ID_Postagem'])]
                

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

    # Exemplo de conteúdo na aba de Analytics
    st.subheader("Aqui vai ser a aba com as 5 consultas que a gente já tem")

    # Consulta para obter o número de propriedades por host
    view1 = prop_por_hosts(conn)
    st.subheader("Ranking dos Hosts")
    st.dataframe(view1)

    view2 = reviews_por_post(conn)
    st.subheader("Review por Post")
    st.dataframe(view2)

    view3 = preco_local_comodidade(conn)
    st.subheader("Preco Local Comodidade")
    st.dataframe(view3)


    # Criando um layout de 2 colunas para os gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico: Número de propriedades por host (barra horizontal)
        st.subheader("Número de Propriedades por Host")
        fig = px.bar(df, x='Numero_De_Propriedades', y='Nome_Host', 
                    orientation='h', title='Número de Propriedades por Host')
        st.plotly_chart(fig)

    with col2:
        # Gráfico: Distribuição de Propriedades por Host (dispersão)
        st.subheader("Distribuição das Propriedades por Host")
        fig2 = px.scatter(df, x='Nome_Host', y='Numero_De_Propriedades', 
                        title='Distribuição das Propriedades por Host', 
                        labels={'Nome_Host': 'Nome do Host', 'Numero_De_Propriedades': 'Número de Propriedades'})
        st.plotly_chart(fig2)

    # Filtro para selecionar um host
    host_selecao = st.selectbox("Selecione um Host", df['Nome_Host'].unique().tolist())

    # Filtro dos dados baseado na seleção do host
    filtered_df = df[df['Nome_Host'] == host_selecao]

    # Exibindo dados do host selecionado
    if not filtered_df.empty:
        st.subheader(f"Detalhes para o Host: {host_selecao}")
        st.dataframe(filtered_df)
    else:
        st.write("Nenhum dado encontrado para o Host selecionado.")

