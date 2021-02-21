import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import plotly.offline as offline

data = pd.read_excel('data.xlsx',sep=';')
data_alt_azs = pd.read_excel('data_alt_azs.xlsx',sep=';')

fig = go.Figure()
fig.add_trace(go.Scattermapbox(legendgroup='group',name='Все заправки', #Главный график!
                                 lat=data['LATITUDE'], 
                                 lon=data['LONGITUDE'], 
                                 text=data['AZS_NAME'],showlegend=True,
                                 mode='markers',
                                 marker=dict(colorbar=dict(title="Литры"),
                                             color=data['ЛИТРЫ'],
                                             size=15,
                                             opacity=1,
                                             colorscale='YlGn'),
                                customdata=np.stack([data['ADDRESS'], data['ЛИТРЫ'], 
                                data['FUEL_TYPE'],data['CENA'],
                                data['CLNREW'],data['CLNDISC'],
                                data['СУММА'], data['SUPPLIER']], axis=-1),
                                hovertemplate='<b>%{text}</b>'+ '<br>' +
                                         'Данные1: %{customdata[0]}' + '<br>' +
                                         'Данные2: %{customdata[1]} л.' + '<br>' +
                                         'Данные3: %{customdata[2]}' + '<br>' +
                                         'Данные4: %{customdata[3]} руб.' + '<br>' +
                                         'Данные5: %{customdata[4]} руб.' + '<br>' +
                                         'Данные6: %{customdata[5]} руб.' + '<br>' +
                                         'Данные7: %{customdata[6]} руб.' + '<br>' +
                                         'Данные8: %{customdata[7]}' +
                                         '<extra></extra>',
               selected=dict(marker=dict(opacity=0.4,size=18,color='#ffa700')),ids=[1,2,3,4,5,6,7,8,9,10]))

map_center = go.layout.mapbox.Center(lat=(data['LATITUDE'].max()+data['LATITUDE'].min())/2, 
                                     lon=(data['LONGITUDE'].max()+data['LONGITUDE'].min())/2)

for df_for in data.groupby(['SUPPLIER']):
    fig.add_trace(go.Scattermapbox(name='{}'.format(df_for[0]),
                                   mode = "markers",
                                 marker=dict(

                                             size=15,
                                             opacity=1,
                                             colorscale='YlGn'),
                                   hoverinfo='skip',
                                   lat=df_for[1]['LATITUDE'],
                                   lon=df_for[1]['LONGITUDE']))    

fig.add_trace(go.Scattermapbox(legendgroup='group',name='Альтернативные АЗС',
                                 lat=data_alt_azs['LATITUDE'], 
                                 lon=data_alt_azs['LONGITUDE'], 
                                 text=data_alt_azs['SNAME'],showlegend=True,
                                 mode='markers',
                                 marker=dict(color=data_alt_azs['РАССТОЯНИЕ'],
                                             size=13,
                                             opacity=1,
                                             colorscale='BrBG'),
                                customdata=np.stack([data_alt_azs['Address'], data_alt_azs['РАССТОЯНИЕ'],
                                                     data_alt_azs['Brand'], data_alt_azs['92'],
                                                    data_alt_azs['95'],data_alt_azs['ДТ']], axis=-1),
                                hovertemplate='Альтернативная АЗС: <b>%{text}</b>'+ '<br>' +
                                         'Данные1: %{customdata[0]}' + '<br>' +
                                         'Данные2: %{customdata[1]} км.' + '<br>' +
                                         'Данные3: %{customdata[2]}' + '<br>' +
                                         'Данные4: %{customdata[3]} руб.' + '<br>' +
                                         'Данные5: %{customdata[4]} руб.' + '<br>' +
                                         'Данные6: %{customdata[5]} руб.' + '<br>' +
                                         '<extra></extra>',
               selected=dict(marker=dict(opacity=0.4,size=18,color='#ffa700')),ids=[1,2,3,4,5,6,7,8,9,10]))
   
fig.update_layout(legend_orientation="h",
    mapbox_style="open-street-map", #мировая карта на анг. - carto-positron
                  mapbox=dict(center=map_center, zoom=5),
                 height=800,
                 hovermode='closest',
                 showlegend=True,
    title_text='Карта маршрутов клиента ' + data['CLIENT_NAME'].to_list()[0] +' за период ' +  
                  data['DT_DAY'].min().strftime('%d-%m-%Y') + ' - ' + data['DT_DAY'].max().strftime('%d-%m-%Y')) 
                  # margin={"r":0,"t":0,"l":0,"b":0},

offline.init_notebook_mode()

offline.plot(fig,
           auto_open=False, filename='C:/Users//Desktop/Python/maps_client')