import requests
import urllib3
import sqlite3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#auth url for user activity from personal profile
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

db = sqlite3.connect("data.db", check_same_thread=False)
cursor = db.cursor()

#https://www.strava.com/oauth/token?client_id=117917&client_secret=a830f572e6291e2f35635914b6a682eecbda64c1&refresh_token=bcd428a5ddc4325c8b993750c04875cdd63b0e71&grant_type=refresh_token

payload = {
    'client_id': "117917",
    'client_secret': 'a830f572e6291e2f35635914b6a682eecbda64c1',
    'refresh_token': 'bcd428a5ddc4325c8b993750c04875cdd63b0e71',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print("Access Token = {}\n".format(access_token))
header = {'Authorization': 'Bearer ' + access_token}

# The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
# each request, so the next time we request the second page, then third, and so on...
request_page_num = 1
all_activities = []


while True:
    param = {'per_page': 200, 'page': request_page_num}
    # initial request, where we request the first page of activities
    my_dataset = requests.get(activites_url, headers=header, params=param).json()

    # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
    # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
    if len(my_dataset) == 0:
        print("breaking out of while loop because the response is zero, which means there must be no more activities")
        break

    # if the all_activities list is already populated, that means we want to add additional data to it via extend.
    if all_activities:
        print("all_activities is populated")
        all_activities.extend(my_dataset)

    # if the all_activities is empty, this is the first time adding data so we just set it equal to my_dataset
    else:
        print("all_activities is NOT populated")
        all_activities = my_dataset

    request_page_num += 1


for activity in all_activities:
    cursor.execute('''
        SELECT * FROM workouts
        WHERE start_date = ?
    ''', (activity["start_date"],))

    existing_entry = cursor.fetchone()

    if not existing_entry:
        # Checking if the key exists before attempting to access it
        if "average_heartrate" in activity:
            activity["average_heartrate"] = round(float(activity.get("average_heartrate", 0)))
        else:
            activity["average_heartrate"] = 0

        if "max_heartrate" in activity:
            activity["max_heartrate"] = round(float(activity.get("max_heartrate", 0)))
        else:
            activity["max_heartrate"] = 0

        if "average_temp" in activity:
            activity["average_temp"] = round(float(activity.get("average_temp", 0)))
        else:
            activity["average_temp"] = 0

        distance_miles = round(float(activity["distance"]) * 0.000621371, 2)

        # Convert time duration from seconds to "HH:MM:SS" format
        duration_seconds = int(activity["elapsed_time"])
        duration_str = str(timedelta(seconds=duration_seconds))
        # Converting datetime format
        start_date_str = activity["start_date"]
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
        date = start_date_obj.strftime("%m/%d/%y")

        # Include user_id in the INSERT statement
        cursor.execute("INSERT INTO workouts (activity, title, start_date, duration, distance, ave_heart, max_heart, ave_temp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (activity["type"], activity["name"], date, duration_str , distance_miles , activity["average_heartrate"], activity["max_heartrate"], activity["average_temp"]))

print(len(all_activities))
for count, activity in enumerate(all_activities):
    print(activity["distance"])
    print(count)

db.commit()

db.close()

#CREATE TABLE workouts (activity STRING, title STRING, start_date STRING, durationINTEGER, distance INTEGER, ave_heart INTEGER, max_heart INTEGER, ave_temp INTEGER);

#print(os.getcwd()) this gets gets path if needed

    #codeblock below prints all keys
#all_keys = {key for d in all_activities for key in d}
#
## Convert the set to a list if needed
#all_keys_list = list(all_keys)
#
## Print the list of all keys
#print(all_keys_list)

#KEEPS reinserting into table?
#if localtime changes then updated table

#duration converted in HR:MIN:SEC in app.py
#insert into table loop without capabilities for client side
