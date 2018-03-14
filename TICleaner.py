import os
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox


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
    if not get_list_of_folders(path):
        App.message('Папка с таблицами не выбрана')
    else:
        files_path = get_ti_path_file_from_folders(path)
        print(len(files_path))
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
        App.message('Очищено файлов: ' + str(len(files_path)))



def parsing_files(path):
    if '' != path:
        open_and_change_ti_files(path)
    else:
        App.message('Папка не выбрана')


class App:
    def __init__(self, root):
        self.root = root
        self.menu()
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

        file.add_command(label=u'Выбрать папку...', command=self.get_path_dir)
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.root.destroy)

        tools.add_command(label=u'Открыть логфайл', command=lambda:self.message('Логфайла нет'))

        help_.add_command(label=u'О программе', command=lambda:self.message('Автор: Манжак С.С.\nВерсия: v0.0.1\n'))

    def buttons(self):

        frame = Frame(self.root)
        frame.pack(pady=10)

        label = ttk.Label(frame, text=u'Выбрать папку c таблицами')
        label.grid(sticky='w', row=0, column=0, columnspan=4)

        self.contents = StringVar()
        entry = ttk.Entry(frame, state='disabled', width=30, textvariable=self.contents)
        entry.grid(row=1, column=0, columnspan=3)

        button1 = ttk.Button(frame, text=u'Выбрать', command=lambda: self.get_path_dir())
        button1.grid(row=1, column=3)

        button2 = ttk.Button(frame, text=u'Очистить', command=lambda: parsing_files(self.contents.get()))
        button2.grid(pady=15, row=2, column=0, columnspan=4)


    def get_path_dir(self):
        path = askdirectory()
        self.contents.set(path)


    @staticmethod
    def message(text):
        messagebox.showinfo(title=u'Сообщение - TICleaner', message=text)


def main():
    root = Tk()
    root.geometry('300x130+500+200')
    root.title(u'TICleaner')
    root.iconbitmap(os.getcwd() + os.path.sep + 'img' + os.path.sep + 'cleaner.ico')
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
