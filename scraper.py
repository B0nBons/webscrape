import requests
from bs4 import BeautifulSoup
import re
import time
import warnings

# Stop future warning
warnings.simplefilter(action='ignore', category=FutureWarning)

# Create a program to store the outside temperature, the daily high, and daily low, every hour. 

time_elapse = 0
URL = "https://forecast.weather.gov/MapClick.php?lat=39.6127&lon=-105.0162"

while time_elapse <= 2880:

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # <p class="myforecast-current-lrg">50°F</p>
    current_temp = soup.find_all('p', {'class':"myforecast-current-lrg"}, recursive=True)
    # <p class="temp temp-high">High: 51 °F</p>
    current_high = soup.find('p', {'class':"temp temp-high"})
    # <p class="temp temp-low">Low: 19 °F</p>
    current_low = soup.find('p', {'class': "temp temp-low"})

    # Now, remove the HTML from the outputs of current_temp,high, and low
    temp = str(current_temp)
    low = str(current_low)
    high = str(current_high)

    temp = temp.strip(">").strip("<")
    low = low.strip(">").strip("<")
    high = high.strip(">").strip("<")

    # Remove random html from the str of current temp
    rem = ['[<p' , 'class="myforecast', ">", "<", "-", "u", "n", "g", "/"]
    pattern = '[' +  ''.join(rem) +  ']'
    temp = re.sub(pattern, '', temp) 
    temp += "F Currently"
    temp = temp.strip()

    # Remove html from str of low
    rem = ['class="temp temp', "Low:", "/", ">", "<"]
    pattern = '[' +  ''.join(rem) +  ']'
    low = re.sub(pattern, '', low) 
    low = "-" + low + " Low"

    # Remove html from str of high
    rem = ['class="temp temp', "High:", "/", ">", "<"]
    pattern = '[' +  ''.join(rem) +  ']'
    high = re.sub(pattern, '', high) 
    high = "-" + high + " high"

    with open('weather.csv', 'a') as f:
        tim = time.ctime()
        x = tim + "|" + temp + "|" + low + "|" + high
        f.writelines(x + '\n')
        print("Finished a line at " + tim)

    time.sleep(1800)
    time_elapse += 1800