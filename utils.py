import re
from collections import Counter
import json

splitters = r'[,\;\?\:\.\s!«»()]'
epsilon = 10

target_words_weight = {
    "константиндер": 10,
    "город/страну": 3,
    "город/страна": 3,
    "свадьба": 1,
    "свадбе": 1,
    'знакомства' : 5,
    'вдвоём': 2,
    'любовь': 2,
    'возраст': 1.5,
    'предложение': 1.5,
    'константдринк': -2,
    "вместе": 1.5,
    "невесты": 1.5,
    "невестa": 1.5,
    "живёте/находитесь": 1.5,
    "совместное": 2,
    "совместный": 2
}

def apply_weights(text, weights):
    word_count = Counter(filter(lambda word: len(word) > 3, text))
    print(word_count)
    return {word: count * weights.get(word, 0) for word, count in word_count.items()}


def split_generator(pattern, string):
    start = 0
    string = string.lower()
    for match in re.finditer(pattern, string):
        yield string[start:match.start()]
        start = match.end()
    # Yield the remaining part of the string after the last delimiter
    yield string[start:]


def get_from_json(filename, key: str):
    with open(filename, 'r+') as f:
        data = json.load(f)
        return data[key]

def update_json(filename, **kwargs):
    with open(filename, 'r+') as f:
        data = json.load(f)
        data.update(kwargs)
        f.seek(0)
        json.dump(data, f, indent=4)