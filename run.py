import requests
import time
from playsound import playsound
from collections import Counter

QUESTIONS = [
    "Can you see the baby's nose?",
    "Can you see the baby's mouth?"
]
ENDPOINT = 'https://wk5xd4yoj9axcu06.eu-west-1.aws.endpoints.huggingface.cloud'

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
        response = requests.post(ENDPOINT, json = payload, headers={'Authorization': 'Bearer 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'})
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