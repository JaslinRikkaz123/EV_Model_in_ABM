from mesa.agent import Agent
from getDataFromExcel import get_XLSX_Data as data
import numpy as np

#Read weather data from database-getDatafromExcel
Weather_Data = data('solardata','Sheet1',{'Temp' : float, 'Radiation':float})

#Read EV data from database-getDatafromExcel
dataset  ={'CAR-0': float, 'Accleration-0': float,'0-available': float,'CAR-1': float, 'Accleration-1': float,'1-available': float
,'CAR-2': float, 'Accleration-2': float,'2-available': float,'CAR-3': float, 'Accleration-3': float,'3-available': float,'CAR-4': float, 'Accleration-4': float,'4-available': float
,'CAR-5': float, 'Accleration-5': float,'5-available': float,'CAR-6': float, 'Accleration-6': float,'6-available': float,'CAR-7': float, 'Accleration-7': float,'7-available': float
,'CAR-8': float, 'Accleration-8': float,'8-available': float,'CAR-9': float, 'Accleration-9': float,'9-available': float,'CAR-10': float, 'Accleration-10': float,'10-available': float
,'CAR-11': float, 'Accleration-11': float,'11-available': float,'CAR-12': float, 'Accleration-12': float,'12-available': float}

EV_Data = data('EVsample1','EVsample',dataset)

#_________________________________________________________________________________   Solar Panel Agent  _______________________________

class SolarPanelAgent(Agent):
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.neeta = 0.153
        self.Tow = 0.9
        self.A = 1.636
        
        self.Gc = 1000
        self.Tc = 298.15
        self.alpha = 0.0043
    #calculate solar PV energy generation
    def calculateSolarEnergy(self):

        cellmates = self.model.grid.get_cell_list_contents ([self.pos])
        weatherAgent = cellmates[1]

        G = weatherAgent.getOutdoorLight() #Read irradiance value from weather agent
        T = weatherAgent.getOutdoorTemp()  #Read temperature value from weather agent
        
        solar_energy = 220*5*(G*self.Tow*self.neeta*self.A*(1 - self.alpha*(T-self.Tc )))/(1000*60)
        #print(solar_energy)
        return solar_energy

    def step(self):
        self.energy_E = self.calculateSolarEnergy()
  
#_________________________________________________________________________________  WEATHER _______________________________

class WeatherAgent(Agent): # weather condition, outdoor temperature,solar irradiance 
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        
        self.outdoorTempList = Weather_Data['Temp']
        self.outLightList = Weather_Data['Radiation']
        
    #Updata temperature values in every 5 minutes
    def getOutdoorTemp(self):
        self.Temp = 273.15 + self.outdoorTempList[self.model.schedule.steps]
        return self.Temp 
    
    #Updata irradiance values in every 5 minutes
    def getOutdoorLight(self): 
        return self.outLightList[self.model.schedule.steps]    
            
    def step(self):
        
        self.outLight = self.getOutdoorLight()
        self.outdoorTemp = self.getOutdoorTemp()

#_________________________________________________________________________________  EV  _______________________________
class EV_Agent(Agent):

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.actual_speed_list= EV_Data[f'CAR-{unique_id}']         #Read list of EVs' speed values
        self.accleration_list = EV_Data[f'Accleration-{unique_id}'] #Read list of EVs' accleration values
        self.availability_list = EV_Data[f'{unique_id}-available']  #Read list of EVs' availability values
        self.availability = 0
        
#Update EVs' accleration values every 5 minutes
    def getAccleration(self):
        self.accleration1 = self.accleration_list[self.model.schedule.steps]
        return  self.accleration1
        
#Update EVs' availability in the university(working hours) every 5 minutes       
    def getAvailability(self):
        return self.availability_list[self.model.schedule.steps]
      
