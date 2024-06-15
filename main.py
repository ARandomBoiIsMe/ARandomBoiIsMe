"""
Very straightforward script to post random XKCD comics to my GitHub profile.
Mostly made this to test out GitHub Actions.
Partly made this cuz I thought it would be funny lol... yeah.
"""

import requests
import random
from dataclasses import dataclass

BASE_URL = "https://xkcd.com/"

@dataclass
class XKCD_Comic:
    title: str
    alt: str
    img: str

def post_random_comic():
    # Gets random comic number, between 1 and the number of the latest comic.
    random_comic_num = 0
    with requests.get(f'{BASE_URL}info.0.json') as response:
        if response.status_code != 200:
            exit()

        max_comic_num = response.json()['num']
        random_comic_num = random.randint(1, max_comic_num)

    # Requests for comic, based on the generated random number.
    with requests.get(f'{BASE_URL}{random_comic_num}/info.0.json') as response:
        if response.status_code != 200:
            exit()

        response_json = response.json()
        random_comic = XKCD_Comic(
                        title=response_json['title'],
                        alt=response_json['alt'],
                        img=response_json['img']
                    )
        
        download_comic_image(random_comic.img)

    # Updates markdown file with new random comic.
    markdown = "## Hello 👀\n\nSomehow, you found yourself here.\n\nHere, have a random XKCD comic for your troubles:\n\n"
    markdown += "-----------------------------------\n\n"
    markdown += f"[{random_comic.title}]({BASE_URL}{random_comic_num})\n\n"
    markdown += f"![{random_comic.title}](./random_comic.png)\n\n"
    markdown += f"{random_comic.alt}\n\n"
    markdown += "-----------------------------------"

    # Save Markdown to file.
    with open("./README.md", "w", encoding="utf-8") as open_markdown:
        open_markdown.write(markdown)

    print("Comic updated.")

def download_comic_image(image_link: str):
    with requests.get(image_link) as response:
        if response.status_code != 200:
            exit()

        # Opens file in 'write-bytes' mode and copies
        # the byte stream from the response into the
        # opened file.
        with open('random_comic.png', 'wb') as file:
            file.write(response.content)

if __name__ == '__main__':
    post_random_comic()
