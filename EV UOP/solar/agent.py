from mesa import Agent, Model
import random
import solar.getDataFromExcel as data
import numpy as np

Weather_Data = data.getData()
EV_Data = data.getData_1()

# Solar Panel Agent in FoE UoP
class SolarPanelAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        
        
        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        
        self.neeta = 0.153
        self.Tow = 0.9
        self.A = 1.636
        
        self.Gc = 1000
        self.Tc = 298.15
        self.alpha = 0.0043

        self.weatherAgent = WeatherAgent('Weather_data',self)
        
    def calculateSolarEnergy(self):

        G = self.weatherAgent.outLight;
        T = self.weatherAgent.outdoorTemp;
        
        amountOfEnergy = 220*(G*self.Tow*self.neeta*self.A*(1 - self.alpha*(T-self.Tc )));
        
#        print ("Amount of Solar Energy W  \t\t:\t{}".format(round(amountOfEnergy))) #real data multiplied on weather coefficient
        return amountOfEnergy

    def step(self):

        self.weatherAgent.step()
        self.E = self.calculateSolarEnergy()
                
        self.minute += 5
        
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 7:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
  

class WeatherAgent(Agent): # weather condition, outdoor temperature,solar irradiance 
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        
        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        
        self.outdoorTempList = Weather_Data[0]
        self.outLightList = Weather_Data[1]
     
        
    def getOutdoorTemp(self):
        
        T =  self.outdoorTempList[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
#        print("Outdoor temperature in K\t\t:\t{}".format(T))
        return T
    
    def getOutdoorLight(self): 

        G = self.outLightList[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
#        print("Outdoor Irradiance in W/m^2\t\t:\t{}".format(G) )
        return G
    
            
    def step(self):

 #       print("Week : {} Day : {} Hour : {} \n".format(self.week, self.day, self.hour))    
        
        self.outLight = self.getOutdoorLight()
        self.outdoorTemp = self.getOutdoorTemp()
        
        self.minute += 5
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 7:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
 
class Charging_Control_Agent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.daylist = [0];
        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        self.s = 0
        self.SOC_value = 1
        
        self.EVagent = EV_Agent('SoC_Data',self)
        self.chargepole = Charge_pole('Charging_power',self)
        
                
        
        
        
        
    def SoC(self):
    
        
        
        self.initial_current_capacity = 112.6
        self.Battery_Current = 0
        self.Opencircuit_Voltage = 312.96
        self.Battery_Resistance = 0.096
           
        self.daylist.append(self.day)
  
        self.Battery_Current = (self.Opencircuit_Voltage - ((self.Opencircuit_Voltage)**2 - 4*self.Battery_Resistance*self.PP )**0.5)*0.5*self.Battery_Resistance
        self.value = self.Battery_Current/self.initial_current_capacity

  
        if self.daylist[self.s-1] != self.day:

            self.SOC_value =1
        else:
            self.SOC_value += -1*self.value
          
        print(self.SOC_value)
        
        return self.SOC_value
        
    def chargingcontrol(self):
    
        self.E = self.chargepole.Charging_unit_1();
        self.D = self.EVagent.ActualSpeed;
        self.P = self.EVagent.Powerconsumed;
        
        self.PP = 0
        
        
    def step(self):
    
        self.EVagent.step()
        self.Control_value = self.chargingcontrol()
        self.stateofcharge = self.SoC()
        
        
        self.minute += 5
        self.s += 1
        
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 7:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
            
class EV_Agent(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        self.Battery_Power = 0
        
  
        self.Actual_speed= EV_Data[0]
        self.Refernce_speed= EV_Data[1]
        self.Accleration1 = EV_Data[2]
        
       
    def Accleration(self):
        self.accleration = self.Accleration1[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]

        return self.accleration
     
    def Get_ref_speed(self):
        self.V_ref = self.Refernce_speed[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        return self.V_ref
        
    def Get_Act_speed(self):
        self.V_act = self.Actual_speed[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        return self.V_act
           
    def deltavalue(self):
        self.delta_V = 0     
        if self.V_act > 0:
        
            self.delta_V = self.V_ref - self.V_act 
        else:
            self.delta_V = 0
        
        return self.delta_V
        
    def Resistance_Force(self):
        self.Rolling_Resistance = 0
        self.Aero_Dynamic = 0
        self.Gradiant = 0
        self.Inertia_Resistance = 0
        
        self.co_effecient_RR = 0
        self.Mass_Vehicle = 1995
        self.Ground_Accleration = 0.98
        self.inclanation_angle = 0.089
        self.Frontal_Area = 2.27
        self.Drag_Coeff = 0.29
        self.AirDensity = 1.184
        self.Wind_speed = 4.5
        self.Rotery_inertia_coeff = 1.15
        
        
        
        
        self.co_effecient_RR = 0.01*(1+0.01*self.V_act)
        
        self.Rolling_Resistance = self.co_effecient_RR*self.Mass_Vehicle*self.Ground_Accleration*np.cos(self.inclanation_angle)
        self.Gradiant = self.Mass_Vehicle*self.Ground_Accleration*np.sin(self.inclanation_angle)
        self.Aero_Dynamic = 0.5*18*18*0.04*self.AirDensity*self.Frontal_Area*self.Drag_Coeff*(self.V_act - self.Wind_speed)**2
        self.Inertia_Resistance = self.Rotery_inertia_coeff*self.Mass_Vehicle*self.accleration
        
        self.R_Force = self.Rolling_Resistance + self.Gradiant + self.Aero_Dynamic + self.Inertia_Resistance

        return self.R_Force
        
    def Power(self):
        
        
        self.Power_Traction = 0
        self.Power_Braking = 0
        self.AuxiliaryPower = 300
        
        self.alpha_regeneration = 0.3
        self.P_regeneration = 20000  
        
        self.power_train_eff = 0.9
        
        self.Power_Traction = 18*0.04*self.R_Force*self.V_act/self.power_train_eff
        self.Power_Braking = self.alpha_regeneration*self.P_regeneration

        
        if self.delta_V > 0:
            
            self.Battery_Power = self.Power_Traction + self.AuxiliaryPower
            
        elif self.delta_V <0:
            
            self.Battery_Power =  -1* self.Power_Braking + self.AuxiliaryPower
            
        else:
            self.Battery_Power = 0
        #print( self.Battery_Power)
        return self.Battery_Power
            
        



        
           
    def step(self):
        
        self.minute += 5
        
        
        self.ReferenceSpeed = self.Get_ref_speed()
        self.ActualSpeed = self.Get_Act_speed()
        self.acclerationvalue = self.Accleration()
        self.ResistanceForce = self.Resistance_Force()
        self.Delta_Velocity = self.deltavalue()
        self.Powerconsumed = self.Power()
   
        
        
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 7:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
        

            
            
class Charge_pole(Agent):
 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        self.chargecapacity = 10000
 
        
        self.solarpanelagent = SolarPanelAgent('Solar_data',self)
        
        
    def Charging_unit_1(self):
    
               
        self.currentsupply = self.chargecapacity
        #print("Current Supply {}".format(self.currentsupply))
        return self.currentsupply

        
        
    def step(self):
        
        self.solarpanelagent.step()

        
        self.S = self.Charging_unit_1()
        
        self.minute += 5
        
        if self.minute > 59:
            self.hour += 1
            self.minute = 0

        if self.hour > 23:
            self.day += 1
            self.hour = 0

        if self.day > 7:
            self.week += 1
            self.day = 1
                
        if self.week > 4:
            self.month +=1
            self.week = 1
            
        print(  "Week : {} Day : {} Hour : {} minute: {}\n".format(self.week, self.day, self.hour,self.minute))        
                