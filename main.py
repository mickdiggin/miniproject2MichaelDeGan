# INF601 - Advanced Programming in Python
# Michael DeGan
# Mini Project 2

# (5/5 points) Initial comments with your name, class and project at the top of your .py file.
# (5/5 points) Proper import of packages used.
# (20/20 points) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or
# retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
# Think of some question you would like to solve such as:
# "How many homes in the US have access to 100Mbps Internet or more?"
# "How many movies that Ridley Scott directed is on Netflix?" - https://www.kaggle.com/datasets/shivamb/netflix-shows
# Here are some other great datasets: https://www.kaggle.com/datasets
# (10/10 points) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data
# is labeled tabular data.
# (10/10 points) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build
# some fancy charts here as it will greatly help you in future homework assignments and in the final project.
# (10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder,
# the project should save these when it executes. You may want to add this folder to your .gitignore file.
# (10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
# (10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt
# file which contains all the packages that need installed. You can create this fille with the output of pip freeze at
# the terminal prompt.
# (20/20 points) There should be a README.md file in your project that explains what your project is, how to install
# the pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on the
# explanations.

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from login import *

def getAllActivities():
    # Request a listing of all activities in the caloriesburned database.
    api_url = 'https://api.api-ninjas.com/v1/caloriesburnedactivities'
    response = requests.get(api_url, headers={'X-Api-Key': theKey})
    if response.status_code != requests.codes.ok:
        print("Error:", response.status_code, response.text)

    # Assign to a DataFrame variable
    df = pd.read_json(response.text)
    # Store in an excel file for later reference to reduce the number of api calls.
    df.to_excel("caloriesburned.xlsx", sheet_name="Sheet1", index=False)

def getActivities(activities):
    # Create a new DataFrame object df that is empty except for the column headers.
    df = pd.DataFrame(columns=["name", "calories_per_hour", "duration_minutes", "total_calories"])
    index = 1
    # Request calorie info for each activity in activities list.
    for activity in activities:
        api_url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}'.format(activity)
        response = requests.get(api_url, headers={'X-Api-Key': theKey})
        if response.status_code != requests.codes.ok:
            print("Error:", response.status_code, response.text)

        temp = json.loads(response.text)
        final = temp[0]
        df.loc[index] = final.values()
        index += 1

    # Store in excel file to see all of our data more easily than in the console.
    df.to_excel("selectedactivities.xlsx", sheet_name="Sheet1", index=False)
    return df

def makePlot(data):
    #Sort data
    data.sort_values(by=['total_calories'], inplace=True)
    data.reset_index(drop=True, inplace=True)

    # fig, barGraph = plt.subplots()
    # barGraph.bar(data['name'], data['total_calories'])
    # plt.xticks(fontsize = 5)

    fig, horizBar = plt.subplots(figsize=(10, 8), facecolor='#c9ac83')
    box = horizBar.get_position()
    box.x0 = box.x0 + 0.11
    horizBar.set_position(box)

    green = '#498f3b'
    red = '#cc3535'
    bar_colors = [green, green, green, red, red, red]
    horizBar.barh(data['name'], data['total_calories'], color=bar_colors, edgecolor='#000000', linewidth=0.5)
    horizBar.invert_yaxis()  # labels read top-to-bottom
    horizBar.set_xlabel('Calories Burned Per Hour')
    horizBar.set_title('Calories Burned,\n Household Chores vs. Competitive Sports')
    horizBar.set_facecolor('#ebcca0')

    plt.yticks(fontsize = 9)
    path = Path('./charts')
    if not path.is_dir():
        path.mkdir()

    savePath = "charts/bargraph.png"
    plt.savefig(savePath, dpi=200)
    plt.show()

# Program start
# Get local copy of all activities in caloriesburned database for easy reference, if not already saved.
path = Path('./caloriesburned.xlsx')
if not path.is_file():
    getAllActivities()

# Send chosen activities to the api.
activities = ["Cleaning, dusting", "Taking out trash", "Mowing lawn, walk, power mower", "Football, competitive",
              "Cross country skiing, racing", "Track and field (hurdles)"]

theActivities = getActivities(activities)

makePlot(theActivities)