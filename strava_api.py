import requests

def get_activities(access_token):
    activities_link = f"https://www.strava.com/api/v3/athlete/activities?access_token={access_token}"
    response = requests.get(activities_link)

    if response.status_code == 200:
        # Assuming the response is in JSON format
        activities_data = response.json()
        return activities_data
    else:
        # Handle errors here
        print(f"Error fetching activities. Status code: {response.status_code}")
        return None

def re_authorize():
    auth_link = "https://www.strava.com/oauth/token"

    response = requests.post(auth_link, json={
        'client_id': '117917',
        'client_secret': 'a830f572e6291e2f35635914b6a682eecbda64c1',
        'refresh_token': '44814352b23a3f285ded0ac457ceea5e0fdb1bcf',
        'grant_type': 'refresh_token'
    })

    if response.status_code == 200:
        auth_data = response.json()
        activities_data = get_activities(auth_data['access_token'])
        return activities_data
    else:
        # Handle errors here
        print(f"Error reauthorizing. Status code: {response.status_code}")
        return None

# Call the re_authorize function to get activities
activities_result = re_authorize()
print(activities_result)
