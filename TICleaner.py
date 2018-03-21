from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox
import configparser
import os



class Config:
    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path)
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
        if not self.is_section():
            self.config.add_section(self.section)
        for option, value in self.settings.items():
            self.config.set(self.section, option, value)
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def get_config_option(self, option):
        if not self.is_file() or not self.is_section() or not self.is_option():
            self.create_file_settings()
        return self.config.get(self.section, option)

    def update_config_options(self, settings):
        for option, value in settings.items():
            self.config.set(self.section, option, str(value))
        with open(self.path, "w") as config_file:
            self.config.write(config_file)


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
            logs = ''
            for file_path in files_path:
                text = ''
                with open(file_path, 'r', encoding="cp866") as file:
                    tu = 0
                    log = None
                    for line in file:
                        if '@BEGIN' in line:
                            log = self.get_name_station(line)
                        if ';@U' not in line:
                            if '@U' in line:
                                if u'РК' not in line:
                                    if u'а' not in line:
                                        line = ';' + line
                                        tu += 1
                        text = text + line
                logs = logs + log + ' - ' + str(tu) + u' импульсов ТУ закомментировано\n'
                with open(file_path, 'w', encoding="cp866") as file:
                    file.write(text)
            message(u'Очищено файлов: ' + str(len(files_path)))
            Logs(logs)

    def get_name_station(self, line):
        text = line
        return text[8:-2]

    def get_folders_and_files(self):
        files_path = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(('.asm', '.ASM')):
                    if file.startswith(('TI', 'ti')):
                        files_path.append(os.path.join(root, file))
        return files_path


class Logs:
    def __init__(self, logs):
        self.config = Config()
        self.write_file(logs)

    def write_file(self, logs):
        if int(self.get_log()):
            if not os.path.exists(self.file_path()):
                os.makedirs(self.file_path())
            with open(self.file_path() + self.file_name() + '.log', 'w') as file:
                file.write(logs)

    def file_path(self):
        return self.get_path() + os.sep + 'logs' + os.sep

    def get_path(self):
        path = self.config.get_config_option('path')
        return path

    def get_log(self):
        log = self.config.get_config_option('log')
        return log

    def file_name(self):
        from datetime import datetime
        return u'TICleaner-log-' + datetime.now().strftime('%Y-%m-%d_%H.%M.%S')


class App:
    def __init__(self, root):
        self.root = root
        self.root.bind('<F1>', self.top_level_about)
        self.root.bind('<Control-q>', self.close)
        self.menu()
        self.setting_path = StringVar()
        self.contents = StringVar()
        self.check_var = IntVar()
        self.elements()

    def menu(self):
        self.root.option_add('*tearOff', False)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file = Menu(menubar)
        tools = Menu(menubar)
        about = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=tools, label=u'Настройки')
        menubar.add_cascade(menu=about, label=u'?')

        file.add_command(label=u'Выбрать папку...', command=self.get_path_dir)
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.close, accelerator="Ctrl+Q")

        tools.add_command(label=u'Параметры...',  command=self.top_level_settings)

        about.add_command(label=u'О программе', command=self.top_level_about, accelerator="F1")

    def close(self, event=None):
        self.root.destroy()

    def elements(self):
        frame = Frame(self.root)
        label = ttk.Label(frame, text=u'Выбрать папку c файлами TI.ASM')
        entry = ttk.Entry(frame, width=30, textvariable=self.contents)
        button1 = ttk.Button(frame, text=u'Выбрать', width=10, command=lambda: self.get_path_dir())
        button2 = ttk.Button(frame, text=u'Очистить', command=lambda: Clear(self.contents.get()))

        frame.pack(pady=10)
        label.grid(sticky='w', row=0, column=0, columnspan=4)
        entry.grid(row=1, column=0, columnspan=3)
        button1.grid(row=1, column=3)
        button2.grid(ipadx=10, ipady=10, pady=15, row=3, column=0, columnspan=4)

    def top_level_about(self, event=None):
        win = Toplevel(self.root)
        win.resizable(0, 0)
        center(win, 220, 100, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'О программе')

        frame = Frame(win)
        frame.pack(pady=10)

        label1 = Label(frame, text=u'TICleaner', font='size=18')
        label2 = Label(frame, text=u'Автор © 2018 Манжак С.С.')
        label3 = Label(frame, text=u'Версия v0.1.5 Win32')

        label1.grid(row=0, column=0, pady=10)
        label2.grid(row=1, column=0)
        label3.grid(row=2, column=0)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def top_level_settings(self):
        config = Config()
        win = Toplevel(self.root)
        win.resizable(0, 0)
        center(win, 270, 170, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
        win.title(u'Параметры...')

        self.check_var.set(config.get_config_option('log'))
        self.setting_path.set(config.get_config_option('path'))

        label_frame = LabelFrame(win, text=u'Включить логфайл', padx=10, pady=10)
        frame = Frame(win)

        check = Checkbutton(label_frame, text=u'Включить логирование', variable=self.check_var, onvalue=1, offvalue=0)
        if int(self.check_var.get()):
            check.select()

        label = ttk.Label(label_frame, text=u'Выбрать папку для логов')
        entry = ttk.Entry(label_frame, width=25, textvariable=self.setting_path)
        button1 = ttk.Button(label_frame, text=u'...', command=lambda: self.get_path_setting_dir())
        button2 = ttk.Button(frame, text=u'Сохранить', command=lambda: self.save_settings(config))

        label_frame.pack(pady=10, padx=10, fill='x')
        frame.pack(side='right', fill='x', padx=10, pady=0)
        check.grid(sticky='w', row=0, column=0)
        label.grid(sticky='w', row=1, column=0)
        entry.grid(sticky='w', row=2, column=0, columnspan=2)
        button1.grid(sticky='w', row=2, column=2)
        button2.grid(sticky='n', row=0, column=0, columnspan=3)

        win.focus_set()
        win.grab_set()
        win.wait_window()

    def save_settings(self, config):
        settings = {'path': self.setting_path.get(), 'log': self.check_var.get()}
        config.update_config_options(settings)

    def get_path_dir(self):
        path = askdirectory(initialdir=os.getcwd())
        if '' != path.strip():
            self.contents.set(path)

    def get_path_setting_dir(self):
        path = askdirectory(initialdir=os.getcwd())
        if '' != path.strip():
            self.setting_path.set(path)


def message(text):
    messagebox.showwarning(title=u'Сообщение', message=text)


def center(root, width, height, offset):
    x = root.winfo_screenwidth()/2-width/2+offset
    y = root.winfo_screenheight()/2-height/2+offset
    root.geometry('{}x{}+{}+{}'.format(width, height, round(x), round(y)))


def main():
    root = Tk()
<<<<<<< HEAD
    
    root.geometry('300x130+500+200')
    root.title(u'TICleaner')
=======
    root.resizable(0, 0)
    center(root, 300, 150, 0)
    root.title(u'TICleaner 0.1.5')
>>>>>>> release/v0.1.5
    root.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
    app = App(root)

    root.mainloop()


if __name__ == '__main__':
    main()
