from mesa import Agent, Model
from .schdule import *
from .agent import *
from .controlagent import *
from mesa.datacollection import DataCollector  #Data collector
from mesa.space import SingleGrid


import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

model_params = {
    "height": 20,
    "width": 20   
}


class ConceptModel(Model):
   
    verbose = True  # Print-monitoring

    
    def __init__(self, height = model_params['height'] , width = model_params['width'], grid_positions = "uncontrolled"  ):
        
        
        self.schedule = CustomBaseSheduler(self)
        self.grid = SingleGrid(width, height, torus=True)

        weatherAgent = WeatherAgent('weather',self)
        self.schedule.add(weatherAgent)
        '''
        irradianceagent = WeatherAgent('irradiance',self)
        self.schedule.add(irradianceagent)
        '''
        solarPanelAgent = SolarPanelAgent('Solar',self)
        self.schedule.add(solarPanelAgent)
        
        EvAgent = EV_Agent('Speed',self)
        self.schedule.add(EvAgent)
        
        ChargeAgent = Charge_pole('charge',self)
        self.schedule.add(ChargeAgent)
        
        ControlAgent = Charging_Control_Agent('control_value',self)
        self.schedule.add(ControlAgent)

        
        if grid_positions == "uncontrolled":
            self.B = 0
        elif  grid_positions == "V2G":
            self.B = 1
        elif grid_positions == "G2V":
            self.B = 2
            
        
       
        self.datacollector = DataCollector(
            {
                "Solar Power (W)": lambda m: m.schedule.getCurrentPower(SolarPanelAgent), 
                "Temperature (K)": lambda m: m.schedule.getCurrentWeather(WeatherAgent),
                "Irradiance (W/m^2)": lambda m: m.schedule.getCurrentIrr(WeatherAgent),
                
                "Actual_Speed (km/h)": lambda m: m.schedule.getactualspeed(EV_Agent)[0][0],
                "Actual_Speed_2 (km/h)": lambda m: m.schedule.getactualspeed(EV_Agent)[0][1],
                
                "Availability_1": lambda m: m.schedule.getavailability(EV_Agent)[0][0],
                "Availability_2": lambda m: m.schedule.getavailability(EV_Agent)[0][1],
                
                "SOC_CAR_1": lambda m: m.schedule.getSoC(Charging_Control_Agent)[0][self.B][0],
                "SOC_CAR_2": lambda m: m.schedule.getSoC(Charging_Control_Agent)[0][self.B][1],
                
                "Car Battery Power(W)": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[0][self.B][0],
                "Car Battery Power_2(W)": lambda m: m.schedule.getcarbattery(Charging_Control_Agent)[0][self.B][1],
                
                "Grid_Power (W)": lambda m: m.schedule.getactualgridpower(Charging_Control_Agent)[0][0][self.B],
                "CP_Battery_Power (W)": lambda m: m.schedule.getactualchargepower(Charging_Control_Agent)[0][1][self.B],
                
                "Battery_SOC": lambda m: m.schedule.getbattsoc(Charging_Control_Agent)[0][self.B]
            }
        )
       

        
        
        
    #create weather agent
        x = 2
        y = 18
        self.grid.position_agent(weatherAgent,x, y)
        
    #create solar agent
        x = 1
        y = 18
        self.grid.position_agent(solarPanelAgent,x,y)
    


    #create chargepole
        x = 6
        y = 10
        self.grid.position_agent(ChargeAgent,x,y)
    #create chargepole
        x = 6
        y = 9
        self.grid.position_agent(ChargeAgent,x,y)   
    #create controlAgent
        x = 6
        y = 11
        self.grid.position_agent(ControlAgent,x,y)
    
        self.running = True
    
        
        
    def step(self):
        self.schedule.step()
        
        
         # collect data
        self.datacollector.collect(self)
               
        if self.verbose:
            #print (self.schedule.getCurrentPower(SolarPanelAgent))
            #print (self.schedule.getCurrentWeather(WeatherAgent))
            #print (self.schedule.getCurrentIrr(WeatherAgent))
            
            #print (self.schedule.getactualspeed(EV_Agent)[0][0])
            #print (self.schedule.getactualspeed(EV_Agent)[0][1])
            
            
            #print(self.schedule.getSoC(Charging_Control_Agent)[0][self.B][0])
            #print(self.schedule.getSoC(Charging_Control_Agent)[0][self.B][1])
            
            #print(self.schedule.getcarbattery(Charging_Control_Agent)[0][self.B][0])
            #print(self.schedule.getcarbattery(Charging_Control_Agent)[0][self.B][1])
            
            #print (self.schedule.getactualgridpower(Charging_Control_Agent)[0][0][self.B])
            #print (self.schedule.getactualchargepower(Charging_Control_Agent)[0][1][self.B])
            
            print (self.schedule.getbattsoc(Charging_Control_Agent)[0][self.B])
            print(self.schedule.getavailability(EV_Agent)[0][0])
            
            
          
    
    def run_model(self,step_count = 4):
        for k in range(step_count):
            for i in range(7):
  #          print("Step {}".format(i))
             
             for j in range(24):
                    self.step()