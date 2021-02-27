import os


class Config:

    API_KEY = os.getenv('API_KEY')
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    # MONGODB_URI = os.getenv('MONGODB_URI')
    OWNER_USERNAME = '@neelplaysac'
    MONGO_USR = os.getenv('MONGO_USR')
    MONGO_PASS = os.getenv('MONGO_PASS')
    MONGO_COLL = os.getenv('MONGO_COLL')
    TEMP_CHANNEL = os.getenv('TEMP_CHANNEL')
