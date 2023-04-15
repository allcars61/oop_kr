def main():
    vk_user_id = input("Введите id пользователя вконтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")

    vk_session = vk_api.VkApi(token='YOUR_TOKEN') # 'YOUR_TOKEN' заменить на токен ВК
    vk = vk_session.get_api()

    photos = vk.photos.get(owner_id=vk_user_id, album_id='profile', photo_sizes=1)['items']

    count = min(len(photos), 5)

    disk = YandexDisk(token=yandex_disk_token)

    folder_name = 'photos_from_vk'
    disk.mkdir(folder_name)

    for i in range(count):
        photo = sorted(photos[i]['sizes'], key=lambda x: x['width'], reverse=True)[0]
        url = photo['url']

        name = str(photos[i]['likes']['count']) + '.jpg'
        size = photo['type']
        width = photo['width']
        height = photo['height']

        r = requests.get(url)
        if r.status_code == 200:
            disk.upload(r.content, folder_name + '/' + name)

        photo_info = {'file_name': name, 'size': size, 'width': width, 'height': height}
        with open('photos_info.json', 'a') as file:
            file.write(json.dumps(photo_info) + '\n')

    print('Готово!')

if __name__ == '__main__':
    main()

