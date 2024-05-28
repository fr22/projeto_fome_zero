#========================================
# Imports
#========================================
import pandas as pd
import inflection
import numpy as np
import plotly.express as px
import streamlit as st
st.set_page_config(
    page_title = 'Cuisines' ,
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



#------------slider--------------
itens = st.sidebar.slider(
    'Selecione a quantidade de itens que deseja exibir',
    value = 5,
    min_value = 1,
    max_value = 20
)
# filtro por culinaria
culinarias = st.sidebar.multiselect('Escolha pelo menos 5 tipos de culinária',
    list(dfb.loc[:,'cuisines'].unique()),
    default = ['Brazilian', 'BBQ', 'Italian', 'Japanese', 'Indian']
)

filtro = (dfb['country_code'].isin(paises)) & (dfb['cuisines'].isin(culinarias))
dfb = dfb.loc[filtro,:]





#========================================
# layout
#========================================

with st.container():
    st.markdown('### Melhores Restaurantes dos Principais tipos Culinários')
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        try:
            cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes', 'currency']
            dfr = dfb.loc[dfb['cuisines'] == culinarias[0], cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
            dfr = dfr.iloc[0,:]
        except:
            st.markdown('#### Erro! Mude os valores dos parâmetros!')
        else:
            st.metric(label = f"{dfr['cuisines']}: {dfr['restaurant_name']}",
                     value = f"{dfr['aggregate_rating']:.2f}/5",
                     help = f"""País: {dfr['country_code']}\n
Cidade: {dfr['city']}\n
Preço pra dois: {dfr['average_cost_for_two']} {dfr['currency']}"""
                     )
    with col2:
        
        try:
            cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes', 'currency']
            dfr = dfb.loc[dfb['cuisines'] == culinarias[1], cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
            dfr = dfr.iloc[0,:]
        except:
            st.markdown('#### Erro! Mude os valores dos parâmetros!')
        else:
            st.metric(label = f"{dfr['cuisines']}: {dfr['restaurant_name']}",
                     value = f"{dfr['aggregate_rating']:.2f}/5",
                     help = f"""País: {dfr['country_code']}\n
Cidade: {dfr['city']}\n
Preço pra dois: {dfr['average_cost_for_two']} {dfr['currency']}"""
                     )
        
    with col3:
        
        try:
            cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes', 'currency']
            dfr = dfb.loc[dfb['cuisines'] == culinarias[2], cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
            dfr = dfr.iloc[0,:]
        except:
            st.markdown('#### Erro! Mude os valores dos parâmetros!')
        else:
            st.metric(label = f"{dfr['cuisines']}: {dfr['restaurant_name']}",
                     value = f"{dfr['aggregate_rating']:.2f}/5",
                     help = f"""País: {dfr['country_code']}\n
Cidade: {dfr['city']}\n
Preço pra dois: {dfr['average_cost_for_two']} {dfr['currency']}"""
                     )
    with col4:
        try:
            cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes', 'currency']
            dfr = dfb.loc[dfb['cuisines'] == culinarias[3], cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
            dfr = dfr.iloc[0,:]
        except:
            st.markdown('#### Erro! Mude os valores dos parâmetros!')
        else:
            st.metric(label = f"{dfr['cuisines']}: {dfr['restaurant_name']}",
                     value = f"{dfr['aggregate_rating']:.2f}/5",
                     help = f"""País: {dfr['country_code']}\n
Cidade: {dfr['city']}\n
Preço pra dois: {dfr['average_cost_for_two']} {dfr['currency']}"""
                     )
    with col5:
        try:
            cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes', 'currency']
            dfr = dfb.loc[dfb['cuisines'] == culinarias[4], cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
            dfr = dfr.iloc[0,:]
        except:
            st.markdown('#### Erro! Mude os valores dos parâmetros!')
        else:
            st.metric(label = f"{dfr['cuisines']}: {dfr['restaurant_name']}",
                     value = f"{dfr['aggregate_rating']:.2f}/5",
                     help = f"""País: {dfr['country_code']}\n
Cidade: {dfr['city']}\n
Preço pra dois: {dfr['average_cost_for_two']} {dfr['currency']}"""
                     )


with st.container():
    st.markdown(f'### Top {itens} restaurantes')
    # top restaurantes
    var = itens
    cols = ['restaurant_id', 'restaurant_name',	'country_code', 'city', 'cuisines',	'average_cost_for_two', 'aggregate_rating', 'votes']
    dfr = dfb.loc[:, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending = [False, True])
    dfr = dfr.iloc[0:var,:]
    st.dataframe(dfr)

with st.container():
    st.markdown('### Culinárias em destaque')
    col1,col2 = st.columns(2)
    with col1:
        st.markdown(f'### Top {itens} melhores culinárias')
        # top tipos de culinarias
        var = itens
        dfr = dfb.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending = False).reset_index()
        dfr['aggregate_rating'] = dfr['aggregate_rating'].apply(lambda x: np.round(x, 1))
        dfr = dfr.iloc[0:var,:]
        gr = px.bar(dfr, x = 'cuisines', y = 'aggregate_rating'#, color = 'country_code'
                    , text = 'aggregate_rating',
                       labels = {'cuisines':'Tipos de culinárias','aggregate_rating':'Avaliação média' })
        st.plotly_chart(gr, use_container_width = True)

    with col2:
        st.markdown(f'### Top {itens} piores culinárias')
        # Top piores
        var = itens
        dfr = dfb.loc[:, ['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending = True).reset_index()
        dfr['aggregate_rating'] = dfr['aggregate_rating'].apply(lambda x: np.round(x, 1))
        dfr = dfr.iloc[0:var,:]
        gr = px.bar(dfr, x = 'cuisines', y = 'aggregate_rating', text = 'aggregate_rating',
                       labels = {'cuisines':'Tipos de culinárias','aggregate_rating':'Avaliação média' })
        st.plotly_chart(gr, use_container_width = True)
