import json
import os
import requests
import re


def sanitize_filename(filename):
    # Loại bỏ ký tự không hợp lệ trong tên thư mục/tệp
    return re.sub(r"[^\w\s-]", "", filename).strip().replace(" ", "_")


def download_file(url, filepath):
    # Tải file từ URL và lưu vào filepath
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Đã tải: {filepath}")
    else:
        print(f"Lỗi khi tải: {url}")


def process_json(json_file):
    # Đọc file JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Duyệt qua từng bài hát
    for item in data:
        song_name = sanitize_filename(item["name"])
        song_dir = os.path.join("downloads", song_name)

        # Tạo thư mục cho bài hát nếu chưa tồn tại
        os.makedirs(song_dir, exist_ok=True)

        # Tải thumbnail
        if "thumbnail" in item and "url" in item["thumbnail"]:
            thumbnail_url = item["thumbnail"]["url"]
            thumbnail_ext = os.path.splitext(thumbnail_url)[1]
            thumbnail_path = os.path.join(song_dir, f"thumbnail{thumbnail_ext}")
            download_file(thumbnail_url, thumbnail_path)

        # Tải background
        if "background" in item and "url" in item["background"]:
            background_url = item["background"]["url"]
            background_ext = os.path.splitext(background_url)[1]
            background_path = os.path.join(song_dir, f"background{background_ext}")
            download_file(background_url, background_path)

        # Tải audio
        if "audio" in item and "url" in item["audio"]:
            audio_url = item["audio"]["url"]
            audio_ext = os.path.splitext(audio_url)[1]
            audio_path = os.path.join(song_dir, f"audio{audio_ext}")
            download_file(audio_url, audio_path)


if __name__ == "__main__":
    # Tạo thư mục chính nếu chưa tồn tại
    os.makedirs("downloads", exist_ok=True)

    # Gọi hàm xử lý với file JSON
    json_file = "songs.json"  # Thay bằng tên file JSON của bạn
    process_json(json_file)
