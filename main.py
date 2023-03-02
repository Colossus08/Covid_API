import network
import time
import urequests
from machine import Pin, I2C
import ssd1306

# connect to wifi
def wifi_connect(connection):
  connection.connect('name of wifi network', 'password of wifi network')
  while not connection.isconnected():
    print(".", end="")
    time.sleep(0.1)
  print(" Connected!")

# get data from covid api
def get(url,country):
  querystring={'country':country}
  headers={
	"X-RapidAPI-Key": "API_KEY",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
  }
  response=urequests.get(url,headers=headers)
  res=response.json()
  Country=res['response'][0]['country']
  Total_Cases=res['response'][0]['cases']['total']
  Total_Deaths=res['response'][0]['deaths']['total']
  Total_Tests=res['response'][0]['tests']['total']
  return [Country,Total_Cases,Total_Deaths,Total_Tests]

# function to show the data
def show_data():
  country=input("Enter Country's Name\n")
  url="https://covid-193.p.rapidapi.com/statistics?country="+country
  results=get(url,country)
  name_list=['Country','Cases','Deaths','Tests']
  y_value=10
  clear_data()
  for count in range(4):
    oled.text(name_list[count]+':'+str(results[count]), 0, y_value)      
    oled.show()
    y_value+=10
    time.sleep(1)

# function to clear data on oled
def clear_data():
  oled.fill(0)
  oled.show()

# --------------------------------------------------------------------

# DRIVER CODE


# connecting to wifi
print("Connecting to WiFi", end="")
connection = network.WLAN(network.STA_IF)
connection.active(True)
wifi_connect(connection)

print('Find out Covid data of various countries')

# oled code
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

con='y'
while True:
  if con=='y':
    show_data()
  else:
    clear_data()
    break
  con=input('do you want to continue?(y/n)\n')
