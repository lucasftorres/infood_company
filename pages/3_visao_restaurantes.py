# Libraries
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
from haversine import haversine
import pandas as pd
import datetime
import streamlit as st
import re
from PIL import Image
import folium
from streamlit_folium import folium_static
import numpy as np

st.set_page_config(layout="wide")

# --------------------------------
# Funções
# --------------------------------


def avg_std_time_on_traffic( df1 ):                
    df2 = ( df1.loc[:, ['City', 'Road_traffic_density','Time_taken(min)']]
                .groupby(['City', 'Road_traffic_density'])
                .agg({'Time_taken(min)': ['mean', 'std']}) )
                
    df2.columns = ['Mean', 'Std']
    df2 = df2.reset_index()
                
    fig = px.sunburst( df2, path = ['City', 'Road_traffic_density'], values = 'Mean',
                        color = 'Std', color_continuous_scale = 'RdBu',
                        color_continuous_midpoint = np.average(df2['Std'] ) )
    return fig


def avg_std_timne_graph( df1 ):                
    df2 = ( df1.loc[:, ['City', 'Time_taken(min)']]
                .groupby( 'City' )
                .agg( {'Time_taken(min)': ['mean', 'std']} ) )
    df2.columns = ['Mean', 'Std']
    df2 = df2.reset_index()
                
    fig = go.Figure()
    fig.add_trace( go.Bar( name = 'Control', x = df2['City'], y = df2['Mean'],
                            error_y = dict( type = 'data', array = df2['Std'] ) ) )
    fig.update_layout( barmode = 'group' )

    return fig


def avg_std_time_delivery(df1, op, festival):  
    df2 = ( df1.loc[:, ['Festival', 'Time_taken(min)']]
                .groupby('Festival')
                .agg({'Time_taken(min)': ['mean', 'std']}))
                
    df2.columns = ['Mean', 'Std']
    df2 = df2.reset_index()
    df2 = np.round(df2.loc[df2['Festival'] == festival, 'Mean'], 2)

    return df2



def distance(df1):
    columns = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude', ]    
    df1['Distance'] = df1.loc[:, columns].apply( lambda x: 
                                                haversine((x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                                            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1 )               
    fig = np.round(df1['Distance'].mean(), 2)
        
    return fig

   


def distance2(df1):
    
    df1['Distance'] = ( df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]]
                                   .apply( lambda x: 
                                    haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1 ))
        
    distance = df1['Distance'].mean()
    avg_distance = df1.loc[:, ['City', 'Distance']].groupby( 'City' ).mean().reset_index()

    fig = go.Figure( data = [go.Pie(labels = avg_distance['City'], values = avg_distance['Distance'], pull = [0, 0.1, 0])])
    return fig




