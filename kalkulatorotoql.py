import pytesseract
import pyautogui
import tkinter as tk
import re
import os

# Path ke tesseract
tesseract_path = os.path.join(os.path.dirname(__file__), 'Tesseract-OCR', 'tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

class AreaDeteksiTransparan(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("210x70+300+300")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.3)
        self.config(bg="black")

        self._offsetx = 0
        self._offsety = 0
        self.bind("<Button-1>", self.click_mouse)
        self.bind("<B1-Motion>", self.drag_mouse)

    def click_mouse(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def drag_mouse(self, event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f"+{x}+{y}")

class MenuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300+800+300")
        self.title("OCR Kalkulator ESP Style")
        self.config(bg="lightyellow")
        self.attributes("-topmost", True)

        self.deteksi_window = AreaDeteksiTransparan(self)
        self.running = False

        self.label_operasi = tk.Label(self, text="Operasi: --", font=("Arial", 14), bg="lightyellow")
        self.label_operasi.pack(pady=(10,5), padx=10)

        self.label_hasil = tk.Label(self, text="Hasil: --", font=("Arial", 16, "bold"), fg="darkblue", bg="lightyellow")
        self.label_hasil.pack(pady=5, padx=10)

        self.label_bilangan = tk.Label(self, text="Bilangan terdeteksi: --", font=("Arial", 12), bg="lightyellow")
        self.label_bilangan.pack(pady=5, padx=10)

        btn_frame = tk.Frame(self, bg="lightyellow")
        btn_frame.pack(pady=10)

        self.cek_btn = tk.Button(btn_frame, text="CEK", command=self.cek_deteksi, width=10)
        self.cek_btn.grid(row=0, column=0, padx=5)

        self.play_btn = tk.Button(btn_frame, text="PLAY", command=self.start_looping, width=10, bg="lightgreen")
        self.play_btn.grid(row=0, column=1, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="STOP", command=self.stop_looping, width=10, bg="tomato")
        self.stop_btn.grid(row=0, column=2, padx=5)

        self.exit_btn = tk.Button(self, text="EXIT", command=self.exit_app, width=15)
        self.exit_btn.pack(pady=(10, 5))

    def screenshot_area(self):
        geo = self.deteksi_window.geometry()
        parts = re.split('[x+]', geo)

        if len(parts) != 4:
            print("[ERROR] Format geometry salah:", geo)
            return None

        w, h, x, y = map(int, parts)
        region = (x, y, w, h)
        screenshot = pyautogui.screenshot(region=region)

        config = '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789+-*/().= '
        text = pytesseract.image_to_string(screenshot, config=config).strip()

        # Koreksi karakter umum
        text = text.replace(' ', '')
        text = text.replace('l', '1').replace('I', '1').replace('|', '1')
        text = text.replace('O', '0').replace('o', '0')
        text = text.replace('–', '-').replace('—', '-').replace('÷', '/')
        text = text.replace('x', '*').replace('X', '*')

        return text

    def cek_deteksi(self):
        teks = self.screenshot_area()
        if teks:
            self.label_operasi.config(text=f"[CEK] Operasi: {teks}")

            match = re.match(r'^(.+?)=([\d\.]+)$', teks)
            if match:
                operasi = match.group(1)
                hasil_di_layar = match.group(2)
                self.label_hasil.config(text=f"[ABA] Diabaikan (hasil: {hasil_di_layar})")
                angka = re.findall(r'[\d\.]+', operasi)
                angka_join = " ".join(angka) if angka else "--"
                self.label_bilangan.config(text=f"[ABA] Bilangan terdeteksi: {angka_join}")
                return

            if '=' in teks:
                teks = teks.split('=')[0]

            teks = re.sub(r'[+\-*/.]$', '', teks)
            tokens = re.findall(r'(\d+(?:\.\d+)?|[+\-*/])', teks)
            angka_awal = None
            operator = None
            angka_akhir = None

            for token in tokens:
                if angka_awal is None and re.match(r'\d', token):
                    angka_awal = token
                elif operator is None and token in "+-*/":
                    operator = token
                elif angka_akhir is None and re.match(r'\d', token):
                    angka_akhir = token
                if angka_awal and operator and angka_akhir:
                    break

            if angka_awal and operator and angka_akhir:
                try:
                    ekspresi = f"{angka_awal}{operator}{angka_akhir}"
                    hasil = eval(ekspresi)
                    self.label_hasil.config(text=f"[CEK] Hasil: {hasil}")
                    self.label_bilangan.config(text=f"[CEK] Bilangan: {angka_awal} dan {angka_akhir}")
                except:
                    self.label_hasil.config(text="[CEK] Hasil: Error")
                    self.label_bilangan.config(text="[CEK] Bilangan: --")
            else:
                self.label_hasil.config(text="[CEK] Hasil: --")
                self.label_bilangan.config(text="[CEK] Bilangan: Tidak lengkap")
        else:
            self.label_operasi.config(text="[CEK] Operasi: --")
            self.label_hasil.config(text="[CEK] Hasil: --")
            self.label_bilangan.config(text="[CEK] Bilangan terdeteksi: --")

        if self.running:
            self.after(1000, self.cek_deteksi)

    def start_looping(self):
        if not self.running:
            self.running = True
            self.cek_deteksi()

    def stop_looping(self):
        self.running = False

    def exit_app(self):
        self.running = False
        self.deteksi_window.destroy()
        self.destroy()

if __name__ == "__main__":
    app = MenuApp()
    app.mainloop()
