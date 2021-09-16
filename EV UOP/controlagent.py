from mesa import Agent, Model
from .agent import *


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
        self.option = self.model.grid_positions
        
        # self.Actual_speed = speed
        # self.Accleration = accelation
        # self.Availability = availability
        self.SOC_value = 1
        # self.SOC_value2 =[1,1]
        # self.SOC_value3 = [1,1]
        
        self.batterySOC = 0.6

        #self.solarpanelagent = SolarPanelAgent('Solar_data',self)
        #self.EVagent = EV_Agent('SoC_Data',speed,accelation,availability,self)
        self.chargepole = Charge_pole('Charging_power',self)
        self.batterypole = Battery_Storage('Battery_capacity',self)
          
        self.Batterypower = 0
        self.Gridpower = 0

           
    def SoC(self):

        self.initial_current_capacity = 112.6
        self.Opencircuit_Voltage = 312.96
        self.Battery_Resistance = 0.096
        
        #Battery_Current = []
        # current1 =[]
        # current2= []
        # current3 = []
        
        #Value = []
        # Value1 =[]
        # Value2 =[]
        # Value3 =[]
        
        self.daylist.append(self.day)
        
        #Calculate battery current [[i1,i2],[],[]]and soc values
        
        #for (power,v,r) in zip(self.Power,self.Opencircuit_Voltage,self.Battery_Resistance):
        Battery_Current = (self.Opencircuit_Voltage - ((self.Opencircuit_Voltage)**2 - 4*self.Battery_Resistance*self.PP )**0.5)*0.5/self.Battery_Resistance
            #Battery_Current.append(c)
                 
        #for (i,cc) in zip(Battery_Current,self.initial_current_capacity):
        Value = 5*Battery_Current/(self.initial_current_capacity*60)
            #Value.append(round(value,2))
                
        # for (power,v,r) in zip(self.PP[1],self.Opencircuit_Voltage,self.Battery_Resistance):
            # c = (v - ((v)**2 - 4*r*power )**0.5)*0.5/r
            # current2.append(c)
                 
        # for (i,cc) in zip(current2,self.initial_current_capacity):
            # value = 5*i/(cc*60)
            # Value2.append(round(value,2))        
                
        # for (power,v,r) in zip(self.PP[2],self.Opencircuit_Voltage,self.Battery_Resistance):
            # c = (v - ((v)**2 - 4*r*power )**0.5)*0.5/r
            # current3.append(c)
                 
        # for (i,cc) in zip(current3,self.initial_current_capacity):
            # value = 5*i/(cc*60)
            # Value3.append(round(value,2)) 
            
        # Battery_Current = [current1,current2,current3]
        # Value = [Value1,Value2,Value3]
        #print(Value)
        
        #Update SOC value of EV as 1 in every start of the day otherthan that,calculate SOC w.r.t value
        if self.daylist[self.s-1] != self.day:

            self.SOC_value = 1
            # self.SOC_value2 = [1,1]
            # self.SOC_value3 = [1,1]
            
        else:
     
           self.SOC_value += -1*Value
           # self.SOC_value2[0] += -1*Value[1][0]
           # self.SOC_value3[0] += -1*Value[2][0]
            
           #self.SOC_value[1] += -1*Value[1]
           # self.SOC_value2[1] += -1*Value[1][1]
           # self.SOC_value3[1] += -1*Value[2][1]
        #self.SOC_value= [[0,1],[0,1],[0,1]]
        #self.SOC_value = [ self.SOC_value1,self.SOC_value2,self.SOC_value3]  
        #print("self.SOC_value:{}".format(self.SOC_value) )
        return self.SOC_value
        
    def chargingcontrol(self):
        
        self.E1 = self.chargepole.L2charging();
        self.E2 = self.chargepole.fastcharging();
        # self.P = self.EVagent.Power()
        # self.D = self.EVagent.a;
        self.D = 9
        self.P = 100
        print(self.option)
        #self.Power = []
        # self.Power2 = []
        # self.Power3 = []
        # self.SOC_value = [ self.SOC_value1,self.SOC_value2,self.SOC_value3]
        
        #If car start to charge in UNCONTROLLED CHARGING PATTERN - whenever car stops in the faculty it charge the car until SOC reach to 1 or disconnection/return to home
        if self.option == "uncontrolled":    
            #for  (p,v,self.SOC_value) in  zip(self.P,self.D,self.SOC_value):  
            if 8 <= self.hour <= 17:
                print("Charge Pole is Available - U Can Charge..!!!")
                        
                if self.D== 1:
                    if self.SOC_value < 1:
                        self.PP = -1*self.E1 + self.P
                                  
                    else:
                        self.PP = self.P
                                
                else:
                    self.PP = self.P
                        
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
            #self.Power.append(PP)        
            
            #if car choose V2G controlled charging - when SOC less than 0.5, it immediately charge in fast charging mode to reach to 0.5,then it charge until SOC = 0.8 afterwards  it is in V2G mode '''
        elif self.option  == "V2G":    
            #for  (p,v,v2g_SOC) in  zip(self.P,self.D,self.SOC_value):   
            if 8 <= self.hour <= 17:
                print("Charge Pole is Available - U Can Charge..!!!")
                        
                if self.D == 1:
                    if self.SOC_value <= 0.5:
                        self.PP = -1*self.E2 + self.P
                        print("SoC less than 50% recharge to 0.5")
                                  
                    elif  0.5< round(self.SOC_value,2) < 0.80:
                        self.PP = -1*self.E1 + self.P
                        print("It's controlled charging - G2V")
                         
                         
                    elif  0.8 <= round(self.SOC_value,2) < 0.82:
                        self.PP =  self.P
                    else:
                        self.PP = self.E1 + self.P
                        print("It's controlled charging - V2G")
                else:
                    self.PP = self.P
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
                    
               # print(round(self.SOC_value,1))    
            #self.Power.append(PP)
        else:    
            #if car choose G2V controlled charging - when SOC is in 0.5 it immediately charge in fast charging mode to reach to 0.5, then it charge in slow charges the car
            #for  (p,v,G2V_SOC) in  zip(self.P,self.D,self.SOC_value):    
            if 8 <= self.hour <= 17:
                print("Charge Pole is Available - U Can Charge..!!!")
                        
                if self.D == 1:
                        
                    if self.SOC_value <= 0.5:
                        self.PP = -1*self.E2 +self.P
                        print("SoC less than 50% recharge to 0.5")
                                  
                    elif  0.5< self.SOC_value <= 1.0:
                        self.PP = -1*self.E1 +self.P
                        print("It's controlled charging - G2V")
                                
                    else:
                        self.PP = self.P
                                
                else:
                    self.PP = self.P
                        
            else:
                print("Charge Pole is not available....SORRY.....!!!")
                self.PP = self.P
            #self.Power.append(PP)
                
            #self.pp1=[s1,s2]
            #self.PP = [self.Power1,self.Power2,self.Power3]
            #print("PP_amount: {}".format(self.PP))
        return  self.PP   
            
    def battery_SOC(self):
        #CP battery SOC calculate here. It starts with 0.5 and it can calculate w.r.t the battery power value
        
        #soc_Value = []
        battery_storage_cappacity = self.batterypole.battery_storage_cap
    
        if self.daylist[self.s-1] == 0:
            
            self.batterySOC = 0.6
            # self.batterySOC2 = 0.6
            # self.batterySOC3 = 0.6
            
        else:
            #for m in self.battpowerlist:
            soc = -1*self.Batterypower*5 /(battery_storage_cappacity*60)
                #soc_Value.append(round(soc,2))
                
            #print(soc_Value)
            self.batterySOC += soc
            # self.batterySOC2 += soc_Value[1]
            # self.batterySOC3 += soc_Value[2]
        
        
        #self.SOC_Value_battery = [ self.batterySOC1, self.batterySOC2, self.batterySOC3]  
        
        #print("SOC: {}".format(self.SOC_Value_battery))
        return self.batterySOC
            
    def power_management(self):
        #self.solar = self.solarpanelagent.calculateSolarEnergy()
        SOC_max_value = 0.8
        SOC_min_value = 0.2
        battery_max_power_limit = self.batterypole.max_power
        
        #Delta = [0,1,2]
        #Delta = []
        
        #self.EV_Battery =[]
        #EV_Battery = []
        # EV_Battery2 = []
        # EV_Battery3 = []
        
        #print("Solar: {}".format(self.solar)  )     
        self.gridpowerlist = []
        self.battpowerlist = []
  
        
        #for (tp,cp) in zip(self.Power,self.P):
        EV_Battery = -1*( self.PP - self.P)
            #EV_Battery.append(evp)
            
        # for (tp,cp) in zip(self.PP[1],self.P):
            # evp = -1*( tp - cp)
            # EV_Battery2.append(evp)

        # for (tp,cp) in zip(self.PP[2],self.P):
            # evp = -1*( tp - cp)
            # EV_Battery3.append(evp)

        #self.EV_Battery = [EV_Battery1,EV_Battery2,EV_Battery3]
            
        #print("self.EV_Battery:{}".format(self.EV_Battery))
        
        #for evp in EV_Battery:
        #EVP = EV_Battery[0] +EV_Battery[1]
        delta = 1000- EV_Battery
        #Delta.append(delta)
           
        #print("delta: {}".format(Delta))
        #power management: initially solar can supply the power to EV, which is not enough CP battery can give it, then EV can get the energy from grid
        
        #for self.delta_P in Delta:
           
        
        if delta <= 0:
            if self.batterySOC <= SOC_min_value:
                
                self.Batterypower = 0
                    
            else:
                
                if delta < -1*battery_max_power_limit:
                    self.Batterypower = battery_max_power_limit
                      
                        
                else:
                    self.Batterypower = -1*delta
                       
                        
        else:
            if self.batterySOC >= SOC_max_value:
                self.Batterypower = 0
                    
            else:
                if delta > battery_max_power_limit:
                    self.Batterypower = -1*battery_max_power_limit
                       
                else:
                    self.Batterypower = -1*delta
                        
        self.Gridpower = -1*(delta+ self.Batterypower)
            
            
             # self.gridpowerlist.append(self.Gridpower) 
             # self.battpowerlist.append(self.Batterypower)
        #print(self.Gridpower,     self.Batterypower)
        return (   self.Gridpower,     self.Batterypower)
    
        
    def step(self):
    
        #self.EVagent.step()
        #self.solarpanelagent.step()
        
        self.batterysoc = self.battery_SOC()
        self.Control_value = self.chargingcontrol()
        self.stateofcharge = self.SoC()
        self.powervalue = self.power_management()
        
        
        
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
            