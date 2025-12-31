import requests
import schedule
import time
from datetime import datetime, timedelta
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
from moviepy.editor import ImageClip
import os

from githublogin import username, password

API_URL = "https://api.orhanaydogdu.com.tr/deprem/kandilli/archive"
FONT_PATH = "C:\\Windows\\Fonts\\arialbd.ttf"

IMAGE_PATH = "gunluk_deprem_ozeti.png"
VIDEO_PATH = "gunluk_deprem_ozeti.mp4"
THUMB_PATH = "gunluk_deprem_ozeti.jpg"
TURKIYE_ILLERI = {
    "ADANA","ADIYAMAN","AFYONKARAHISAR","AGRI","AMASYA","ANKARA",
    "ANTALYA","ARTVIN","AYDIN","BALIKESIR","BILECIK","BINGOL",
    "BITLIS","BOLU","BURDUR","BURSA","CANAKKALE","CANKIRI",
    "CORUM","DENIZLI","DIYARBAKIR","EDIRNE","ELAZIG","ERZINCAN",
    "ERZURUM","ESKISEHIR","GAZIANTEP","GIRESUN","GUMUSHANE",
    "HAKKARI","HATAY","ISPARTA","MERSIN","ISTANBUL","IZMIR",
    "KARS","KASTAMONU","KAYSERI","KIRKLARELI","KIRSEHIR",
    "KOCAELI","KONYA","KUTAHYA","MALATYA","MANISA","MARDIN",
    "MUGLA","MUS","NEVSEHIR","NIGDE","ORDU","OSMANIYE","RIZE",
    "SAKARYA","SAMSUN","SIIRT","SINOP","SIVAS","SANLIURFA",
    "SIRNAK","TEKIRDAG","TOKAT","TRABZON","TUNCELI","USAK",
    "VAN","YALOVA","YOZGAT","ZONGULDAK"
}



# -----------------------------
# Instagram Login (AYNEN SENİN ŞEKLİN)
# -----------------------------
cl = Client()
cl.load_settings("session.json")

try:
    cl.login(username, password)
except Exception:
    cl.relogin()

# -----------------------------
# Ana Fonksiyon
# -----------------------------
def gunluk_deprem_reels_olustur_ve_paylas():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    start_dt = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    end_dt   = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)

    try:
        response = requests.get(API_URL, params={"limit": 5000}, timeout=15)
        data = response.json()
    except Exception as e:
        print("❌ API bağlantı hatası:", e)
        return


    if "result" not in data:
        print("❌ Deprem verisi alınamadı")
        return

    il_sayaci = Counter()

    for d in data["result"]:
        
        dt_str = d.get("date_time")
        if not dt_str:
            continue

        deprem_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        if not (start_dt <= deprem_dt <= end_dt):
            continue

        title = d.get("title", "")
        if "(" in title and ")" in title:
            
            il = title.split("(")[-1].split(")")[0].strip().upper()
            if not il:
                continue
            if il not in TURKIYE_ILLERI:
                continue
            il_sayaci[il] += 1

    if not il_sayaci:
        print("⚠️ Dün için deprem yok")
        return

    top3 = il_sayaci.most_common(3)

    # -----------------------------
    # 9:16 GÖRSEL
    # -----------------------------
    img = Image.new("RGB", (1080, 1920), (15, 15, 15))
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(FONT_PATH, 70)
    font_list  = ImageFont.truetype(FONT_PATH, 80)
    font_small = ImageFont.truetype(FONT_PATH, 45)

    yellow = (255, 200, 0)

    title_text = (
        f"{yesterday.strftime('%d.%m.%Y')} tarihinde\n"
        f"deprem açısından\n"
        f"günü hareketli geçiren\n"
        f"ilk 3 il"
    )

    draw.multiline_text(
        (540, 300),
        title_text,
        fill=yellow,
        font=font_title,
        anchor="mm",
        align="center"
    )

    y = 800
    for i, (il, sayi) in enumerate(top3, 1):
        draw.text(
            (540, y),
            f"{i}. {il} — {sayi} deprem",
            fill=yellow,
            font=font_list,
            anchor="mm"
        )
        y += 150

    draw.text(
        (540, 1700),
        "Kaynak: Kandilli Rasathanesi \n \n HABERDAR OLMAK İÇİN TAKİP ET",
        fill=(180, 180, 180),
        font=font_small,
        anchor="mm"
    )

    img.save(IMAGE_PATH)

    # -----------------------------
    # FOTOĞRAFTAN 10 SN REELS
    # -----------------------------
    clip = ImageClip(IMAGE_PATH).resize((1080, 1920)).set_duration(10)

    clip.write_videofile(
        VIDEO_PATH,
        fps=30,
        codec="libx264",
        audio=False,
        ffmpeg_params=[
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart"
        ],
        verbose=False,
        logger=None
    )

    # Thumbnail (Instagram hata vermesin diye)
    clip.save_frame(THUMB_PATH, t=0.0)

    clip.close()

    # -----------------------------
    # REELS PAYLAŞIMI
    # -----------------------------
    caption = (
        f"KAYDET - PAYLAŞ 👇\n"
        f"📊 Deprem Özeti – {yesterday.strftime('%d.%m.%Y')}\n\n"
        f"Dünü deprem açısından\n"
        f"en hareketli geçiren\n"
        f"ilk 3 il 👇\n\n"
        f"#deprem #kandilli #sondakika #reels #depremanaliz"
    )

    cl.clip_upload(VIDEO_PATH, caption, thumbnail=THUMB_PATH)
    print("✅ Reels Instagram'da paylaşıldı")

# -----------------------------
# Zamanlama
# -----------------------------
schedule.every().day.at("00:01").do(gunluk_deprem_reels_olustur_ve_paylas)

print("⏳ Sistem aktif — her gün 00:01'de 10 sn Reels paylaşılacak")

while True:
    schedule.run_pending()
    time.sleep(1)
