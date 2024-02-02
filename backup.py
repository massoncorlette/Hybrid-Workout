#import requests
#import urllib3
#import sqlite3
#import os
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#auth_url = "https://www.strava.com/oauth/token"
#activites_url = "https://www.strava.com/api/v3/athlete/activities"
#
#db = sqlite3.connect("data.db", check_same_thread=False)
#cursor = db.cursor()
#
##https://www.strava.com/oauth/token?client_id=117917&client_secret=a830f572e6291e2f35635914b6a682eecbda64c1&refresh_token=bcd428a5ddc4325c8b993750c04875cdd63b0e71&grant_type=refresh_token
#
#payload = {
#    'client_id': "117917",
#    'client_secret': 'a830f572e6291e2f35635914b6a682eecbda64c1',
#    'refresh_token': 'bcd428a5ddc4325c8b993750c04875cdd63b0e71',
#    'grant_type': "refresh_token",
#    'f': 'json'
#}
#
#print("Requesting Token...\n")
#res = requests.post(auth_url, data=payload, verify=False)
#access_token = res.json()['access_token']
#
#print("Access Token = {}\n".format(access_token))
#header = {'Authorization': 'Bearer ' + "b458d5e2c23dbc3b624ed99b2a07edfa5d9966ff"}
#
## The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
## each request, so the next time we request the second page, then third, and so on...
#request_page_num = 1
#all_activities = []
#
#while True:
#    param = {'per_page': 200, 'page': request_page_num}
#    # initial request, where we request the first page of activities
#    my_dataset = requests.get(activites_url, headers=header, params=param).json()
#
#    # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
#    # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
#    if len(my_dataset) == 0:
#        print("breaking out of while loop because the response is zero, which means there must be no more activities")
#        break
#
#    # if the all_activities list is already populated, that means we want to add additional data to it via extend.
#    if all_activities:
#        print("all_activities is populated")
#        all_activities.extend(my_dataset)
#
#    # if the all_activities is empty, this is the first time adding data so we just set it equal to my_dataset
#    else:
#        print("all_activities is NOT populated")
#        all_activities = my_dataset
#
#    request_page_num += 1
#    #codeblock below prints all keys
##all_keys = {key for d in all_activities for key in d}
##
### Convert the set to a list if needed
##all_keys_list = list(all_keys)
##
### Print the list of all keys
##print(all_keys_list)
#
#    #code below insert into table loop
##for activity in all_activities:
##cursor.execute("INSERT INTO your_table_name (name, count) VALUES (?, ?)", (activity["name"], activity["count"]))
#
#
#print(len(all_activities))
#for count, activity in enumerate(all_activities):
#    print(activity["type"])
#    print(count)
#
#
#db.close()
#
##print(os.getcwd()) this gets gets path if needed
#
