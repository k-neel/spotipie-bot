# Spotipie-bot
A python bot to share currently playing spotify songs on telegram.

Can be found on telegram as [Spotipiebot](https://t.me/Spotipiebot).

Based on [SpotifyNowBot](https://github.com/notdedsec/SpotifyNow).

### Configuration

The following env variables are supported:

 - `API_KEY`: Your bot token, as a string.
 - `SPOTIFY_CLIENT_ID`: Your Spotify Client ID.
 - `SPOTIFY_CLIENT_SECRET`: Your Spotify Client Secret.
 - `REDIRECT_URI`: Your Spotify Authentication URL.
 - `MONGO_USR`: Your MongoDB database username.
 - `MONGO_PASS`: Your MongoDB database password.
 - `MONGO_COLL`: Your MongoDB collection name.
 - `TEMP_CHANNEL`: A temporary channel for caching images.

### Python dependencies

Install the necessary python dependencies by moving to the project directory and running:

`pip3 install -r requirements.txt`.

This will install all necessary python packages.

