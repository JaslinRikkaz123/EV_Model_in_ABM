from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from .model import ConceptModel
from .agent import SolarPanelAgent,WeatherAgent, EV_Agent,Charge_pole
from .controlagent import Charging_Control_Agent
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
        #print(ConceptModel.grid.position_agent().agent.pos)
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
        if agent.Availability() ==1:
            portrayal["Shape"] = "solar/resources/car.png"
            portrayal["scale"] = 1.0
            portrayal["Layer"] = 2
            portrayal["text"] = 'C1'
            portrayal["text_color"] = 'white'
            
        else:
            portrayal["Shape"] = "solar/resources/pole.jpg"
            portrayal["scale"] = 1.0
            portrayal["Layer"] = 1
            portrayal["text"] = 'CP-1'
            portrayal["text_color"] = 'white'

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
    [{"Label": "Solar Power (W)", "Color": "#AA0000"}]
)

chart_element2 = ChartModule(
    [{"Label": "Temperature (K)", "Color": "#666666"},{"Label": "Irradiance (W/m^2)", "Color": "#14aa00"}]
)

chart_element3 = ChartModule(
    [{"Label": "Actual_Speed (km/h)", "Color": "#14aa00"}, {"Label": "Actual_Speed_2 (km/h)", "Color": "#AA0000"}]
)

chart_element4 = ChartModule(
    [{"Label": "SOC_CAR_1", "Color": "#14aa00"},{"Label": "SOC_CAR_2", "Color": "#AA0000"},{"Label": "Battery_SOC", "Color": "#DDA0DD"}]
)
chart_element5 = ChartModule(
    [{"Label": "Car Battery Power(W)", "Color": "#14aa00"}, {"Label": "Car Battery Power_2(W)", "Color": "#AA0000"}]   
)
chart_element6 = ChartModule(
[{"Label": "Grid_Power (W)", "Color": "#AA0000"} ,{"Label": "CP_Battery_Power (W)", "Color": "#46FF33"}]
)

chart_element7 = ChartModule(
[{"Label": "Availability_1", "Color": "#AA0000"} ,{"Label": "Availability_2", "Color": "#46FF33"}]
)
choice_option = UserSettableParameter('choice', 'Charge_option', value='uncontrolled',
                                              choices = ConceptModel.grid_positions)
server = ModularServer(
   ConceptModel, [canvas_element,chart_element,chart_element2,chart_element3,chart_element4,chart_element5,chart_element6 ],"Energy Model",  {"grid_positions": choice_option}
)

server.port = 8889