#Update EVs' speed values every 5 minutes       
    def getSpeed(self):
        self.Actual_speed1 = self.actual_speed_list[self.model.schedule.steps]
        return  self.Actual_speed1    
     
    def Energy(self): #Calculate/Update Energy consumption of each EVs
        
   
        self.Actual_speed1 = self.actual_speed_list[self.model.schedule.steps]
        self.accleration1 = self.accleration_list[self.model.schedule.steps]
        
        self.AuxiliaryPower =300
        self.alpha_regeneration = 0.4
       
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
    
        self.Powerusage = 0.277*self.R_Force*self.Actual_speed1
        
        self.power_train_eff = 0.96
        self.Power_Traction = self.Powerusage/self.power_train_eff
        self.Power_Braking = self.alpha_regeneration*self.Powerusage
     
            
        if self.availability!= 1 and self.Actual_speed1 == 0:
                
            self.Battery_Power = self.Power_Traction + -1*self.Power_Braking
            
        elif self.availability == 1 and self.Actual_speed1 == 0:
                
            self.Battery_Power = 0
                
        else:
                
            self.Battery_Power =  (self.Power_Traction + self.AuxiliaryPower +-1*self.Power_Braking)*5/60
            self.Battery_Energy = self.Battery_Power*5/60
        
        return self.Battery_Power
           
     def carSOC(self):#Read the SOC value of EVs' from charging control agent
       
         cellmates = self.model.grid.get_cell_list_contents ([self.pos])
         chargingcontrolagent = cellmates[1]

         self.SOC_value = chargingcontrolagent.SoC()
   
         return self.SOC_value

    def Total_car_Energy(self):#Read the charging energy value of EVs' from charging control agent
        cellmates = self.model.grid.get_cell_list_contents ([self.pos])
        chargingcontrolagent = cellmates[1]

        self.totalcarenergy  = chargingcontrolagent.Charging_control() 
        
        return self.totalcarenergy      
    def step(self):
       
        
        self.speed = self.getSpeed()
        self.accleration = self.getAccleration()
        self.availability  = self.getAvailability()
        self.Energyconsumed = self.Energy()
        #self.stateofcharge = self.carSOC()
        self.carE = self.Total_car_Energy()

#_________________________________________________________________________________  Utility_Grid  _______________________________

class Utility_Grid(Agent):#It is a unlimited energy resourse - return grid supply and injected energy values

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

    def Grid_Power(self):#Read the Grid supply and inject energy value from main control agent

        
        all_maincontrol_agents_in_grid = self.model.schedule.getAllAgentsListByClass(Main_Control_Agent)
        
        for mca in all_maincontrol_agents_in_grid:
            self.grid_power =  mca.powervalue[4]
        
        return self.grid_power

    def step(self):
        self.gridP = self.Grid_Power()


#_________________________________________________________________________________  Battery_Storage  _______________________________
 ###I use 20kWh battery storage capacity, 10kW maximum power limit, capital cost = €398/kWh, Nominal Voltage = 51.2 and Nominal capacity = 400Ah###

class Battery_Storage(Agent):#Update BS's charging and discharing energy and it's SOC values

    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

        self.battery_storage_cap = 20000#kwh
        
        self.s = 0
        self.daylist = [-1];
        self.lifecycle_list = [1571.56];
        
    def battery_power(self):#Read Battery charging and discharging energy from main control agent
        all_maincontrol_agents_in_grid = self.model.schedule.getAllAgentsListByClass(Main_Control_Agent)
        
        for mca in all_maincontrol_agents_in_grid:
            self.Batteryenergy =  mca.powervalue[5]
            
        return self.Batteryenergy

    def battery_SOC(self):#Calculate/Update BS's SOC value based on BS's charging and discharging energy
        self.daylist.append(self.model.day)
        
        if self.daylist[self.s-1] == -1:
            self.batterySOC = 0.5

        else:

            soc = -1000*self.Batteryenergy /(self.battery_storage_cap)  
            
            self.batterySOC += soc
        print("Battsoc:{}".format(self.batterySOC))
        return round(self.batterySOC,2)
        
    def degradation_cost(self):#Calculate BS's degradation cost as per the lifecycle and DOD.
    
        self.daylist.append(self.model.day)
        capital_cost = 100000

        
        if self.daylist[self.s-1] == -1:
            
            DOD = 0.5
            self.SOH = 0.000636
            
        else:
            
            DOD = 1-self.batterySOC
            self.life_cycle = -1808*np.log(DOD*100)+8644.5
 
            
            self.lifecycle_list.append(self.life_cycle)
 
            
            self.SOH = -1*(1/self.lifecycle_list[self.s-2]) + 1/self.life_cycle
            
            
        self.battcost = capital_cost *self.SOH
        
        print(self.SOH,self.battcost)
        
        return self.SOH
          
    def step(self):
        self.s += 1
        self.Batteryenergy = self.battery_power()
        self.batterysoc = self.battery_SOC()
        self.cost = self.degradation_cost()
                                                                                                                                                                  
#_________________________________________________________________________________  Charge_pole  _______________________________

class Charge_pole(Agent):#ADD as dummy agent for future development 
 
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        
    def step(self):
        pass

