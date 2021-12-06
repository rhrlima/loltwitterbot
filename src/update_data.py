import os
import json

from urllib import request

from sources import LOCAL_CHAMPION_DATA, VERSION_URL, CHAMPION_URL


def _read_data_from_url(url: str):

    with request.urlopen(url) as f:
        return json.loads(f.read().decode('utf-8'))


def _get_version_from_server(version_url: str):

    return _read_data_from_url(version_url)[0]


def _read_data_from_local(file_name: str):

    if not os.path.exists(file_name):
        return None

    with open(file_name, 'r') as f:
        return json.loads(f.read())


def _read_data_from_server(data_url: str):

    return _read_data_from_url(data_url)


def _save_data(file_name: str, data: dict):

    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def _parse_data(data: dict):

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


def _compare_versions(ver1: str, ver2: str):
    '''returns True is ver1 < ver2'''

    ver1 = list(map(int, ver1.split('.')))
    ver2 = list(map(int, ver2.split('.')))

    return ver1 < ver2


def get_updated_data(file_name: str=LOCAL_CHAMPION_DATA, force: bool=False):

    print('reading local data')
    data = _read_data_from_local(file_name)

    # server version
    s_ver = _get_version_from_server(VERSION_URL)

    if data is None or force or _compare_versions(data['version'], s_ver):

        if data is None:
            print('no local data found')

        elif force:
            print('force update requested')

        else:
            l_ver = data['version']
            print(f'local version {l_ver} older than server version {s_ver}')

        print('loading from server')
        data = _read_data_from_server(CHAMPION_URL.format(s_ver))

        print('parsing data')
        data = _parse_data(data)

        print('saving')
        _save_data(file_name, data)

        print('data version updated to', data['version'])

    else:
        print('local data is up to date', data['version'])


if __name__ == '__main__':

    get_updated_data()
