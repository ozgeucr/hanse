# --- KLAVYE TUŞ DİZİLİMİ (QWERTY) ---
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
class Button():
    """Sanal klavye ve UI butonlarını oluşturmak için kullanılan sınıf."""
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos      # (x, y) konumu
        self.size = size    # [genişlik, yükseklik]
        self.text = text    # Buton üzerindeki metin

# Butonları Listeye Ekleme
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

# Space Tuşu (Özel Boyut)
buttonList.append(Button([350, 350], "SPACE", [300, 60]))

# --- UI ÇİZİM FONKSİYONU ---
def drawAll(img, buttonList):
    """
    Tüm butonları ekrana çizer.
    Performans için yarı saydam (overlay) tekniği kullanılır.
    """
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(imgNew, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out