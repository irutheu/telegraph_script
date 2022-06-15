import os
import json
import argparse
from typing import List

import requests
import yaml
from tqdm import tqdm

with open('credentials.yaml', 'r') as stream:
    try:
        data = yaml.safe_load(stream)
        TOKEN = data['telegraph_token']
    except yaml.YAMLError as exc:
        print(exc)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory',
                    help='Путь к папке с изображениями'
                    )
parser.add_argument('-t', '--title',
                    default='Манга',
                    help='Название страницы'
                    )
parser.add_argument('-an', '--author_name',
                    default='Мангал',
                    help='Имя автора'
                    )
parser.add_argument('-au', '--author_url',
                    default='https://t.me/Kawaiimangal',
                    help='Ссылка'
                    )
args = parser.parse_args()



def upload_img_telegraph(img_path: str, retries: int=3) -> str:
    with open(img_path, 'rb') as img_file:
        success_flag = True
        retry_count = 0
        while success_flag:
            try:
                result = requests.post(
                    'https://telegra.ph/upload',
                    files={
                        'file': ('file', img_file, 'image/jpg')
                    }
                ).json()
                success_flag = False
            except:
                retry_count += 1
                if retries == retry_count:
                    raise Exception(f'Image upload cancelled after {retries}.')
                print(f'Image upload failed. Retrying for {retries - retry_count} more times...')


        return result[0]['src']


def upload_folder(folder_path: str) -> List[str]:
    file_list = []

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if filepath.lower().endswith('jpg', 'png', 'jpeg', 'gif'):
                file_list.append(filepath)

    img_links = []
    for file in tqdm(sorted(file_list)):
        img_links.append('https://telegra.ph/'+upload_img_telegraph(file))

    return img_links

def construct_contents(img_links: List[str]) -> List[dict]:
    content = []
    
    for img_link in img_links:
        temp_element = {
            'tag': 'img',
            'attrs': {'src': img_link}
        }
        content.append(temp_element)
    
    return json.dumps(content)

if __name__ == '__main__':
    links = upload_folder(args.directory)
    content = construct_contents(links)

    result = requests.post(
        'https://api.telegra.ph/createPage',
        data={
            'access_token': TOKEN,
            'title': args.title,
            'author_name': args.author_name,
            'author_url': args.author_url,
            'content': content,
        }
    ).json()

    try:
        page_link = result['result']['url']
        print('Ссылка на страницу:', page_link)
    except Exception as exc:
        print('Что-то сломалось, напиши мне и прикрепи скрин с ошибкой:')
        print(result)
        print(exc)