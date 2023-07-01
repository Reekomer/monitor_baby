import requests
import time
import os

from loguru import logger
from playsound import playsound
from collections import Counter

QUESTIONS = [
    "Can you see the baby's nose?",
    "Can you see the baby's mouth?"
]
ENDPOINT = os.getenv('ENDPOINT')

def main():
    # prepare image + question
    images = _fetch_images()
    for image in images:
        _check_images(image)


def _check_images(image):
    for question in QUESTIONS:
        payload = {
            'inputs': {
                'text':question,
                'image':image
                }
        }
        response = requests.post(ENDPOINT, json = payload, headers={'Authorization': f'Bearer {os.getenv("TOKEN")}'})
        result = response.json()[0]['answer']
        answer_count = Counter(result)
        if answer_count["yes"] != len(QUESTIONS):
            _play_alarm()


def _fetch_images():
    with open('./images/th-483835542', mode='rb') as file:
        return str(bytearray(file.read()))

def _play_alarm():
    playsound('./sounds/mixkit-critical-alarm-1004.wav')

if __name__ == '__main__':
    while True:
        main()
        time.sleep(10)