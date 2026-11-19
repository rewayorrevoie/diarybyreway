#импортировал всю информацию из книжек бурмалды 

import tkinter as tk 
from tkinter import filedialog, messagebox
from datetime import datetime 
from PIL import Image, ImageTk 
import os 

#импортировал всю информацию из книжек бурмалды 

#вот это вот хренотень нужна для того что б сохронять ваши самые мерзкие желания в ссдшник пк НУ ИЛИ ЕСЛИ ВЫ БОМЖ КАК И Я ТО НА ЖЕСТКИЙ ДИСК 

SAVE_DIR = os.path.expanduser('~/MyDiary')
os.makedirs(SAVE_DIR, exist_ok=True)
DIARY_FILE = os.path.join(SAVE_DIR, 'thoughts.md')

#вот это вот хренотень нужна для того что б сохронять ваши самые мерзкие желания в ссдшник пк НУ ИЛИ ЕСЛИ ВЫ БОМЖ КАК И Я ТО НА ЖЕСТКИЙ ДИСК



class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Личный дневник")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e2e') #уголек на фоне,мы типо тру хатскеры

        self.bg_image_path = None
        self.bg_photo = None


        #кнопочки на топе
        toolbar = tk.Frame(root, bg='#181825', height=40)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        btn_style = {"bg": "#313244", "fg": "#cdd6f4", "bd": 0, "padx": 12, "pady": 6, "font": ("Consolas", 10)}


        tk.Button(toolbar, text="Сохранить запись (Ctrl+S)", command=self.save_entry, **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Картинка в угол", command=self.choose_image, **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Открыть файл записей", command=self.open_diary_file, **btn_style).pack(side=tk.RIGHT, padx=5, pady=5)

        #кнопочки на топе (Я УСТАЛ БОСС)



        self.canvas = tk.Canvas(root, bg='#1e1e2e', highlightthickness=0)   #тут короче холст и бла бла
        self.canvas.pack(fill=tk.BOTH, expand=True)


        #а тут текстовое поле и тумба юмба

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



        #текстовое поле по верху холста 

        self.text_window = self.canvas.create_window(0, 0, anchor="nw", window=self.text_area)



        #метка label для картинок с аниме девчатами
        self.corner_label = tk.Label(self.canvas, bg = "#1e1e2e", bd=0)
        self.corner_window = self.canvas.create_window(800, 560, anchor="se", window=self.corner_label)


        #передергиваем позиции да бы при изменении размера окна все было норм
        self.canvas.bind("<Configure>", self.on_resize)

        #горячая штучка для сейва 
        self.root.bind("<Control-s>", lambda event: self.save_entry())


    def on_resize(self, event):
        #растяг на все окно
        self.canvas.itemconfig(self.text_window, width=event.width, height=event.height)
        #ротейтим тянку на правый нижний угол
        self.canvas.coords(self.corner_window, event.width - 15, event.height - 15)

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Выберите картинку",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif *.webp")]
        )
        if not path:
            return

        self.bg_image_path = path
        img = Image.open(path)

        #МАСШТАБИРУЕМ СУКААААААААААА
        img.thumbnail((220, 220), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(img)

        self.corner_label.config(image=self.bg_photo)
        self.corner_label.lift()


    def save_entry(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwaring("Пусто", "Напишите хоя бы пару слов")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H :%M:%S")
        formatted_entry = f"\n## [{timestamp}]\n{content}\n\n---\n"

        #append на ссд,честно хз как это вам пояснить в этом комменте поэтоу похуй
        with open(DIARY_FILE, "a", encoding="UTF-8") as f:
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





        





