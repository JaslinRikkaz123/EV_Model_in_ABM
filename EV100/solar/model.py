from mesa import Agent, Model
from .schdule import *
from .agent import *
from .controlagent import *
from mesa.datacollection import DataCollector  #Data collector
from mesa.space import SingleGrid
import solar.getDataFromExcel as data

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


dataset  ={'CAR-1A': float, 'Accleration-1A': float,'1A-available': float,'CAR-1B': float, 'Accleration-1B': float,'1B-available': float
,'CAR-1': float, 'Accleration-1': float,'1-available': float,'CAR-2': float, 'Accleration-2': float,'2-available': float,'CAR-3': float, 'Accleration-3': float,'3-available': float
,'CAR-4': float, 'Accleration-4': float,'4-available': float,'CAR-5': float, 'Accleration-5': float,'5-available': float,'CAR-6': float, 'Accleration-6': float,'6-available': float
,'CAR-7': float, 'Accleration-7': float,'7-available': float,'CAR-8': float, 'Accleration-8': float,'8-available': float,'CAR-9': float, 'Accleration-9': float,'9-available': float
,'CAR-10': float, 'Accleration-10': float,'10-available': float,'CAR-11': float, 'Accleration-11': float,'11-available': float,'CAR-12': float, 'Accleration-12': float,'12-available': float
,'CAR-13': float, 'Accleration-13': float,'13-available': float,'CAR-14': float, 'Accleration-14': float,'14-available': float,'CAR-15': float, 'Accleration-15': float,'15-available': float
,'CAR-16': float, 'Accleration-16': float,'16-available': float,'CAR-17': float, 'Accleration-17': float,'17-available': float,'CAR-18': float, 'Accleration-18': float,'18-available': float
,'CAR-19': float, 'Accleration-19': float,'19-available': float,'CAR-20': float, 'Accleration-20': float,'20-available': float,'CAR-21': float, 'Accleration-21': float,'21-available': float
,'CAR-22': float, 'Accleration-22': float,'22-available': float,'CAR-23': float, 'Accleration-23': float,'23-available': float,'CAR-24': float, 'Accleration-24': float,'24-available': float
,'CAR-25': float, 'Accleration-25': float,'25-available': float}
EV_Data = data.get_EV_agent_data(dataset)

        

