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

st.set_page_config( page_title = "Visão Empresa", page_icon= "", layout= "wide" )

# ============================================================================================
# Funções
# ============================================================================================
def country_maps( df1 ):
    """Essa função tem a responsabilidade de gerar um Mapa
        
        Métrica : Relação central de cada cidade por tipo de tráfego
        
        Input: DataFrame
        Output: Plotar Mapa
    """  
    # seleção de linhas
    cols = ['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']
    df_aux = (df1.loc[:, cols]
                 .groupby(['City','Road_traffic_density'])
                 .median()
                 .reset_index())

    # desenhar o gráfico de mapa
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
      folium.Marker( [location_info['Delivery_location_latitude'],
                      location_info['Delivery_location_longitude']],
                      popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

    folium_static( map, width=1024, height=600 )

def order_share_by_week( df1 ):
    """Essa função tem a responsabilidade de gerar um gráfico de Linha
        
        Métrica : Relação pedido x entregadores por semana
        
        Input: DataFrame
        Output: Plotar Gráfico de Linha
    """  
    # Seleção de linhas para o cálculo/criação de coluna (Qtd de pedidos por semana / Número único de entregadores por semana)
    df_aux01 = (df1.loc[:, ['ID', 'week_of_year']]
                   .groupby('week_of_year')
                   .count().reset_index())
    df_aux02 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                   .groupby('week_of_year')
                   .nunique()
                   .reset_index())

    # união de Data Frame
    df_aux = pd.merge(df_aux01, df_aux02, how='inner')

    # criar a coluna de semana
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    # desenhar o gráfico de linhas
    fig = px.line( df_aux, x='week_of_year', y='order_by_deliver')

    return fig

def order_by_week( df1 ):
    """Essa função tem a responsabilidade de gerar um gráfico de Linha
        
        Métrica : Pedidos por semana
        
        Input: DataFrame
        Output: Plotar Gráfico de Linha
    """  
    # criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')

    # seleção de linhas
    df_aux = (df1.loc[:,['ID', 'week_of_year']]
                 .groupby('week_of_year')
                 .count()
                 .reset_index())

    # desenhar o gráfico de linhas
    fig = px.line(df_aux, x='week_of_year', y='ID')

    return fig

def traffic_order_city( df1 ):
    """Essa função tem a responsabilidade de gerar um gráfico de Bolhas
        
        Métrica : Tipos de trânsito por cidade
        
        Input: DataFrame
        Output: Plotar Gráfico de Bolhas
    """   
    # seleção de linhas
    df_aux = (df1.loc[:,['ID', 'City', 'Road_traffic_density']]
                 .groupby(['City','Road_traffic_density'])
                 .count()
                 .reset_index())

    # desenhar o gráfico de bolha
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')

    return fig

def traffic_order_share( df1):
    """Essa função tem a responsabilidade de gerar um gráfico de Pizza
        
        Métrica : Tipos de trânsito
        
        Input: DataFrame
        Output: Plotar Gráfico de Pizza
    """                
    # seleção de linhas
    df_aux = (df1.loc[:, ['ID','Road_traffic_density']]
                 .groupby(['Road_traffic_density'])
                 .count()
                 .reset_index())

    # criar a coluna de semana
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

    # desenhar o gráfico de pizza
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    
    return fig

def order_metric( df1 ):   
    """ Essa função tem a responsabilidade de gerar um gráfico de barras
        
        Métrica : Pedidos por dia
        
        Input: DataFrame
        Output: Plotar Gráfica de barras
    """
    # coluna
    cols = ['ID','Order_Date']

    # seleção de linhas
    df_aux = (df1.loc[:, cols]
                 .groupby('Order_Date')
                 .count()
                 .reset_index())

    # desenhar o gráfico de barra
    fig = px.bar(df_aux, x='Order_Date', y='ID')

    return fig

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
df = pd.read_csv('train.csv')

# ============================================================================================
# Limpando os dados
# ============================================================================================
df1 = clean_code( df )

# ============================================================================================
# Barra lateral
# ============================================================================================
st.markdown('# Marktplace - Visão Cliente')

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
st.sidebar.markdown('### Powerd by Comunidade DS')

#Filtro de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ============================================================================================
# Layout no Streamlit
# ============================================================================================

tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        fig = order_metric( df1 )
        st.header('Orders by Day')
        st.plotly_chart( fig, use_container_width=True )     
    
        with st.container():    
            col1, col2 = st.columns( 2 )
            with col1:
                fig = traffic_order_share( df1 )
                st.header(' Traffic Order Share')
                st.plotly_chart( fig, use_container_width=True )                
              
            with col2:
                fig = traffic_order_city( df1 )
                st.header(' Traffic Order City')
                st.plotly_chart( fig, use_container_width=True ) 
                   
with tab2:
        with st.container():
            fig = order_by_week( df1 )
            st.markdown('# Order by Week')
            st.plotly_chart( fig, use_container_width=True )
        
        with st.container():
            fig = order_share_by_week( df1 )
            st.markdown('# Order Share by Week')
            st.plotly_chart( fig, use_container_width=True ) 
            
with tab3:
    with st.container():                   
        st.markdown("# Country Maps")
        country_maps( df1 )
        
        

        



