import sys
import vk_api
import json
from datetime import datetime
from yadisk import YaDisk
from tqdm import tqdm


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
    photos_info = []

    for i in range(len(photos)):
        photo = sorted(photos[i]['sizes'], key=lambda x: (x['width'], x['height']), reverse=True)[0]
        url = photo['url']
        likes = photos[i]['likes']['count']
        date = datetime.utcfromtimestamp(photos[i]['date']).strftime('%Y-%m-%d_%H-%M-%S')
        file_name = str(likes) + '_' + date + '.jpg'
        size = photo['type']

        photos_info.append({'file_name': file_name, 'likes': likes})

    return photos_info, user_name


def save_photos_to_disk(photos_info, user_name, yandex_disk_token):
    disk = YaDisk(token=yandex_disk_token)
    folder_name = user_name + '_photos_from_vk'

    try:
        disk.mkdir(folder_name)
    except:
        pass

    for photo in tqdm(photos_info, desc="Загрузка на Яндекс.Диск"):
        url = "https://sun9-73.userapi.com/impg/" + vk_user_id + "/" + photo[
            'file_name'] + "?size=604x604&quality=96&sign=fcfd9095e5b46f5c7bc472442dcf630b&c_uniq_tag=TARV9xEKMfANSSlkA2oDTwvJl1ykEp_0IzUhFUcGVws&type=album"
        file_name = photo['file_name']
        disk.upload_url(url, folder_name + '/' + file_name)

    with open('photos_info.json', 'w', encoding='utf-8') as file:
        json.dump(photos_info, file, ensure_ascii=False, indent=4)

    print('Готово!')


def main():
    vk_user_id = input("Введите id пользователя вконтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")

    photos_info, user_name = get_photos_info(vk_user_id)
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)


if __name__ == '__main__':
    main()