#__________________________________________________________  Charging_Control_Agent  _______________________________ 
###It reads solar panel agent energy, EV agent energy consumption and calculate/update charging energy as per the charging control###
class Charging_Control_Agent(Agent):#Each CCA controls the EV agents' charging scenario
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)

  
        self.option = self.model.Flat_Charging_structure
        self.pricing = self.model.price_structure
        self.TOU_Charging = self.model.TOU_Charging_structure
       
        self.daylist = [-1];
        self.s = 0
        self.SOC_value = 1

        self.actual_speed_list= EV_Data[f'CAR-{unique_id}']
        self.accleration_list = EV_Data[f'Accleration-{unique_id}']
        self.availability_list = EV_Data[f'{unique_id}-available']

        self.E0 = 2300*5/60
        self.E1 = 6600*5/60
        self.E2 = 30000*5/60
        
    def EV_data(self):#Read EV agent energy consumption
   
        cellmates = self.model.grid.get_cell_list_contents ([self.pos])
        evagent = cellmates[0]
        self.energy = evagent.Energy()
        return self.energy
         
    def Solar_Data(self):#Read solar energy generation
        all_SOLAR_agents_in_grid = self.model.schedule.getAllAgentsListByClass(SolarPanelAgent)
        
        for solar in all_SOLAR_agents_in_grid:
            self.solar_energy = solar.calculateSolarEnergy()
       
        return self.solar_energy

    def SoC(self):#calculate/Update EVs' SOC as per the energy consumption
        
        
        self.Opencircuit_Voltage = 312.96
        self.Battery_Resistance = 0.096
        self.initial_current_capacity = 119.6
        
        self.daylist.append(self.model.day)
        
        #for ev in all_EV_agents_in_grid:   
        i = (self.Opencircuit_Voltage - ((self.Opencircuit_Voltage)**2 - 4*self.Battery_Resistance*self.Power*1000 )**0.5)*0.5/self.Battery_Resistance
        value = i/(self.initial_current_capacity)
        
        #Update SOC value of EV as 1 in every start of the day otherthan that,calculate SOC w.r.t value
        if self.daylist[self.s-1] != self.model.day:

            self.SOC_value = 1
         
        else:
            self.SOC_value = self.SOC_value + -1*value
   
        #print(self.SOC_value)
        return self.SOC_value 
        
    def Charging_control(self):#Calculate/Update charging energy as per the charging option
        
        cellmates = self.model.grid.get_cell_list_contents ([self.pos])
        evagent = cellmates[0]
        self.availability = evagent.getAvailability()
        
        '''If car start to charge in UNCONTROLLED CHARGING PATTERN - whenever car stops in the faculty it charge
        the car until SOC reach to 1 or disconnection/return to home'''
        
        if self.pricing == "FLAT":
            if self.option == "uncontrolled":    
                    
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                        
                        if self.SOC_value < 1:
                            self.PP = -1*self.E1 +  self.energy
                                    
                        else:
                            self.PP =  self.energy
                                            
                    else:
                        self.PP =  self.energy
                                    
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    
                    self.PP =  self.energy
                            
                self.Power=self.PP/1000       
                
                #if car choose V2G controlled charging - when SOC less than 0.5, it immediately charge in fast charging mode to reach to 0.5,
                #then it charge until SOC = 0.8 afterwards  it is in V2G mode 
            
            elif self.option  == "V2G":    
                    
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                        if self.SOC_value <= 0.5:
                            self.PP = -1*self.E2 +  self.energy
                            #print("SoC less than 50% recharge to 0.5")
                                              
                        elif  0.5< round(self.SOC_value,2) < 0.80:
                            self.PP = -1*self.E1 +  self.energy
                            #print("It's controlled charging - V2G")
                                    
                        elif  0.8 <= round(self.SOC_value,2) < 0.82:
                            self.PP =   self.energy
                                    
                        else:
                            self.PP = self.E1 +  self.energy
                            #print("It's controlled charging - V2G")
                    else:
                        self.PP =  self.energy
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    self.PP =  self.energy
                                
                    # print(round(self.SOC_value,1))    
                self.Power = self.PP/1000
            
            #if car choose G2V controlled charging - when SOC is in 0.5 it immediately charge in fast charging mode to reach to 0.5,
            #then it charge by average charging mode
                
            elif self.option  == "G2V":     
          
                     
                if 8 <= self.model.hour <= 17:
                    # print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                                    
                        if self.SOC_value <= 0.5:
                            self.PP = -1*self.E2 + self.energy
                            #print("SoC less than 50% recharge to 0.5")
                                              
                        elif  0.5< self.SOC_value <= 1.0:
                            self.PP = -self.E1 + self.energy
                            #print("It's controlled charging - G2V")
                                            
                        else:
                            self.PP =  self.energy
                                            
                    else:
                        self.PP =  self.energy
                                    
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    self.PP =  self.energy
                self.Power = self.PP/1000
            
            #if car choose G2V slow charging - when SOC is in 0.5 it immediately charge in fast charging mode to reach to 0.5,
            #then it charge by slow charging mode
            else:     
                        
                    if 8 <= self.model.hour <= 17:
                        # print("Charge Pole is Available - U Can Charge..!!!")
                                        
                        if self.availability == 1:
                                        
                            if self.SOC_value <= 0.5:
                                self.PP = -1*self.E2 + self.energy
                                #print("SoC less than 50% recharge to 0.5")
                                                  
                            elif  0.5< self.SOC_value <= 1.0:
                                self.PP = -self.E0 + self.energy
                                #print("It's controlled charging - G2V")
                                                
                            else:
                                self.PP =  self.energy
                                                
                        else:
                            self.PP =  self.energy
                                        
                    else:
                        #print("Charge Pole is not available....SORRY.....!!!")
                        self.PP =  self.energy
                    self.Power = self.PP/1000
            
        #TOU - Charging, It has three mode of charging as slow, average and fast charging
        else:
            if self.TOU_Charging == 'Slow':
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                        
                        if self.SOC_value < 1:
                            self.PP = -self.E0 + self.energy
                                    
                        else:
                            self.PP =  self.energy
                                            
                    else:
                        self.PP =  self.energy
                                    
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    
                    self.PP =  self.energy
             
                
            elif self.TOU_Charging == 'Average':
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                        
                        if self.SOC_value < 1:
                            self.PP = -self.E1 + self.energy
                                    
                        else:
                            self.PP =  self.energy
                                            
                    else:
                        self.PP =  self.energy
                                    
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    
                    self.PP =  self.energy
               
            else:
                
                if 8 <= self.model.hour <= 17:
                    #print("Charge Pole is Available - U Can Charge..!!!")
                                    
                    if self.availability == 1:
                        
                        if self.SOC_value < 1:
                            self.PP = -self.E2 + self.energy
                                    
                        else:
                            self.PP =  self.energy
                                            
                    else:
                        self.PP =  self.energy
                                    
                else:
                    #print("Charge Pole is not available....SORRY.....!!!")
                    
                    self.PP =  self.energy
            self.Power = self.PP/1000
        #print( 'self.Power:{}'.format(self.Power)) 
        return  self.Power
   

    def step(self):
    
        self.s += 1
        
        self.EV_data()
        self.Solar_Data()
    
        self.controlvalue = self.Charging_control()
        self.stateofcharge = self.SoC()
        
   
  #_________________________________________________________________________________  Main_Control_Agent  _______________________________  
