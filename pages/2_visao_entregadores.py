#Librares(Bibliotecas necessárias)
import pandas as pd
import re
import folium
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config( page_title = "Visão Entregadores", page_icon= "", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def top_delivers( df1, top_asc): 
    """ Esta função tem a responsabilidade de gerar dataframe
        
        métrica = 10 entregadores mais rápidos por cidades ou 10 entregadores mais lentos por cidade
                
        Input: DataFrame
        Output: DataFrame
    """
    # seleção de linhas
    df2 = (df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)','City']]
              .groupby(['City','Delivery_person_ID'])
              .mean()
              .sort_values(['City','Time_taken(min)'], ascending=top_asc)
              .reset_index())
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03 ]).reset_index ( drop=True)

    return df3

def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Input: DataFrame
        Output: DataFrame
    """
    # Remover spaco da string
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Delivery_person_Age'] = df1.loc[:, 'Delivery_person_Age'].str.strip()
    df1.loc[:, 'multiple_deliveries'] = df1.loc[:, 'multiple_deliveries'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    df1 = df1.loc[df1['Delivery_person_Age'] != 'NaN', :]
    df1 = df1.loc[df1['Road_traffic_density'] != "NaN",:]
    df1 = df1.loc[df1['City'] != "NaN", :]
    df1 = df1.loc[df1['Road_traffic_density'] != "NaN", :]
    df1 = df1.loc[df1['multiple_deliveries'] != 'NaN', :]
    df1 = df1.loc[df1['Festival'] != 'NaN', :]

    # Conversao de texto/categoria/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    # Conversao de texto/categoria/strings para numeros decimais
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Conversao de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

    # Comando para remover o texto de números
    df1 = df1.reset_index( drop=True )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    
    return df1

#--------------------------------------- Inicio da Estrutura lógica do código ------------------------------------------------------------

# ============================================================================================
#Import Dataset
# ============================================================================================
#Import Dataset
df = pd.read_csv('train.csv')

# ============================================================================================
# Limpando os dados
# ============================================================================================
# Fazendo uma cópia do DataFrame Lido
df1 = clean_code( df )

# ============================================================================================
# Barra lateral
# ============================================================================================
st.markdown('# Marktplace - Visão Entregadores')

image_path='logo.png'
Image = Image.open(image_path)
st.sidebar.image(Image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022,4,13),
    min_value=pd.datetime(2022,2,11),
    max_value=pd.datetime(2022,4,6),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High' , 'Jam'],
    default =  ['Low', 'Medium', 'High' , 'Jam'])
st.sidebar.markdown("""---""")

Weatherconditions_options = st.sidebar.multiselect(
    'Quais as condições do clima',
    ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms' , 'conditions Cloudy' , 'conditions Fog', 'conditions Windy'],
    default =  ['conditions Sunny', 'conditions Stormy', 'conditions Sandstorms' , 'conditions Cloudy' , 'conditions Fog', 'conditions Windy'])
st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powerd by Comunidade DS')

#Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Clima
linhas_selecionadas = df1['Weatherconditions'].isin(Weatherconditions_options)
df1 = df1.loc[linhas_selecionadas, :]

# ============================================================================================
# Layout no Streamlit
# ============================================================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    with st.container():
        st.title( 'Overall Metrics' )
        col1, col2, col3, col4 = st.columns( 4, gap='large' )
        with col1:
            # A maior idade entregadores
            maior_idade = df1.loc[:,"Delivery_person_Age"].max()
            col1.metric( 'Maior Idade',maior_idade )
        with col2:
            # A menor idade entregadores
            menor_idade = df1.loc[:,"Delivery_person_Age"].min()
            col2.metric( 'Menor Idade',menor_idade )
        with col3:
            # A melhor condição de veículo
            melhor_condicao_veiculo = df1.loc[:,"Vehicle_condition"].max()
            col3.metric( 'Melhor Condição', melhor_condicao_veiculo )
        with col4:
            # A pior condição de veículo
            pior_condicao_veiculo = df1.loc[:,"Vehicle_condition"].min()
            col4.metric( 'Pior Condição', pior_condicao_veiculo )
            
    with st.container():
        st.markdown("""___""")
        st.title( 'Avaliações' )
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown('##### Avaliação média por entregador')
            # seleção de linhas
            df_ratings_por_delivery = (df1.loc[:, ['Delivery_person_Ratings','Delivery_person_ID']]
                                          .groupby(['Delivery_person_ID'])
                                          .mean()
                                          .reset_index())
            st.dataframe(df_ratings_por_delivery)
            
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            # seleção de linhas
            df_ratings_por_trafego = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density']]
                                        .groupby(['Road_traffic_density'])
                                        .agg({'Delivery_person_Ratings' : ['mean','std']}))

            # alteração dos nomes das colunas
            df_ratings_por_trafego.columns = ['Delivery_mean','Delivery_std']

            # reset_index
            df_ratings_por_trafego = df_ratings_por_trafego.reset_index()
            st.dataframe(df_ratings_por_trafego)
            
            st.markdown('##### Avaliação média por clima')
            # seleção de linhas
            df_ratings_por_condicao_climatica = (df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                                                    .groupby(['Weatherconditions'])
                                                    .agg({'Delivery_person_Ratings' : ['mean','std']}))

            # alteração dos nomes das colunas
            df_ratings_por_condicao_climatica.columns = ['Delivery_mean','Delivery_std']

            # reset_index
            df_ratings_por_condicao_climatica = df_ratings_por_condicao_climatica.reset_index()
            st.dataframe(df_ratings_por_condicao_climatica)
            
    with st.container():
        st.markdown("""___""")
        st.title( 'Velocidade de Entrega' )
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivers( df1, top_asc=True)
            st.dataframe(df3)
            
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivers( df1, top_asc=False)
            st.dataframe(df3)
            
            
            
            
                                
