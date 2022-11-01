from mesa.model import Model
from schdule import CustomBaseSheduler
from agents import *

from mesa.datacollection import DataCollector  #Data collector
from mesa.space import MultiGrid, SingleGrid

#Create the grid with model_params
model_params = {
    "height": 20,
    "width": 20   
}


class ConceptModel(Model):
    Flat_Charging_structure = ['uncontrolled', 'V2G','G2V','G2V-SC']
    TOU_Charging_structure = ['Slow','Average','Fast']
    price_structure = ['TOU', 'FLAT']
    
    def __init__(self ,height = model_params['height'] , width = model_params['width'], Flat_Charging_structure = "uncontrolled" ,price_structure = "TOU" , TOU_Charging_structure = "Slow"):
        
        self.steps = 0
        self.minute = 0
        self.hour = 0
        self.day = 0
        self.week = 0
        self.month = 0

        self.reporter_params = {}

        self.schedule = CustomBaseSheduler(self)

        self.grid = MultiGrid(width, height, torus=True)
        self.Flat_Charging_structure = Flat_Charging_structure
        self.price_structure = price_structure
        self.TOU_Charging_structure = TOU_Charging_structure
        
        for id,cord in {'1':(10,10)}.items():    #Main control agent       
            maincontrolAgent = Main_Control_Agent(f'MCA{id}',self)
            ExbatteryAgent = Battery_Storage(f'EBS{id}',self)
            self.schedule.add(maincontrolAgent)
            self.schedule.add(ExbatteryAgent)
            self.grid.place_agent(maincontrolAgent, (cord[0], cord[1]))   
            self.grid.place_agent(ExbatteryAgent, (cord[0], cord[1])) 

        for id,cord in {'0':(0,14) , '1': (0,13),  '2': (0,12), '3': (0,11),  '4': (0,10),  '5': (0,9), '6': (0,8), '7': (0,7), '8': (0,6), '9': (0,5), '10': (0,4), '11': (0,3)
        , '12': (0,2)}.items():             # EV agent  and Charging_Control_Agent  are in one cell-Multi grid 
            evAgent = EV_Agent(id,self)
            controlAgent = Charging_Control_Agent(id,self)
            self.schedule.add(evAgent)
            self.schedule.add(controlAgent)
            self.grid.place_agent(evAgent, (cord[0], cord[1]))   
            self.grid.place_agent(controlAgent, (cord[0], cord[1]))        
            
        for id,cord in {'1':(1,14) ,'2':(1,13) ,'3':(1,12) ,'4':(1,11) ,'5':(1,10) ,'6':(1,9) ,'7':(1,8) ,'8':(1,7) ,'9':(1,6) ,'10':(1,5) ,'11':(1,4),'12':(1,3) ,'13':(1,2) }.items():             # chargepole_agent    
            chargepole_agent = Charge_pole(id,self)
            self.schedule.add(chargepole_agent)
            self.grid.place_agent(chargepole_agent, (cord[0], cord[1]))        # Charge Pole agent
      
        for id,cord in {'1':(1,18)}.items():            #Solar and weather agent in one grid   
            solarPanelAgent = SolarPanelAgent(f'Solar{id}',self)
            weatherAgent = WeatherAgent(f'ws{id}',self)
            self.schedule.add(solarPanelAgent)
            self.schedule.add(weatherAgent)
            self.grid.place_agent(solarPanelAgent, (cord[0], cord[1]))   
            self.grid.place_agent(weatherAgent, (cord[0], cord[1])) 

        for id,cord in {'UG':(5,14)}.items():             
            utility_agent = Utility_Grid(id,self)
            self.schedule.add(utility_agent)
            self.grid.place_agent(utility_agent, (cord[0], cord[1]))        # Utility agent
    
        self.datacollector = DataCollector(self.reporter_params)
  
        self.running = True
        
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.steps += 1

        self.minute += 5
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 6:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
               
        print(  "Week : {} Day : {} Hour : {} minute: {}\n".format(self.week, self.day, self.hour,self.minute))     
        
        '''This is getting RESET AlWAYS - see the console - values might be different, because the agents load values from shedule.steps'''   
  
