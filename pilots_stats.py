import csv
from unittest import result
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

######################################
#selenium code

# setting up the web driver
URL = 'https://portlandpilots.com/sports/baseball'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(URL)

#switches to results tab
driver.find_element(By.ID, "ui-id-2").click()

button = driver.find_elements(By.CLASS_NAME, "load-more__button")

#there is one other load-more button, this checks to make sure there are still two 
#before we click on it (after we run out of games to load, the button will disappear)
while len(driver.find_elements(By.CLASS_NAME, "load-more__button")) > 1: 
    button[1].click()   #loads more games
    time.sleep(2) #makes sure we let the games load before moving on 

# saving the html for parsing with BeautifulSoup library
html = driver.page_source

driver.close()


######################################
#Beautiful Soup code
soup = BeautifulSoup(html, 'html5lib')

#finds section with the game results
results = soup.find("results-component")
games = []
for game in results.find_all('div', attrs={'class':'c-events__item flex flex-align-center flex-column text-center'}):
    game_info = {}

    details = game.find('div', attrs={'class':'c-events__details'})
    opponent_details = details.find('div', attrs={'class':'c-events__opponent-wrap'})

    # getting name of opponent
    opponent_name = (opponent_details.find('span', attrs={'class':'c-events__opponent'})).text
    game_info['opponent'] = opponent_name
    
    # getting where the game was played (Home field or Away)
    location = (opponent_details.find('span', attrs={'class':'c-events__location'})).text
    game_info['location'] = location


    # getting win/loss and score details
    stats = details.find('div', attrs={'class':'c-events__date-time-wrap'})
    stats_details = stats.find_all('span')

    status = stats_details[2].text #win or lose
    game_info['status'] = status
    
    team_score = stats_details[3].text
    game_info['team_score'] = team_score
    
    opponent_score = stats_details[5].text
    game_info['opponent_score'] = opponent_score
    
    # adding all of the game info to a list of games
    games.append(game_info)


filename = 'pilots_scores.csv'
with open(filename, 'w', newline='') as f:
    # names of columns
    w = csv.DictWriter(f,['opponent','location','status','team_score','opponent_score']) 
    w.writeheader()
    # write game data into csv for each game
    for game in games:
        w.writerow(game)






