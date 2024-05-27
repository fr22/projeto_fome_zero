#========================================
# Imports
#========================================
import pandas as pd
import inflection
import numpy as np
import plotly.express as px
import streamlit as st
st.set_page_config(
    page_title = 'Countries' ,
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
st.title('Visão Países')

with st.container():
    
    st.markdown('### Quantidade de restaurantes registrados por país')
    # Quantidade de restaurantes registrados por país
    dfr = dfb.loc[:, ['country_code', 'restaurant_id' ]].groupby('country_code').count().sort_values('restaurant_id', ascending = False).reset_index()
    dfr.columns = ['Países', 'Quantidade de restaurantes']
    
    img = px.bar(dfr, x='Países', y='Quantidade de restaurantes',text = 'Quantidade de restaurantes')
    st.plotly_chart(img, use_container_width = True)

with st.container():
    st.markdown('### Quantidade de cidades registadas por país')
    # Quantidade de cidades registadas por país
    dfr = dfb.loc[:, ['country_code', 'city' ]].groupby('country_code').nunique().sort_values('city', ascending = False).reset_index()
    dfr.columns = ['Países', 'Quantidade de cidades']
    img = px.bar(dfr, x='Países', y='Quantidade de cidades', text = 'Quantidade de cidades')
    st.plotly_chart(img, use_container_width = True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Média de avaliações por país')
        # Média de avaliações por país
        cols = ['country_code','restaurant_id', 'votes']
        dfr = dfb.loc[:, cols].groupby('country_code').agg({'restaurant_id': 'count', 'votes': 'sum'}).reset_index()
        dfr.columns = ['country', 'restaurants', 'votes']
        dfr['avg_votes'] =  np.round(dfr['votes'] / dfr['restaurants'], 1)
        dfr = dfr.sort_values('avg_votes', ascending = False) #.reset_index()
        dfr = dfr.reset_index().drop(columns = 'index', axis = 1)
        img = px.bar(dfr, x= 'country', y = 'avg_votes', text = 'avg_votes', labels = {'country': 'Países', 'avg_votes': 'Avaliações por país'} )
        st.plotly_chart(img, use_container_width = True)

    with col2:
        st.markdown('### Média de preço de prato de duas pessoas por país')
        # Média de preço de prato de duas pessoas por país
        dfr = dfb.loc[:, ['country_code', 'average_cost_for_two']].groupby('country_code').mean().reset_index().sort_values('average_cost_for_two', ascending = False)
        dfr['average_cost_for_two'] = dfr['average_cost_for_two'].apply(lambda x: np.round(x, 1))
        img = px.bar(dfr, x= 'country_code', y = 'average_cost_for_two', text = 'average_cost_for_two', labels = {'country_code': 'Países', 'average_cost_for_two': 'Preço médio de prato pra dois'} )
        st.plotly_chart(img, use_container_width = True)
