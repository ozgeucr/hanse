import platform
import os

# İşletim sistemini tespit et
SYSTEM_OS = platform.system() # 'Darwin' (Mac) veya 'Windows' döner
# --- OS ENTEGRASYONU ---
def change_brightness(increase=True):
    """AppleScript kullanarak macOS parlaklık tuşlarını (F1/F2) simüle eder."""
    key_code = 144 if increase else 145
    os.system(f"osascript -e 'tell application \"System Events\" to key code {key_code}'")

def set_mac_volume(vol_level):
    """AppleScript ile sistem ses seviyesini ayarlar (0-100)."""
    cmd = f"osascript -e 'set volume output volume {vol_level}'"
    os.system(cmd)