model_params = {
    "height": 20,
    "width": 20   
}

    
class ConceptModel(Model):


    verbose = True  # Print-monitoring
    day = 1
    hour= 1
    grid_positions = ['uncontrolled', 'V2G','G2V']
   
    
    def __init__(self ,height = model_params['height'] , width = model_params['width'], grid_positions = "uncontrolled",day = 1,hour = 1 ):
        
       
        self.schedule = CustomBaseSheduler(self)
        self.grid = SingleGrid(model_params['width'], model_params['height'], torus=True)
        
        self.grid_positions = grid_positions
       
        
        self.steps = 0
        self.minute = 0
        self.hour = hour
        self.day = day
        self.week = 1
        self.month = 1
     
        for id,cord in {'WA1':(2,18) }.items():           
            weatherAgent = WeatherAgent(id,self)
            self.schedule.add(weatherAgent)
            self.grid.position_agent(weatherAgent, cord[0], cord[1]) 
            
        for sid,cord in {'Solar1':(5,18)}.items():               
            solarPanelAgent = SolarPanelAgent(sid,self)
            self.schedule.add(solarPanelAgent)
            self.grid.position_agent(solarPanelAgent, cord[0], cord[1]) 
            
        for xid,cord in {'1A':(0,14) , '1B': (0,13),  '1': (0,12), '2': (0,11),  '3': (0,10),  '4': (0,9), '5': (0,8), '6': (0,7), '7': (0,6), '8': (0,5), '9': (0,4), '10': (0,3)
        , '11': (0,2), '12': (19,3), '13': (19,4), '14': (19,5), '15': (19,6), '16': (19,7), '17': (19,8), '18': (19,9), '19': (19,10), '20': (19,11), '21': (19,12), '22': (19,13), '23': (19,14)
        , '24': (19,15), '25': (19,16)}.items():             
            
            car = EV_Agent(xid,self,speed = EV_Data[f'CAR-{xid}'],accelation =  EV_Data[f'Accleration-{xid}'],availability = EV_Data[f'{xid}-available'])
            self.schedule.add(car)
            self.grid.position_agent(car, cord[0], cord[1]) 
        
        for cid,cord in {'1':(1,14) ,'2':(1,13) ,'3':(1,12) ,'4':(1,11) ,'5':(1,10) ,'6':(1,9) ,'7':(1,8) ,'8':(1,7) ,'9':(1,6) ,'10':(1,5) ,'11':(1,4) ,'12':(1,3) ,
        '13':(1,2) ,'14': (18,3),'15': (18,4),'16': (18,5),'17': (18,6),'18': (18,7),'19': (18,8),'20': (18,9),'21': (18,10),'22': (18,11),'23': (18,12),'24': (18,13),'25': (18,14)
        ,'26': (18,15),'27': (18,16)}.items():          
            chargepole = Charge_pole(cid,self)
            self.schedule.add(chargepole)
            self.grid.position_agent(chargepole, cord[0], cord[1])
  
        for id,cord in {'C1':(10,11) }.items():           
            controlAgent = Charging_Control_Agent(id,self)
            self.schedule.add(controlAgent)
            self.grid.position_agent(controlAgent, cord[0], cord[1])
            
        for id,cord in {'BS1':(6,6) }.items():           
            battery_storage = Battery_Storage(id,self)
            self.schedule.add(battery_storage)
            self.grid.position_agent(battery_storage, cord[0], cord[1])
            
        for id,cord in { 'UG': (3,10)}.items():           
            utilityAgent = Utility_Grid(id,self)
            self.schedule.add(utilityAgent)
            self.grid.position_agent(utilityAgent, cord[0], cord[1])
            
        
      
        self.datacollector = DataCollector(
            {
                "Solar Power (kW)": lambda m: m.schedule.getCurrentPower(SolarPanelAgent), 
                "Temperature (K)": lambda m: m.schedule.getCurrentWeather(WeatherAgent),
                "Irradiance (W/m^2)": lambda m: m.schedule.getCurrentIrr(WeatherAgent),
                #f'{cid} : speed': lambda m: m.schedule.getactualspeed(EV_Agent)[cid],
                
                "Speed_1": lambda m: m.schedule.getactualspeed(EV_Agent)[0],
                "Speed_2": lambda m: m.schedule.getactualspeed(EV_Agent)[1],
                "Speed_3": lambda m: m.schedule.getactualspeed(EV_Agent)[2],
                "Speed_4": lambda m: m.schedule.getactualspeed(EV_Agent)[3],
                "Speed_5": lambda m: m.schedule.getactualspeed(EV_Agent)[4],
                "Speed_6": lambda m: m.schedule.getactualspeed(EV_Agent)[5],
                "Speed_7": lambda m: m.schedule.getactualspeed(EV_Agent)[6],
                "Speed_8": lambda m: m.schedule.getactualspeed(EV_Agent)[7],
                "Speed_9": lambda m: m.schedule.getactualspeed(EV_Agent)[8],
                "Speed_10": lambda m: m.schedule.getactualspeed(EV_Agent)[9],
                "Speed_11": lambda m: m.schedule.getactualspeed(EV_Agent)[10],
                "Speed_12": lambda m: m.schedule.getactualspeed(EV_Agent)[11],
                "Speed_13": lambda m: m.schedule.getactualspeed(EV_Agent)[12],
                "Speed_14": lambda m: m.schedule.getactualspeed(EV_Agent)[13],
                "Speed_15": lambda m: m.schedule.getactualspeed(EV_Agent)[14],
                "Speed_16": lambda m: m.schedule.getactualspeed(EV_Agent)[15],
                "Speed_17": lambda m: m.schedule.getactualspeed(EV_Agent)[16],
                "Speed_18": lambda m: m.schedule.getactualspeed(EV_Agent)[17],
                "Speed_19": lambda m: m.schedule.getactualspeed(EV_Agent)[18],
                "Speed_20": lambda m: m.schedule.getactualspeed(EV_Agent)[19],
                "Speed_21": lambda m: m.schedule.getactualspeed(EV_Agent)[20],
                "Speed_22": lambda m: m.schedule.getactualspeed(EV_Agent)[21],
                "Speed_23": lambda m: m.schedule.getactualspeed(EV_Agent)[22],
                "Speed_24": lambda m: m.schedule.getactualspeed(EV_Agent)[23],
                "Speed_25": lambda m: m.schedule.getactualspeed(EV_Agent)[24],
                "Speed_26": lambda m: m.schedule.getactualspeed(EV_Agent)[25],
                "Speed_27": lambda m: m.schedule.getactualspeed(EV_Agent)[26],
                    
                "SOC_1": lambda m: m.schedule.getSoC(Charging_Control_Agent)[0],
                "SOC_2": lambda m: m.schedule.getSoC(Charging_Control_Agent)[1],
                "SOC_3": lambda m: m.schedule.getSoC(Charging_Control_Agent)[2],
                "SOC_4": lambda m: m.schedule.getSoC(Charging_Control_Agent)[3],
                "SOC_5": lambda m: m.schedule.getSoC(Charging_Control_Agent)[4],
                "SOC_6": lambda m: m.schedule.getSoC(Charging_Control_Agent)[5],
                "SOC_7": lambda m: m.schedule.getSoC(Charging_Control_Agent)[6],
                "SOC_8": lambda m: m.schedule.getSoC(Charging_Control_Agent)[7],
                "SOC_9": lambda m: m.schedule.getSoC(Charging_Control_Agent)[8],
                "SOC_10": lambda m: m.schedule.getSoC(Charging_Control_Agent)[9],
                "SOC_11": lambda m: m.schedule.getSoC(Charging_Control_Agent)[10],
                "SOC_12": lambda m: m.schedule.getSoC(Charging_Control_Agent)[11],
                "SOC_13": lambda m: m.schedule.getSoC(Charging_Control_Agent)[12],
                "SOC_14": lambda m: m.schedule.getSoC(Charging_Control_Agent)[13],
                "SOC_15": lambda m: m.schedule.getSoC(Charging_Control_Agent)[14],
                "SOC_16": lambda m: m.schedule.getSoC(Charging_Control_Agent)[15],
                "SOC_17": lambda m: m.schedule.getSoC(Charging_Control_Agent)[16],
                "SOC_18": lambda m: m.schedule.getSoC(Charging_Control_Agent)[17],
                "SOC_19": lambda m: m.schedule.getSoC(Charging_Control_Agent)[18],
                "SOC_20": lambda m: m.schedule.getSoC(Charging_Control_Agent)[19],
                "SOC_21": lambda m: m.schedule.getSoC(Charging_Control_Agent)[20],
                "SOC_22": lambda m: m.schedule.getSoC(Charging_Control_Agent)[21],
                "SOC_23": lambda m: m.schedule.getSoC(Charging_Control_Agent)[22],
                "SOC_24": lambda m: m.schedule.getSoC(Charging_Control_Agent)[23],
                "SOC_25": lambda m: m.schedule.getSoC(Charging_Control_Agent)[24],
                "SOC_26": lambda m: m.schedule.getSoC(Charging_Control_Agent)[25],
                "SOC_27": lambda m: m.schedule.getSoC(Charging_Control_Agent)[26],
                    
                    
                "Car_P_1": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[0],
                "Car_P_2": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[1],
                "Car_P_3": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[2],
                "Car_P_4": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[3],
                "Car_P_5": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[4],
                "Car_P_6": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[5],
                "Car_P_7": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[6],
                "Car_P_8": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[7],
                "Car_P_9": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[8],
                "Car_P_10": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[9],
                "Car_P_11": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[10],
                "Car_P_12": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[11],
                "Car_P_13": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[12],
                "Car_P_14": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[13],
                "Car_P_15": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[14],
                "Car_P_16": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[15],
                "Car_P_17": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[16],
                "Car_P_18": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[17],
                "Car_P_19": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[18],
                "Car_P_20": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[19],
                "Car_P_21": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[20],
                "Car_P_22": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[21],
                "Car_P_23": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[22],
                "Car_P_24": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[23],
                "Car_P_25": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[24],
                "Car_P_26": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[25],
                "Car_P_27": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[26],
                    
                "Grid_Power (kW)": lambda m: m.schedule.getactualchargepower(Charging_Control_Agent)[0],
                "Battery_Storage_Power (kW)": lambda m: m.schedule.getactualchargepower(Charging_Control_Agent)[1],
                    
                "Battery_SOC": lambda m: m.schedule.getbattsoc(Charging_Control_Agent)
            }
        )
       


    
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
               
        # print(  "Week : {} Day : {} Hour : {} minute: {}\n".format(self.week, self.day, self.hour,self.minute))    
               
        #if self.verbose:
            #print(self.datacollector )
            # #print (self.schedule.getCurrentPower(SolarPanelAgent))
            # #print (self.schedule.getCurrentWeather(WeatherAgent))
            # #print (self.schedule.getCurrentIrr(WeatherAgent))
            #print(self.schedule.getactualspeed(EV_Agent)[xid])
            # # print (self.schedule.getactualspeed(EV_Agent)[0])
            # # print (self.schedule.getactualspeed(EV_Agent)[1])
            
            
            # # print(self.schedule.getSoC(Charging_Control_Agent))
            # # print(self.schedule.getSoC(Charging_Control_Agent))
            
            # # print(self.schedule.getcarbattery(Charging_Control_Agent))
            # # print(self.schedule.getcarbattery(Charging_Control_Agent))
            
            # print (self.schedule.getactualchargepower(Charging_Control_Agent))
            # print (self.schedule.getactualchargepower(Charging_Control_Agent))
            
            # #print (self.schedule.getbattsoc(Charging_Control_Agent))
            # #print(self.schedule.getavailability(EV_Agent)[0][0])
            
    
    def run_model(self,step_count = 4):
        for k in range(step_count):
            for i in range(7):
  #          print("Step {}".format(i))
             
             for j in range(24):
                    self.step()