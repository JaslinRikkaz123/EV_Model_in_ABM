from mesa import Agent, Model
import random
import solar.getDataFromExcel as data
import numpy as np
from .schdule import *

Weather_Data = data.getData()

#_________________________________________________________________________________  CHARGE_POLE_AGENT _______________________________
class Charge_pole(Agent):
 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
  
    def fastcharging(self):
        charging_amount = 30000
        return charging_amount
        
    def L2charging(self):
        charging_amount = 6600
        return charging_amount
        
    def L1charging(self):
        charging_amount = 2300
        return charging_amount
        
    def step(self):

        self.F = self.fastcharging()
        self.S = self.L2charging()
        self.S1 = self.L1charging()
       
     
#_________________________________________________________________________________   SOLAR_PANEL_AGENT in FoE UoP _______________________________
'''Electrical Department 40kWp(21.89m^2,20x4) and 15kWp(98.21m^2,15x4) total = 55kWp'''
class SolarPanelAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
      
        self.neeta = 0.153
        self.Tow = 0.9
        self.A = 1.636
        
        self.Gc = 1000
        self.Tc = 298.15
        self.alpha = 0.0043
        
          
    def calculateSolarEnergy(self):
        
        T = self.model.schedule.getCurrentWeather(WeatherAgent)[0];
        G = self.model.schedule.getCurrentIrr(WeatherAgent)[0];
        
        self.amountOfEnergy_kW = 220*(G*self.Tow*self.neeta*self.A*(1 - self.alpha*(T-self.Tc )));
        self.amountOfEnergy  = self.amountOfEnergy_kW/1000

        return self.amountOfEnergy

    def step(self):
       
        self.E = self.calculateSolarEnergy()
#_________________________________________________________________________________  WEATHER_AGENT _______________________________
'''weather condition, outdoor temperature,solar irradiance in Kandy,Peradeniya region '''
class WeatherAgent(Agent): 
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
 
        self.outdoorTempList = Weather_Data[0]
        self.outLightList = Weather_Data[1]
     

    def getOutdoorTemp(self):

        
        self.T =  self.outdoorTempList[self.model.schedule.steps]
#        print("Outdoor temperature in K\t\t:\t{}".format(T))
        return self.T
    
    def getOutdoorLight(self): 

        self.G = self.outLightList[self.model.schedule.steps]
#        print("Outdoor Irradiance in W/m^2\t\t:\t{}".format(G) )
        return self.G
    
            
    def step(self):

 #       print("Week : {} Day : {} Hour : {} \n".format(self.week, self.day, self.hour))    
       
        self.outLight = self.getOutdoorLight()
        self.outdoorTemp = self.getOutdoorTemp()
        
      
