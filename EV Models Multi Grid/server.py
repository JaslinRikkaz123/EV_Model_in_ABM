from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import ConceptModel
from agents import *


import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


model_params = {    "height": 20, "width": 20   }
Flat_Charging_structure = ['uncontrolled', 'V2G','G2V','G2V-SC', 'TOU Charging']
TOU_Charging_structure = ['Slow','Average','Fast']
price_structure = ['TOU', 'FLAT']

def visual_portrayal(agent):
   
    portrayal = {
        'scale'         : 1.0,
        'Layer'         : 0,
        'Text'          : type(agent).__name__ +" : "+  agent.unique_id,
        'text_color'    : 'white'
    }

    if type(agent) is SolarPanelAgent:
       
        portrayal["Shape"] = "resources/solar.jpg"
        portrayal["Layer"] = 1
        
    elif type(agent) is WeatherAgent:

        portrayal["Shape"] = "resources/temp.png"
                 
    elif type(agent) is EV_Agent:
        portrayal["Layer"] = 1
        
        if agent.getAvailability() :
            portrayal["Shape"] = "resources/car.png"
        else :
            # portrayal.update({"Shape": "circle", "Color":"white", "Filled": "true", "r": 0.5})
            portrayal = {"Shape": "circle", "Color":"white", "Layer" : 0, "Filled": "true", "r": 0.5}

    elif type(agent) is Charge_pole:
        portrayal["Shape"] = "resources/pole.jpg"
        
    elif type(agent) is Charging_Control_Agent:
        portrayal = {"Shape": "circle", "Color":"white", "Layer" : 0, "Filled": "true", "r": 0.5}
        
    elif type(agent) is Main_Control_Agent:
        portrayal["Shape"] = "resources/control.png"

    elif type(agent) is Battery_Storage:
        portrayal = {"Shape": "circle", "Color":"white", "Layer" : 0, "Filled": "true", "r": 0.5}
        
    elif type(agent) is Utility_Grid:
        portrayal["Shape"] = "resources/grid.png"

    return portrayal

canvas_element = CanvasGrid(visual_portrayal, model_params['width'], model_params['height'], 500, 500)

chart_element = ChartModule(
    [{"Label": "Solar1 : Solar Energy (kWh)", "Color": "#FF8C00"}],title = "Solar Energy in kWh")

chart_element2 = ChartModule(
    [{"Label": "ws1 : Temperature (K)", "Color": "#666666"},{"Label": "ws1 : Irradiance (W/m^2)", "Color": "#14aa00"}],title = "Weather Data")

chart_element3 = ChartModule(
    [{"Label": "1 : km/h", "Color": "#AA0000"} ,{"Label": "2 : km/h", "Color": "#0000FF"}, {"Label": "3 : km/h", "Color": "#FF1493"}, {"Label": "4 : km/h", "Color": "#FF8C00"}
    , {"Label": "5 : km/h", "Color": "#B8860B"}, {"Label": "6 : km/h", "Color": "#008080"}, {"Label": "7 : km/h", "Color": "#D2691E"}, {"Label": "8 : km/h", "Color": "#F4A460"}, {"Label": "9 : km/h", "Color": "#FF6347"}
    , {"Label": "10 : km/h", "Color": "#BA55D3"}, {"Label": "11 : km/h", "Color": "#FF4500"}, {"Label": "12 : km/h", "Color": "#7CFC00"}],canvas_height=500,canvas_width=1000,title = "EV Speed in km/h")

chart_element4 = ChartModule(
    [{"Label": "1 : SOC", "Color": "#AA0000"},{"Label": "2 : SOC", "Color": "#0000FF"},{"Label": "3 : SOC", "Color": "#FF1493"},{"Label": "4 : SOC", "Color": "#FF8C00"}
    ,{"Label": "5 : SOC", "Color": "#B8860B"},{"Label": "6 : SOC", "Color": "#008080"},{"Label": "7 : SOC", "Color": "#D2691E"},{"Label": "8 : SOC", "Color": "#F4A460"},{"Label": "9 : SOC", "Color": "#FF6347"}
    ,{"Label": "10 : SOC", "Color": "#BA55D3"},{"Label": "11 : SOC", "Color": "#FF4500"},{"Label": "12 : SOC", "Color": "#7CFC00"}],canvas_height=500,canvas_width=1000,title = "EV SOC")

