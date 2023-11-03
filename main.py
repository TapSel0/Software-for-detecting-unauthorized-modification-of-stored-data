import logging
from const import *
from json_actions import read_json, write_json
from config_actions import read_config, set_config
from autification_window import authentication
from event_handler_window import create_window
from hash_functions import match_hashes, files_hashes, hash_algos
import datetime
from watchdog.observers import Observer
import PySimpleGUI as sg
import os
from watchdog.events import FileSystemEventHandler


class MyLoggingEventHandler(FileSystemEventHandler):  # регистратор событий
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger or logging.root

    def on_moved(self, event):
        super().on_moved(event)

        modifiable_object = 'папка' if event.is_directory else 'файл'
        self.logger.info("Перемещён(а) %s: из %s в %s", modifiable_object, event.src_path.replace("/", "\\"),
                         event.dest_path.replace("/", "\\"))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_msg = now + " Перемещён(а) " + modifiable_object + " : из " + event.src_path.replace("/", "\\") + " в " + \
                     event.dest_path.replace("/", "\\")
        print(output_msg)
        audit_file.write(output_msg + "\n")

    def on_created(self, event):
        super().on_created(event)

        modifiable_object = 'папка' if event.is_directory else 'файл'
        self.logger.info("Создан(а) %s: %s", modifiable_object, event.src_path.replace("/", "\\"))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_msg = now + " Создан(а) " + modifiable_object + " : " + event.src_path.replace("/", "\\")
        print(output_msg)
        audit_file.write(output_msg + "\n")

    def on_deleted(self, event):
        super().on_deleted(event)

        modifiable_object = 'папка' if event.is_directory else 'файл'
        self.logger.info("Удалён(а) %s: %s", modifiable_object, event.src_path.replace("/", "\\"))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_msg = now + " Удалён(а) " + modifiable_object + " : " + event.src_path.replace("/", "\\")
        print(output_msg)
        audit_file.write(output_msg + "\n")

    def on_modified(self, event):
        super().on_modified(event)

        modifiable_object = 'папка' if event.is_directory else 'файл'
        self.logger.info("Изменён(а) %s: %s", modifiable_object, event.src_path.replace("/", "\\"))
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_msg = now + " Изменён(а) " + modifiable_object + " : " + event.src_path.replace("/", "\\")
        print(output_msg)
        audit_file.write(output_msg + "\n")


def observer_initialization():
    global observer
    print("Инициализация отслеживание изменений по выбранному пути:", tracked_file_path, "\n\n")

    event_handler = MyLoggingEventHandler()  # MyHandler()

    # Инициализация Observer
    observer = Observer()
    observer.schedule(event_handler, tracked_file_path, recursive=False)

    # Начало отслеживания
    observer.start()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
audit_path, hashes_path, path_to_dirs_files, tracked_file_path = read_config(CONFIG_PATH)  # Считываем пути для данных
try:
    files_hashes_dict = read_json(hashes_path)
    dirs_files_dict = read_json(path_to_dirs_files)  # словарь для папок
    audit_file = open(audit_path.replace("/", "\\"), "a")
except:
    set_config(CONFIG_PATH, DEFAULT_PATH_TO_AUDIT, DEFAULT_PATH_TO_HASH, DEFAULT_PATH_TO_DIRS_FILES, tracked_file_path)
    audit_path, hashes_path, path_to_dirs_files, tracked_file_path = read_config(
        CONFIG_PATH)  # Считываем пути для данных
    files_hashes_dict = read_json(hashes_path)
    dirs_files_dict = read_json(path_to_dirs_files)  # словарь для папок
    audit_file = open(audit_path.replace("/", "\\"), "a")
observer = Observer()


