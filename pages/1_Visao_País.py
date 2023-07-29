#bibliotecas
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config( page_title='Visão País', layout='wide')

# Arquivo para upload
df = pd.read_csv('zomato.csv')

#funções
#Preenchimento do nome dos paises
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id): 
    return COUNTRIES[country_id]


#Criação do tipo de categoria de comida

def price_tye(price_range):
    if price_range == 1: return "cheap"
    elif price_range == 2: return "normal"
    elif price_range == 3: return "expensive"
    else:
        return "gourmet"
    
# Criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]  

#Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x) 
    snakecase = lambda x: inflection.underscore(x) 
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old)) 
    cols_new = list(map(snakecase, cols_old)) 
    df.columns = cols_new
    return df

#Limpeza dos dados duplicados
df = df.drop_duplicates(subset='Restaurant ID')

#verificando e retirando os valores NAN
# encontramos valores nulos na coluna Cuiisines
#df.isnull().sum()  nesta linha vai fazer a verificação
df= df.copy()
df = df.dropna(subset=['Cuisines'])
#df.isnull().sum() exibindo o resultado após o drop de valor ausente
df = df.reset_index()
del df['index']
#df.loc[:,'Cuisines'] = df.loc[:,'Cuisines'].str.strip()

#df['Cuisines'].fillna('null', inplace=True)
#linhas_selecionadas = (df['Cuisines'] != 'null')
#df = df.loc[linhas_selecionadas,:].copy()

#Verificando valores duplicados
# df.duplicated().sum() com esata função verificamos que há 583 valores duplicados
# Removendo os valores duplicados e deixando apenas a primeira ocorrencia. Realizamos também o reset do index
df = df.drop_duplicates().reset_index()
del df['index']

#Edições

## Edição da tabela country

df['Country_Name'] = df['Country Code'].apply(country_name)
## Edição da tabela price

df['Price'] = df['Price range'].apply(price_tye)

#Conversão de texto/categoria/string para numeros inteiros
df['Price range'] = df['Price range'].astype(int)

#Conversão de texto/categoria/string para numeros decimais
df['Average Cost for two'] =df['Average Cost for two'].astype(int)

df['Aggregate rating'] = df['Aggregate rating'].astype(float)

# A coluna Cuisines possui mais de 1 valor de culinaria. Então esse código pega apenas 1 valor.
df['Cuisines']= df.loc[:,'Cuisines'].apply(lambda x: x.split(',')[0])

# Retirar os valores 0 
df = df.loc[df['Aggregate rating'] != 0]
# Retirar valores Other da coluna Cuisines
df = df.loc[df['Cuisines'] != 'Others']



#==============================
# Layout no Streamlit
#==============================

st.header('Países em que atuamos 🌎')
#image_path='/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/pages/NewLogo.png'

image = Image.open('logo.png')
st.sidebar.image( image, width=80)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Encontre seu restaurante favorito conosco')
st.sidebar.markdown('---')

st.sidebar.markdown('## Selecione os locais que deseja visualizar')

country_options = st.sidebar.multiselect(
    'Seleção de Países',
    ['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'],
    default=['India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'])

#Filtro de países
line = df['Country_Name'].isin(country_options)
df = df.loc[line,:]

#================================================

st.markdown('### Quantidade de restaurantes registrados por País')

#=====Dash 1======

cols = ['Country_Name', 'Restaurant ID']

df_aux = df.loc[:,cols].groupby('Country_Name').count().sort_values('Restaurant ID', ascending=False).reset_index()
df_aux.rename(columns={'Country_Name': 'Nome do País','Restaurant ID' : 'Qtd de Restaurantes'}, inplace=True)
fig = px.bar(df_aux, x='Nome do País', y='Qtd de Restaurantes')
st.plotly_chart(fig, use_container_width=True)

#====Dash 2================================

st.markdown('### Quantidade de Cidades registradas por País')

cols = ['Country_Name', 'City']
df_aux = df.loc[:,cols].groupby('Country_Name').nunique().sort_values('City', ascending=False).reset_index()
df_aux.rename(columns={'Country_Name':'Nome do País', 'City' : 'Qtd de Cidades'}, inplace=True)
fig = px.bar( df_aux, x='Nome do País', y= 'Qtd de Cidades')
st.plotly_chart(fig, use_container_width=True)

#=============Dash 3 e 4====================

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Top 5 Países com mais avaliações ')
        cols = ['Country_Name', 'Votes']
        df_aux = df.loc[:,cols].groupby('Country_Name').mean().sort_values('Votes',ascending=False).reset_index()
        df_aux.rename(columns={'Country_Name':'Nome do País','Votes' : 'Avaliações'}, inplace=True)
        df_aux = round(df_aux)
        df_aux = df_aux.head(5)
        fig =px.bar(df_aux, x='Nome do País', y='Avaliações')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('##### Média de preço de um prato para 2 pessoas por País ')
        df_aux = df.loc[:,['Average Cost for two','Country_Name']].groupby('Country_Name').mean().round().sort_values('Average Cost for two', ascending=False).reset_index()
        df_aux.rename(columns={'Country_Name': 'Nome do País', 'Average Cost for two' : 'Média de valor para duas pessoas'}, inplace=True)
        fig = px.bar (df_aux, x='Nome do País', y='Média de valor para duas pessoas')
        st.plotly_chart(fig, use_container_width=False)
