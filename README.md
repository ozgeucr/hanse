# 🚀 HANSE: AI Sanal Kokpit (Virtual Cockpit)

![Project Logo](https://via.placeholder.com/150x150.png?text=AI+Cockpit)
> *Bilgisayarınızı sadece el hareketleriyle, fiziksel temas olmadan yönetin.*
##Not: Şimdilik sadece MACOS işletim sisteminde çalışır
## 📖 Proje Hakkında
Bu proje, bilgisayarlı görü (Computer Vision) ve yapay zeka teknolojilerini kullanarak standart bir web kamerasını gelişmiş bir giriş aygıtına dönüştürür. **MediaPipe** ve **OpenCV** kullanılarak geliştirilen sistem, sol ve sağ elinizi ayırt eder ve her iki elinize farklı "süper güçler" tanımlar.

Mouse kontrolü, sanal klavye ile yazı yazma, ses/parlaklık ayarı ve ekran görüntüsü alma gibi işlemler, klavye veya mouse'a dokunmadan gerçekleştirilebilir.


## 🎥 Demo
*(Buraya proje çalışırken çektiğin ekran kaydının GIF halini ekleyeceksin)*
![Demo GIF](demo_placeholder.gif)

## ✨ Özellikler

* **👻 Hayalet İmleç (Ghost Cursor):** Klavye modu aktifken gerçek mouse imleci sabit kalır, sanal imleç ile odak kaybetmeden arka plandaki uygulamaya (Word, Chrome vb.) yazı yazabilirsiniz.
* **⌨️ Sanal Klavye:** Havada yazı yazmanızı sağlayan QWERTY klavye arayüzü.
* **🎛️ Sol El Medya İstasyonu:**
    * **Ses Kontrolü:** Başparmak ve işaret parmağı ile sesi kısın/açın.
    * **Parlaklık Kontrolü:** "Alo" (Shaka) işareti ile ekran parlaklığını ayarlayın.
* **🖱️ Gelişmiş Mouse Kontrolü:**
    * İmleç takibi (Smoothing ile titreme önleyici).
    * Sol Tık, Sağ Tık.
    * Akıllı Scroll (Kaydırma).
    * **Sürükle & Bırak:** Elinizi yumruk yaparak dosyaları taşıyın. Tam olarak bu sürümde işini yapmıyor.
* **📸 Akıllı Screenshot:** 5 parmağınızı göstererek otomatik ekran görüntüsü alın ve masaüstüne kaydedin. Tam olarak bu sürümde işini yapmıyor

## 🛠️ Kurulum

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1.  Repoyu klonlayın (veya indirin):
    ```bash
    git clone [https://github.com/kullaniciadi/proje-isminiz.git](https://github.com/kullaniciadi/proje-isminiz.git)
    cd proje-isminiz
    ```

2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

3.  Uygulamayı başlatın:
    ```bash
    python src/main.py
    ```

## 🎮 Kullanım Kılavuzu (Kokpit Kontrolleri)

Sistem, sol ve sağ el hareketlerini birbirinden bağımsız olarak algılar.

| El | Hareket | Fonksiyon | Detay |
| :--- | :--- | :--- | :--- |
| **✋ SOL EL** | **Başparmak + İşaret** | **Ses Kontrolü** 🔊 | Parmak arası mesafe sesi ayarlar. |
| **✋ SOL EL** | **Başparmak + Serçe** | **Parlaklık** ☀️ | "Alo" (Shaka) işareti yapın. Mesafe parlaklığı belirler. |
| **✋ SOL EL** | **5 Parmak Açık** | **Screenshot** 📸 | 3 saniye bekleyin, bar dolunca fotoğraf çekilir. |
| | | | |
| **🤚 SAĞ EL** | **İşaret Parmağı** | **Mouse Gezdir** 🖱️ | İmleci hareket ettirir. |
| **🤚 SAĞ EL** | **İşaret + Orta (Birleş)** | **Sol Tık** 👆 | Tıklama yapar (Klavye açıkken tuşa basar). |
| **🤚 SAĞ EL** | **3 Parmak Açık** | **Sağ Tık** 🖱️ | Menüleri açar. |
| **🤚 SAĞ EL** | **Yumruk Yap** | **Sürükle & Bırak** ✊ | Dosyayı tutar. Bırakmak için elinizi açın. |
| **🤚 SAĞ EL** | **KB Butonu** | **Klavye Modu** ⌨️ | Mouse donar, "Hayalet İmleç" ile yazı yazarsınız. |

## ⚙️ Gereksinimler
* Python 3.10+
* Web Kamera
* macOS (Parlaklık ve Ses kontrolü için AppleScript kullanır - Windows için `actions.py` düzenlenmelidir).

## 📄 Lisans
Bu proje [MIT License](LICENSE) altında lisanslanmıştır.