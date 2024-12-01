import pandas as pd
import streamlit as st

# Simular um DataFrame com URLs de imagens de pessoas e casas
data = {
    "host": ["João", "Maria", "Carlos", "Ana"],
    "local": ["Rio de Janeiro", "São Paulo", "Curitiba", "Paris"],
    "nota": [4.5, 4.8, 4.2, 4.9],
    "preço": ["R$200", "R$150", "R$100", "€300"],
    "imagem_host": [
        "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400",
        "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400",
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400",
        "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400"
    ],
    "imagem_casa": [
        "https://demo-source.imgix.net/house.jpg",  # Casa 1
        "https://demo-source.imgix.net/house.jpg",  # Casa 2
        "https://demo-source.imgix.net/house.jpg",  # Casa 3
        "https://demo-source.imgix.net/house.jpg"   # Casa 4
    ]
}
df = pd.DataFrame(data)

# Limpar o campo 'preço' para valores numéricos
df['preço_numérico'] = df['preço'].replace({'R\$': '', '€': '', ',': ''}, regex=True).astype(float)

tab = st.radio("Escolha uma aba", ["Feed", "Analytics"], index=0, horizontal=True)

# Exibindo o conteúdo das abas

# Aba Feed
if tab == "Feed":
    # Configuração da página
    st.title("Feed")

    # Filtros de pesquisa
    st.subheader("Filtrar Publicações")

    # Filtro para local
    local_filter = st.selectbox("Escolha um local", ["Todos"] + df['local'].unique().tolist())

    # Filtro para nota
    nota_filter = st.slider("Escolha a nota mínima", 0.0, 5.0, 0.0)

    # Filtro para preço com valores numéricos
    preço_filter_min = st.slider("Escolha o preço mínimo", float(df['preço_numérico'].min()), float(df['preço_numérico'].max()), float(df['preço_numérico'].mean()))

    # Filtrar o DataFrame com base nas escolhas
    filtered_df = df
    if local_filter != "Todos":
        filtered_df = filtered_df[filtered_df['local'] == local_filter]
    if nota_filter > 0:
        filtered_df = filtered_df[filtered_df['nota'] >= nota_filter]
    filtered_df = filtered_df[filtered_df['preço_numérico'] >= preço_filter_min]

    # CSS para estilizar as caixas
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
        # Criar uma caixa para cada linha do DataFrame filtrado
        for _, row in filtered_df.iterrows():
            st.markdown(
                f"""
                <div class="div-box">
                    <img src="{row['imagem_host']}" alt="Foto do Host" class="host-img">
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
