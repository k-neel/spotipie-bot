import requests


class SpotifyUser:
    def __init__(self, refresh_token, clientId, clientSecret):
        self.refresh_token = refresh_token
        self.clientId = clientId
        self.clientSecret = clientSecret

    def getCurrentyPlayingSong(self):
        refresh = ''
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': "localghost:3000/callback",
            'client_id': self.clientId,
            'client_secret': self.clientSecret
        }
        token = requests.post(
            'https://accounts.spotify.com/api/token', data=data).json()

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token['access_token']
        }
        r = requests.get(
            'https://api.spotify.com/v1/me/player/currently-playing', headers=headers)

        return r
