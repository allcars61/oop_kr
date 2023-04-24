import sys
import vk_api
import requests
import json
from datetime import datetime
from yadisk import YaDisk


def get_photos_info(vk_user_id):
    vk_session = vk_api.VkApi(token='YOUR_TOKEN')  # 'YOUR_TOKEN' заменить на токен ВК
    vk = vk_session.get_api()

    try:
        user_info = vk.users.get(user_ids=vk_user_id)[0]
    except:
        print("Ошибка! Пользователь не найден.")
        sys.exit()

    user_name = user_info['first_name'] + '_' + user_info['last_name']
    photos = vk.photos.get(owner_id=vk_user_id, album_id='profile', photo_sizes=1, extended=1)['items']
    photos_info = {}

    for i in range(len(photos)):
        photo = sorted(photos[i]['sizes'], key=lambda x: (x['width'], x['height']), reverse=True)[0]
        url = photo['url']
        likes = photos[i]['likes']['count']
        date = datetime.utcfromtimestamp(photos[i]['date']).strftime('%Y-%m-%d_%H-%M-%S')
        file_name = str(likes) + '_' + date + '.jpg'
        size = photo['type']
        width = photo['width']
        height = photo['height']

        photos_info[likes] = [url, file_name, size, width, height]

    return photos_info, user_name


def save_photos_to_disk(photos_info, user_name, yandex_disk_token):
    disk = YaDisk(token=yandex_disk_token)
    folder_name = user_name + '_photos_from_vk'
    disk.mkdir(folder_name)

    for likes in sorted(photos_info.keys(), reverse=True):
        url = photos_info[likes][0]
        file_name = photos_info[likes][1]
        r = requests.get(url)

        if r.status_code == 200:
            disk.upload(r.content, folder_name + '/' + file_name)

        photo_info = {'file_name': file_name, 'likes': likes}
        with open('photos_info.json', 'a') as file:
            file.write(json.dumps(photo_info) + '\n')

    print('Готово!')


def main():
    vk_user_id = input("Введите id пользователя вконтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")

    photos_info, user_name = get_photos_info(vk_user_id)
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)


if __name__ == '__main__':
    main()
