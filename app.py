import pandas as pd
import streamlit as st

# Substituir o dataframe pela consulta no banco de dados
data = {
    "host": ["João", "Maria", "Carlos", "Ana"],
    "local": ["Rio de Janeiro", "São Paulo", "Curitiba", "Paris"],
    "nota": [4.5, 4.8, 4.2, 4.9],
    "preço": ["R$200", "R$150", "R$100", "€300"]
}
df = pd.DataFrame(data)

# Adicionar título à página
st.set_page_config(page_title="Feed de Postagens", layout="wide")
st.title("Feed de Postagens")

# CSS para a caixa estilizada
st.markdown(
    """
    <style>
    .div-box {
        background-color: #333333;  /* Cor de fundo cinza escuro */
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        color: white; /* Texto branco */
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Criar uma caixa para cada linha do DataFrame
for _, row in df.iterrows():
    st.markdown(
        f"""
        <div class="div-box">
            <h3>Postagem</h3>
            <p><strong>Host:</strong> {row['host']}</p>
            <p><strong>Local:</strong> {row['local']}</p>
            <p><strong>Nota:</strong> {row['nota']} ⭐</p>
            <p><strong>Preço:</strong> {row['preço']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )