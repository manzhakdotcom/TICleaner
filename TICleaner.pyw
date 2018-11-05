# coding: utf-8
import os
try:
    from Tkinter import *
    from tkFileDialog import *
    import tkMessageBox as messagebox
    import ConfigParser as configparser
    import codecs
except ImportError:
    from tkinter import *
    from tkinter.filedialog import *
    from tkinter import messagebox
    import configparser


class Config:
    def __init__(self):
        self.path = 'settings.ini'
        self.config = configparser.ConfigParser()
        if self.is_file(self.path):
            self.config.read(self.path)
            if not self.is_section('Settings'):
                self.config['Settings'] = {'log': '0', 'path': os.getcwd()}
        else:
            self.config['Settings'] = {'log': '0', 'path': os.getcwd()}

    def is_file(self, path):
        if not os.path.exists(path):
            return False
        else:
            return True

    def is_section(self, section):
        if self.config.has_section(section):
            return True
        else:
            return False

    def is_option(self, section, option):
        if self.config.has_option(section, option):
            return True
        else:
            return False

    def get_config_option(self, section, option):
        return self.config.get(section, option)

    def update_config_options(self, section, settings):
        for option, value in settings.items():
            self.config.set(section, option, str(value))
        with open(self.path, "w") as config_file:
            self.config.write(config_file)


class Clear:
    def __init__(self, path):
        if '' != path:
            self.path = path
            self.clear()
        else:
            messagebox.showwarning(u'Предупреждение', u'Папка не выбрана.')

    def clear(self):
        files_path = self.get_folders_and_files()
        if not files_path:
            messagebox.showwarning(u'Предупреждение', u'Файлов TI.ASM не найдено')
        else:
            logs = ''
            for file_path in files_path:
                file_name = os.path.basename(file_path)
                text = ''
                try:
                    file = open(file_path, 'r', encoding="cp866")
                except TypeError:
                    file = codecs.open(file_path, 'r', encoding="cp866")
                tu = 0
                station = u'Название файла'
                for line in file:
                    if '@BEGIN' in line:
                        station = self.get_name_station(line)
                    if ';@U' not in line:
                        if '@U' in line:
                            if u'РК' not in line:
                                if u'а' not in line:
                                    line = ';' + line
                                    tu += 1
                    text = text + line
                file.close()
                logs = logs + station.replace("'", "") + ' ' + str(file_name[2:-4]) + ' - ' + str(tu) + u' импульсов ТУ закомментировано\n'
                try:
                    file = open(file_path, 'w', encoding="cp866")
                except TypeError:
                    file = codecs.open(file_path, 'w', encoding="cp866")
                file.write(text)
                file.close()
            messagebox.showinfo(u'Сообщение', u'Очищено файлов: [ ' + str(len(files_path)) + ' ].')
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
        if self.get_log():
            if not os.path.exists(self.file_path()):
                os.makedirs(self.file_path())
            try:
                file = open(self.file_path() + self.file_name() + '.log', 'w', encoding="cp1251")
            except TypeError:
                file = codecs.open(self.file_path() + self.file_name() + '.log', 'w', encoding="cp1251")
            file.write(logs)
            file.close()
            messagebox.showinfo(u'Сообщение', u'Логфайл с результатами работы программы записан в файл:\n'
                                + self.file_path()
                                + self.file_name()
                                + '.log')

    def file_path(self):
        return self.get_path() + os.path.sep + 'logs' + os.path.sep

    def get_path(self):
        return self.config.get_config_option('Settings', 'path')

    def get_log(self):
        return int(self.config.get_config_option('Settings', 'log'))

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

        tools.add_command(label=u'Параметры...', command=self.top_level_settings)

        about.add_command(label=u'О программе', command=self.top_level_about, accelerator="F1")

    def close(self, event=None):
        self.root.destroy()

    def elements(self):
        frame = Frame(self.root)
        label = Label(frame, text=u'Папка c файлами TI.ASM')
        entry = Entry(frame, width=30, textvariable=self.contents)
        button1 = Button(frame, text=u'Выбрать', width=10, command=lambda: self.get_path_dir())
        button2 = Button(frame, text=u'Очистить', command=lambda: Clear(self.contents.get()))

        frame.pack(pady=10)
        label.grid(sticky='w', row=0, column=0, columnspan=4)
        entry.grid(row=1, column=0, columnspan=3)
        button1.grid(row=1, column=3)
        button2.grid(ipadx=10, ipady=10, pady=15, row=3, column=0, columnspan=4)

    def top_level_about(self, event=None):
        win = Toplevel(self.root)
        win.resizable(0, 0)
        center(win, 220, 150, 0)
        win.iconbitmap(os.getcwd() + os.path.sep + u'icon.ico')
        win.title(u'О программе')

        frame = Frame(win)
        frame.pack(pady=10)

        label1 = Label(frame, text=u'Программа TICleaner\nкомментирует строки с\nимпульсами ТУ.')
        label2 = Label(frame, text=u'Автор © Манжак С.С.')
        label3 = Label(frame, text=u'Версия v' + self.root.version + u' Win 32')

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
        win.iconbitmap(os.getcwd() + os.path.sep + 'icon.ico')
        win.title(u'Параметры...')

        self.check_var.set(config.get_config_option('Settings', 'log'))
        self.setting_path.set(config.get_config_option('Settings', 'path'))

        label_frame = LabelFrame(win, text=u'Включить логфайл', padx=10, pady=10)
        frame = Frame(win)

        check = Checkbutton(label_frame, text=u'Включить логирование', variable=self.check_var, onvalue=1, offvalue=0)
        if int(self.check_var.get()):
            check.select()

        label = Label(label_frame, text=u'Выбрать папку для логов')
        entry = Entry(label_frame, width=25, textvariable=self.setting_path)
        button1 = Button(label_frame, text=u'...', command=lambda: self.get_path_setting_dir())
        button2 = Button(frame, text=u'Сохранить', command=lambda: self.save_settings(config, win))

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

    def save_settings(self, config, win):
        settings = {'path': self.setting_path.get(), 'log': self.check_var.get()}
        config.update_config_options('Settings', settings)
        win.destroy()

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
    x = round(root.winfo_screenwidth() / 2 - width / 2 + offset)
    y = round(root.winfo_screenheight() / 2 - height / 2 + offset)
    root.geometry('{}x{}+{}+{}'.format(width, height, int(x), int(y)))


def main():
    root = Tk()
    root.version = '0.1.9'
    root.resizable(0, 0)
    center(root, 300, 150, 0)
    root.title(u'TICleaner')
    root.iconbitmap(os.getcwd() + os.path.sep + 'icon.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
