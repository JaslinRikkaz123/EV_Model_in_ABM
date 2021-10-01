from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from .model import ConceptModel
#from .agent import SolarPanelAgent,WeatherAgent, EV_Agent,Charge_pole
from .controlagent import *
from mesa.visualization.UserParam import UserSettableParameter


# Green
OPENED_CLR = "#46FF33"
# Red
CLOSED_CLR = ["#84e184", "#adebad", "#d6f5d6"]
# Blue
MID_COLOR = "#3349FF"

def visual_portrayal(agent):
   
    portrayal = {}

  
    if type(agent) is SolarPanelAgent:
        
        portrayal["Shape"] = "solar/resources/solar.jpg"
        portrayal["scale"] = 2.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'S1'
        portrayal["text_color"] = 'white'
                 

                 
    elif type(agent) is WeatherAgent:
      
        portrayal["Shape"] = "solar/resources/temp.png"
        portrayal["scale"] = 2.0
        portrayal["Layer"] = 0
        portrayal["text"] = 'W1'
        portrayal["text_color"] = 'white'
                 
    elif type(agent) is EV_Agent:
        if agent.Availability() ==1:
            #portrayal["Shape"] = "solar/resources/car.png"
            # portrayal["scale"] = 1.0
            # portrayal["Layer"] = 2
            
            portrayal = {"Shape": "circle", "Filled": "true", "r": 0.7,   "Color": "black","Layer": 0   ,"text": agent.unique_id,"text_color":'white'}
            
            
        else:
            portrayal = {"Shape": "rect", "Filled": "true",   "w":1,"h":1,   "Color": ["#84e184", "#adebad", "#d6f5d6"],"Layer": 0}

    elif type(agent) is Charge_pole:
      
        portrayal["Shape"] = "solar/resources/pole.jpg"
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 1
#portrayal["text"] = 'CP-1'
        #portrayal["text_color"] = 'white'
        
        
    elif type(agent) is Charging_Control_Agent:
      
        portrayal["Shape"] = "solar/resources/control.png"
        portrayal["scale"] = 2.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'W1'
        portrayal["text_color"] = 'white'
    
        
    return portrayal
   
canvas_element = CanvasGrid(visual_portrayal, 20, 20, 800, 800)

chart_element = ChartModule(
    [{"Label": "Solar Power (kW)", "Color": "#AA0000"}]
)

chart_element2 = ChartModule(
    [{"Label": "Temperature (K)", "Color": "#666666"},{"Label": "Irradiance (W/m^2)", "Color": "#14aa00"}]
)

