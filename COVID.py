# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 10:32:38 2020

@author: adria
"""
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import sys

url = 'https://docs.google.com/spreadsheets/d/16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA/export?format=csv&id=16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA&gid=0'
df = pd.read_csv(url)

covid = pd.read_csv('Covid19Casos.csv')
covid = covid.drop(['residencia_pais_nombre', 'fecha_internacion', 'carga_provincia_nombre', 'fecha_apertura', 'sepi_apertura', 'fecha_cui_intensivo', 'carga_provincia_id', 'origen_financiamiento', 'ultima_actualizacion', 'residencia_departamento_id', 'residencia_provincia_id', 'fecha_fallecimiento', 'asistencia_respiratoria_mecanica'], axis=1)
covid.columns = ["ID", "sexo", "edad", "años/meses", "provincia", "departamento", "fechasintomas", "intensiva", "fallecido", "clasificacion", "resumenclasificacion", "fecha"]
covid.set_index('ID', inplace=True)
covid = covid.sort_values('ID', ascending=True)

#Cambiamos valor indice que empiece por caso 1. Tratamos datos faltantes
covid['fecha'] = pd.to_datetime(covid['fecha'], errors ='coerce')
covid = covid.sort_values(by='fecha', ascending=True)
#covid = covid.fillna('Dato faltante')
covid.index = [x for x in range(1, len(covid.values)+1)]
covid.set_index('fecha')

#Conteo positivos y negativos
nulos = covid.isnull().sum()
print(nulos)
confirmados = covid.resumenclasificacion[covid.resumenclasificacion == 'Confirmado'].count()
descartados = covid.resumenclasificacion[covid.resumenclasificacion == 'Descartado'].count()
lista = covid['sexo'].unique()
lista2 = covid['provincia'].unique()
print(f"Confirmados: {confirmados}, Descartados: {descartados}, TipoSexo: {lista}, Clasificaciones: {lista2}")

#Armando nuevo dataframe por fecha
covid2 = pd.DataFrame()
covid2['Hisopados'] = covid.resumenclasificacion.groupby(covid.fecha).count()
covid2['Positivos'] = covid.resumenclasificacion[covid.resumenclasificacion == 'Confirmado'].groupby(covid.fecha).count()
covid2['Negativos'] = covid.resumenclasificacion[covid.resumenclasificacion == 'Descartado'].groupby(covid.fecha).count()
covid2['Masculino'] = covid.sexo[covid.sexo == 'M'].groupby(covid.fecha).count()
covid2['Femenino'] = covid.sexo[covid.sexo == 'F'].groupby(covid.fecha).count()
covid2['Indeterminado'] = covid.sexo[covid.sexo == 'NR'].groupby(covid.fecha).count()
covid2['Fallecidos'] = covid.fallecido[covid.fallecido == 'SI'].groupby(covid.fecha).count()
covid2['Buenos Aires'] = covid.provincia[covid.provincia == 'Buenos Aires'].groupby(covid.fecha).count()
covid2['CABA'] = covid.provincia[covid.provincia == 'CABA'].groupby(covid.fecha).count()
covid2['Neuquen'] = covid.provincia[covid.provincia == 'Neuquén'].groupby(covid.fecha).count()
covid2['Rio Negro'] = covid.provincia[covid.provincia == 'Río Negro'].groupby(covid.fecha).count()
covid2['Jujuy'] = covid.provincia[covid.provincia == 'Jujuy'].groupby(covid.fecha).count()
covid2['Mendoza'] = covid.provincia[covid.provincia == 'Mendoza'].groupby(covid.fecha).count()
covid2['Santiago del Estero'] = covid.provincia[covid.provincia == 'Santiago del Estero'].groupby(covid.fecha).count()
covid2['Tierra del Fuego'] = covid.provincia[covid.provincia == 'Tierra del Fuego'].groupby(covid.fecha).count()
covid2['Cordoba'] = covid.provincia[covid.provincia == 'Córdoba'].groupby(covid.fecha).count()
covid2['Formosa'] = covid.provincia[covid.provincia == 'Formosa'].groupby(covid.fecha).count()
covid2['Corrientes'] = covid.provincia[covid.provincia == 'Corrientes'].groupby(covid.fecha).count()
covid2['Entre Rios'] = covid.provincia[covid.provincia == 'Entre Ríos'].groupby(covid.fecha).count()
covid2['La Rioja'] = covid.provincia[covid.provincia == 'La Rioja'].groupby(covid.fecha).count()
covid2['San Luis'] = covid.provincia[covid.provincia == 'San Luis'].groupby(covid.fecha).count()
covid2['Chaco'] = covid.provincia[covid.provincia == 'Chaco'].groupby(covid.fecha).count()
covid2['Tucuman'] = covid.provincia[covid.provincia == 'Tucumán'].groupby(covid.fecha).count()
covid2['Santa Fe'] = covid.provincia[covid.provincia == 'Santa Fe'].groupby(covid.fecha).count()
covid2['San Juan'] = covid.provincia[covid.provincia == 'San Juan'].groupby(covid.fecha).count()
covid2['Chubut'] = covid.provincia[covid.provincia == 'Chubut'].groupby(covid.fecha).count()
covid2['Salta'] = covid.provincia[covid.provincia == 'Salta'].groupby(covid.fecha).count()
covid2['Catamarca'] = covid.provincia[covid.provincia == 'Catamarca'].groupby(covid.fecha).count()
covid2['La Pampa'] = covid.provincia[covid.provincia == 'La Pampa'].groupby(covid.fecha).count()
covid2['Santa Cruz'] = covid.provincia[covid.provincia == 'Santa Cruz'].groupby(covid.fecha).count()
covid2['Misiones'] = covid.provincia[covid.provincia == 'Misiones'].groupby(covid.fecha).count()
covid2['Sin especificar'] = covid.provincia[covid.provincia == 'SIN ESPECIFICAR'].groupby(covid.fecha).count()
covid2.index.name = "Fecha"
covid2 = covid2.reset_index()
covid2.sort_values(by='Fecha', ascending=True)
covid2 = covid2.drop([0,1], axis=0)

#Empezamos a aplicar funciones estadisticas
covid2['Variacion hisopados'] = round(covid2['Hisopados'].pct_change() * 100, 2)
covid2['Variacion positivos'] = round(covid2['Positivos'].pct_change() * 100, 2)
covid2['Variacion fallecidos'] = round(covid2['Fallecidos'].pct_change() * 100, 2)



for c in covid2.columns:
    print(c, covid2[c].dtype)


#TRABAJAMOS CON LA API OPENMAPI DE REGISTROS DE COVID EN ARGENTINA
sys.path.insert(1, './Open-mAPI-master')
from openmapi.registros import Registros

data = Registros()

#DESCARGAMOS DATOS DESDE LA API//GRAFICOS DE LINEAS
#bsas = data.getHistorialCasosProvincia("NE")
#buenosaires = pd.DataFrame(bsas, columns=['Fecha','Infectados'])
#buenosaires['Infectados'] = buenosaires['Infectados'].str.replace('-', '0').astype(float)

#DESCARGAMOS DATOS DESDE LA API//INFECTADOS
info = 'infectados'
api = [[str(prov), prov.getCasos(info)] for prov in data.provincias.values()]
infectados = pd.DataFrame(api, columns=['Provincias','Infectados'])
infectados['Provincias'] = infectados['Provincias'].str.replace('-', ' ').astype(str)
infectados['Infectados'] = infectados['Infectados'].str.replace(',', '').astype(float)
infectados = infectados.set_index('Provincias')
#DESCARGAMOS DATOS DESDE LA API//RECUPERADOS
info2 = 'recuperados'
api1 = [[str(prov), prov.getCasos(info2)] for prov in data.provincias.values()]
recuperados = pd.DataFrame(api1, columns=['Provincias','Recuperados'])
recuperados['Provincias'] = recuperados['Provincias'].str.replace('-', ' ').astype(str)
recuperados['Recuperados'] = recuperados['Recuperados'].str.replace(',', '').astype(float)
recuperados = recuperados.set_index('Provincias')
#DESCARGAMOS DATOS DESDE LA API//FALLECIDOS
info3 = 'fallecidos'
api2 = [[str(prov), prov.getCasos(info3)] for prov in data.provincias.values()]
fallecidos = pd.DataFrame(api2, columns=['Provincias','Fallecidos'])
fallecidos['Provincias'] = fallecidos['Provincias'].str.replace('-', ' ').astype(str)
fallecidos['Fallecidos'] = fallecidos['Fallecidos'].str.replace(',', '').astype(float)
fallecidos = fallecidos.set_index('Provincias')


pieplots = [infectados['Infectados'], recuperados['Recuperados'], fallecidos['Fallecidos']]
pieplots2 = pd.DataFrame(pieplots).reset_index()

import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

#df = px.data.tips()
#fig = px.pie(df, values='tip', names='day')
#fig.show()

plt.figure(figsize=(16, 10))
ax1 = plt.subplot(111)
ax1.plot(covid2['Fecha'], covid2['Hisopados'], label='Hisopados', color='crimson')
ax1.plot(covid2['Fecha'], covid2['Positivos'], label='Positivos')
ax1.plot(covid2['Fecha'], covid2['Fallecidos'], label='Fallecidos')
ax1.legend(loc='upper left', shadow=True)

ax1.grid(linewidth=0.1, color='#8f8f8f')
ax1.set_facecolor("black") 
plt.title("COVID EN ARGENTINA\n", size=30, color='#28a9ff') 
plt.show()

#BARPLOT GRAL
f, ax = plt.subplots(figsize=(15, 15))
ax = sns.barplot(data=covid2, x='Fecha', y='Positivos')
sns.set(font_scale=2.5)


#PLOTS
#principales = covid2[['Fecha', 'Buenos Aires', 'CABA', 'Mendoza', 'Cordoba', 'Sin especificar', 'Santa Fe']]
#principales.set_index('Fecha', inplace=True)
#f, ax = plt.subplots(figsize=(15, 15))
#lineas = sns.lineplot(data=principales, marker=".", dashes=False)

#secundarias = covid2[['Fecha', 'Jujuy', 'Santiago del Estero', 'Formosa', 'Corrientes', 'Sin especificar',
# 'Entre Rios', 'La Rioja', 'Rio Negro', 'San Luis', 'Chaco', 'Tucuman', 'San Juan', 'Chubut', 'Salta', 'Catamarca', 'Neuquen', 'La Pampa',
# 'Santa Cruz', 'Misiones']]
#secundarias.set_index('Fecha', inplace=True)
#f, ax = plt.subplots(figsize=(15, 15))
#lineas2 = sns.lineplot(data=secundarias, marker=".", dashes=False)

