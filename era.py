import pandas as pd
import matplotlib.pyplot as plt
from math import pi, cos, sin, isnan

ax = None 
DIAGSIZE = 10
EARTHSIZE = 5
LINELENGTH = 100
LINEWIDTH = 0.5

def setAxis ():
    plt.clf ()
    global ax
    ax = plt.axes(aspect="equal")
    ax.cla()
    ax.set_xlim ((-DIAGSIZE,DIAGSIZE))
    ax.set_ylim ((-DIAGSIZE,DIAGSIZE))
    ax.set_yticklabels([])
    ax.set_xticklabels([])

def ang_rad (ang_deg):
    return ang_deg / (360 / (2*pi))

def convertToFloat (data):
    return float(data.replace('[A-Za-z]', '').replace(',', '.'))
    
def plotEarthCircle ():
    circle=plt.Circle((0,0),EARTHSIZE)
    ax.add_patch(circle)
    
def plotEraLines (columnName):    
    data = pd.read_csv("era.csv", sep=';')
    for index, row in data.iterrows():
        lat = convertToFloat(row['Latitude'])
        ang = convertToFloat(row[columnName])
        xBase = EARTHSIZE*cos(ang_rad(lat))
        x = [xBase,xBase+LINELENGTH*(cos(ang_rad(lat-ang)))]
        yBase = EARTHSIZE*sin(ang_rad(lat))
        y = [yBase,yBase+LINELENGTH*(sin(ang_rad(lat-ang)))]
        plt.plot (x,y, marker='o', lw = LINEWIDTH)
        r = row['Label']
        if not(isinstance(r, float) and isnan(r)):
            labelText = str(r)
            plt.text (x[0], y[0], labelText + " ", ha = "right")        

def plotFlatEarth ():
    xBase = EARTHSIZE*(pi/2)
    x = [-xBase, xBase]
    y = [0,0]
    plt.plot (x,y, marker='o')
    rect = plt.Rectangle((-xBase, 0), 2*xBase, -100, linewidth=1, edgecolor='b')
    ax.add_patch(rect)    
    
def plotEraFlatLines (columnName):
    data = pd.read_csv("era.csv", sep=';')
    for index, row in data.iterrows():
        lat = convertToFloat(row['Latitude'])
        ang = convertToFloat(row[columnName])
        xbase = ((-lat)/(180/pi)*EARTHSIZE)
        x = [xbase, xbase+LINELENGTH*(cos(ang_rad(90-ang)))]
        y = [0,           LINELENGTH*(sin(ang_rad(90-ang)))]
        r = row['Label']
        plt.plot (x,y, marker='o', lw = LINEWIDTH)
        r = row['Label']
        if not(isinstance(r, float) and isnan(r)):
            labelText = str(r)       
            plt.text (x[0], y[0], labelText + " ", rotation = 270, va = "top")

setAxis ()    
plotEarthCircle ()
plotEraLines ('Angle')  
plt.savefig('era.png')

setAxis ()    
plotEarthCircle ()
plotEraLines ('ActualAngle')  
plt.savefig('era.actual.png')

setAxis ()
plotFlatEarth ()
plotEraFlatLines ('Angle')
plt.savefig('era.flat.png')

setAxis ()
plotFlatEarth ()
plotEraFlatLines ('ActualAngle')
plt.savefig('era.flat.actual.png')