if authentication():
    window = create_window().Finalize()
    if audit_path.replace("audit.txt", ""):
        window["recording_path"].update(audit_path.replace("audit.txt", ""))
    else:
        window["recording_path"].update("Корневая папка")
    if tracked_file_path:
        window["tracked_file"].update(tracked_file_path)
        observer_initialization()

    #values:
    # "tracked_file":"Путь к отслеживанию", "recording_path":"Путь для записи
    # 1: Стрибог, 2: ГОСТ, 3: MD5, 4: SHA1, 5:SHA256
    while True:  # Event Loop
        event, values = window.read()

        # Проверяем хочет ли пользователь выйти или отменить
        if event == sg.WIN_CLOSED or event == 'Сохранить и выйти':
            audit_file.close()
            set_config(CONFIG_PATH, audit_path, hashes_path, path_to_dirs_files, tracked_file_path)  # запоминаем все значения выбранных путей для записи
            write_json(path_to_dirs_files, dirs_files_dict)
            write_json(hashes_path, files_hashes_dict)
            try:
                observer.stop()
                observer.join()
                break
            except:
                break

        if event == "Сохранить хеши файлов по выбранному пути":
            file_path = values["tracked_file"].replace("/", "\\")
            if not values["tracked_file"]:
                print("Не был выбран файл")
                continue
            if values["tracked_file"] and not os.path.exists(file_path):
                print("Выбран неправильный путь к файлу")
                continue

            algorithms = []  # Список для алгоритмов
            if values[1]:
                algorithms.append('Стрибог')
            if values[2]:
                algorithms.append('ГОСТ')
            if values[3]:
                algorithms.append('MD5')
            if values[4]:
                algorithms.append('SHA1')
            if values[5]:
                algorithms.append('SHA256')
            if algorithms:
                files_hashes_dict, dirs_files_dict = files_hashes(file_path, algorithms, files_hashes_dict, dirs_files_dict)
                print("Запись о хешах файла(ов) по пути - " + file_path + ", для алгоритмов - " +
                      "".join([i + ", " for i in algorithms]) + "была успешно выполнена")
            else:
                print("Выберите хотя бы 1 алгоритм")

        if event == "Провести сравнение файлов с помощью хеш-функций":
            file_path = values["tracked_file"].replace("/", "\\")
            if not values["tracked_file"]:
                print("Не был выбран файл")
                continue
            if values["tracked_file"] and not os.path.exists(file_path):
                print("Выбран неправильный путь к файлу")
                continue

            algorithms = []  # Список для алгоритмов
            if values[1]:
                algorithms.append('Стрибог')
            if values[2]:
                algorithms.append('ГОСТ')
            if values[3]:
                algorithms.append('MD5')
            if values[4]:
                algorithms.append('SHA1')
            if values[5]:
                algorithms.append('SHA256')

            if not algorithms:
                print("Выберите хоть бы 1 алгоритм")
                continue

            for algorithm in algorithms:
                print(f"\n{algorithm}:")
                if os.path.isfile(file_path):  # если это файл, то проверяем совпадение хэша
                    path_exist_in_dict = files_hashes_dict.get(file_path, 0)
                    if not(path_exist_in_dict) or not(path_exist_in_dict.get(algorithm, 0)):  # если есть запись о файле и о хеше, то сравниваю
                        print("Недостаточно данных для проверки файла")
                        continue
                    print(f"Прошлый хеш по пути {file_path}: {path_exist_in_dict[file_path][algorithm]}")
                    print(f"Хэш файла {file_path} на данный момент: {path_exist_in_dict[file_path][algorithm]}")
                    if path_exist_in_dict[file_path][algorithm] == hash_algos(file_path, algorithm):
                        print("Хэши файлов совпадают\n")
                    else:
                        print("Хэши не файлов совпадают\n")

                elif os.path.isdir(file_path):  # если это папка, то вызываем функцию для сравнивания элементов в папке
                    if not os.listdir(file_path):  # если пустая папка
                        print("Указанная папка пустая")
                        continue
                    matched_files = match_hashes(file_path, algorithm, files_hashes_dict, dirs_files_dict)
                    # Возвращает список с 5 списками:
                    # [[файлы с одинаковыми хешами], [с разными хешами], [не было записи о хеше],
                    # [файлы, которые новые для этой папки], [файлы, которые пропали из папки]]
                    if matched_files[0]:
                        if not any([i for i in matched_files[1:]]):
                            window['Output'].print("В файлах изменений не обнаружено", text_color='green')
                        else:
                            window['Output'].print("Файлы в которых не было обнаружено изменений: ", "".join([i + ", " for i in matched_files[0]]), "\n",
                                                   text_color='green')
                    if matched_files[1]:
                        window['Output'].print("Файлы, в которых были обнаружены изменения: ",
                                                                   "".join([i + ", " for i in matched_files[1]]), "\n",
                                                                   text_color='red', background_color='light grey')
                    if matched_files[2]:
                        print(f"Файлы без сохранённых хэш-значений: ", "".join([i + ", " for i in matched_files[2]]), "\n")
                    if matched_files[3]:
                        window['Output'].print(f"Новые файлы в этой папке: ",
                                                                   "".join([i + ", " for i in matched_files[3]]), "\n",
                            text_color='yellow', background_color='light grey')
                    if matched_files[4]:
                        window['Output'].print(f"Отсутствующие файлы в папке: ",
                                                                   "".join([i + ", " for i in matched_files[4]]), "\n",
                            text_color='yellow', background_color='light grey')
                else:
                    print("Не получилось сравнить")
            print("\n\n")

        if event == "Начать отслеживание изменений по выбранному пути":
            if not values["tracked_file"]:
                print("Выберите или впишите путь", end="\n\n")
                continue

            path = values["tracked_file"].replace("/", "\\")
            if not os.path.exists(path):
                print('Выбран неправильный путь к файлу', end="\n\n")
                continue

            if os.path.isfile(path):
                print('Выбран файл')
                print('Размер:', os.path.getsize(path) // 1024, 'Кб')
                print('Дата создания:', datetime.datetime.fromtimestamp(int(os.path.getctime(path))))
                print('Дата последнего открытия:', datetime.datetime.fromtimestamp(int(os.path.getatime(path))))
                print('Дата последнего изменения:', datetime.datetime.fromtimestamp(int(os.path.getmtime(path))), end="\n\n")
            elif os.path.isdir(path):
                print('Выбран путь к каталогу')
                print('Список объектов в нем: ', os.listdir(path), end="\n\n\n")
            tracked_file_path = path
            observer_initialization()

        if event == "Сменить папку записи данных":
            if not values["recording_path"]:
                print("Новый путь не указан.")
                continue

            storage_path = values["recording_path"].replace("/", "\\")

            if not os.path.exists(storage_path):
                print("Такой путь не существует.")
                continue

            audit_path = storage_path + "\\audit.txt"
            hashes_path = storage_path + "\\files_hashes.json"
            path_to_dirs_files = storage_path + "\\dirs_files.json"

            set_config(CONFIG_PATH, audit_path, hashes_path, path_to_dirs_files, tracked_file_path)

            print("Папка записи сменена на:", storage_path)

    # Завершаем закрытием окна
    window.close()

