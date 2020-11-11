# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 23:42:16 2020

@author: tadeo
"""
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt

#DATA CLEANING
covid = pd.DataFrame()
url = 'https://docs.google.com/spreadsheets/d/16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA/export?format=csv&id=16-bnsDdmmgtSxdWbVMboIHo5FRuz76DBxsz_BbsEVWA&gid=0'    
covid = pd.read_csv(url).drop(['dia_cuarentena_dnu260', 'osm_admin_level_8', 
                                                  'informe_tipo',
                                                  'informe_link',
                                                  'covid19argentina_admin_level_4'], axis=1)

covid.columns = ['Fecha', 'diaInicio', 'Pais', 'Provincia', 'TotalCasos', 'VariacionTotalCasos',
                 'TotalFallecidos', 'TotalCasosFallecidos', 'TotalRec', 'TotalTerapia',
                 'TestPcrNegativo', 'TotalPCRNeg', 'Transmision', 'Observacion']

#VERIFICAMOS TIPO Y CANTIDAD DATOS
for c in covid.columns:
    print(c, covid[c].dtype)
    
covid['Fecha'] = pd.to_datetime(covid['Fecha'], errors ='coerce')
covid[['Pais', 'Provincia', 'TotalRec', 'Transmision', 'Observacion']] = covid[['Pais', 
                                                                                'Provincia', 
                                                                                'TotalRec', 
                                                                                'Transmision', 
                                                                               'Observacion']].astype(str)

nulos = covid.isnull().sum()
provincias = covid['Provincia'].unique()
transmision = covid['Transmision'].unique()
observacion = covid['Observacion'].unique()
print(f"Provincias: {provincias}, Transmisiones: {transmision}, Observaciones: {observacion}")

#DEBEMOS ARMAR UN NUEVO DATASET CON FECHAS UNICAS; YA QUE SE REPITEN.
covid2 = pd.DataFrame()
covid2['TotalCasos'] = covid.TotalCasos[covid.Provincia == 'CABA'].groupby(covid.Fecha).sum()

sns.lineplot(data=covid, x='Fecha',  y='TotalCasos')