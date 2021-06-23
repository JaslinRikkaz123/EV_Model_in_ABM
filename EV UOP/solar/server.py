from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from .model import ConceptModel
from .agent import SolarPanelAgent,WeatherAgent, EV_Agent,Charge_pole,Charging_Control_Agent
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
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'S1'
        portrayal["text_color"] = 'white'
                 

                 
    elif type(agent) is WeatherAgent:
      
        portrayal["Shape"] = "solar/resources/temp.png"
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'W1'
        portrayal["text_color"] = 'white'
                 
    elif type(agent) is EV_Agent:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

        color = MID_COLOR

        
        if 9<= agent.hour <=17:
            if agent.Battery_Power ==0:
                portrayal["Shape"] = "solar/resources/car.png"
                portrayal["scale"] = 1.0
                portrayal["Layer"] = 1
                portrayal["text"] = 'C1'
                portrayal["text_color"] = 'white'
            else:
                color = OPENED_CLR 
        else:
            color = CLOSED_CLR

        portrayal["Color"] = color
 
    elif type(agent) is Charge_pole:
      
        portrayal["Shape"] = "solar/resources/pole.jpg"
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'CP-1'
        portrayal["text_color"] = 'white'
        
    

        
    elif type(agent) is Charging_Control_Agent:
      
        portrayal["Shape"] = "solar/resources/control.png"
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 1
        portrayal["text"] = 'W1'
        portrayal["text_color"] = 'white'
    
        
    return portrayal
   
canvas_element = CanvasGrid(visual_portrayal, 20, 20, 800, 800)

chart_element = ChartModule(
    [{"Label": "Solar Energy (W)", "Color": "#AA0000"}]
)

chart_element2 = ChartModule(
    [{"Label": "Temperature (K)", "Color": "#666666"},{"Label": "Irradiance (W/m^2)", "Color": "#14aa00"}]
)

chart_element3 = ChartModule(
    [{"Label": "Reference_Speed (km/h)", "Color": "#666666"},{"Label": "Actual_Speed (km/h)", "Color": "#14aa00"}]
)


chart_element4 = ChartModule(
    [{"Label": "SoC", "Color": "#666666"}]
)
choice_option = UserSettableParameter('choice', 'Charge_option', value='uncontrolled',
                                              choices=['uncontrolled', 'V2G','G2V'])
server = ModularServer(
   ConceptModel, [canvas_element,chart_element,chart_element2,chart_element3,chart_element4 ], {"grid_positions": choice_option},"Energy Model" 
)

server.port = 8889
