from mesa import Agent, Model
from .schdule import *
from .agent import *
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

    def __init__(self, height = model_params['height'] , width = model_params['width'], grid_positions = "uncontrolled" ):
    
        
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
            if 9 <= self.hour <= 16:
                print("Charge Pole is Available - U Can Charge..!!!")
                    
                if self.D == 0:
                    if self.SOC_value <= 1:
                        self.PP = -1*self.E + self.P
                              
                    else:
                        self.PP = self.P
                            
                else:
                    self.PP = self.P
                    
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
                    
            print(self.PP)
            return self.PP 
            
        elif grid_positions == "V2G":
            if 9 <= self.hour <= 16:
                print("Charge Pole is Available - U Can Charge..!!!")
            
                if self.D == 0:
                
                    if self.SOC_value <= 0.5:
                        self.PP = -1*self.E + self.P
                        print("SoC less than 50% recharge to 0.5")
                          
                    elif  0.5< self.SOC_value <= 0.8:
                        self.PP = -1*self.E + self.P
                        print("It's controlled charging - G2V")
                        
                    else:
                        self.PP = self.E + self.P
                        print("It's controlled charging - V2G")
                        
                else:
                    self.PP = self.P
                
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
            return self.PP
                
        elif grid_positions == "G2V":
            if 9 <= self.hour <= 16:
                print("Charge Pole is Available - U Can Charge..!!!")
            
                if self.D == 0:
                
                    if self.SOC_value <= 0.5:
                        self.PP = -1*self.E + self.P
                        print("SoC less than 50% recharge to 0.5")
                          
                    elif  0.5< self.SOC_value <= 1.0:
                        self.PP = -1*self.E + self.P
                        print("It's controlled charging - G2V")
                        
                    else:
                        self.PP = self.P   
                        
                else:
                    self.PP = self.P
                
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
                
            print(self.PP)
            return self.PP
        
        
       
       
        self.datacollector = DataCollector(
            {
                "Solar Energy (W)": lambda m: m.schedule.getCurrentPower(SolarPanelAgent), 
                "Temperature (K)": lambda m: m.schedule.getCurrentWeather(WeatherAgent),
                "Irradiance (W/m^2)": lambda m: m.schedule.getCurrentIrr(WeatherAgent),
                "Reference_Speed (km/h)": lambda m: m.schedule.getreferencespeed(EV_Agent),
                "Actual_Speed (km/h)": lambda m: m.schedule.getactualspeed(EV_Agent),
                "SoC": lambda m: m.schedule.getSoC(Charging_Control_Agent),
                "Charge_power (W)": lambda m: m.schedule.getactualchargepower(Charge_pole)
                
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
    
    #create ev agent
        x = 5
        y = 10
        self.grid.position_agent(EvAgent,x,y)
        
    #create chargepole
        x = 6
        y = 10
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
            print (self.schedule.getactualspeed(EV_Agent))
            print (self.schedule.getreferencespeed(EV_Agent))
            #print(self.schedule.getactualchargepower(Charge_pole))
            #print (self.schedule.getSoC(Charging_Control_Agent))
            
            
          
    
    def run_model(self,step_count = 4):
        for k in range(step_count):
            for i in range(7):
  #          print("Step {}".format(i))
                for j in range(24):
                    self.step()