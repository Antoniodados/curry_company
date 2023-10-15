import streamlit as st
from PIL import Image


st.set_page_config(
    page_title = "Home",
    page_icon = ""
)

image_path='logo.png'
Image = Image.open(image_path)
st.sidebar.image(Image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write( "# Curry Company Growth Dashboard" )

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores  Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crecimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Time de Data Sciense no email
        - antonio.ds@outlook.com.br
    
    """)