chart_element5 = ChartModule(
    [{"Label": "1 : kWh", "Color": "#AA0000"},{"Label": "2 : kWh", "Color": "#0000FF"},{"Label": "3 : kWh", "Color": "#FF1493"},{"Label": "4 : kWh", "Color": "#FF8C00"}
    ,{"Label": "5 : kWh", "Color": "#B8860B"},{"Label": "6 : kWh", "Color": "#008080"},{"Label": "7 : kWh", "Color": "#D2691E"},{"Label": "8 : kWh", "Color": "#F4A460"},{"Label": "9 : kWh", "Color": "#FF6347"}
    ,{"Label": "10 : kWh", "Color": "#BA55D3"},{"Label": "11 : kWh", "Color": "#FF4500"},{"Label": "12 : kWh", "Color": "#7CFC00"}] ,canvas_height=500,canvas_width=1000,title = "EV Consumed Energy in kWh")

chart_element8 = ChartModule(
    [{"Label": "MCA1 : Grid_Energy (kWh)", "Color": "#AA0000"} ,{"Label": "MCA1 : Ex.Battery_Storage_Energy (kWh)", "Color": "#46FF33"} 
    ,{"Label": "Solar1 : Solar Energy (kWh)", "Color": "#FF8C00"}],title = "Total Grid, Ex.Battery and Solar Energy in kWh ")

chart_element7 = ChartModule(
    [{"Label": "EBS1 : Ex.Battery_SOC", "Color": "#8B008B"}],canvas_height=500,canvas_width=1000,title = "External Battery SOC")

chart_element6 = ChartModule(
    [{"Label": "MCA1 : Grid_Injected_Price (rs)", "Color": "#8B008B"}, {"Label": "MCA1 : CEB_EV_Price (rs)", "Color": "#BA55D3"}, 
    {"Label": "MCA1 : EV_Price (rs)", "Color": "#FF1493"}, {"Label": "MCA1 : Grid_Price (rs)", "Color": "#F4A460"}])   

# chart_element9 = ChartModule(
#     [{"Label": "1 : rs", "Color": "#AA0000"},{"Label": "2 : rs", "Color": "#0000FF"},{"Label": "3 : rs", "Color": "#FF1493"},{"Label": "4 : rs", "Color": "#FF8C00"}
#     ,{"Label": "5 : rs", "Color": "#B8860B"},{"Label": "6 : rs", "Color": "#008080"},{"Label": "7 : rs", "Color": "#D2691E"},{"Label": "8 : rs", "Color": "#F4A460"},{"Label": "9 : rs", "Color": "#FF6347"}
#     ,{"Label": "10 : rs", "Color": "#BA55D3"},{"Label": "11 : rs", "Color": "#FF4500"},{"Label": "12 : rs", "Color": "#7CFC00"}]  ,canvas_height=500,canvas_width=1000,title = "Total Price in Rs"  )

choice_option = {"price_structure":UserSettableParameter('choice', 'Price_option', value='TOU',
                                              choices = ConceptModel.price_structure),
                "Flat_Charging_structure":UserSettableParameter('choice', 'Flat_Charge_structure', value='uncontrolled',
                                              choices = ConceptModel.Flat_Charging_structure),
                 
                 "TOU_Charging_structure":UserSettableParameter('choice', 'TOU_Charging_structure', value='Slow',
                                              choices = ConceptModel.TOU_Charging_structure)}
server = ModularServer(
   ConceptModel, [canvas_element, chart_element, chart_element2, chart_element3, chart_element4,chart_element5,chart_element7, chart_element8],"Energy Model", choice_option)


