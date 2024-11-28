import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
st.title("Hola!")
df = pd.read_csv('Latitud - Longitudes.csv')

lat= {}
lon = {}

for index, row in df.iterrows():
  lat[row['Comuna']] = row['Latitud (Decimal)']
  lon[row['Comuna']] = row['Longitud (decimal)']
#Creamos el menu interactivo
def menu():
  comunas = list(df["Comuna"])
  st.subheader("bienvenido al menu de datos meteorológicos de Chile")
  st.subheader("En este menú, están todas las ciudades de Chile")
  st.subheader("Seleccione una comuna que quiere investigar")
  c1, c2 = st.columns([0.4,0.8])
  with c1:
    Respuesta = st.selectbox("Digame que comuna quiere saber:", options=comunas)
  try:
    return Respuesta,c1,c2
  except Exception as e:
    st.write("Escriba la comuna de su interes")
@st.cache_data
def datos(ciudad):
  url = f"https://api.open-meteo.com/v1/forecast?latitude={lat[ciudad]}&longitude={lon[ciudad]}&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m"
  response = requests.get(url)
  datos_df = response.json()
  print(url)
  return datos_df,ciudad
def Analisis(datos,ciudad,C1,C2):

  if 'hourly' in datos:
    temperatura = datos['hourly']['temperature_2m'][0]
    humedad = datos['hourly']['relative_humidity_2m'][0]
    probabilidad_precipitacion = datos['hourly']['precipitation_probability'][0]
    velocidad_viento = datos['hourly']['wind_speed_10m'][0]
    tiempo = datos['hourly']
    temperatura_completa = datos['hourly']['temperature_2m']
    humedad_completa = datos['hourly']['relative_humidity_2m']
    probabilidad_precipitacion_completa = datos['hourly']['precipitation_probability']
    velocidad_viento_completa = datos['hourly']['wind_speed_10m']
    with c1:
      
      st.write(f"Datos meteorológicos para {ciudad}:")
      st.write(f"Temperatura: {temperatura} °C")
      st.write(f"Humedad: {humedad} %")
      st.write(f"Probabilidad de precipitación: {probabilidad_precipitacion} %")
      st.write(f"Velocidad del viento: {velocidad_viento} km/h")
    tiempo_final = [x.split('T')[0] for x in tiempo["time"]]
    Año =[fecha.split('-')[0] for fecha in tiempo_final]
    Dias = [fecha.split('-')[1] + '-' + fecha.split('-')[2] for fecha in tiempo_final]
    Año = list(dict.fromkeys(Año))
    Dias = list(dict.fromkeys(Dias))
    tiempo_final = list(dict.fromkeys(tiempo_final))
    dias_final = []
    dias_contador = 0
    hora=0
    
    with c2:
      dias_mostrar = st.number_input("Cuantos dias desea ver?", min_value=1, max_value=7)
      if dias_mostrar>4:
        intervalo = ["6", "12", "24"]
      elif dias_mostrar>1:
        intervalo = ["3", "6", "12", "24"]
      else:
        intervalo=["1", "3", "6", "12", "24"]
      intervalos = st.selectbox("De cuanto quiere que sea el intervalo?", options=intervalo)
      y = st.selectbox("Eliga la variable a comparar", options= ["Temperatura", "Humedad", "Probabilidades de Precipitaciones", "Velocidad del viento (Km/H)"])
    if int(dias_mostrar)==7:
      comprobar =0
    else:
      comprobar = 1
    for i in range(0,int((dias_mostrar*24)/int(intervalos))+comprobar):
      if i>=1:
        if float(i)%int(24/int(intervalos))==0:
          if dias_contador!=6:
            dias_contador+=1
          hora = 0
      dias_final.append(Dias[dias_contador]+f" {hora*int(intervalos)}:00")
      hora+=1
    if y == "Temperatura":
      promedios = []
      for i in range(0,24*dias_mostrar+comprobar,int(intervalos)):
        promedio = sum(temperatura_completa[i:i+int(intervalos)])/int(intervalos) 
        promedios.append(promedio)
      fig, ax = plt.subplots()
      plt.plot(dias_final, promedios,marker='o')
      plt.xlabel(f'Tiempo {Año[0]}')
      plt.ylabel('Temperatura (°C)')
      plt.title('Temperatura a lo largo del tiempo')
      
      with c1:
        maximo = max(promedios)
        minimo = min(promedios)
        max_day_index = promedios.index(maximo)
        min_day_index = promedios.index(minimo)
        max_day = dias_final[max_day_index]
        min_day = dias_final[min_day_index]
        st.write("<h3 style='color:#FF0000';>ANALISIS:</h3>",unsafe_allow_html=True)
        st.write(f"Día con la temperatura más alta: {max_day}, Temperatura: {np.round(maximo)} °C")
        st.write(f"Día con la temperatura más baja: {min_day}, Temperatura: {np.round(minimo)} °C")
    elif y == "Humedad":
      promedios = []
      for i in range(0,24*dias_mostrar+comprobar,int(intervalos)):
        promedio = sum(humedad_completa[i:i+24])/24
        promedios.append(promedio)
      fig, ax = plt.subplots()
      plt.plot(dias_final, promedios,marker='o')
      plt.xlabel(f'Tiempo {Año[0]}')
      plt.ylabel('Humedad %')
      plt.title('Humedad a lo largo del tiempo')
      plt.xticks(rotation=90)
      with c1:
        maximo = max(promedios)
        minimo = min(promedios)
        max_day_index = promedios.index(maximo)
        min_day_index = promedios.index(minimo)
        max_day = dias_final[max_day_index]
        min_day = dias_final[min_day_index]
        st.write("<h3 style='color:#FF0000';>ANALISIS:</h3>",unsafe_allow_html=True)
        st.write(f"Día con la humedad más alta: {max_day}, humedad: {np.round(maximo)} %")
        st.write(f"Día con la humedad más baja: {min_day}, humedad: {np.round(minimo)} %")
    elif y == "Probabilidades de Precipitaciones":
      promedios = []
      for i in range(0,24*dias_mostrar+comprobar,int(intervalos)):
        promedio = sum(probabilidad_precipitacion_completa[i:i+24])/24
        promedios.append(promedio)
      fig, ax = plt.subplots()
      plt.plot(dias_final, promedios,marker='o')
      plt.xlabel(f'Tiempo {Año[0]}')
      plt.ylabel('Probabilidades de Precipitaciones %')
      plt.title('Probabilidades de Precipitaciones a lo largo del tiempo')
      with c1:
        maximo = max(promedios)
        minimo = min(promedios)
        max_day_index = promedios.index(maximo)
        min_day_index = promedios.index(minimo)
        max_day = dias_final[max_day_index]
        min_day = dias_final[min_day_index]
        st.write("<h3 style='color:#FF0000';>ANALISIS:</h3>",unsafe_allow_html=True)
        st.write(f"Día con la probabilidad de precipitacion más alta: {max_day}, probabilidad de precipitacion: {np.round(maximo)} %")
        st.write(f"Día con la probabilidad de precipitacion más baja: {min_day}, probabilidad de precipitacion: {np.round(minimo)} %")
    else:
      promedios = []
      for i in range(0,24*dias_mostrar+comprobar,int(intervalos)):
        promedio = sum(velocidad_viento_completa[i:i+24])/24
        promedios.append(promedio)
      fig, ax = plt.subplots()
      plt.plot(dias_final, promedios,marker='o')
      plt.xlabel(f'Tiempo {Año[0]}')
      plt.ylabel('Velocidad del viento Km/h')
      plt.title('Velocidad del viento Km/h a lo largo del tiempo')
      with c1:
        maximo = max(promedios)
        minimo = min(promedios)
        max_day_index = promedios.index(maximo)
        min_day_index = promedios.index(minimo)
        max_day = dias_final[max_day_index]
        min_day = dias_final[min_day_index]
        st.write("<h3 style='color:#FF0000';>ANALISIS:</h3>",unsafe_allow_html=True)
        st.write(f"Día con la velocidad más alta: {max_day}, Velocidad: {np.round(maximo)} Km/h")
        st.write(f"Día con la velocidad más baja: {min_day}, Velocidad: {np.round(minimo)} Km/h")
    with c2:
      plt.xticks(rotation=90)
      st.pyplot(fig)
ciudad,c1,c2 = menu()
datos_df,ciudad = datos(ciudad)
Analisis(datos_df,ciudad,c1,c2)