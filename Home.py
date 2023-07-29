import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Página Principal',
    page_icon="🍽️",
    layout='wide'
)
#image_path = '/Users/derekaugusto/Desktop/comunidadeDS/Repos/ftc_python/dataset/'
image = Image.open('logo.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown('# Somos o Fome Zero!')
st.sidebar.markdown('## O melhor lugar para encontrar o seu mais novo restaurante favorito!')

st.write('# Fome Zero Dashboard')

st.markdown(""" O Fome Zero tem o propósito de estreitar a relação entre restaurantes e usuários. No dashboard inicial, o usuário irá se familiarizar com a plataforma.
            
            Há três páginas principais:
            Visão País - Mostra a quantidade de restaurantes cadastrados em cada país, os top 5 países com as melhores avaliações e a média de valores praticados.
            Visão Cidade - Exibe as cidades com as melhores avaliações de restaurantes.
            Visão Culinária - Fornece informações sobre avaliações das melhores tipos de culinárias oferecidas pelos restaurantes. """)