class Main_Control_Agent(Agent):#Its like a processor of the system, calculate aggregated EVs energy consumption and calculate cost value
    def __init__(self,unique_id, model):
        super().__init__(unique_id, model)
        self.daylist = [-1];
        self.s = 0
       
        self.lifecycle_list = [1571.56];
        self.batterySOCvalue = 0.5
        self.Gridenergy = 0
        self.grid_injected_price = 0
        self.grid_price = 0

        self.total_demand = 0

        self.totalbatteryenergy = 0
        self.totalgridenergy = 0

        self.totalEVchargingprice = 0
        self.totalCEBEVchargingprice = 0
        self.totalGridprice = 0
        self.totaolgridinjectedprice = 0

        self.Grid_Injected_energy = 0
        self.Grid_Consumed_energy = 0
        self.Battery_Charging_Energy = 0
        self.Battery_Discharging_Energy = 0

        self.needthansolar = 0
        self.balancefromsolar = 0

        self.Batteryenergy1 = 0
        self.Batteryenergy2 = 0
        self.Gridenergy1 = 0
        self.Gridenergy2 = 0
        
        self.Batteryenergy = 0
        self.Gridenergy = 0

        self.option = self.model.Flat_Charging_structure
        self.pricing = self.model.price_structure
        self.TOU_Charging = self.model.TOU_Charging_structure

    def Car_Total_demand(self):#Calculate aggregated EVs' energy consumption
        self.total = 0
        self.total1 = 0
        self.Delta = 0
        self.deltalist = []

        all_chargingcontrol_agents_in_grid = self.model.schedule.getAllAgentsListByClass(Charging_Control_Agent)
        for cca in all_chargingcontrol_agents_in_grid:
            self.p = cca.EV_data()
            self.P = cca.Charging_control()
            
            self.total =self.p/1000
            self.total1 =self.P
            self.Delta += -1*(self.total1 - self.total)
            self.deltalist.append(self.Delta)
            #print(self.Delta)
        return self.Delta    
        
    def power_management(self):#Calculate/Update energy value based on energy management algorithm.
         '''It has two charging scenarios as SOC based and TOU tariff based. SOC based charging has a flat tariff system. 
         Which has Uncontrolled,V2G,G2V and G2V-slow charging scenarios.TOU tariff based charging has timly based cost value.
         Which has slow, Average and Fast charging scenarios.'''
          
        SOC_max_value = 0.79
        SOC_min_value = 0.21
        self.price =0
        self.price2 =0
        battery_max_power_limit = (10000)*5/(60)
        self.battery_storage_cap = 20000
       
        self.daylist.append(self.model.day)
        capital_cost = 100000
        
        all_SOLAR_agents_in_grid = self.model.schedule.getAllAgentsListByClass(SolarPanelAgent)
        
        for solar in all_SOLAR_agents_in_grid:
            self.solar_energy = solar.calculateSolarEnergy()

        delta= self.solar_energy - self.Delta
        
        #Solar Energy Value
        if delta <= 0:
                
            self.needthansolar += delta
            
        else:
            self.balancefromsolar += delta 


        '''Grid_Injected Price'''
        self.Grid_Injected_Price = 22
        
        '''Grid_Price'''
        if 18 < self.model.hour < 22:
            self.Grid_Price = 23.50
                 
        elif 5 <   self.model.hour <= 18:
            self.Grid_Price = 10.25
         
        else:
            self.Grid_Price = 5.90
        
        '''EV_Charging_Price'''
        if self.TOU_Charging == 'Slow':
            if 18 < self.model.hour < 22:
                self.EV_Price = 15
               
            elif 5 <   self.model.hour <= 18:
                self.EV_Price = 7
       
            else:
                self.EV_Price = 6
             
        elif self.TOU_Charging == 'Average':
            if 18 < self.model.hour < 22:
                self.EV_Price = 18
                
            elif 5 <   self.model.hour < 18:
                self.EV_Price = 9
               
            else:
                self.EV_Price = 8 
        else:
            if 18 < self.model.hour < 22:
                self.EV_Price = 21
               
            elif 5 <   self.model.hour <= 18:
                self.EV_Price = 10
               
            else:
                self.EV_Price = 9

        #CEB_EV_Price       
        if self.TOU_Charging == 'Slow':
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 54
               
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 25
       
            else:
                self.CEB_EV_Price = 13
             
        elif self.TOU_Charging == 'Average':
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 55
                
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 30
               
            else:
                self.CEB_EV_Price = 20 
        else:
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 70
               
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 50
               
            else:
         
                self.CEB_EV_Price = 30
       
        
        if self.daylist[self.s-1] == -1:
            
   
            self.SOH = 0
        else:
            
            DOD = 1-self.batterySOCvalue
      
            self.life_cycle = -1808*np.log(DOD*100)+8644.5
          
            self.lifecycle_list.append(self.life_cycle)
    
            
            self.SOH = -1*(1/self.lifecycle_list[self.s-2]) + 1/self.life_cycle
            
        self.battcost = capital_cost *self.SOH
        if self.battcost <0:
            self.battcost = self.Grid_Price+10
        else:
            self.battcost = self.battcost
           
        print("soh from MCA:{}".format(self.battcost))
        #Pricing
        if self.pricing == "FLAT":
        
            self.EVp = 10
            self.price = self.EVp*self.Delta
            self.price2   =  self.Delta*self.CEB_EV_Price

            delta= 1000*(self.solar_energy - self.Delta )
            if delta <= 0:#Grid is discharging + 0
                if self.batterySOCvalue <= SOC_min_value:
                        
                    self.Batteryenergy = 0
                    self.Batteryenergy1= self.Batteryenergy
                    self.Gridenergy1 = -1*(delta+ self.Batteryenergy1)       
                else:
                        
                    if delta < -1*battery_max_power_limit:#Battery is Discharging balance is discharged by grid + +
                        self.Batteryenergy = battery_max_power_limit
                        self.Batteryenergy1= self.Batteryenergy
                        self.Gridenergy1 = -1*(delta+ self.Batteryenergy1)     
                                
                    else:#Battery is Discharging + 0
                        self.Batteryenergy = -1*delta
                        self.Batteryenergy1= self.Batteryenergy
                        self.Gridenergy1 = 0     
                                
            else:#Grid is charging - 0
                if self.batterySOCvalue >= SOC_max_value:
                    self.Batteryenergy = 0
                    self.Batteryenergy2 = self.Batteryenergy
                    self.Gridenergy2 = -1*(delta+ self.Batteryenergy2)
                    
                else:#Battery is charging and balance is injected to grid - -
                    if delta > battery_max_power_limit:
                        self.Batteryenergy = -1*battery_max_power_limit
                        self.Batteryenergy2 = self.Batteryenergy
                        self.Gridenergy2 = -1*(delta+ self.Batteryenergy2)
                        
                    else:
                        self.Batteryenergy = -1*delta
                        self.Batteryenergy2 = self.Batteryenergy
                        self.Gridenergy2 = -1*(delta+ self.Batteryenergy2)
                        
            self.Gridenergy = -1*(delta+ self.Batteryenergy)
            #print([ self.Gridenergy/1000,     self.Batteryenergy/1000])
          
            self.grid_price = self.Gridenergy1*self.Grid_Price/1000
            self.grid_injected_price = self.Gridenergy2*self.Grid_Price/1000

        #print([ self.Gridenergy/1000,     self.Batteryenergy/1000])

        ##############TOU#################
        else:
        
          
            if self.Delta > self.solar_energy:
                self.grid_injected_price = 0
                self.price = self.solar_energy*self.EV_Price
                #self.price2= self.chargePower*self.CEB_EV_Price/1000
                #print(self.price)
                print("charged by solar")
                delta = 1000*(self.Delta - self.solar_energy) 
                
                print("Over Load")
                
                #Total EV demand isn't full
                if self.Grid_Price < self.battcost: #G2EV-Grid is Discharging +
                    self.Gridenergy = delta
                    self.price = delta*self.CEB_EV_Price/1000
                    #self.price2 = self.chargePower*self.CEB_EV_Price/1000

                    self.grid_price = self.Gridenergy*self.Grid_Price/1000
           
                    print("G2EV-grid price is low")
                    if  self.Grid_Price < self.EV_Price:
                    
                        if self.batterySOCvalue <= SOC_max_value:#G2BSS
                            self.Batteryenergy = -1*battery_max_power_limit
                            self.Gridenergy = battery_max_power_limit
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            print("G2BSS")
                        else:
                            self.Batteryenergy = 0
                            self.Gridenergy  = 0
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                    else:
                        self.Batteryenergy = 0
                        self.Gridenergy  = 0
                        self.grid_price = self.Gridenergy*self.Grid_Price/1000
                else:
                    if self.batterySOCvalue <= SOC_min_value: #Can't charge by BSS G2EV - Grid is discharging +
                        self.Gridenergy =  delta
                        self.Batteryenergy = 0
                        
                        self.price = delta*self.CEB_EV_Price/1000
                        #self.price2 = self.chargePower*self.CEB_EV_Price/1000

                        self.grid_price = self.Gridenergy*self.Grid_Price/1000

                        print("G2EV")
                        
                        
                    else:
                        delta = 1000*(self.Delta - self.solar_energy)
                        if delta < self.batterySOCvalue*self.battery_storage_cap:#BSS2EV****************************
                            if self.batterySOCvalue > SOC_min_value:

                                if delta <= battery_max_power_limit:

                                    self.Batteryenergy = delta
                                    self.Gridenergy = 0
                                    
                                    print("BSS2EV")
                                    self.price = self.Batteryenergy*self.battcost/1000
                                # self.price2 = self.chargePower*self.CEB_EV_Price/1000
                                    self.grid_price = self.Gridenergy*self.Grid_Price/1000
                                else:
                                    self.Batteryenergy = battery_max_power_limit
                                    self.Gridenergy = delta - self.Batteryenergy
                                    
                                    print("BSS2EV+G2EV-delta <= battery_max_power_limit")
                                    self.price = self.Batteryenergy*self.battcost/1000 +  self.Gridenergy*self.CEB_EV_Price/1000
                                # self.price2 = self.chargePower*self.CEB_EV_Price/1000
                                    self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            else:
                                self.Gridenergy = delta - self.Batteryenergy
                                self.Batteryenergy = 0

                                self.price = delta*self.CEB_EV_Price/1000
                                #self.price2 = self.chargePower*self.CEB_EV_Price/1000
                                self.grid_price = self.Gridenergy*self.Grid_Price/1000
                                print("G2EV-after battery finished")
                            
                        else:#BSS2EV
                            self.Batteryenergy = battery_max_power_limit
                            self.Gridenergy = 0
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            print("BSS2EV-delta<totalbattenergy")
                            self.price = self.Batteryenergy*self.battcost/1000
                            
                                   
                '''Under Load'''
            elif (self.Delta >0 and self.Delta <= self.solar_energy*1000):
                print("Under Load")
                delta = -1000*(self.Delta - self.solar_energy)
                
                self.price = delta*self.EV_Price/1000
                #self.price2 = self.chargePower*self.CEB_EV_Price/1000
                    
                
                
                
                if self.batterySOCvalue <= SOC_max_value:
                
                    if delta < battery_max_power_limit:#PV2BSS- Battery is charging -
                       
                        
                        if self.Grid_Price < self.EV_Price:#G2BSS - Grid is discharging and battery is charging
                            self.Batteryenergy = -battery_max_power_limit
                            self.Gridenergy = battery_max_power_limit
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            self.grid_injected_price = 0
                            print("G2BSS")
                        else:
                            self.Batteryenergy = -delta
                            self.Gridenergy = 0
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            self.grid_injected_price = 0
                            print("PV2BSS")
                    else:#PV2BSS -BSS is charging then remaining Power is in PV2G - Grid is charging -  
                        self.Batteryenergy = -1*battery_max_power_limit
                        self.Gridenergy = -1*(delta - battery_max_power_limit )
                        self.grid_injected_price = (delta - battery_max_power_limit )*self.Grid_Injected_Price/1000
                        self.grid_price = 0
                        print("PV2BSS")
                else:#PV2G
                    self.Batteryenergy = 0
                    self.Gridenergy = -1*delta
                    self.grid_injected_price = delta*self.Grid_Injected_Price/1000
                    self.grid_price = 0
                    print("PV2G")
                
                '''No Load''' 
            elif(self.Delta ==0 and self.solar_energy*1000>0):
                self.price = delta*self.EV_Price/1000
                print("NoLoad")
                if self.batterySOCvalue <= SOC_max_value:
                
                    if self.solar_energy*1000 > battery_max_power_limit:
                        #PV2BSS - BSS is charging -
                        print("PV2BSS")
                        self.Batteryenergy =  -1*battery_max_power_limit
                        self.Gridenergy = -1*(self.solar_energy*1000- -1*self.Batteryenergy )   #PV2G
                        self.grid_injected_price = (self.solar_energy*1000- -1*self.Batteryenergy )*self.Grid_Injected_Price/1000
                        self.grid_price = 0
                    else:#PV2BSS
                        
                        
                        if self.Grid_Price < self.EV_Price:#G2BSS
                            self.Batteryenergy =  -battery_max_power_limit
                            self.Gridenergy = battery_max_power_limit 
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            self.grid_injected_price = 0
                            print("noload-g2bss")
                        else:
                            self.Batteryenergy =  -1*self.solar_energy*1000
                            self.Gridenergy = 0
                            self.grid_price = self.Gridenergy*self.Grid_Price/1000
                            self.grid_injected_price = 0
                else:#PV2G
                    self.Batteryenergy =  0
                    self.Gridenergy = -1*self.solar_energy*1000
                    self.grid_injected_price = self.solar_energy*self.Grid_Injected_Price
                    self.grid_price = 0
            else:   
                print("Noload and noPV") 
                self.price = delta*self.EV_Price/1000    
                if self.Grid_Price < self.EV_Price:
                    if self.batterySOCvalue <= SOC_max_value:
                        self.Batteryenergy =  -battery_max_power_limit
                        self.Gridenergy = battery_max_power_limit
                        self.grid_price = self.Gridenergy*self.Grid_Price/1000
                        self.grid_injected_price = 0
                        print("offpeakcharging")

                    else:
                        self.Batteryenergy =  0
                        self.Gridenergy = 0 
                        self.grid_price = self.Gridenergy*self.Grid_Price/1000
                        self.grid_injected_price = 0
                else:
                    self.Batteryenergy =  0
                    self.Gridenergy = 0
                    self.grid_price = self.Gridenergy*self.Grid_Price/1000
                    self.grid_injected_price = 0
  
            self.price2   =  self.Delta*self.CEB_EV_Price
        self.Price = round(self.price,2)

        self.value = [self.Price,self.price2 ,self.grid_price, self.grid_injected_price,self.Gridenergy/1000,self.Batteryenergy/1000]
        print(self.value)
        print("Total need than Solar Supply in kWh: {}".format(round(self.needthansolar,2)))
        print("Total balance from Solar Supply in kWh: {}".format(round(self.balancefromsolar,2))) 

        return self.value
    

    def Batt_SOC_Read(self):#Calculate/Update BS's SOC value as per battery charging and discharging energy

        self.battery_storage_cap = 20000
        self.daylist.append(self.model.day)
        
        if self.daylist[self.s-1] == -1:
            self.batterySOCvalue = 0.5

        else:

            soc = -1000*self.value[5] /(self.battery_storage_cap)  
            print("MCAsocvalue{},{}".format(self.value[5],soc))
            self.batterySOCvalue  += soc
        print("battsocfromMCA:{}".format(self.batterySOCvalue))
        return self.batterySOCvalue
        


    def price_value(self):#Unit price value for charging
        '''Grid_Injected Price'''
        self.Grid_Injected_Price = 22
        
        '''Grid_Price'''
        if 18 < self.model.hour < 22:
            self.Grid_Price = 23.50
                 
        elif 5 <   self.model.hour <= 18:
            self.Grid_Price = 10.25
         
        else:
            self.Grid_Price = 5.90
        
        '''EV_Charging_Price'''
        if self.TOU_Charging == 'Slow':
            if 18 < self.model.hour < 22:
                self.EV_Price = 15
               
            elif 5 <   self.model.hour <= 18:
                self.EV_Price = 7
       
            else:
                self.EV_Price = 6
             
        elif self.TOU_Charging == 'Average':
            if 18 < self.model.hour < 22:
                self.EV_Price = 18
                
            elif 5 <   self.model.hour < 18:
                self.EV_Price = 9
               
            else:
                self.EV_Price = 8 
        else:
            if 18 < self.model.hour < 22:
                self.EV_Price = 21
               
            elif 5 <   self.model.hour <= 18:
                self.EV_Price = 10
               
            else:
                self.EV_Price = 9

        #CEB_EV_Price       
        if self.TOU_Charging == 'Slow':
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 54
               
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 25
       
            else:
                self.CEB_EV_Price = 13
             
        elif self.TOU_Charging == 'Average':
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 55
                
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 30
               
            else:
                self.CEB_EV_Price = 20 
        else:
            if 18 < self.model.hour < 22:
                self.CEB_EV_Price = 70
               
            elif 5 <   self.model.hour <= 18:
                self.CEB_EV_Price = 50
               
            else:
                self.CEB_EV_Price = 30

        return [self.Grid_Injected_Price, self.CEB_EV_Price, self.EV_Price, self.Grid_Price ]  

    def Total_Energy(self):
        self.gridenergy = self.value[4]
        self.batteryenergy = self.value[5]

        self.totalgridenergy += self.gridenergy
        self.totalbatteryenergy += self.batteryenergy

        #Grid energy
        if self.gridenergy <= 0:
            self.Grid_Injected_energy += self.gridenergy

        else:
            self.Grid_Consumed_energy += self.gridenergy

        #Battery energy
        if self.batteryenergy <= 0:
                
            self.Battery_Charging_Energy += self.batteryenergy

        else:
                
            self.Battery_Discharging_Energy += self.batteryenergy


        self.total_demand += self.Delta
        print("Total demand Energy in kWh: {}".format(round(self.total_demand,2)))

        energy = [self.totalgridenergy,self.totalbatteryenergy]
        print("Net Grid and Battery energy :{}".format(energy))

        print("Total Grid Consumed energy in kWh: {}".format(round(self.Grid_Consumed_energy,2)))
        print("Total Grid Injected energy in kWh: {}".format(round(self.Grid_Injected_energy,2)))
        print("Total Battery Charging energy in kWh: {}".format(round(self.Battery_Charging_Energy,2)))
        print("Total Battery Discharging energy in kWh: {}".format(round(self.Battery_Discharging_Energy,2)))
        return energy

    def Total_Price(self):#Total cost calculation
        self.EVCharging_price = self.value[0]
        self.CEBEVCharging_price = self.value[1]
        self.Gridprice = self.value[2]
        self.GridInjected_price = self.value[3]

        self.totalEVchargingprice +=self.EVCharging_price
        self.totalCEBEVchargingprice += self.CEBEVCharging_price
        self.totalGridprice += self.Gridprice
        self.totaolgridinjectedprice += self.GridInjected_price

        price = [ self.totalEVchargingprice, self.totalCEBEVchargingprice,self.totalGridprice,self.totaolgridinjectedprice]
        print("Total EV, CEB, Grid and Injected price :{}".format(price))
        return price

    def step(self):
        self.s += 1

        self.carTdemand = self.Car_Total_demand()
        self.powervalue = self.power_management()
        self.battvalueread = self.Batt_SOC_Read()
        self.price = self.price_value()
        self.totalenergy = self.Total_Energy()
        self.totalprice = self.Total_Price()
    
