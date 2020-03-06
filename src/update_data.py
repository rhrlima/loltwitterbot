'''
Downloads and updates the champions.json file when needed

https://ddragon.leagueoflegends.com/api/versions.json
http://ddragon.leagueoflegends.com/cdn/<version>/data/en_US/champion.json
'''

import os
import sys
import json

import numpy as np

from urllib import request


def _get_version_from_server(base_url):
    with request.urlopen(base_url+'/api/versions.json') as f:
        return json.loads(f.read().decode('utf-8'))[0]


def _read_from_file(file_name):

    if not os.path.exists(file_name):
        return None

    with open(file_name, 'r') as f:
        return json.loads(f.read())


def _read_from_server(base_url, version):
    with request.urlopen(base_url+f'/cdn/{version}/data/en_US/champion.json') as f:
        return json.loads(f.read().decode('utf-8'))


def _save_data(file_name, data):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def _parse_data(data):
    parsed_data = {}
    tags_to_copy = ['id', 'key', 'name', 'title', 'info', 'tags']

    parsed_data['version'] = data['version']
    parsed_data['data'] = {}
    parsed_data['tags'] = {}

    for key in data['data'].keys():
        
        if key not in parsed_data:
            parsed_data['data'][key] = {}

        for tag in tags_to_copy:
            parsed_data['data'][key][tag] = data['data'][key][tag]

            if tag == 'tags':
                for class_tag in data['data'][key][tag]:
                    if class_tag not in parsed_data['tags']:
                        parsed_data['tags'][class_tag] = [key]
                    else:
                        parsed_data['tags'][class_tag].append(key)

    return parsed_data


def _compare_versions(ver1, ver2):

    ver1 = [int(v) for v in ver1.split('.')]# int(ver1.replace('.', ''))
    ver2 = [int(v) for v in ver2.split('.')]

    for v1, v2 in zip(ver1, ver2):
        if v1 < v2:
            return True
    return False


def get_updated_data(file_name='data/champions.json', force=False):
    base_url = 'https://ddragon.leagueoflegends.com'

    print('reading local data')
    data = _read_from_file(file_name)
    s_ver = _get_version_from_server(base_url)
    
    if (data is None or _compare_versions(data['version'], s_ver)) or force:

        if data is None:
            print('no local data found')

        elif _compare_versions(data['version'], s_ver):
            l_ver = data['version']
            print(f'local version {l_ver} older than server version {s_ver}')

        if force:
            print('force update requested')

        print('loading from server')
        data = _read_from_server(base_url, s_ver)

        print('parsing data')
        data = _parse_data(data)

        print('saving')
        _save_data(file_name, data)

    print('data version is', data['version'])


if __name__ == '__main__':
    
    get_updated_data(file_name='../data/champions.json')
