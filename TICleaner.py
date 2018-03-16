import os
import configparser
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox


class Config:
    def create_config(self, path):
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "log", "0")

        with open(path, "w") as config_file:
            config.write(config_file)

    def get_config(self, path):
        if not os.path.exists(path):
            self.create_config(path)

        config = configparser.ConfigParser()
        config.read(path)
        return config

    def get_setting(self, path, section, setting):
        config = self.get_config(path)
        value = config.get(section, setting)
        return value

    def update_setting(self, path, section, setting, value):
        config = self.get_config(path)
        config.set(section, setting, value)
        with open(path, "w") as config_file:
            config.write(config_file)

    def delete_setting(self, path, section, setting):
        config = self.get_config(path)
        config.remove_option(section, setting)
        with open(path, "w") as config_file:
            config.write(config_file)


class Clear:
    def __init__(self, path):
        if '' != path:
            self.path = path
            self.clear()
        else:
            App.message(u'Папка не выбрана')

    def clear(self):
        files_path = self.get_folders_and_files()
        if not files_path:
            App.message(u'Файлов TI.ASM не найдено')
        else:
            for file_path in files_path:
                text = ''
                with open(file_path, 'r', encoding="cp866") as file:
                    for line in file:
                        if ';@U' not in line:
                            if '@U' in line:
                                if u'РК' not in line:
                                    if u'а' not in line:
                                        line = ';' + line
                        text = text + line
                with open(file_path, 'w', encoding="cp866") as file:
                    file.write(text)
            App.message(u'Очищено файлов: ' + str(len(files_path)))

    def get_folders_and_files(self):
        files_path = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(('.asm', '.ASM')):
                    if file.startswith(('TI', 'ti')):
                        files_path.append(os.path.join(root, file))
        return files_path


class App(Config):
    def __init__(self, root):
        self.root = root
        self.menu()
        self.elements()

    def menu(self):
        self.root.option_add('*tearOff', False)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file = Menu(menubar)
        tools = Menu(menubar)
        about = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=tools, label=u'Опции')
        menubar.add_cascade(menu=about, label=u'?')

        file.add_command(label=u'Выбрать папку...', command=self.get_path_dir)
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.root.destroy)

        tools.add_command(label=u'Настройки',  command=self.top_level_window_for_settings)

        about.add_command(label=u'О программе', command=self.top_level_window_for_about)

    def elements(self):

        frame = Frame(self.root)
        frame.pack(pady=10)

        label = ttk.Label(frame, text=u'Выбрать папку c файлами TI.ASM')
        label.grid(sticky='w', row=0, column=0, columnspan=4)

        self.contents = StringVar()
        entry = ttk.Entry(frame, width=30, textvariable=self.contents)
        entry.grid(row=1, column=0, columnspan=3)

        button1 = ttk.Button(frame, text=u'Выбрать', width=10, command=lambda: self.get_path_dir())
        button1.grid(row=1, column=3)

        button2 = ttk.Button(frame, text=u'Очистить', command=lambda: Clear(self.contents.get()))
        button2.grid(pady=15, row=2, column=0, columnspan=4)

    def top_level_window_for_about(self):
        win = Toplevel(self.root)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'О программе')
        center(win, 200, 100, 0)

        frame = Frame(win)
        frame.pack(pady=10)

        label1 = ttk.Label(frame, text=u'TICleaner v0.1.3 Win7 (32-bit)')
        label2 = ttk.Label(frame, text=u'Автор: Манжак С.С.')
        label3 = ttk.Label(frame, text=u'Контакты: manzhak.ru')

        label1.grid(sticky='w', row=0, column=0)
        label2.grid(sticky='w', row=1, column=0)
        label3.grid(sticky='w', row=2, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def top_level_window_for_settings(self):
        win = Toplevel(self.root)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'Настройки')
        center(win, 200, 100, 0)

        frame = Frame(win)
        frame.pack(pady=10)

        check_var = IntVar()
        check = Checkbutton(frame, text=u'Включить логирование', variable=check_var, onvalue=1, offvalue=0)
        if '1' == self.get_setting("settings.ini", "Settings", "log"):
            check.select()
        check.grid(sticky='w', row=0, column=0)

        button = ttk.Button(frame, text=u'Сохранить', command=lambda: self.update_setting("settings.ini", "Settings", "log", str(check_var.get())))
        button.grid(sticky='s', row=1, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def get_path_dir(self):
        path = askdirectory()
        self.contents.set(path)

    @staticmethod
    def message(text):
        messagebox.showinfo(title=u'Сообщение', message=text)


def center(root, width, height, offset):
    x = root.winfo_screenwidth()/2-width/2+offset
    y = root.winfo_screenheight()/2-height/2+offset
    root.geometry('{}x{}+{}+{}'.format(width, height, round(x), round(y)))


def main():
    root = Tk()
    center(root, 300, 130, 0)
    root.title(u'TICleaner 0.1.3')
    root.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