def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe

    Tipos de limpeza:
    1. Remoção de dados NaN
    2. Mudança do tipo de Coluna de dados
    3. Remoção dos espaços das variáveis de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo ( remoção do texto da variável numérica )

    Input: Dataframe
    Output: Dataframe

    """
    
    # 1. Remoção das Linhas que possuam NaN
    # Remove as linhas da coluna Delivery_person_Age que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['Delivery_person_Age'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'Road_traffic_density' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['Road_traffic_density'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'City' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['City'] != 'NaN ' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna 'Develivery_person_Age' que tenham o conteudo igual ao NaN
    linhas_selecionadas = ( df1['Festival'] != 'NaN' )
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linhas da coluna Weatherconditions que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['Weatherconditions'] != 'NaN' ) 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # Remove as linha da coluna multiple_deliveries  que tenham o conteudo igual a NaN
    linhas_selecionadas = ( df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    
     # 2.
    # Conversão de texto/categoria/string para numeros float utilizando o método astype()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    # 3.
    # Conversão de texto para data utilizando o método to_datetime() onde em format= o ano sempre será marcado com Y maíusculo
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    
    # 4.
    # O método strip() irá remover os espaços vazios da string
    # Substituindo as colunas por novas sem os espaços na string
    
    
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # O método reset_index irá fazer uma atualização do DataFrame após a remoção das linhas que tinham o 'NaN '
    df1 = df1.reset_index(drop=True)
    
    # Comando para remover o texto de números
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split(' ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )

    return df1


# ------------------------------ Início da Estrutura Lógica do Código


# ===================
# Import dataset
# ===================
df = pd.read_csv( 'dataset/train.csv' )
df1 = df.copy()

df1 = clean_code( df )


# ==============================
# Barra Lateral
# ==============================

st.markdown('<div style="text-align: center; font-size:50px; font-weight: 600;">Marketplace - Restaurantes</div>', unsafe_allow_html=True)

image = Image.open( 'Icon.png' )
st.sidebar.image( image, width = 120 )

st.sidebar.markdown('<div style="text-align: center; font-size:30px; font-weight: 600;"><i>InFood</i></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div style="text-align: center; font-size:20px; font-weight: 600;">The Best Delivery</div>', unsafe_allow_html=True)
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = datetime.date( 2022, 4 , 13 ),
    min_value = datetime.date( 2022, 2, 11 ),
    max_value = datetime.date( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown("""---""")
print(type(date_slider))
traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

# Filtro de data
linhas_selecionadas = ( df1['Order_Date'].dt.date < date_slider )
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = ( df1['Road_traffic_density'].isin(traffic_options) )
df1 = df1.loc[linhas_selecionadas, :]

# ==============================
# Layout no Streamlit
# ==============================


tab1, tab2, tab3 = st.tabs( [ 'Visão Gerencial', '-', '-'] )

with tab1:
    with st.container():
        st.markdown('<div style="text-align: center; font-size:40px; font-weight: 600;padding-bottom: 20px;">Overall  Metrics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric( 'Entregadores únicos', delivery_unique )
            
        with col2:
            distance = distance(df1)
            col2.metric('Distancia Média', distance)
                
        with col3:
            df2 = avg_std_time_delivery( df1, 'Mean', 'Yes')
            col3.metric('Tempo Médio', df2)
                      
        with col4:
            df2 = avg_std_time_delivery( df1, 'Std', 'Yes')
            col4.metric('STD Entrega', df2)
    
        with col5:
            df2 = avg_std_time_delivery( df1, 'Mean', 'No')
            col5.metric('Tempo Médio', df2)
            
        with col6:
            df2 = avg_std_time_delivery( df1, 'Std', 'No')
            col6.metric('STD Entrega', df2)
        
    with st.container():
        st.markdown( """---""" )
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig = avg_std_timne_graph( df1 )
            st.plotly_chart(fig, use_container_width = True )
        
        with col2:        
            df2 = ( df1.loc[:, ['City', 'Type_of_order', 'Time_taken(min)']]
                       .groupby(['City', 'Type_of_order'])
                       .agg({'Time_taken(min)': ['mean', 'std']}) )
        
            df2.columns = ['Mean', 'Std']
            df2 = df2.reset_index()
            st.dataframe(df2, use_container_width = True )
        
    
    with st.container():
        st.markdown('<div style="text-align: center; font-size:40px; font-weight: 600;padding-bottom: 10px;">Distribuição do Tempo</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns( 2 )
        
        with col1:
            fig = distance2( df1)
            st.plotly_chart( fig, use_container_width = True  )
            #st.title( "Distribuição do Tempo" )       
        with col2:
            fig = avg_std_time_on_traffic( df1 )
            st.plotly_chart( fig, use_container_width = True  )
    
    with st.container():
        st.markdown("""---""")
        st.markdown('<div style="text-align: center; font-size:40px; font-weight: 600;padding-bottom: 20px;">Distribuição da Distancia</div>', unsafe_allow_html=True)
        
        df2 = ( df1.loc[:, ['City', 'Type_of_order', 'Time_taken(min)']]
                  .groupby(['City', 'Type_of_order'])
                  .agg({'Time_taken(min)': ['mean', 'std']}) )
        
        df2.columns = ['Mean', 'Std']
        df2 = df2.reset_index()
        st.dataframe(df2, use_container_width = True )