chart_element3 = ChartModule(
    [{"Label": "Speed_1", "Color": "#14aa00"}, {"Label": "Speed_2", "Color": "#AA0000"}, {"Label": "Speed_3", "Color": "#0000FF"}, {"Label": "Speed_4", "Color": "#FF1493"}, {"Label": "Speed_5", "Color": "#FF8C00"}
    , {"Label": "Speed_6", "Color": "#B8860B"}, {"Label": "Speed_7", "Color": "#008080"}, {"Label": "Speed_8", "Color": "#D2691E"}, {"Label": "Speed_9", "Color": "#F4A460"}, {"Label": "Speed_10", "Color": "#FF6347"}
    , {"Label": "Speed_11", "Color": "#BA55D3"}, {"Label": "Speed_12", "Color": "#FF4500"}, {"Label": "Speed_13", "Color": "#7CFC00"}, {"Label": "Speed_14", "Color": "#00FFFF"}, {"Label": "Speed_15", "Color": "#6A5ACD"}
    , {"Label": "Speed_16", "Color": "#BBE8BB"}, {"Label": "Speed_17", "Color": "#FFFF00"}, {"Label": "Speed_18", "Color": "#F08080"}, {"Label": "Speed_19", "Color": "#00FF00"}, {"Label": "Speed_20", "Color": "#FA8072"}
    , {"Label": "Speed_21", "Color": "#800000"}, {"Label": "Speed_22", "Color": "#9BCFE5"}, {"Label": "Speed_23", "Color": "#BBD43E"}, {"Label": "Speed_24", "Color": "#888888"}, {"Label": "Speed_25", "Color": "#33C4BF"}
    , {"Label": "Speed_26", "Color": "#F5D8F5"}, {"Label": "Speed_27", "Color": "#EFC7C0"}],canvas_height=500,canvas_width=1000

)
chart_element4 = ChartModule(
    [{"Label": "SOC_1", "Color": "#14aa00"},{"Label": "SOC_2", "Color": "#AA0000"},{"Label": "SOC_3", "Color": "#0000FF"},{"Label": "SOC_4", "Color": "#FF1493"},{"Label": "SOC_5", "Color": "#FF8C00"}
    ,{"Label": "SOC_6", "Color": "#B8860B"},{"Label": "SOC_7", "Color": "#008080"},{"Label": "SOC_8", "Color": "#D2691E"},{"Label": "SOC_9", "Color": "#F4A460"},{"Label": "SOC_10", "Color": "#FF6347"}
    ,{"Label": "SOC_11", "Color": "#BA55D3"},{"Label": "SOC_12", "Color": "#FF4500"},{"Label": "SOC_13", "Color": "#7CFC00"},{"Label": "SOC_14", "Color": "#00FFFF"},{"Label": "SOC_15", "Color": "#6A5ACD"}
    ,{"Label": "SOC_16", "Color": "#BBE8BB"},{"Label": "SOC_17", "Color": "#FFFF00"},{"Label": "SOC_18", "Color": "#F08080"},{"Label": "SOC_19", "Color": "#00FF00"},{"Label": "SOC_20", "Color": "#FA8072"}
    ,{"Label": "SOC_21", "Color": "#800000"},{"Label": "SOC_22", "Color": "#9BCFE5"},{"Label": "SOC_23", "Color": "#BBD43E"},{"Label": "SOC_24", "Color": "#888888"},{"Label": "SOC_25", "Color": "#33C4BF"}
    ,{"Label": "SOC_21", "Color": "#F5D8F5"},{"Label": "SOC_27", "Color": "#EFC7C0"}],canvas_height=500,canvas_width=1000
)
chart_element5 = ChartModule(
    [{"Label": "Car_P_1", "Color": "#14aa00"}, {"Label": "Car_P_2", "Color": "#AA0000"}, {"Label": "Car_P_3", "Color": "#0000FF"}, {"Label": "Car_P_4", "Color": "#FF1493"}, {"Label": "Car_P_5", "Color": "#FF8C00"}
    , {"Label": "Car_P_6", "Color": "#B8860B"} , {"Label": "Car_P_7", "Color": "#008080"} , {"Label": "Car_P_8", "Color": "#D2691E"} , {"Label": "Car_P_9", "Color": "#F4A460"} , {"Label": "Car_P_10", "Color": "#FF6347"}
     , {"Label": "Car_P_11", "Color": "#BA55D3"} , {"Label": "Car_P_12", "Color": "#FF4500"} , {"Label": "Car_P_13", "Color": "#7CFC00"}, {"Label": "Car_P_14", "Color": "#00FFFF"}, {"Label": "Car_P_15", "Color": "#6A5ACD"}
     , {"Label": "Car_P_16", "Color": "#BBE8BB"}, {"Label": "Car_P_17", "Color": "#FFFF00"}, {"Label": "Car_P_18", "Color": "#F08080"}, {"Label": "Car_P_19", "Color": "#00FF00"}, {"Label": "Car_P_20", "Color": "#FA8072"}
     , {"Label": "Car_P_21", "Color": "#800000"}, {"Label": "Car_P_22", "Color": "#9BCFE5"}, {"Label": "Car_P_23", "Color": "#BBD43E"}, {"Label": "Car_P_24", "Color": "#888888"}, {"Label": "Car_P_25", "Color": "#33C4BF"}
     , {"Label": "Car_P_26", "Color": "#F5D8F5"}, {"Label": "Car_P_27", "Color": "#EFC7C0"}]   ,canvas_height=500,canvas_width=1000
)
chart_element6 = ChartModule(
[{"Label": "Grid_Power (kW)", "Color": "#AA0000"} ,{"Label": "Battery_Storage_Power (kW)", "Color": "#46FF33"},{"Label": "Solar Power (kW)", "Color": "#F4A460"}]
)

chart_element7 = ChartModule(
[{"Label": "Battery_SOC", "Color": "#8B008B"}]
)
choice_option = UserSettableParameter('choice', 'Charge_option', value='uncontrolled',
                                              choices = ConceptModel.grid_positions)
server = ModularServer(
   ConceptModel, [canvas_element,chart_element,chart_element2,chart_element3,chart_element4,chart_element5,chart_element6,chart_element7 ],"Energy Model",  {"grid_positions": choice_option}
)

server.port = 8889
