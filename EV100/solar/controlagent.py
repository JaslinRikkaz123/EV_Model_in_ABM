from mesa import Agent, Model
from .agent import *

dataset = {'Initial SOC': float,'initial_current_capacity':float,'Opencircuit_Voltage':float,'Battery_Resistance':float}
EV_Dataset = data.get_EV_value(dataset)

#_________________________________________________________________________________  CHARGING_CONTROL_AGENT ______________________________________________________________
'''It controls charging pattern 3 charging patterns(uncon,V2G,G2V) and power management with soc'''

class Charging_Control_Agent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        
        self.daylist = [0];
        self.s = 0
        self.option = self.model.grid_positions
    
        self.SOC_value = EV_Dataset['Initial SOC']
  
        self.Batterypower = 0
        self.Gridpower = 0

           
    def SoC(self):
        
        self.initial_current_capacity = EV_Dataset['initial_current_capacity']
        self.Opencircuit_Voltage = EV_Dataset['Opencircuit_Voltage']
        self.Battery_Resistance = EV_Dataset['Battery_Resistance']
        Battery_Current = []
        Value = []
        
        self.daylist.append(self.model.day)
        
        for (power,v,r) in zip(self.Power,self.Opencircuit_Voltage,self.Battery_Resistance):
            i = (v - ((v)**2 - 4*r*power*1000 )**0.5)*0.5/r
            Battery_Current.append(i)
            
        for (i,cc) in zip(Battery_Current,self.initial_current_capacity):
            value = 5*i/(cc*60)
            Value.append(round(value,2))
     
        #Update SOC value of EV as 1 in every start of the day otherthan that,calculate SOC w.r.t value
        if self.daylist[self.s-1] != self.model.day:

            self.SOC_value =EV_Dataset['Initial SOC']
            
        else:
     
           for i in range(0,len(self.SOC_value)):
                self.SOC_value[i] = self.SOC_value[i] + -1*Value[i]

        return self.SOC_value
        
    def chargingcontrol(self):
        self.E0 = self.model.schedule.getchargeL1(Charge_pole)[0];
        self.E1 = self.model.schedule.getchargeL2(Charge_pole)[0];
        self.E2 = self.model.schedule.getchargefast(Charge_pole)[0];
        self.Pq = self.model.schedule.getcarbattery_P(EV_Agent);
        self.Dq = self.model.schedule.getavailability(EV_Agent);
        
        self.Power =[]
       
        #If car start to charge in UNCONTROLLED CHARGING PATTERN - whenever car stops in the faculty it charge the car until SOC reach to 1 or disconnection/return to home
        if self.option == "uncontrolled":    
            for (self.P,self.D,self.SOC) in zip(self.Pq,self.Dq,self.SOC_value):
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                            
                    if self.D == 1:
                        if self.SOC < 1:
                            self.PP = -1*self.E1 + self.P
                                      
                        else:
                            self.PP = self.P
                                    
                    else:
                        self.PP = self.P
                            
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    self.PP = self.P
                    
                self.Power.append(self.PP/1000)        
            
            #if car choose V2G controlled charging - when SOC less than 0.5, it immediately charge in fast charging mode to reach to 0.5,then it charge until SOC = 0.8 afterwards  it is in V2G mode '''
        elif self.option  == "V2G":    
            for (self.P,self.D,self.SOC) in zip(self.Pq,self.Dq,self.SOC_value):
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                            
                    if self.D == 1:
                        if self.SOC <= 0.5:
                            self.PP = -1*self.E2 + self.P
                            #print("SoC less than 50% recharge to 0.5")
                                      
                        elif  0.5< round(self.SOC,2) < 0.80:
                            self.PP = -1*self.E1 + self.P
                            #print("It's controlled charging - V2G")
                            
                        elif  0.8 <= round(self.SOC,2) < 0.82:
                            self.PP =  self.P
                            
                        else:
                            self.PP = self.E1 + self.P
                            print("It's controlled charging - V2G")
                    else:
                        self.PP = self.P
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    self.PP = self.P
                        
                   # print(round(self.SOC_value,1))    
                self.Power.append(self.PP/1000)
        else:    
            #if car choose G2V controlled charging - when SOC is in 0.5 it immediately charge in fast charging mode to reach to 0.5, then it charge in slow charges the car
            for (self.P,self.D,self.SOC) in zip(self.Pq,self.Dq,self.SOC_value):      
                if 8 <= self.model.hour <= 17:
                   # print("Charge Pole is Available - U Can Charge..!!!")
                            
                    if self.D == 1:
                            
                        if self.SOC <= 0.5:
                            self.PP = -1*self.E2 +self.P
                            #print("SoC less than 50% recharge to 0.5")
                                      
                        elif  0.5< self.SOC <= 1.0:
                            self.PP = -self.E0 +self.P
                            #print("It's controlled charging - G2V")
                                    
                        else:
                            self.PP = self.P
                                    
                    else:
                        self.PP = self.P
                            
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    self.PP = self.P
                self.Power.append(self.PP/1000)
            #print(self.Power)
        return  self.Power 
            
    def battery_SOC(self):
        #CP battery SOC calculate here. It starts with 0.7 and it can calculate w.r.t the battery power value
        
        battery_storage_cappacity = self.model.schedule.getbattstorageCap(Battery_Storage)[0]
    
        if self.daylist[self.s-1] == 0:
            
            self.batterySOC = 0.7
          
            
        else:
        
            soc = -1*self.Batterypower*5 /(battery_storage_cappacity*60)
            
            self.batterySOC += soc
           
        return self.batterySOC
            
    def power_management(self):
        solar = self.model.schedule.getCurrentPower(SolarPanelAgent)[0];
        SOC_max_value = 0.8
        SOC_min_value = 0.2
        battery_max_power_limit = self.model.schedule.getbattstoragemaxP(Battery_Storage)[0]
        EV_Battery_List = []
        Delta = 0
        
        for (PP,P) in zip(self.Power,self.Pq):
            EV_Battery = -1*( 1000*PP - P)
            EV_Battery_List.append(EV_Battery)
            
        for ev in range(0,len(EV_Battery_List)):
            Delta = Delta + EV_Battery_List[ev]
            delta= solar*1000 - Delta 
      
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
        
        return [ self.Gridpower/1000,     self.Batterypower/1000]
    
        
    def step(self):
    
        
        self.batterysoc = self.battery_SOC()
        self.Control_value = self.chargingcontrol()
        self.stateofcharge = self.SoC()
        self.powervalue = self.power_management()
     
        self.s += 1
        
       