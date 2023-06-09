import sys
import vk_api
import json
from datetime import datetime
import requests
from tqdm import tqdm


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
        )[0]
        url = photo["url"]
        likes = str(photos[i]["likes"]["count"])
        date = datetime.utcfromtimestamp(photos[i]["date"]).strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

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
            "https://cloud-api.yandex.net/v1/disk/resources",
            headers=headers,
            params={"path": folder_name},
            timeout=10,
        )
    except:
        print("Ошибка при создании папки на Яндекс.Диске")
        sys.exit()
    photos_data = []
    for likes in tqdm(photos_info):
        url = photos_info[likes]["url"]
        file_name = likes + ".jpg"
        params = {
            "url": url,
            "path": folder_name + "/" + file_name,
        }
        requests.post(upload_url, headers=headers, params=params)
        photos_data.append({"file_name": file_name, "likes": likes})

        with open("photos_info.json", "w", encoding="utf-8") as file:
            json.dump(photos_data, file, ensure_ascii=False, indent=4)

    print("Готово!")


if __name__ == "__main__":
    vk_user_id = input("Введите ID пользователя ВКонтакте: ")
    yandex_disk_token = input("Введите токен Яндекс.Диска: ")
    photos_info, user_name = get_photos_info(vk_user_id)
    save_photos_to_disk(photos_info, user_name, yandex_disk_token)
