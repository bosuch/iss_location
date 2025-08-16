import turtle
import geocoder
import time
import requests
import json

def iss_current_loc():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200:
        data = json.dumps(response.json())
        output = json.loads(data)
    else:
        return response.status_code
    return output

def clear_trail():
    iss.clear()

# Set up the display
screen = turtle.Screen()
screen.setup(720, 360)
screen.setworldcoordinates(-180, -90, 180, 90)
screen.bgpic('map.gif')
screen.bgcolor("black")
screen.title("Real-time ISS tracker")

# Get the user's latitude & longitude
g = geocoder.ip('me')

if g.ok:
    # Register and display the home shape
    home_latitude, home_longitude = g.latlng
    print('Your location: {}, {}'.format(home_latitude, home_longitude))
    screen.register_shape('home.gif')
    home = turtle.Turtle()
    home.shape('home.gif')
    home.penup()
    home.goto(home_longitude, home_latitude)
    
# Register the ISS shape
screen.register_shape('station.gif')
iss = turtle.Turtle()
iss.shape('station.gif')
iss.penup()
iss.pen(pencolor="red", pensize=1)

screen.onkey(clear_trail, "space")
screen.listen()

# Main loop
while True:
    try:
        current_location = iss_current_loc()
        latitude = float(current_location['iss_position']['latitude'])
        longitude = float(current_location['iss_position']['longitude'])
        
        location_string = 'ISS location: ' + str(latitude) + ',' + str(longitude)
        print(location_string)
        screen.title(location_string)
               
        if iss.xcor() >= 178:
            iss.penup()
            iss.goto(longitude, latitude)
        else:
            iss.goto(longitude, latitude)
            iss.pendown()

    except Exception as e:
        print("Fatal error:", e)
        
    time.sleep(15)#seconds