#_________________________________________________________________________________  EV_AGENT ______________________________________________________________
'''EV cars assume as NISSAN LEAF 2013 model,Total 27 cars are available in the faculty car park'''
class EV_Agent(Agent):

    def __init__(self,unique_id, model,speed,accelation,availability):
        super().__init__(unique_id, model)

        
        self.daylist = [0];
        self.s = 0
        
        self.Actual_speed11 = speed
        self.Accleration1 = accelation
        self.Availability1 = availability
   
    def Accleration(self):
        
        self.accleration1 = self.Accleration1[self.model.schedule.steps]


        return self.accleration1
     
    def Availability(self):
        self.availability = self.Availability1[self.model.schedule.steps]
 
        return self.availability
        
    def Get_Act_speed(self):

        self.Actual_speed1 = self.Actual_speed11[self.model.schedule.steps]
        
        return self.Actual_speed1

        
    def Resistance_Force(self):
        self.Rolling_Resistance = 0
        self.Aero_Dynamic = 0
        self.Gradiant = 0
        self.Inertia_Resistance = 0
        
        self.co_effecient_RR = 0
        self.Mass_Vehicle = 1577
        self.Ground_Accleration = 9.8
        self.inclanation_angle = 0
        self.Frontal_Area = 2.27
        self.Drag_Coeff = 0.29
        self.AirDensity = 1.184
        self.Wind_speed = 4.5
        self.Rotery_inertia_coeff = 1.15
        
        self.co_effecient_RR = 0.01*(1+0.01*0.277*self.Actual_speed1)
        
        self.Rolling_Resistance = self.co_effecient_RR*self.Mass_Vehicle*self.Ground_Accleration*np.cos(self.inclanation_angle)
        self.Gradiant = self.Mass_Vehicle*self.Ground_Accleration*np.sin(self.inclanation_angle)
        self.Aero_Dynamic = 0.5*self.AirDensity*self.Frontal_Area*self.Drag_Coeff*(0.277*(self.Actual_speed1 - self.Wind_speed))**2
        self.Inertia_Resistance = self.Rotery_inertia_coeff*self.Mass_Vehicle*abs(self.accleration1)
        
        self.R_Force = self.Rolling_Resistance + self.Gradiant + self.Aero_Dynamic + self.Inertia_Resistance
        
        return self.R_Force
        
    def Power(self):
        
        self.Battery_Power = 0
   
        self.Power_Traction = 0
        self.Power_Braking = 0
        
        self.AuxiliaryPower =300
        
        self.alpha_regeneration = 0.4
        self.Powerusage = 0.277*self.R_Force*self.Actual_speed1
        
        self.power_train_eff = 0.96
        
        self.Power_Traction = self.Powerusage/self.power_train_eff
        self.Power_Braking = self.alpha_regeneration*self.Powerusage
     
            
        if self.availability!= 1 and self.Actual_speed1 ==0:
                
            self.Battery_Power = self.Power_Traction + -1*self.Power_Braking
            
        elif self.availability == 1 and self.Actual_speed1 ==0:
                
            self.Battery_Power = 0
                
        else:
                
            self.Battery_Power =  self.Power_Traction + self.AuxiliaryPower +-1*self.Power_Braking


        #print(self.Battery_Power )
        return self.Battery_Power 
    
            
    def carSOC(self):
        self.initial_current_capacity = 112.6
        self.Opencircuit_Voltage = 312.96
        self.Battery_Resistance = 0.096
        
  
        self.SOC_value = 1
        self.daylist.append(self.model.day)
        
        current = (self.Opencircuit_Voltage - ((self.Opencircuit_Voltage)**2 - 4*self.Battery_Resistance*self.Battery_Power )**0.5)*0.5/self.Battery_Resistance

        Value = 5*current/(self.initial_current_capacity*60)
        
        
        #Update SOC value of EV as 1 in every start of the day otherthan that,calculate SOC w.r.t value
        if self.daylist[self.s-1] != self.model.day:

            self.SOC_value = 1
         
        else:
     
            self.SOC_value = self.SOC_value + -1*Value
            
        
        
        #print("SOC: {}".format(self.SOC_value))
        return self.SOC_value
           
    def step(self):
        

        self.s += 1
        
     
        self.ActualSpeed = self.Get_Act_speed()
        self.acclerationvalue = self.Accleration()
        self.a  = self.Availability()
        self.ResistanceForce = self.Resistance_Force()
        self.Powerconsumed = self.Power()
        self.stateofcharge = self.carSOC()

#_________________________________________________________________________________  UTILITY_GRID_AGENT ______________________________________________________________
'''It has been developed as infinite source'''
class Utility_Grid(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

#_________________________________________________________________________________  BATTERY_STORAGE_AGENT ______________________________________________________________
'''This is an external storage for stroing excess power from solar PV and supply power to EV when the Solar PV is not enough '''         
class Battery_Storage(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

       
        #battery_storage_cap in Wh & max_power in W
        self.max_power  = 50000
        self.battery_storage_cap = 40000
        self.soc_max = 0.8
        self.soc_min = 0.2
        
    def step(self):
        
        pass