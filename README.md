# Solar_PV_Based_EV_Charging_Station

## Summary
A model of solar PV based EV charging station in the university premises consisting of eight agent types: Weather, SOlar, EV, Main_Control, Charging_Control, Charge_Pole, Utility and Battery_Storage agents. 
EV agent operate based on the database.The charging control agent updates/calculates the requested EV charging energy in accordance with the charging option (chosen in the concept model from the visualization portrayal) and the SOC value of EVs when they park in the university car park. The main control agent reads the aggregated energy from EVs and solar energy from the Solar agent and operates the system in accordance with the energy management(EM) algorithm. Functioning as external energy sources are the utility and battery storage systems. The EMS ensures reliable operation of the system. While maximize the PV utilization, meeting the EVs demand and maximize the life of battery storage system.
The concept modeling is modeled based on SOC based charging and TOU tariff based charging.

The model is tests and demonstrates several Mesa concepts and features:
 - MultiGrid for creating shareable space for agents.
 - Multiple agent types (Weather,Solar,EV,Charging_Control,Main_Control,Charge_Pole,Utility and Battery_Storage agents)
 - DataCollector for collecting data on individual model runs.
 - Line Charts for time-series data of multiple model parameters.
 - ModularServer for visualization of agent interaction.
 - UserSettableParameters for adjusting initial model parameters
 - Agents inheriting a behavior with BaseScheduler. 
 - Writing a model composed of multiple files.
 


## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.
