# https://kinokcdn.b-cdn.net/kinok/uptv/series/siliconValley/3/silicon_valley_720p_s3_e6.mp4
# https://kinokcdn.b-cdn.net/kinok/uptv/series/siliconValley/3/silicon_valley_720p_s3_e6.mp4
import requests
import os

import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

BASE_URL = "https://kinokcdn.b-cdn.net/kinok/uptv/series/siliconValley"
MAX_WORKERS = 4  # Nechta oqim bilan yuklash

stop_flag = False  # Ctrl+C bosilganda to‘xtash uchun

def check_file_exists(url):
    """Fayl bor-yo'qligini 1 KB yuklab tekshiradi va hajmini qaytaradi"""
    try:
        resp = requests.get(url, headers={"Range": "bytes=0-1023"}, stream=True, timeout=5)
        if resp.status_code in (200, 206):
            head = requests.head(url, timeout=5)
            total_size = int(head.headers.get("Content-Length", 0))
            return total_size
    except:
        return None
    return None

def download_file(url, file_name, total_size):
    """Progress bar bilan yuklab olish"""
    global stop_flag
    if stop_flag:
        return
    start_time = time.time()
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, "wb") as f, tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=file_name,
            ascii=True
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                if stop_flag:
                    print(f"\n[STOPPED] {file_name}")
                    return
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
    elapsed = time.time() - start_time
    speed = total_size / elapsed / 1024 / 1024
    print(f"[DONE] {file_name} | {total_size/1024/1024:.2f} MB | {elapsed:.2f} sec | {speed:.2f} MB/s")

def main():
    global stop_flag
    urls = []
    try:
        # Avval mavjud fayllarni tekshiramiz
        for season in range(2, 3):
            for episode in range(3, 5):
                url = f"{BASE_URL}/{season}/silicon_valley_720p_s{season}_e{episode}.mp4"
                size = check_file_exists(url)
                if size:
                    urls.append((url, f"s{season:02}_e{episode:02}.mp4", size))

        total_size = sum(size for _, _, size in urls)
        print(f"\nTopildi: {len(urls)} ta fayl | Umumiy hajm: {total_size/1024/1024:.2f} MB\n")

        start_all = time.time()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(download_file, url, name, size) for url, name, size in urls]
            for future in as_completed(futures):
                if stop_flag:
                    break
                future.result()
        elapsed_all = time.time() - start_all
        avg_speed = total_size / elapsed_all / 1024 / 1024
        print(f"\n[FINISHED] {len(urls)} ta fayl | {total_size/1024/1024:.2f} MB | {elapsed_all:.2f} sec | {avg_speed:.2f} MB/s")

    except KeyboardInterrupt:
        stop_flag = True
        print("\n❌ Yuklab olish foydalanuvchi tomonidan to‘xtatildi!")

if __name__ == "__main__":
    main()
