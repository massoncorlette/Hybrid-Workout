const auth_link = "https://www.strava.com/oauth/token"

function getActivites(res){
    
    const activities_link = `https://www.strava.com/api/v3/athlete/activities?access_token=${res.access_token}`
    fetch(activities_link)
        .then((res) => console.log(res.json()))
}

function reAuthorize(){
    fetch(auth_link,{
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'

        },

        body: JSON.stringify({

            client_id: '117917',
            client_secret: 'a830f572e6291e2f35635914b6a682eecbda64c1',
            refresh_token: '44814352b23a3f285ded0ac457ceea5e0fdb1bcf',
            grant_type: 'refresh_token'
        })
    }).then(res => res.json())
        .then(res => getActivites(res))
}

reAuthorize()
