import requests

input_url = input("URL video tiktok: ").split("?")
get_id_video = input_url[0].split("/")[5]
print(get_id_video)
video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={get_id_video}').json()
print(type(video_api))
video_url = video_api.get("aweme_list")[0].get("video").get("play_addr").get("url_list")[0]
print(video_url)
if video_url:
    print("Скачиваем видео...")
    title_video = video_api.get("aweme_list")[0].get("desc")
    print(title_video)
    try:
        with open(f'video/(title_video).mp4', 'wb') as video_file:
            video_file.write(requests.get(video_url).content)
        print(f"Видео (title_video) успешно скачан XD")
    except Exception as error:
        print(f"Error: (error)")
# https://www.tiktok.com/@6k.ezz/video/7211954017960725762?_r=1&_t=8g0rA3OQbPF
# https://www.tiktok.com/@6k.ezz/video/7211954017960725762