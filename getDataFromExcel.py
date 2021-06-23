import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
from mesa import Agent, Model

#Get Temperature and irradiance data for weather agent
def getData():
    df = pd.read_excel('solardata.xlsx', sheet_name='Sheet1',engine='openpyxl')
    ds = df
    ds['Temp '] = ds['Temp '].astype(str)
    ds[' Radiation'] = ds[' Radiation'].astype(str)
    
    
    TemperatureList = ds['Temp ']
    df = pd.DataFrame({'Temp ': TemperatureList})
    df=df.astype(float)
    
    IrradianceList = ds[' Radiation']
    dm = pd.DataFrame({' Radiation': IrradianceList})
    dm=dm.astype(float)
    
    for index, row in df.iterrows():

        dm.iat[index, 0] = round(dm.iat[index, 0], 2)
        df.iat[index, 0] = round(df.iat[index, 0] + 273.15, 2)
        
    IrradianceList = dm[' Radiation'].tolist()
    TemperatureList = df['Temp '].tolist()
    
    my_list=[TemperatureList,  IrradianceList ]
    
    return my_list
    
def getData_1():
    df = pd.read_csv('EVsample.csv',usecols = ['CAR-1A'])
    Ref_speed =  df['CAR-1A'].values.tolist()
    
    df = pd.read_csv('EVsample.csv',usecols = ['CAR-1B'])
    Act_speed =  df['CAR-1B'].values.tolist()
    
    df = pd.read_csv('EVsample.csv',usecols = ['Acccleration'])
    Acceleration =  df['Acccleration'].values.tolist()
    
    aggregate_list = [Ref_speed, Act_speed,Acceleration]
    
    return aggregate_list
