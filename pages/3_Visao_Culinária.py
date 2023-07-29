#bibliotecas
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium

st.set_page_config( page_title='Visão Culinária', layout='wide')


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
df=df.loc[df['Cuisines'] != 'Others']

#==============================
# Layout no Streamlit
#==============================

#===Header========
st.header('Overview - Culinária 🍽️')

#=======Barra Lateral===========

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

########### Slicer de restaurantes ################
st.sidebar.markdown('## Selecione a quantidade de restaurantes que deseja visualizar')
x = st.sidebar.slider('',min_value=1, max_value=10, value=5)

#============Filtro de Culinaria====================
st.sidebar.markdown('## Selecione o tipo de Culinária')
cuisines_opt = st.sidebar.multiselect(
    '',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
    'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
    'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
    'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
    'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
    'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
    'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
    'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
    'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
    'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
    'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
    'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
    'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
    'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
    'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
    'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
    'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
    'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
    'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
    'Continental', 'South Indian', 'North Indian', 'Salad',
    'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
    'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
    'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
    'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
    'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
    'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
    'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
    'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
    'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
    'South African', 'Drinks Only', 'Durban', 'World Cuisine',
    'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
    'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
    'Kokoreç'],
    default=['Home-made', 'BBQ','Japanese','Brazilian','Arabian','American','Italian'])


#============Início================

st.header('Melhores Restaurantes dos tipos Culinários selecionados')
#==========dash 1====================
cols = ['Restaurant Name','Cuisines','Country_Name','Average Cost for two','Aggregate rating','Votes','City']
df_aux = df.loc[:,cols]
df_filter = df_aux[df_aux['Cuisines'].isin(cuisines_opt)].head(x).reset_index()
st.dataframe(df_filter)

#===========2 dash===============

with st.container():
    col1,col2 = st.columns(2)

with col1:
    st.markdown('##### Top 5 melhores tipos de Culinárias')
    df_aux = df.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=False).reset_index()
    df_aux.rename(columns={'Aggregate rating' : 'Nota Média','Cuisines' : 'Culinária'}, inplace=True)
    df_aux = df_aux.head(5)
    fig = px.bar(df_aux, x='Culinária',y='Nota Média')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('##### Top 5 Piores tipos de Culinárias')
    df_aux = df.loc[:,['Cuisines','Aggregate rating']].groupby('Cuisines').mean().sort_values('Aggregate rating', ascending=True).reset_index()
    df_aux.rename(columns={'Aggregate rating' : 'Nota Média','Cuisines' : 'Culinária'}, inplace=True)
    df_aux = df_aux.head(5)
    fig = px.bar(df_aux, x='Culinária',y='Nota Média')
    st.plotly_chart(fig, use_container_width=True)

