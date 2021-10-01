import random
from collections import defaultdict
from mesa.time import *

class CustomBaseSheduler(BaseScheduler):
    agents_dict = defaultdict(list)
    def __init__(self,model):
        super().__init__(model)
        
        self.steps = 0
        self.time = 0
        self.agents_dict = defaultdict(list)
        
    def add(self,agent):
        self.agents.append(agent)
        
        agent_class = type(agent)
        self.agents_dict[agent_class].append(agent)
       
    def remove(self, agent):
        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_dict[agent_class]:
            self.agents_dict[agent_class].remove(agent)
            
#Get all the agent to add it in dictionary
    def getAllAgentsList(self,agent):
        if agent in self.agents_dict:
            x = self.agents_dict[agent]
            
        return x
#Solar Agent      
    def getCurrentPower(self,powerAgent):
    
        powerAgentList = self.getAllAgentsList(powerAgent)
        powerlist = [];
        for agent in powerAgentList:
            powerlist.append(round(agent.E))
        return powerlist 
        
#temperature data from weather agent     
    def getCurrentWeather(self,weatherAgent):
    
        weatherAgentList = self.getAllAgentsList(weatherAgent)
        weatherlist = [];
        for agent in weatherAgentList:
            weatherlist.append(round(agent.outdoorTemp,2))
        return weatherlist
        
#Irradinace data from weather agent      
    def getCurrentIrr(self,irradianceagent):
    
        irrAgentList = self.getAllAgentsList(irradianceagent)
        IrradianceList = [];
        for agent in irrAgentList:
            IrradianceList.append(round(agent.outLight,2))
        return IrradianceList 
         
        
    def getactualspeed(self,carAgent):
    
        supplyAgentList = self.getAllAgentsList(carAgent)
        supplylist = [];
        for agent in supplyAgentList:
            supplylist.append(agent.ActualSpeed)
            
        # print(supplylist)
        return supplylist 
        
    def getSoC(self,controlchargingAgent):
    
        supplyAgentList = self.getAllAgentsList(controlchargingAgent)
        supplylist = 0;
        for agent in supplyAgentList:
            supplylist=agent.stateofcharge
        return supplylist 

    def getcarbattery(self,controlchargingAgent):
    
        supplyAgentList = self.getAllAgentsList(controlchargingAgent)
        supplylist = 0;
        for agent in supplyAgentList:
            supplylist = agent.Control_value
        return supplylist 
    def getcarbattery_P(self,controlchargingAgent):
    
        supplyAgentList = self.getAllAgentsList(controlchargingAgent)
        supplylist = [];
        for agent in supplyAgentList:
            supplylist.append(agent.Powerconsumed)
        return supplylist 
        
    def getactualchargepower(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = 0;
        for agent in ChargepoleList:
            chargelist = agent.powervalue
        return chargelist 
        

    def getbattsoc(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.batterysoc)
        return chargelist    
        
    def getavailability(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.a)
        #print(chargelist)
        return chargelist 
#Battery_Storage
    def getbattstoragemaxP(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.max_power)
        #print(chargelist)
        return chargelist 
        
    def getbattstorageCap(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.battery_storage_cap)
        #print(chargelist)
        return chargelist 
#Charge_pole
    def getchargeL2(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.S)
        #print(chargelist)
        return chargelist
        
    def getchargeL1(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.S1)
        #print(chargelist)
        return chargelist 

    def getchargefast(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.F)
        #print(chargelist)
        return chargelist 
        
    def getCount(self, agent_class):
        return len(self.agents_dict[agent_class])
        
    def step(self):
        self.steps += 1
        self.time += 1
        for agent_class in self.agents_dict:
            agents = self.agents_dict[agent_class]
            
            for agent in agents:
                agent.step()
 #           print("Step done! \n")



