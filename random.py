import random
CAPTION_TEMPLATES = [
    "KAYDET – PAYLAŞ 👇\n📊 Deprem Özeti – {date}\n\nSon 48 saatte en hareketli ilk 5 il 👇",
    "DEPREM GÜNDEMİ ⚠️\n📊 {date}\n\nSon 48 saatlik deprem hareketliliği 👇",
    "BUGÜNÜN DEPREM ÖZETİ 📉\n({date})\n\nEn çok deprem olan 5 il 👇",
    "SON 48 SAATTE NELER OLDU?\n📊 Deprem Özeti – {date}\n\nİlk 5 il 👇",
    "DEPREM RAPORU ⚠️\n{date}\n\nEn hareketli bölgeler 👇"
]


HASHTAG_POOLS = [
    ["#deprem", "#kandilli", "#sondakika", "#reels", "#haber"],
    ["#depremoldu", "#afad", "#depremhaber", "#turkiye", "#kesfet"],
    ["#earthquake", "#kandilli", "#guncel", "#reelsvideo", "#kesfet"],
    ["#deprembilgi", "#depremanaliz", "#sondurum", "#instareels"],
    ["#deprem", "#haberler", "#gundem", "#turkiyegundemi"]
]

def generate_random_caption(yesterday):
    caption_text = random.choice(CAPTION_TEMPLATES).format(
        date=yesterday.strftime('%d.%m.%Y')
    )

    hashtags = random.sample(random.choice(HASHTAG_POOLS), k=4)

    return caption_text + "\n\n" + " ".join(hashtags)


    
caption = generate_random_caption(yesterday)
