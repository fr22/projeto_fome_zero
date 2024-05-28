#========================================
# Imports
#========================================
import pandas as pd
import inflection
import numpy as np
import plotly.express as px
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title = 'Main page' ,
    layout = 'wide'
)
#========================================
# Funções
#========================================



###############

#========================================
# Carregamento de dataset
#========================================
df = pd.read_csv('dataset/zomato.csv')

#========================================
# Limpeza
#========================================
# removendo coluna Switch to order menu	
dfb = df.drop(columns = 'Switch to order menu', axis = 1, inplace= False)
# removendo NA
dfb = dfb.dropna()
# removendo duplicatas
dfb = dfb.drop_duplicates(subset='Restaurant ID')

# Colocar o nome dos países com base no código de cada país
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
dfb['Country Code'] = dfb['Country Code'].apply(country_name)

#Criar a categoria do tipo de comida com base no range de valores
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

dfb['Price range'] = dfb['Price range'].apply(create_price_type)

#Criar o nome das cores com base nos códigos de cores

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

dfb['Rating color'] = dfb['Rating color'].apply(color_name)

# Renomear as colunas do DataFrame

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

dfb = rename_columns(dfb)

# Simplificar culinária

dfb["cuisines"] = dfb.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

#========================================
# Side bar
#========================================
# imagem
with st.sidebar:
    col1,col2 = st.columns(2)
    with col1:
        image = Image.open('logo.png')
        st.image(image, width = 100, )
    with col2:    
        st.markdown('# Fome Zero')
st.sidebar.markdown('## Filtros')
st.sidebar.markdown('### Países')
# filtro por países
paises = st.sidebar.multiselect('Escolha os países de que deseja visualizar informações',
    list(dfb.loc[:,'country_code'].unique()),
    default = ['Brazil', 'England', 'Canada', 'South Africa', 'Australia', 'Qatar']
)
filtro = dfb['country_code'].isin(paises)
dfr = dfb.loc[filtro,:]

# botao
st.sidebar.markdown('### Dados tratados')
def convert_df(df):
    return df.to_csv().encode('utf-8')
file = convert_df(dfb)
st.sidebar.download_button(label = 'Download', data = file, mime = 'text/csv',
                           file_name = 'dados_tratados.csv')
#========================================
# layout
#========================================
st.title('Fome Zero')
st.markdown('## O melhor lugar para encontrar seu mais novo restaurante favorito')

with st.container():
    st.markdown('## Temos as seguintes marcas dentro de nossa plataforma')
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        #resturantes cadastrados
        restaurantes = dfb.loc[:, 'restaurant_id'].nunique()
        st.metric(label = 'Resturantes cadastrados', value= f'{restaurantes:,}')
    with col2:
        # países cadastrados
        paises =  dfb.loc[:, 'country_code'].nunique()
        st.metric(label = 'Países cadastrados', value= paises)
    with col3:
        # cidades cadastrados
        cidades =  dfb.loc[:, 'city'].nunique()
        st.metric(label = 'Cidades cadastradas', value= cidades)
    with col4:
        # avaliações
        avaliacoes =  dfb.loc[:, 'votes'].sum()
        st.metric(label = 'Total de avaliações', value= f'{avaliacoes:,}')
    with col5:
        #tipos de culinarias
        culinarias =  dfb.loc[:, 'cuisines'].nunique()
        st.metric(label = 'Tipos de culinária', value= culinarias)
with st.container():
    
    map = folium.Map()
    cluster = MarkerCluster().add_to(map)
    for index, row in sample.iterrows():
        popup_content = f"""
                        <b>{row['restaurant_name']}</b><br>
                        Preço para dois: {row['average_cost_for_two']} {row['currency']} <br>
                        Culinária: {row['cuisines']}<br>
                        Avaliação: {row['aggregate_rating']}/5
        """
        icon = folium.Icon(color = row['rating_color'],
                          icon = 'utensils', prefix='fa')
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(location = [row['latitude'], row['longitude']]
                      , popup = popup, icon = icon
                     ).add_to(cluster)
    #, popup = row['average_cost_for_two']
    folium_static(map, width=1024, height =600)
    
        
    
