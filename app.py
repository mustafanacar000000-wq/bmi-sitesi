from flask import Flask, render_template, request

app = Flask(__name__)


def bmi_hesapla(kilo, boy_cm):
    """Kiloyu (kg) ve boyu (cm) alır, vücut kitle indeksini döndürür."""
    boy_m = boy_cm / 100
    return kilo / (boy_m ** 2)


def kategori_bul(bmi):
    """BMI değerine göre kategori adı, mesaj ve renk anahtarı döndürür."""
    if bmi < 18.5:
        return "Zayıf", "Değeriniz normal aralığın altında.", "dusuk"
    elif bmi < 25:
        return "Normal", "Değeriniz normal aralıkta.", "normal"
    elif bmi < 30:
        return "Kilolu", "Değeriniz normal aralığın üzerinde.", "yuksek"
    else:
        return "Obez", "Değeriniz obezite aralığında. Bir hekime danışmanız önerilir.", "cok-yuksek"


@app.route("/", methods=["GET", "POST"])
def ana_sayfa():
    # Sayfa ilk açıldığında gösterilecek boş değerler
    sonuc = None
    hata = None
    kilo_girilen = ""
    boy_girilen = ""

    # Kullanıcı formu gönderdiyse burası çalışır
    if request.method == "POST":
        kilo_girilen = request.form.get("kilo", "")
        boy_girilen = request.form.get("boy", "")

        try:
            kilo = float(kilo_girilen.replace(",", "."))
            boy = float(boy_girilen.replace(",", "."))
        except ValueError:
            hata = "Lütfen sayı girin. Örnek: 72,5"
        else:
            if not (20 <= kilo <= 400):
                hata = "Kilo 20 ile 400 kg arasında olmalı."
            elif not (80 <= boy <= 250):
                hata = "Boy 80 ile 250 cm arasında olmalı."
            else:
                bmi = bmi_hesapla(kilo, boy)
                baslik, mesaj, renk = kategori_bul(bmi)
                sonuc = {
                    "bmi": round(bmi, 1),
                    "baslik": baslik,
                    "mesaj": mesaj,
                    "renk": renk,
                    # Ölçek çubuğundaki işaretçinin soldan yüzde kaçta duracağı
                    "konum": min(max((bmi - 15) / 25 * 100, 0), 100),
                }

    return render_template(
        "index.html",
        sonuc=sonuc,
        hata=hata,
        kilo_girilen=kilo_girilen,
        boy_girilen=boy_girilen,
    )


if __name__ == "__main__":
    app.run(debug=True)
