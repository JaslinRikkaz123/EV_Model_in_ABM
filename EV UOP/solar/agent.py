from mesa import Agent, Model
import random
import solar.getDataFromExcel as data
import numpy as np

Weather_Data = data.getData()
EV_Data = data.getData_1()
EV_Data2 = data.getData_2()

class Charge_pole(Agent):
 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
     
    def fastcharging(self):
        charging_amount = 30000
        return charging_amount
        
    def L2charging(self):
        charging_amount = 6600
        return charging_amount
        
        
    def step(self):
        
        
        self.F = self.fastcharging()
        self.S = self.L2charging()
        
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

        G = self.weatherAgent.getOutdoorLight();
        T = self.weatherAgent.getOutdoorTemp();
        
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
 

class EV_Agent(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
     
        
        self.daylist = [0];
        self.s = 0
        
        self.Actual_speed= EV_Data[0]
        self.Accleration1 = EV_Data[1]
        self.Availability1 = EV_Data[2]
        
        self.Actual_speed2 = EV_Data2[0]
        self.Accleration2 = EV_Data2[1]
        self.Availability2 = EV_Data2[2]
        

       
    def Accleration(self):
        self.accleration1 = self.Accleration1[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.accleration2 = self.Accleration2[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.accleration = [self.accleration1,self.accleration2]
        
        return self.accleration
     
    def Availability(self):
        self.availability1 = self.Availability1[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.availability2 = self.Availability2[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.availability = [self.availability1,self.availability2]
        
        return self.availability
        
    def Get_Act_speed(self):
        self.V_act1 = self.Actual_speed[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.V_act2 = self.Actual_speed2[24 * 12* (self.day - 1) + 12*(self.hour -1)+ 24 *12 *(self.week - 1) + int(self.minute/5)]
        self.V_act = [self.V_act1,self.V_act2]
        
        return self.V_act

        
    def Resistance_Force(self):
        self.Rolling_Resistance = []
        self.Aero_Dynamic = []
        self.Gradiant = []
        self.Inertia_Resistance = []
        self.R_Force = []
        
        self.co_effecient_RR = []
        self.Mass_Vehicle = [1800,1800]
        self.Ground_Accleration = 9.8
        self.inclanation_angle = 0
        self.Frontal_Area = 2.27
        self.Drag_Coeff = 0.29
        self.AirDensity = 1.184
        self.Wind_speed = 4.5
        self.Rotery_inertia_coeff = 1.04
        
        for V in self.V_act:
            co_effecient_rr = 0.01*(1+0.01*0.277*V)
            self.co_effecient_RR.append(co_effecient_rr)
            
            aero_Dynamic = 0.5*self.AirDensity*self.Frontal_Area*self.Drag_Coeff*(0.277*(V - self.Wind_speed))**2
            self.Aero_Dynamic.append(aero_Dynamic)
            
        for (co_effecient_rr,m) in  zip(self.co_effecient_RR,self.Mass_Vehicle):
            rolling_Resistance =  co_effecient_rr*m*self.Ground_Accleration*np.cos(self.inclanation_angle)
            self.Rolling_Resistance.append(rolling_Resistance)
            
        for (a,m) in zip(self.accleration,self.Mass_Vehicle):
            inertia_Resistance = self.Rotery_inertia_coeff*m*a
            self.Inertia_Resistance.append(inertia_Resistance)
        
        for m in self.Mass_Vehicle:
            gradiant_force = m*self.Ground_Accleration*np.sin(self.inclanation_angle)
            self.Gradiant.append(gradiant_force)

        for (rr,ir,ad,gf) in zip(self.Rolling_Resistance,self.Inertia_Resistance,self.Aero_Dynamic,self.Gradiant):
            self.r_Force = rr + gf + ad + ir
            self.R_Force.append(self.r_Force)
        #print( "r_force:{} ".format(self.R_Force))  
        return self.R_Force
        
    def Power(self):
        
        self.Battery_Powerlist = []
       
        self.AuxiliaryPower = 300
        self.Powerusage = []
        self.Power_Traction = [] 
        self.Power_Braking = []
        
        self.alpha_regeneration = 0.3
        self.power_train_eff = 0.92
        
        for (V,r) in zip(self.V_act,self.R_Force):
            powerusage = 0.277*r*V  
            self.Powerusage.append(powerusage)
          
        for P in self.Powerusage:
            tp = P/self.power_train_eff
            bp = self.alpha_regeneration*P
            
            self.Power_Traction.append(tp)
            self.Power_Braking.append(bp)
            
        
        
        for (a,tp,bp )in zip(self.accleration,self.Power_Traction,self.Power_Braking):
        
            if a > 0:
                
                self.Battery_Power = tp + self.AuxiliaryPower
                
            elif a <0:
                
                self.Battery_Power =  bp + self.AuxiliaryPower
            else:
                self.Battery_Power = tp
                
            self.Battery_Powerlist.append(self.Battery_Power)
        #print("Battery_Powerlist: {}".format(self.Battery_Powerlist))
        return self.Battery_Powerlist
            
    def carSOC(self):
        self.initial_current_capacity = 112.6
        self.Opencircuit_Voltage = 312.96
        self.Battery_Resistance = 0.096
        
        Current = []
        Value = []
        self.SOC_value = [1,1]
        self.daylist.append(self.day)
        
        for self.Battery_Power in self.Battery_Powerlist:
            current = (self.Opencircuit_Voltage - ((self.Opencircuit_Voltage)**2 - 4*self.Battery_Resistance*self.Battery_Power )**0.5)*0.5/self.Battery_Resistance
            Current.append(current)
            
        for i in Current:
        
            value = 5*i/(self.initial_current_capacity*60)
            Value.append(value)
        
        #Update SOC value of EV as 1 in every start of the day otherthan that,calculate SOC w.r.t value
        if self.daylist[self.s-1] != self.day:

            self.SOC_value = [1,1]
         
        else:
            for i in range(len(self.SOC_value)):
                self.SOC_value[i] = self.SOC_value[i] + -1*Value[i]
            
        
        
        #print("SOC: {}".format(self.SOC_value))
        return self.SOC_value
           
    def step(self):
        
        self.minute += 5
        self.s += 1
        
     
        self.ActualSpeed = self.Get_Act_speed()
        self.acclerationvalue = self.Accleration()
        self.a  = self.Availability()
        self.ResistanceForce = self.Resistance_Force()
        self.Powerconsumed = self.Power()
        self.stateofcharge = self.carSOC()
   
        
        
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
        
class Utility_Grid(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1


    def step(self):
        
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
         
class Battery_Storage(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.minute = 0
        self.hour = 1
        self.day = 1
        self.week = 1
        self.month = 1
        #battery_storage_cap in Wh & max_power in W
        self.max_power  = 25000
        self.battery_storage_cap = 19730
        self.soc_max = 0.8
        self.soc_min = 0.2

        
    def step(self):
        
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
         
