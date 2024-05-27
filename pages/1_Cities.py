#========================================
# Imports
#========================================
import pandas as pd
import inflection
import numpy as np
import plotly.express as px
import streamlit as st
st.set_page_config(
    page_title = 'Cities' ,
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

st.sidebar.markdown('## Filtros')
st.sidebar.markdown('### Países')
# filtro por países
paises = st.sidebar.multiselect('Escolha os países de que deseja visualizar informações',
    list(dfb.loc[:,'country_code'].unique()),
    default = ['Brazil', 'England', 'Canada']
)

filtro = dfb['country_code'].isin(paises)
dfb = dfb.loc[filtro,:]


#========================================
# layout
#========================================
st.title('Visão Cidades')
#dfr = dfb.copy()
with st.container():
    st.markdown('### Top 10 cidades com mais restaurantes registrados')
    # Top 10 cidades com mais restaurantes registrados
    dfr = dfb.loc[:, ['city', 'country_code', 'restaurant_id']].groupby(['city','country_code']).count().sort_values('restaurant_id', ascending = False).reset_index()
    dfr = dfr.loc[0:9,:]
    gr = px.bar(dfr, x = 'city', y = 'restaurant_id', color = 'country_code', text = 'restaurant_id',
                   labels = {'city':'Cidade','restaurant_id':'Restaurantes','country_code':'País' })
    st.plotly_chart(gr, use_container_width = True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Top 7 cidades com mais restaurantes cuja média de avaliação é acima de 4')
        # top 7 cidades com mais restaurantes cuja média de avaliação é acima de 4
        filtro = dfb['aggregate_rating'] > 4
        dfr = dfb.loc[filtro, ['city', 'country_code', 'restaurant_id']].groupby(['city','country_code']).count().sort_values('restaurant_id', ascending = False).reset_index()
        
        dfr = dfr.iloc[0:7,:]
        
        gr = px.bar(dfr, x = 'city', y = 'restaurant_id', color = 'country_code', text = 'restaurant_id',
                       labels = {'city':'Cidade','restaurant_id':'Restaurantes','country_code':'País' })
        st.plotly_chart(gr, use_container_width =True)
    with col2:
        st.markdown('### Top 7 cidades com mais restaurantes cuja média de avaliação é abaixo de 2.5')
        # top 7 cidades com mais restaurantes cuja média de avaliação é abaixo de 2.5
        filtro = dfb['aggregate_rating'] < 2.5
        dfr = dfb.loc[filtro, ['city', 'country_code', 'restaurant_id']].groupby(['city','country_code']).count().sort_values('restaurant_id', ascending = False).reset_index()
        dfr = dfr.iloc[0:7,:]
        gr = px.bar(dfr, x = 'city', y = 'restaurant_id', color = 'country_code', text = 'restaurant_id',
                       labels = {'city':'Cidade','restaurant_id':'Restaurantes','country_code':'País' })
        st.plotly_chart(gr, use_container_width =True)
        
with st.container():
    st.markdown('### Top 10 cidades com mais tipos de culinárias')
    # Top 10 cidades com mais tipos de culinárias
    dfr = dfb.loc[filtro, ['city', 'country_code', 'cuisines']].groupby(['city','country_code']).nunique().sort_values('cuisines', ascending = False).reset_index()
    
    dfr = dfr.iloc[0:10,:]
    
    gr = px.bar(dfr, x = 'city', y = 'cuisines', color = 'country_code'
                , text = 'cuisines',
                   labels = {'city':'Cidade','cuisines':'Tipos de culinárias','country_code':'País' })
    st.plotly_chart(gr, use_container_width =True)
    