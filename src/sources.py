# versions url 
# https://ddragon.leagueoflegends.com/api/versions.json

# champions data
# http://ddragon.leagueoflegends.com/cdn/<version>/data/en_US/champion.json


SERVER_BASE_URL = 'https://ddragon.leagueoflegends.com'
SERVER_VERSION_URL = '/api/versions.json'
SERVER_CHAMPION_URL = '/cdn/{}/data/{}/champion.json'
SERVER_LANG = 'en_US'

VERSION_URL = SERVER_BASE_URL + SERVER_VERSION_URL
CHAMPION_URL = SERVER_BASE_URL + SERVER_CHAMPION_URL.format('{}', SERVER_LANG)

LOCAL_CHAMPION_DATA = 'data/champions.json'
LOCAL_PHRASES_DATA = 'data/phrases.json'
