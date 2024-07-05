''' This is a module for conversion of data files from the Eratosthenes.eu project, 
    converting it into graphs. 
    See https://eratosthenes.eu 
    Also see the challenge document at https://earthform.linnman.net/iii-eratosthenes-experiment
    '''

from math import pi, cos, sin, isnan
import pandas as pd
import matplotlib.pyplot as plt


AX = None
DIAGSIZE = 10
EARTHSIZE = 5
LINELENGTH = 100
LINEWIDTH = 0.5

def set_axis ():
    ''' Initialize the graphics engine. '''
    plt.clf ()
    # global ax
    a = plt.axes(aspect="equal")
    a.cla()
    a.set_xlim ((-DIAGSIZE,DIAGSIZE))
    a.set_ylim ((-DIAGSIZE,DIAGSIZE))
    a.set_yticklabels([])
    a.set_xticklabels([])
    return a

def ang_rad (ang_deg):
    ''' Convert degrees to radians '''
    return ang_deg / (360 / (2*pi))

def convert_to_float (data):
    ''' Extract a float value from table data '''
    return float(data.replace('[A-Za-z]', '').replace(',', '.'))

def plot_earth_circle ():
    ''' Plot a circle representing the Earth '''
    circle=plt.Circle((0,0),EARTHSIZE)
    AX.add_patch(circle)

def plot_era_lines (column_name):
    ''' Plot the lines representing various sights '''
    data = pd.read_csv("era.csv", sep=';')
    for index, row in data.iterrows():
        print (index)
        lat = convert_to_float(row['Latitude'])
        ang = convert_to_float(row[column_name])
        x_base = EARTHSIZE*cos(ang_rad(lat))
        x = [x_base,x_base+LINELENGTH*(cos(ang_rad(lat-ang)))]
        y_base = EARTHSIZE*sin(ang_rad(lat))
        y = [y_base,y_base+LINELENGTH*(sin(ang_rad(lat-ang)))]
        plt.plot (x,y, marker='o', lw = LINEWIDTH)
        r = row['Label']
        if not(isinstance(r, float) and isnan(r)):
            label_text = str(r)
            plt.text (x[0], y[0], label_text + " ", ha = "right")

def plot_flat_earth ():
    ''' Plot a graph representing a flat earth view '''
    x_base = EARTHSIZE*(pi/2)
    x = [-x_base, x_base]
    y = [0,0]
    plt.plot (x,y, marker='o')
    rect = plt.Rectangle((-x_base, 0), 2*x_base, -100, linewidth=1, edgecolor='b')
    AX.add_patch(rect)

def plot_era_flat_lines (column_name):
    ''' Plot the sight lines for a flat earth view '''
    data = pd.read_csv("era.csv", sep=';')
    for index, row in data.iterrows():
        print (index)
        lat = convert_to_float(row['Latitude'])
        ang = convert_to_float(row[column_name])
        xbase = (-lat)/(180/pi)*EARTHSIZE
        x = [xbase, xbase+LINELENGTH*(cos(ang_rad(90-ang)))]
        y = [0,           LINELENGTH*(sin(ang_rad(90-ang)))]
        r = row['Label']
        plt.plot (x,y, marker='o', lw = LINEWIDTH)
        r = row['Label']
        if not(isinstance(r, float) and isnan(r)):
            label_text = str(r)
            plt.text (x[0], y[0], label_text + " ", rotation = 270, va = "top")

AX = set_axis ()
plot_earth_circle ()
plot_era_lines ('Angle')
plt.savefig('era.png')

AX = set_axis ()
plot_earth_circle ()
plot_era_lines ('ActualAngle')
plt.savefig('era.actual.png')

AX = set_axis ()
plot_flat_earth ()
plot_era_flat_lines ('Angle')
plt.savefig('era.flat.png')

AX = set_axis ()
plot_flat_earth ()
plot_era_flat_lines ('ActualAngle')
plt.savefig('era.flat.actual.png')
