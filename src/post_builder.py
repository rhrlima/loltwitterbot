import json
import random

from sources import LOCAL_CHAMPION_DATA, LOCAL_PHRASES_DATA


def _read_data(file_name):
    with open(file_name, 'r') as f:
        return json.loads(f.read())


class PostBuilder:

    def __init__(self):
        self.champions_data = _read_data(LOCAL_CHAMPION_DATA)
        self.phrases = _read_data(LOCAL_PHRASES_DATA)
        self.tags = list(self.champions_data['tags'].keys())
        self.rotation = -1
        self.message = self.phrases['message']

    def _get_next_tag(self):
        self.rotation += 1
        if self.rotation >= len(self.tags):
            self.rotation = 0
        return self.tags[self.rotation]

    def _get_random_champion(self, tag=None):
        if tag is None:
            pool = list(self.champions_data['data'].keys())
        else:
            pool = self.champions_data['tags'][tag]
        return self.champions_data['data'][random.choice(pool)]

    def _get_random_phrase(self):
        return random.choice(self.phrases['posts'])

    def get_formated_message(self, tag=None):

        tag = self._get_next_tag() if tag is None else tag
        champ = self._get_random_champion(tag)
        phrase = self._get_random_phrase()

        phrase = phrase.format(champ['name'], champ['title'])
        text = self.message.format(
            phrase,
            '⚔️'*champ['info']['attack'],
            '🛡️'*champ['info']['defense'],
            '🔥'*champ['info']['magic'],
            '⭐'*champ['info']['difficulty'],
            ' '.join(['#'+t for t in champ['tags']])
        )
        return text


if __name__ == '__main__':
    
    # local run
    post = PostBuilder()
    print(post.get_formated_message())
