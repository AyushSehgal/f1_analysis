import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen 
import re
import sys

# Class and List Definitions
class Driver:
    def __init__(self, name, team, points) -> None:
        self.name = name
        self.team = team 
        self.points = points 
    def __str__(self) -> str:     
        return "Name: " + self.name + "\n" + "Constructor: " + self.team.name + "\n" + "Points: " + str(self.points) + "\n" + "Drivers: " + str(self.team)

class Constructor:
    points = 0
    def __init__(self, name) -> None:
        self.name = name
        self.drivers = []
    def __str__(self) -> str:
        return "Name: " + self.name + "\n" + "Points: " + str(self.points)
    def get_points(self): 
        if len(self.drivers) == 2:
            return self.drivers[0].points + self.drivers[1].points
    def to_dict(self): 
        return {
            'Name: ' + self.name,
            'Points: ' + str(self.get_points())
        }
        
points_per_position = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
races = ['Bahrain', 'Saudi Arabia', 'Australia', 'Azerbaijan', 'Miami', 'Imola', 'Monaco', 'Spain', 'Canada', 'Austria', 'Silverstone', 'Hungary', 'Belgium', 'Netherlands', 
         'Monza', 'Singapore', 'Japan', 'Qatar', 'Austin', 'Mexico', 'Brazil', 'Vegas', 'Abu Dhabi']

# Populate Class Objects
driver_names = ['Lewis Hamilton', 'George Russell', 'Max Verstappen', 'Sergio Perez', 'Charles Leclerc', 'Carlos Sainz', 'Lando Norris', 'Oscar Piastri', 'Pierre Gasley', 'Esteban Ocon', 'Yuki Tsunoda', 'Nick De Vries', 'Lance Stroll', 'Fernando Alsonso', 'Zhou Guanyu', 'Valtteri Bottas', 'Kevin Magnussen', 'Nico Hulkenberg']
team_names = ['mercedes', 'redbull', 'ferrari', 'mclaren', 'alpine', 'alphatauri', 'astonmartin', 'alpharomeo', 'haas','williams']
constructors = []
drivers = []
driver_start_index = 0
for t in team_names: 
    constructor = Constructor(t)
    constructors.append(constructor)
    for i in range(driver_start_index, min(driver_start_index + 2, len(driver_names))):
        driver = Driver(driver_names[i], constructor, 0)
        drivers.append(driver)   
        constructor.drivers.append(driver)
        driver_start_index += 1

drivers_standings = {}
for n in driver_names: 
    drivers_standings[n] = 0

drivers_standings_url = "https://www.formula1.com/en/results.html/2023/drivers.html"

# Get latest results
def get_latest_results():
    html = requests.get(drivers_standings_url)
    parser = BeautifulSoup(html.text, "html.parser")
    results_table = parser.find_all("table")[0]
    results_table_str = str(results_table)
    results_table = re.sub('<span class="uppercase hide-for-desktop">.*</span>', "", results_table_str)
    df = pd.read_html(str(results_table), flavor='bs4', header=[0])[0]
    df.drop(['Unnamed: 0', 'Unnamed: 6', 'Nationality', 'Car', 'Pos'], axis=1, inplace=True)
    return df 

def update_results(scores):
    for d in scores: 
        name = d['Driver']
        score = d['PTS']
        if name not in drivers_standings: 
            drivers_standings[name] = 0
        else: 
            drivers_standings[name] += score
    for driver in drivers: 
        if driver.name in scores: 
            driver.points += scores[driver.name]

def display_drivers_results():
    drivers_standings_sorted = dict(sorted(drivers_standings.items(), key=lambda x: x[1])[::-1])
    print("Name: \t Points:")
    for d in drivers_standings_sorted:
        print("Name: " + d + "\t Points: " + str(drivers_standings_sorted[d]))
        

def main():
    # args = len(sys.argv)
    # if args == 1:
    #     print("Please pass the name of the race that just passed")
    #     return 
    race = "Bahrain"
    df = get_latest_results()
    print("----- " + race + " Results" + " ----")
    print(df)
    print(" ")
    print("----- Drivers Standings -----")
    update_results(df.to_dict(orient='records'))
    display_drivers_results()

main()


