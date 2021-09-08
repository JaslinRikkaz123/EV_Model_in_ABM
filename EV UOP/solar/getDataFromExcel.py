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
    df = pd.read_excel('EVsample.xlsx', sheet_name='EVsample',engine='openpyxl')
    ds = df
    ds['CAR-1A'] = ds['CAR-1A'].astype(str)
    ds['Acccleration-1A'] = ds['Acccleration-1A'].astype(str)
    ds['1A-available'] = ds['1A-available'].astype(str)
    
    Act_speed = ds['CAR-1A']
    df = pd.DataFrame({'CAR-1A': Act_speed})
    df=df.astype(float)
    
    Acceleration = ds['Acccleration-1A']
    dm = pd.DataFrame({'Acccleration-1A': Acceleration})
    dm=dm.astype(float)
    
    Availability = ds['1A-available']
    dr = pd.DataFrame({'1A-available': Availability})
    dr=dr.astype(float)
    for index, row in df.iterrows():

        dm.iat[index, 0] = round(dm.iat[index, 0], 2)
        df.iat[index, 0] = round(df.iat[index, 0], 2)
        dr.iat[index, 0] = round(dr.iat[index, 0], 2)
        
    Acceleration = dm['Acccleration-1A'].tolist()
    Act_speed = df['CAR-1A'].tolist()
    Availability = dr['1A-available'].tolist()
   
    
    aggregate_list = [Act_speed, Acceleration,Availability]
    
    return aggregate_list
def getData_2():
    df = pd.read_excel('EVsample.xlsx', sheet_name='EVsample',engine='openpyxl')
    ds = df
    ds['CAR-1B'] = ds['CAR-1B'].astype(str)
    ds['Accleration-1B'] = ds['Accleration-1B'].astype(str)
    ds['1B-available'] = ds['1B-available'].astype(str)
    
    
    Act_speed = ds['CAR-1B']
    df = pd.DataFrame({'CAR-1B': Act_speed})
    df=df.astype(float)
    
    Acceleration = ds['Accleration-1B']
    dm = pd.DataFrame({'Accleration-1B': Acceleration})
    dm=dm.astype(float)
    
    Availability = ds['1B-available']
    dr = pd.DataFrame({'1B-available': Availability})
    dr=dr.astype(float)
    
    for index, row in df.iterrows():

        dm.iat[index, 0] = round(dm.iat[index, 0], 2)
        df.iat[index, 0] = round(df.iat[index, 0], 2)
        dr.iat[index, 0] = round(dr.iat[index, 0], 2)
        
    Acceleration = dm['Accleration-1B'].tolist()
    Act_speed = df['CAR-1B'].tolist()
    Availability = dr['1B-available'].tolist()
  
    aggregate_list = [Act_speed, Acceleration,Availability]
    return aggregate_list
    
    
def getData_3():

    
    df = pd.read_csv('EVsample.csv',usecols = ['CAR-1B'])
    Act_speed =  df['CAR-1B'].values.tolist()
    
    df = pd.read_csv('EVsample.csv',usecols = ['Acccleration-1B'])
    Acceleration =  df['Acccleration-1B'].values.tolist()
    
    aggregate_list = [Act_speed,Acceleration]
    
    return aggregate_list