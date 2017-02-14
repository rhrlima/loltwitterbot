import json
import requests


config = json.loads(open("config.json").read()) #


classes = {"TANK":[], "FIGHTER":[], "MAGE":[], "ASSASSIN":[], "MARKSMAN":[], "SUPPORT":[]} #classes


def getJsonDataFromUrl(url):
    json_data = json.loads(requests.get(url + "api_key=" + config['key']).text)
    if "status" in json_data.keys():
        if "status_code" in json_data["status"].keys():
            print("<<Error>>\t", json_data['status']['status_code'], json_data['status']['message'])
            return None
    return json_data


def get_champions_data(region):
	url = "https://global.api.pvp.net/api/lol/static-data/"+region+"/v1.2/champion?champData=tags&"
	return getJsonDataFromUrl(url)


def to_json(data):
	return json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def save_data(file_name, data):
    data_file = open(file_name, "w")
    data_file.write(to_json(data))
    data_file.close()


data = get_champions_data("na")


for key in data['data'].keys():
	champion = data['data'][key]
	classes[champion['tags'][0].upper()].append(champion)


save_data("classes.json", classes)


print("Champion classes updated succefully.")