# **Airbnb Data Explorer**  

Este repositório contém um projeto focado na criação de um site interativo, desenvolvido com **Streamlit**, que explora os dados do Airbnb e oferece insights detalhados sobre propriedades, avaliações e anfitriões.  

O projeto utiliza um banco de dados relacional modelado a partir de dados reais do Airbnb (dataset disponível no Kaggle), abordando funcionalidades como pesquisa por localidade, análise de preços e avaliações, e visualizações personalizadas.

---

## **Funcionalidades do Site**  

1. **Exploração de Propriedades**  
   - Lista de propriedades com informações detalhadas (preço, tipo, comodidades).  
   - Filtros por cidade, faixa de preço, número de quartos e mais.  

2. **Avaliações e Notas**  
   - Avaliações de usuários para cada propriedade.  
   - Rankings de propriedades com base nas notas médias.  

3. **Análise Geográfica**  
   - Visualização das propriedades em um mapa interativo com coordenadas geográficas.  

4. **Insights de Anfitriões**  
   - Estatísticas sobre anfitriões, como o número de propriedades e tempo médio de resposta.  

5. **Consultas Personalizadas**  
   - Painel para executar consultas SQL diretamente no banco de dados.  

---

## **Tecnologias Utilizadas**  

### **Frontend**  
- **[Streamlit](https://streamlit.io/)**: Framework para criar interfaces web interativas de forma rápida e eficiente.  

### **Backend**  
- **MySQL**: Banco de dados utilizado para armazenar as informações processadas.  

### **Data Pipeline**  
- **Python (Pandas, SQLAlchemy)**: Para manipulação de dados e integração com o banco de dados.  

---

## **Arquitetura do Projeto**  

### **Modelo de Banco de Dados**  

O banco foi modelado para representar as relações entre propriedades, anfitriões, localizações e avaliações.  

### **Fluxo de Dados**  
1. **Ingestão de Dados**:  
   - Dados importados do [dataset do Kaggle](https://www.kaggle.com/datasets/airbnb/boston) em arquivos CSV.  
2. **Armazenamento**:  
   - Dados carregados no MySQL após limpeza e transformação.  
3. **Visualização**:  
   - O Streamlit consome os dados para renderizar gráficos, tabelas e mapas interativos.  

---

## **Como Executar o Projeto**  

### **1. Pré-requisitos**  
- **Python 3.8+**  
- **MySQL 8.0+**  
- Bibliotecas Python:  
  ```bash
  pip install -r requirements.txt
  ```
  Arquivo `requirements.txt` inclui:  
  - `streamlit`  
  - `pandas`  
  - `sqlalchemy`  
  - `mysql-connector-python`  

---

### **2. Configuração do Banco de Dados**  
1. Crie o banco de dados:  
   - Use o script `db_setup.sql` disponível no repositório.  
   - Popule as tabelas com os dados do dataset utilizando o script `data_ingestion.py`.  

2. Configure as credenciais do banco no arquivo `.env`:  
   ```
   DB_HOST=localhost
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=nome_do_banco
   ```

---

### **3. Executando o Site**  
No diretório do projeto, rode o comando:  
```bash
streamlit run app.py
```  
O site estará disponível no navegador em: `http://localhost:8501`  

---

## **Capturas de Tela**  

### Página Inicial  
![Página Inicial](assets/home_page.png)  

### Visualização de Propriedades  
![Visualização](assets/property_view.png)  

---

## **Contribuições**  
Contribuições são bem-vindas! Siga os passos abaixo para colaborar:  
1. Faça um fork do projeto.  
2. Crie uma branch para suas alterações:  
   ```bash
   git checkout -b minha-feature
   ```  
3. Envie um pull request detalhando suas alterações.  

---

