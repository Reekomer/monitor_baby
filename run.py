import requests
import time
import os

from loguru import logger
from pydub import AudioSegment
from pydub.playback import play
from collections import Counter

QUESTIONS = [
    "Can you see the baby's nose?",
    "Can you see the baby's mouth?",
    "Is the baby awake?"
]
ENDPOINT = os.getenv('ENDPOINT')

def main():
    # prepare image + question
    filename_to_bytes = _fetch_images()
    for filename_to_byte in filename_to_bytes:
        logger.info(f'Parsing: {filename_to_byte["filename"]} ...')
        _check_images(filename_to_byte["bytes"])


def _check_images(image):
    results = []
    for question in QUESTIONS:
        payload = {
            'inputs': {
                'text':question,
                'image':image
                }
        }
        response = requests.post(ENDPOINT, json = payload, headers={'Authorization': f'Bearer {os.getenv("TOKEN")}'})
        answer = response.json()[0]['answer']
        logger.info(f"{question}: {answer}")
        if "Is the baby awake?" == question:
            logger.info("Sleeping for 30 secs ...")
            time.sleep(30)
            continue
        results.append(answer)

    answer_count = Counter(results)
    if answer_count["yes"] != len(QUESTIONS):
        logger.warning("Baby has an issue!")
        _play_alarm()
    else:
        logger.success("Baby is ok!")


def _fetch_images() -> dict:
    images = []
    image_names = os.listdir('images')
    for image_name in image_names:
        with open(f'./images/{image_name}', mode='rb') as file:
            data = {
                "filename": image_name,
                "bytes": str(bytearray(file.read()))
            }
            images.append(data)
    return images

def _play_alarm():
    song = AudioSegment.from_wav("sounds/mixkit-emergency-alert-alarm-1007.wav")
    # play(song)

if __name__ == '__main__':
    while True:
        main()
        logger.info("Sleeping for 10 secs ...")
        time.sleep(10)