from mesa import Agent, Model
from .schdule import *
from .agent import *
from .controlagent import *
from mesa.datacollection import DataCollector  #Data collector
from mesa.space import SingleGrid
import solar.getDataFromExcel as data

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
EV_Data = data.getData_1()
EV_Data2 = data.getData_2()


# ev_agents = []
        

model_params = {
    "height": 20,
    "width": 20   
}

    
class ConceptModel(Model):

   
    verbose = True  # Print-monitoring
    # ev_coordinates =[(2,3),(4,5)]
    Actual_speed= EV_Data[0]
    Accleration1 = EV_Data[1]
    Availability1 = EV_Data[2]
        
    Actual_speed2 = EV_Data2[0]
    Accleration2 = EV_Data2[1]
    Availability2 = EV_Data2[2]
    
    grid_positions = ['uncontrolled', 'V2G','G2V']
    #grid = SingleGrid(model_params['width'], model_params['height'], torus=True)
    
    def __init__(self , N=2,height = model_params['height'] , width = model_params['width'], grid_positions = "uncontrolled" 
     ,Actual_speed= EV_Data[0]
        ,Accleration1 = EV_Data[1]
        ,Availability1 = EV_Data[2]
        
        ,Actual_speed2 = EV_Data2[0]
        ,Accleration2 = EV_Data2[1]
        ,Availability2 = EV_Data2[2] ):
        
        self.num_agents = N
        self.Actual_speed =EV_Data[0]
        self.Accleration1 = EV_Data[1]
        self.Availability1 = EV_Data[2]
        
        self.Actual_speed2 = EV_Data2[0]
        self.Accleration2 = EV_Data2[1]
        self.Availability2 = EV_Data2[2]
                   
        self.schedule = CustomBaseSheduler(self)
        self.grid = SingleGrid(model_params['width'], model_params['height'], torus=True)
        self.grid_positions = grid_positions
        
        weatherAgent = WeatherAgent('weather',self)
        self.schedule.add(weatherAgent)
        '''
        irradianceagent = WeatherAgent('irradiance',self)
        self.schedule.add(irradianceagent)
        '''
        solarPanelAgent = SolarPanelAgent('Solar',self)
        self.schedule.add(solarPanelAgent)
        
        # ev_agents.add(car1)     
        # ev_agents.add(car2) 
        #for i in range(self.num_agents):
        
        car1 = EV_Agent('agent_id', self,speed =self.Actual_speed,accelation = self.Accleration1,availability = self.Availability1 )
        self.schedule.add(car1)
                
        car2 = EV_Agent('agent_id', self,speed =self.Actual_speed2,accelation = self.Accleration2,availability = self.Availability2 )
        self.schedule.add(car2)
            
        ChargeAgent1 = Charge_pole('charge',self)
        self.schedule.add(ChargeAgent1)
        
        ChargeAgent2 = Charge_pole('charge',self)
        self.schedule.add(ChargeAgent2)
        
        ControlAgent = Charging_Control_Agent('control_value',self)
        self.schedule.add(ControlAgent)

        
        # if grid_positions == "uncontrolled":
            # self.B = 0
        # elif  grid_positions == "V2G":
            # self.B = 1
        # elif grid_positions == "G2V":
            # self.B = 2
        
        self.datacollector = DataCollector(
            {
                "Solar Power (W)": lambda m: m.schedule.getCurrentPower(SolarPanelAgent), 
                "Temperature (K)": lambda m: m.schedule.getCurrentWeather(WeatherAgent),
                "Irradiance (W/m^2)": lambda m: m.schedule.getCurrentIrr(WeatherAgent),
                
                "Actual_Speed (km/h)": lambda m: m.schedule.getactualspeed(EV_Agent)[0],
                "Actual_Speed_2 (km/h)": lambda m: m.schedule.getactualspeed(EV_Agent)[1],
                
                "Availability_1": lambda m: m.schedule.getavailability(EV_Agent)[0],
                "Availability_2": lambda m: m.schedule.getavailability(EV_Agent)[1],
                
                "SOC_CAR_1": lambda m: m.schedule.getSoC(Charging_Control_Agent),
                "SOC_CAR_2": lambda m: m.schedule.getSoC(Charging_Control_Agent),
                
                "Car Battery Power(W)": lambda m: m.schedule.getcarbattery(Charging_Control_Agent),
                "Car Battery Power_2(W)": lambda m: m.schedule.getcarbattery(Charging_Control_Agent),
                
                "Grid_Power (W)": lambda m: m.schedule.getactualgridpower(Charging_Control_Agent),
                "CP_Battery_Power (W)": lambda m: m.schedule.getactualchargepower(Charging_Control_Agent),
                
                "Battery_SOC": lambda m: m.schedule.getbattsoc(Charging_Control_Agent)
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
        
     #Create EV agent
      
        # for x,y in ev_coordinates:
            # i= ev_coordinates.index(x)
            # self.grid.position_agent(ev_agents[i], x, y) 
        x = 7
        y = 11

        self.grid.position_agent(car1,x,y) 
        x = 5
        y = 9
        self.grid.position_agent(car2,x,y)
 
    #create chargepole
        x = 6
        y = 10
        self.grid.position_agent(ChargeAgent1,x,y)
    #create chargepole
        x = 6
        y = 9
        self.grid.position_agent(ChargeAgent2,x,y)   
    #create controlAgent
        x = 6
        y = 11
        self.grid.position_agent(ControlAgent,x,y)
    
        self.running = True
    
        
        
    def step(self):
        
        self.schedule.step()
        
        #self.check()
         # collect data
        self.datacollector.collect(self)
               
        if self.verbose:
            #print (self.schedule.getCurrentPower(SolarPanelAgent))
            #print (self.schedule.getCurrentWeather(WeatherAgent))
            #print (self.schedule.getCurrentIrr(WeatherAgent))
            
            # print (self.schedule.getactualspeed(EV_Agent)[0])
            # print (self.schedule.getactualspeed(EV_Agent)[1])
            
            
            print(self.schedule.getSoC(Charging_Control_Agent))
            print(self.schedule.getSoC(Charging_Control_Agent))
            
            #print(self.schedule.getcarbattery(Charging_Control_Agent)[0][0])
            #print(self.schedule.getcarbattery(Charging_Control_Agent)[0][1])
            
            # print (self.schedule.getactualgridpower(Charging_Control_Agent))
            # print (self.schedule.getactualchargepower(Charging_Control_Agent))
            
            #print (self.schedule.getbattsoc(Charging_Control_Agent))
            #print(self.schedule.getavailability(EV_Agent)[0][0])
            
            
          
    # def check(self):
        # v = 1
        # if v ==1:
            # x=3
            # y=7
                    
            # car1 = EV_Agent('agent_id', self)
            # self.schedule.add(car1)
        
            # self.grid.position_agent(car1,x,y)
        # else:
            # None
            
    def run_model(self,step_count = 4):
        for k in range(step_count):
            for i in range(7):
  #          print("Step {}".format(i))
             
             for j in range(24):
                    self.step()