import os
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox


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
            App.message(u'Папка с таблицами не выбрана')
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


class App:
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
        help_ = Menu(menubar)

        menubar.add_cascade(menu=file, label=u'Файл')
        menubar.add_cascade(menu=tools, label=u'Инструменты')
        menubar.add_cascade(menu=help_, label=u'Справка')

        file.add_command(label=u'Выбрать папку...', command=self.get_path_dir)
        file.add_command(label=u'Настройки',  command=lambda: self.message(u'В разработке'))
        file.add_separator()
        file.add_command(label=u'Выйти', command=self.root.destroy)

        tools.add_command(label=u'Открыть логфайл', command=lambda: self.message(u'В разработке'))

        help_.add_command(label=u'О программе', command=lambda: self.message(u'Автор: Манжак С.С.\nВерсия: v0.0.2\n'))

    def elements(self):

        frame = Frame(self.root)
        frame.pack(pady=10)

        label = ttk.Label(frame, text=u'Выбрать папку c таблицами')
        label.grid(sticky='w', row=0, column=0, columnspan=4)

        self.contents = StringVar()
        entry = ttk.Entry(frame, state='disabled', width=30, textvariable=self.contents)
        entry.grid(row=1, column=0, columnspan=3)

        button1 = ttk.Button(frame, text=u'Выбрать', command=lambda: self.get_path_dir())
        button1.grid(row=1, column=3)

        button2 = ttk.Button(frame, text=u'Очистить', command=lambda: Clear(self.contents.get()))
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
    root.iconbitmap(os.getcwd() + os.path.sep + os.path.sep + 'icon.ico')
    app = App(root)

    root.mainloop()


if __name__ == '__main__':
    main()
