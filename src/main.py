import cv2
import numpy as np
import hand_detector as htm
import time
import pyautogui
import os
import math
import config  # <--- AYAR DOSYASINI BURAYA ÇAĞIRIYORUZ

# --- DIŞ BAĞIMLILIK KONTROLÜ ---
try:
    import screen_brightness_control as sbc
except ImportError:
    sbc = None

# --- PYAUTOGUI BAŞLANGIÇ AYARLARI ---
# Bu ayarlar programın çalışma mekaniğini etkilediği için main içinde kalması uygundur.
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
def main():
    # Hareket Değişkenleri
    pTime = 0               # Önceki zaman (FPS için)
    plocX, plocY = 0, 0     # Önceki mouse konumu
    clocX, clocY = 0, 0     # Şimdiki mouse konumu
    
    # Durum Değişkenleri
    last_click_time = 0
    keyboard_active = False 
    last_key_press_time = 0

    # Drag & Drop Değişkenleri
    drag_active = False
    drag_start_time = 0
    drag_offset_x = 0
    drag_offset_y = 0
    
    # Screenshot Değişkenleri
    screenshot_start_time = 0
    screenshot_taken = False
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Parlaklık
    last_bright_dist = 0

    # Kamera Başlatma
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.HandDetector(max_hands=1) # Tek el takibi (Performans için)
    wScr, hScr = pyautogui.size() # Ekran boyutunu al

    print(f"Sistem Başlatıldı: {wCam}x{hCam}")

    while True:
        success, img = cap.read()
        if not success: break
        
        # 1. Görüntüyü İşle
        img = cv2.flip(img, 1) # Ayna etkisi için çevir
        img = detector.findHands(img, draw=False) # İskeleti çizme (FPS artışı)
        lmList = detector.findPosition(img, draw=False)

        # 2. Sabit UI Elemanları
        # Çıkış (X)
        cv2.rectangle(img, (1150, 20), (1250, 70), (0, 0, 255), -1) 
        cv2.putText(img, "X", (1180, 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        
        # Klavye Modu (KB)
        kb_color = (0, 255, 0) if keyboard_active else (100, 100, 100)
        cv2.rectangle(img, (1030, 20), (1130, 70), kb_color, -1) 
        cv2.putText(img, "KB", (1050, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        if keyboard_active: 
            img = drawAll(img, buttonList)

        # 3. El Hareketi Algılama
        if len(lmList) != 0:
            # Kritik Landmark Noktaları
            x1, y1 = lmList[8][1:]   # İşaret Parmağı Ucu
            x2, y2 = lmList[12][1:]  # Orta Parmak Ucu
            x_thumb, y_thumb = lmList[4][1:] # Başparmak Ucu
            x_pinky, y_pinky = lmList[20][1:] # Serçe Parmak Ucu
            x_knuckle, y_knuckle = lmList[5][1:] # İşaret Parmağı Eklem Kökü

            # Sol El Tespiti (Geometrik Yöntem)
            # Flip modunda Başparmak(4), Serçe(20)'den daha sağdaysa (X büyükse) Sol Eldir.
            is_left_hand = x_thumb > x_pinky

            # Parmakların Açık/Kapalı Durumu
            fingers = []
            tips = [4, 8, 12, 16, 20] # Parmak ucu ID'leri
            
            # Başparmak (Sağ/Sol ayrımı)
            if is_left_hand:
                if lmList[tips[0]][1] > lmList[tips[0] - 1][1]: fingers.append(1)
                else: fingers.append(0)
            else:
                if lmList[tips[0]][1] < lmList[tips[0] - 1][1]: fingers.append(1)
                else: fingers.append(0)

            # Diğer 4 Parmak
            for id in range(1, 5):
                if lmList[tips[id]][2] < lmList[tips[id] - 2][2]: fingers.append(1)
                else: fingers.append(0)

            # -------------------------------------------------------------
            # SAĞ EL LOJİĞİ (İmleç, Tıklama, Klavye)
            # -------------------------------------------------------------
            if not is_left_hand:
                
                # Koordinat Dönüşümü (Kamera -> Ekran)
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                
                # Smoothing (Titreme Önleme)
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # A. İmleç Hareketi
                if keyboard_active:
                    # Hayalet İmleç Modu: Gerçek mouse hareket etmez, ekrana çizilir.
                    cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
                elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                     try: pyautogui.moveTo(clocX, clocY)
                     except: pass
                plocX, plocY = clocX, clocY

                # B. Klavye Etkileşimi
                if keyboard_active:
                    for button in buttonList:
                        x, y = button.pos
                        w, h = button.size
                        if x < x1 < x + w and y < y1 < y + h:
                            cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                            
                            dist_click = math.hypot(x2 - x1, y2 - y1)
                            if dist_click < 40 and fingers[1]==1 and fingers[2]==1:
                                if time.time() - last_key_press_time > 0.4:
                                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                                    if button.text == "SPACE": pyautogui.press('space')
                                    else: pyautogui.press(button.text)
                                    last_key_press_time = time.time()

                # C. UI Kontrolleri ve Tıklama
                if fingers[1] == 1 and fingers[2] == 1:
                    dist_click = math.hypot(x2 - x1, y2 - y1)
                    if dist_click < 40:
                        if 1030 < x1 < 1130 and 20 < y1 < 70: # KB Butonu
                            if time.time() - last_click_time > 0.5:
                                keyboard_active = not keyboard_active
                                last_click_time = time.time()
                        elif 1150 < x1 < 1250 and 20 < y1 < 70: # Çıkış
                            break
                        elif not keyboard_active: # Normal Tık
                             if time.time() - last_click_time > 0.3:
                                pyautogui.click()
                                last_click_time = time.time()

                # D. Sürükle Bırak (Yumruk Jesti)
                if not keyboard_active:
                    is_fist = (sum(fingers) == 0)
                    if is_fist:
                        if not drag_active:
                            # Offset hesapla (Sıçramayı önlemek için)
                            curr_mouse_x, curr_mouse_y = pyautogui.position()
                            k_x3_start = np.interp(x_knuckle, (frameR, wCam - frameR), (0, wScr))
                            k_y3_start = np.interp(y_knuckle, (frameR, hCam - frameR), (0, hScr))
                            drag_offset_x = curr_mouse_x - k_x3_start
                            drag_offset_y = curr_mouse_y - k_y3_start
                            pyautogui.mouseDown()
                            drag_active = True
                            drag_start_time = time.time()
                        
                        # Kilit (0.4sn) ve Taşıma
                        if time.time() - drag_start_time < 0.4:
                            cv2.putText(img, "KILITLENDI...", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                        else:
                            k_x3 = np.interp(x_knuckle, (frameR, wCam - frameR), (0, wScr))
                            k_y3 = np.interp(y_knuckle, (frameR, hCam - frameR), (0, hScr))
                            try: pyautogui.moveTo(k_x3 + drag_offset_x, k_y3 + drag_offset_y)
                            except: pass
                            cv2.putText(img, "SURUKLE", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    elif drag_active:
                        pyautogui.mouseUp()
                        drag_active = False
                
                # E. Sağ Tık (3 Parmak)
                if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0 and not keyboard_active:
                     if time.time() - last_click_time > 0.5:
                        pyautogui.rightClick()
                        last_click_time = time.time()
                        cv2.putText(img, "SAG TIK", (x2, y2 - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


            # -------------------------------------------------------------
            # SOL EL LOJİĞİ (Medya Kontrolü)
            # -------------------------------------------------------------
            if is_left_hand:
                
                # A. Ses (Başparmak + İşaret)
                if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[4] == 0:
                     dist_vol = math.hypot(x1 - x_thumb, y1 - y_thumb)
                     cx, cy = (x1 + x_thumb) // 2, (y1 + y_thumb) // 2
                     cv2.line(img, (x_thumb, y_thumb), (x1, y1), (255, 0, 0), 3)
                     cv2.putText(img, "SES", (x1 + 20, y1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                     vol_level = np.interp(dist_vol, [30, 200], [0, 100])
                     set_mac_volume(int(vol_level))

                # B. Parlaklık (Başparmak + Serçe)
                elif fingers[0] == 1 and fingers[4] == 1 and fingers[1] == 0:
                     dist_bright = math.hypot(x_pinky - x_thumb, y_pinky - y_thumb)
                     cv2.line(img, (x_thumb, y_thumb), (x_pinky, y_pinky), (255, 255, 0), 3)
                     cv2.putText(img, "PARLAKLIK", (x_thumb, y_thumb + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                     threshold = 3
                     if last_bright_dist != 0:
                        if dist_bright > last_bright_dist + threshold: change_brightness(increase=True)
                        elif dist_bright < last_bright_dist - threshold: change_brightness(increase=False)
                     last_bright_dist = dist_bright
                else:
                    last_bright_dist = 0

                # C. Screenshot (5 Parmak)
                if sum(fingers) == 5:
                    if screenshot_start_time == 0: screenshot_start_time = time.time()
                    elapsed = time.time() - screenshot_start_time
                    bar = int((elapsed / screenshot_delay) * 200)
                    if bar > 200: bar = 200
                    cv2.rectangle(img, (200, 200), (200 + bar, 230), (255, 0, 0), -1)
                    cv2.rectangle(img, (200, 200), (400, 230), (255, 255, 255), 2)
                    cv2.putText(img, f"SS: {3.0 - elapsed:.1f}sn", (200, 190), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                    
                    if elapsed > screenshot_delay and not screenshot_taken:
                        ts = time.strftime("%Y%m%d-%H%M%S")
                        filename = f"screenshot_{ts}.png"
                        full = os.path.join(desktop_path, filename)
                        try:
                            pyautogui.screenshot(full)
                            os.system("afplay /System/Library/Sounds/Tink.aiff")
                            screenshot_taken = True
                        except Exception as e: print(e)
                    if screenshot_taken:
                        cv2.putText(img, "FOTO CEKILDI!", (200, 280), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                else:
                    screenshot_start_time = 0
                    screenshot_taken = False

        # FPS Göstergesi
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("AI Sanal Kokpit v16.0", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()