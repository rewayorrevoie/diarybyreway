#импортировал всю информацию из книжек бурмалды 

import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os
import json

# вот это вот хренотень нужна для того что б сохранять мысли на SSD или HDD
SAVE_DIR = os.path.expanduser('~/MyDiary')
os.makedirs(SAVE_DIR, exist_ok=True)
DIARY_FILE = os.path.join(SAVE_DIR, 'thoughts.md')
CONFIG_FILE = os.path.join(SAVE_DIR, "config.json")


class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Личный дневник")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e2e')

        self.bg_image_path = None
        self.bg_photo = None

        # кнопочки на топе
        toolbar = tk.Frame(root, bg='#181825', height=40)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        btn_style = {"bg": "#313244", "fg": "#cdd6f4", "bd": 0, "padx": 12, "pady": 6, "font": ("Consolas", 10)}

        tk.Button(toolbar, text="Сохранить запись (Ctrl+S)", command=self.save_entry, **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Картинка в угол", command=self.choose_image, **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Открыть файл записей", command=self.open_diary_file, **btn_style).pack(side=tk.RIGHT, padx=5, pady=5)

        self.canvas = tk.Canvas(root, bg='#1e1e2e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(
            self.canvas,
            bg='#1e1e2e',
            fg="#cdd6f4",
            insertbackground="#f5e0dc",
            font=("Consolas", 12),
            bd=0,
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        self.text_window = self.canvas.create_window(0, 0, anchor="nw", window=self.text_area)

        # метка label для картинки в правом нижнем углу
        self.corner_label = tk.Label(self.canvas, bg="#1e1e2e", bd=0)
        self.corner_window = self.canvas.create_window(800, 560, anchor="se", window=self.corner_label)

        self.canvas.bind("<Configure>", self.on_resize)

        # подгружаем сохранённую картинку при старте
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.apply_image(data.get("corner_image"))
            except Exception as e:
                print("Ошибка чтения config.json:", e)

        # горячая клавиша Ctrl+S (на любой раскладке)
        self.root.bind("<Control-Key>", self.on_ctrl_key)

    def on_ctrl_key(self, event):
        if event.keycode == 83:
            self.save_entry()

    def on_resize(self, event):
        self.canvas.itemconfig(self.text_window, width=event.width, height=event.height)
        self.canvas.coords(self.corner_window, event.width - 15, event.height - 15)

    def apply_image(self, path):
        if not path or not os.path.exists(path):
            return
        self.bg_image_path = path
        img = Image.open(path)
        img.thumbnail((220, 220), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)

        self.corner_label.config(image=self.bg_photo)
        self.corner_label.lift()
        self.canvas.tag_raise(self.corner_window)
        self.root.update_idletasks()

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Выберите картинку",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if not path:
            return

        self.apply_image(path)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"corner_image": path}, f, ensure_ascii=False, indent=2)

    def save_entry(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Пусто", "Напишите хотя бы пару слов")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_entry = f"\n## [{timestamp}]\n{content}\n\n---\n"

        with open(DIARY_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_entry)

        self.text_area.delete("1.0", tk.END)
        messagebox.showinfo("Готово", f"Запись сохранена в:\n{DIARY_FILE}")

    def open_diary_file(self):
        if os.path.exists(DIARY_FILE):
            if os.name == "nt":
                os.startfile(DIARY_FILE)
            else:
                os.system(f"xdg-open '{DIARY_FILE}'")
        else:
            messagebox.showinfo("Инфо", "Записей пока нет")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()
