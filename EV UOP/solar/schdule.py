import random
from collections import defaultdict
from mesa.time import *

class CustomBaseSheduler(BaseScheduler):
    agents_dict = defaultdict(list)
    def __init__(self,model):
        super().__init__(model)

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
         
        
    def getactualspeed(self,controlAgent):
    
        supplyAgentList = self.getAllAgentsList(controlAgent)
        supplylist = [];
        for agent in supplyAgentList:
            supplylist.append(agent.ActualSpeed)
        return supplylist 
        
    def getSoC(self,controlchargingAgent):
    
        supplyAgentList = self.getAllAgentsList(controlchargingAgent)
        supplylist = [];
        for agent in supplyAgentList:
            supplylist.append(agent.stateofcharge)
        return supplylist 

    def getcarbattery(self,controlchargingAgent):
    
        supplyAgentList = self.getAllAgentsList(controlchargingAgent)
        supplylist = [];
        for agent in supplyAgentList:
            supplylist.append(agent.Control_value)
        return supplylist 
        
    def getactualchargepower(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.powervalue)
        return chargelist 
        
    def getactualgridpower(self,controlchargingAgent):
    
        ChargepoleList = self.getAllAgentsList(controlchargingAgent)
        chargelist = [];
        for agent in ChargepoleList:
            chargelist.append(agent.powervalue)
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
        return chargelist 
        
    def getCount(self, agent_class):
        return len(self.agents_dict[agent_class])
        
    def step(self):
    
        for agent_class in self.agents_dict:
            agents = self.agents_dict[agent_class]
            
            for agent in agents:
                agent.step()
 #           print("Step done! \n")
            self.steps += 1
            self.time += 1


