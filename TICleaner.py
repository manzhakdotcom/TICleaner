import os
import configparser
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.path = 'settings.ini'
        self.section = 'Settings'
        self.settings = {'log': '0', 'path': os.getcwd()}

    def is_file(self):
        if not os.path.exists(self.path):
            return False
        else:
            return True

    def is_section(self):
        if self.config.has_section(self.section):
            return True
        else:
            return False

    def is_option(self):
        for option, value in self.settings.items():
            if self.config.has_option(self.section, option):
                continue
            else:
                return False
        return True

    def create_file_settings(self):
        self.config.add_section(self.section)
        for option, value in self.settings.items():
            self.config.set(self.section, option, value)
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def get_configs(self):
        if not self.is_file():
            self.create_file_settings()
            return self.config.items(self.section)
        elif not self.is_section():
            self.config.add_section(self.section)
        elif not self.is_option():
            for option, value in self.settings.items():
                if self.config.has_option(self.section, option):
                    print('is', self.config.get(self.section, option))
                    continue
                else:
                    self.config.set(self.section, option, value)
            with open(self.path, "a") as config_file:
                self.config.write(config_file)
        else:
            return self.config.read(self.path)


    def create_configs(self, path):
        config = configparser.ConfigParser()
        config.add_section(self.section)
        for option in self.options:
            for value in self.values:
                print(option, value)
                config.set(self.section, option, value)
        with open(path, "w") as config_file:
            config.write(config_file)



    def get_setting(self, path, section, option):
        config = self.get_config(path)
        if not config.has_option(section, option):
            config.set(section, option, '')
        value = config.get(section, option)
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
            message(u'Папка не выбрана')

    def clear(self):
        files_path = self.get_folders_and_files()
        if not files_path:
            message(u'Файлов TI.ASM не найдено')
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
            message(u'Очищено файлов: ' + str(len(files_path)))

    def get_folders_and_files(self):
        files_path = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(('.asm', '.ASM')):
                    if file.startswith(('TI', 'ti')):
                        files_path.append(os.path.join(root, file))
        return files_path


class Logs:
    pass


class App:
    def __init__(self, root):
        self.config = Config()
        self.root = root
        self.menu()
        self.setting_path = StringVar()
        self.contents = StringVar()
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

        tools.add_command(label=u'Настройки',  command=self.top_level_settings)

        about.add_command(label=u'О программе', command=self.top_level_about)

    def elements(self):

        frame = Frame(self.root)
        frame.pack(pady=10)

        label = ttk.Label(frame, text=u'Выбрать папку c файлами TI.ASM')
        label.grid(sticky='w', row=0, column=0, columnspan=4)

        entry = ttk.Entry(frame, width=30, textvariable=self.contents)
        entry.grid(row=1, column=0, columnspan=3)

        button1 = ttk.Button(frame, text=u'Выбрать', width=10, command=lambda: self.get_path_dir())
        button1.grid(row=1, column=3)

        button2 = ttk.Button(frame, text=u'Очистить', command=lambda: Clear(self.contents.get()))
        button2.grid(ipadx=10, ipady=10, pady=15, row=3, column=0, columnspan=4)

    def top_level_about(self):
        win = Toplevel(self.root)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'О программе')
        center(win, 200, 100, 0)

        frame = Frame(win)
        frame.pack(pady=10)

        label1 = ttk.Label(frame, text=u'TICleaner', font='size=18')
        label2 = ttk.Label(frame, text=u'Автор © 2018 Манжак С.С.')
        label3 = ttk.Label(frame, text=u'Версия v0.1.3 Win7 (32-bit)')

        label1.grid(row=0, column=0, pady=10)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def top_level_settings(self):
        win = Toplevel(self.root)
        center(win, 270, 170, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'Настройки')

        label_frame = LabelFrame(win, text='Включить логфайл', padx=10, pady=10)
        label_frame.pack(pady=10, padx=10)

        frame = Frame(win)
        frame.pack()

        check_var = IntVar()
        check = Checkbutton(label_frame, text=u'Включить логирование', variable=check_var, onvalue=1, offvalue=0)
        #if '1' == self.config.get_setting("settings.ini", "Settings", "log"):
            #check.select()
        check.grid(sticky='w', row=0, column=0)

        label = ttk.Label(label_frame, text=u'Выбрать папку для логов')
        label.grid(sticky='w', row=1, column=0)

        entry = ttk.Entry(label_frame, width=25, textvariable=self.setting_path)
        #if '' != self.config.get_setting("settings.ini", "Settings", "path"):
            #self.setting_path.set(self.config.get_setting("settings.ini", "Settings", "path"))
        entry.grid(sticky='w', row=2, column=0, columnspan=2)

        button1 = ttk.Button(label_frame, text=u'...', width=10, command=lambda: self.get_path_setting_dir())
        button1.grid(sticky='w', row=2, column=2)

        button2 = ttk.Button(frame, text=u'Сохранить', command=lambda: print(self.config.get_configs()))
        button2.grid(sticky='se', row=0, column=0, columnspan=3)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def save_settings(self, settings):
        self.config.update_setting("settings.ini", "Settings", "log", settings['log'])
        self.config.update_setting("settings.ini", "Settings", "path", settings['path'])

    def get_path_dir(self):
        path = askdirectory()
        self.contents.set(path)

    def get_path_setting_dir(self):
        path = askdirectory()
        self.setting_path.set(path)


def message(text):
    messagebox.showwarning(title=u'Сообщение', message=text)


def center(root, width, height, offset):
    x = root.winfo_screenwidth()/2-width/2+offset
    y = root.winfo_screenheight()/2-height/2+offset
    root.geometry('{}x{}+{}+{}'.format(width, height, round(x), round(y)))


def main():
    root = Tk()
    center(root, 300, 150, 0)
    root.title(u'TICleaner 0.1.3')
    root.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
