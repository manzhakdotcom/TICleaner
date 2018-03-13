import os
import json


def get_settings_from_config_file():
    if os.path.isfile('config.json'):
        with open('config.json', 'r', encoding="utf-8") as file:
            json_data = file.read()
        return json.loads(json_data)
    else:
        alert_message('Нет файла конфигурации')


def get_setting_source_path_from_config_file(settings):
    path = settings['sourcePath']
    if '' != path:
        return path
    else:
        alert_message('Путь пустой')


def alert_message(text):
    print(text)
    exit()


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
                if '@U' in line:
                    if 'РК' not in line:
                        if 'а' not in line:
                            line = ';' + line
                text = text + line
        with open(file_path, 'w', encoding="OEM") as file:
            file.write(text)


def parsing_files_tiasm_in_folders_of_tables(path):
    open_and_change_ti_files(path)


def main():
    settings = get_settings_from_config_file()
    path = get_setting_source_path_from_config_file(settings)
    parsing_files_tiasm_in_folders_of_tables(path)


if __name__ == '__main__':
    main()
