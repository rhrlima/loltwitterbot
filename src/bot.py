import json
import random


class Bot:

    def __init__(self, 
        champions_file='data/champions.json', 
        phrases_file='data/phrases.json'):
        self.initialize(champions_file, phrases_file)

    def initialize(self, champions_file, phrases_file):
        self.champions_data = self._read_champions_data(champions_file)
        self.phrases = self._read_phases_data(phrases_file)

    def _read_champions_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.loads(f.read())

    def _read_phases_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.loads(f.read())

    def _get_random_champion(self, data, tag):
        if tag is None:
            pool = list(data['data'].keys())
        else:
            pool = data['tags'][tag]
        return data['data'][random.choice(pool)]

    def _get_random_phrase(self, data):
        return random.choice(data['posts'])

    def _get_pick(self, champ, phrase):
        return phrase.format(champ['name'], champ['title'])

    def get_pick(self, tag=None):

        champ = self._get_random_champion(self.champions_data, tag)
        phrase = self._get_random_phrase(self.phrases)

        phrase = phrase.format(champ['name'], champ['title'])
        text = '''{}\n\nStats:\nAttack: {}\nDefense: {}\nMagic: {}\nDifficulty: {}\n\n{}'''.format(
            phrase,
            '*'*champ['info']['attack'],
            '*'*champ['info']['defense'],
            '*'*champ['info']['magic'],
            '*'*champ['info']['difficulty'],
            ' '.join(['#'+t for t in champ['tags']])
        )
        return text


if __name__ == '__main__':
    
    bot = Bot()
    print(bot.get_pick())