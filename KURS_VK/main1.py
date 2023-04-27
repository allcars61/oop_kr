def get_photos_info(vk_user_id):
    vk_session = vk_api.VkApi(token="YOUR_TOKEN")  # 'YOUR_TOKEN' заменить на токен ВК
    vk = vk_session.get_api()

    try:
        user_info = vk.users.get(user_ids=vk_user_id)[0]
    except:
        print("Ошибка! Пользователь не найден.")
        sys.exit()

    user_name = user_info["first_name"] + "_" + user_info["last_name"]
    photos = vk.photos.get(
        owner_id=vk_user_id, album_id="profile", photo_sizes=1, extended=1
    )["items"]
    photos_info = {}

    for i in range(len(photos)):
        photo = sorted(
            photos[i]["sizes"], key=lambda x: (x["width"], x["height"]), reverse=True
@@ -32,19 +29,15 @@ def get_photos_info(vk_user_id):
        )
        file_name = likes + "_" + date + ".jpg"
        size = photo["type"]

        if likes in photos_info:
            likes += "_" + date

        photos_info[likes] = {"url": url, "size": size}

    return photos_info, user_name


def save_photos_to_disk(photos_info, user_name, yandex_disk_token):
    headers = {"Authorization": "OAuth " + yandex_disk_token}
    folder_name = user_name + "_photos_from_vk"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    try:
        requests.put(
@@ -62,33 +55,62 @@ def save_photos_to_disk(photos_info, user_name, yandex_disk_token):
    for likes in photos_info:
        url = photos_info[likes]["url"]
        file_name = likes + ".jpg"

        response = requests.get(url)

        files = {"file": (file_name, response.content)}
        params = {
            "url": upload_url,
            "method": "PUT",
            "path": folder_name + "/" + file_name,
        }

        response = requests.get(upload_url, headers=headers, params=params)

        params = {"path": folder_name + "/" + file_name, "url": url}
        response = requests.post(upload_url, headers=headers, params=params)
        photos_data.append({"file_name": file_name, "likes": likes})

    with open("photos_info.json", "w", encoding="utf-8") as file:
        json.dump(photos_data, file, ensure_ascii=False, indent=4)
    with open("photos_info.json", "w", encoding="utf-8") as f:
        json.dump(photos_data, f, ensure_ascii=False, indent=4)

    print("Готово!")
    print("Фотографии сохранены на Яндекс.Диск")


def main():
    vk_user_id = input("Введите id пользователя вконтакте: ")
if __name__ == "__main__":
    vk_user_id = input("Введите ID пользователя ВКонтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")

    photos_info, user_name = get_photos_info(vk_user_id)
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)
    headers = {"Authorization": "OAuth " + yandex_disk_token}
    folder_name = user_name + "_photos_from_vk"

    try:
        requests.put(
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers=headers,
            params={"path": folder_name},
            timeout=10,
        )
    except:
        print("Ошибка при создании папки на Яндекс.Диске")
        sys.exit()

    upload_url = requests.get(
        "https://cloud-api.yandex.net/v1/disk/resources/upload",
        headers=headers,
        params={"path": folder_name},
        timeout=10,
    ).json()["href"]
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)

if __name__ == "__main__":
    main()
    vk_user_id = input("Введите ID пользователя ВКонтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")
    photos_info, user_name = get_photos_info(vk_user_id)
    
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)
