import os
import json
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox


def get_settings_from_config_file():
    if os.path.isfile('config.json'):
        with open('config.json', 'r', encoding="utf-8") as file:
            json_data = file.read()
        return json.loads(json_data)
    else:
        App.message('Нет файла конфигурации')


def get_setting_source_path_from_config_file(settings):
    path = settings['sourcePath']
    if '' != path:
        return path
    else:
        App.message('Путь пустой')


def get_list_of_folders(path):
    items = os.listdir(path)
    folders = []
    for item in items:
        if -1 == item.find('.'):
            folders.append(item)
    return folders


def get_list_of_folders_path(path):
    folders = get_list_of_folders(path)
    folders_path = []
    for folder in folders:
        folder_path = path + os.sep + folder
        if os.path.isdir(folder_path):
            folders_path.append(folder_path)
    return folders_path


def get_ti_path_file_from_folders(path):
    folders_path = get_list_of_folders_path(path)
    folders = get_list_of_folders(path)
    files_path = []
    for folder_path, folder in zip(folders_path, folders):
        file_path = folder_path + os.sep + 'TI' + folder + '.asm'
        if os.path.isfile(file_path):
            files_path.append(folder_path + os.sep + 'TI' + folder + '.asm')
    return files_path


def open_and_change_ti_files(path):
    files_path = get_ti_path_file_from_folders(path)
    for file_path in files_path:
        text = ''
        with open(file_path, 'r', encoding="OEM") as file:
            for line in file:
                if ';@U' not in line:
                    if '@U' in line:
                        if 'РК' not in line:
                            if 'а' not in line:
                                line = ';' + line
                text = text + line
        with open(file_path, 'w', encoding="OEM") as file:
            file.write(text)


def parsing_files_tiasm_in_folders_of_tables(path):
    #settings = get_settings_from_config_file()
    #path = get_setting_source_path_from_config_file(settings)
    open_and_change_ti_files(path)


class App:
    def __init__(self, root):
        self.root = root
        self.menu()
        self.frames()
        self.buttons()

    def menu(self):
        self.root.option_add('*tearOff', False)
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file = Menu(menubar)
        tools = Menu(menubar)
        help_ = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=tools, label=u'Инструменты')
        menubar.add_cascade(menu=help_, label=u'Справка')

        file.add_command(label=u'Открыть папку', command=self.get_path_dir)
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.root.destroy)

        tools.add_command(label=u'Открыть логфайл', command=lambda:self.message('Логфайла нет'))

        help_.add_command(label=u'О программе', command=lambda:self.message('Автор: Манжак С.С.\nВерсия: v0.0.1\n'))

    def frames(self):
        self.frame_top = Frame(self.root, bd=1, relief='sunken')
        self.frame_bottom = Frame(self.root, bd=1, relief='sunken')

        self.frame_top.pack(side='top', fill='x')
        self.frame_bottom.pack(side='top', fill='x')


    def buttons(self):
        self.contents = StringVar()
        ttk.Label(self.frame_top, text=u'Выбрать папку c таблицами').grid(sticky='nw', row=1, column=0)
        ttk.Entry(self.frame_top, width=30, textvariable=self.contents).grid(row=2, column=0)
        ttk.Button(self.frame_top, text=u'Открыть', command=lambda: self.get_path_dir()).grid(row=2, column=1)
        # here is the application variable
        ttk.Button(self.frame_top, text=u'Очистить', command=lambda: parsing_files_tiasm_in_folders_of_tables(self.contents.get())).grid(row=3, column=0)

        ttk.Button(self.frame_bottom, text=u'Отмена', command=self.root.destroy).grid(sticky='e', row=1, column=0)


    def get_path_dir(self):
        path = askdirectory()
        self.contents.set(path)


    @staticmethod
    def message(text):
        messagebox.showinfo(title=u'Сообщение - TICleaner', message=text)


def main():
    root = Tk()
    root.geometry('300x300+500+200')
    root.title(u'Очистка файлов TI от ТУ - TICleaner')
    root.iconbitmap(os.getcwd() + os.path.sep + 'img' + os.path.sep + 'cleaner.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
