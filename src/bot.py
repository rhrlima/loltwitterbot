import json
import random


class PostBuilder:

    def __init__(self, 
        champions_file='data/champions.json', 
        phrases_file='data/phrases.json'):
        self._initialize(champions_file, phrases_file)

    def _initialize(self, champions_file, phrases_file):
        self.champions_data = self._read_champions_data(champions_file)
        self.phrases = self._read_phases_data(phrases_file)
        self.tags = list(self.champions_data['tags'].keys())
        self.rotation = -1
        self.message = self.phrases['message']

    def _read_champions_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.loads(f.read())

    def _read_phases_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.loads(f.read())

    def _get_next_tag(self):
        self.rotation += 1
        if self.rotation >= len(self.tags):
            self.rotation = 0
        return self.tags[self.rotation]

    def _get_random_champion(self, data, tag):
        if tag is None:
            pool = list(data['data'].keys())
        else:
            pool = data['tags'][tag]
        return data['data'][random.choice(pool)]

    def _get_random_phrase(self, data):
        return random.choice(data['posts'])

    def get_formated_message(self, tag=None):

        tag = self._get_next_tag() if tag is None else tag
        champ = self._get_random_champion(self.champions_data, tag)
        phrase = self._get_random_phrase(self.phrases)

        phrase = phrase.format(champ['name'], champ['title'])
        text = self.message.format(
            phrase,
            '⚔'*champ['info']['attack'],
            '🛡'*champ['info']['defense'],
            '🔥'*champ['info']['magic'],
            '⭐'*champ['info']['difficulty'],
            ' '.join(['#'+t for t in champ['tags']])
        )
        return text


if __name__ == '__main__':
    
    post = PostBuilder('../data/champions.json', '../data/phrases.json')
    print(post.get_formated_message())
