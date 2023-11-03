import hashlib
import os
from gost_hash import GOST_hash
from stribog_func import Str512


def hash_algos(fname, algo):
    with open(fname, 'rb') as f:  # Считываются байты файла для создания хеша
        data = f.read()
    if algo == 'Стрибог':
        return Str512(data)
    elif algo == "ГОСТ":
        return GOST_hash(data)
    elif algo == 'MD5':
        calculated_hash = hashlib.md5()
        calculated_hash.update(data)
        return calculated_hash.hexdigest()
    elif algo == 'SHA1':
        calculated_hash = hashlib.sha1()
        calculated_hash.update(data)
        return calculated_hash.hexdigest()
    elif algo == 'SHA256':
        calculated_hash = hashlib.sha256()
        calculated_hash.update(data)
        return calculated_hash.hexdigest()



# Функция проверяет на то папка это или файл и делает записи в словарь исходя из этого
def files_hashes(path: str, algorithms: list, files_hashes_dict: dict, dirs_files_dict: dict) -> tuple[dict, dict]:
    if os.path.isfile(path):  # если это файл, то для этого файла делает запись
        # в словаре в виде [имя файла]: {выбранный алгоритм: хэш}
        file_algos = dict()
        for algorithm in algorithms:
            file_algos[algorithm] = hash_algos(path, algorithm)
        files_hashes_dict[path] = file_algos
    elif os.path.isdir(path):  # если это папка, то вызывает рекурсию
        list_of_files = os.listdir(path)
        if list_of_files:  # если не пустая папка, то выполняется алгоритм, если пустая, то возвращает пустой словарь
            dirs_files_dict[path] = list_of_files
            for name in list_of_files:
                file_path = f"{path}\\{name}"
                files_hashes(file_path, algorithms, files_hashes_dict, dirs_files_dict)
        else:
            dirs_files_dict[path] = []
    return files_hashes_dict, dirs_files_dict


# Возвращает список со списками:
# [[файлы с одинаковыми хешами], [с разными хешами], [не было записи о хеше],
# [файлы, которые новые для этой папки], [файлы, которые пропали из папки]]
def match_hashes(path: str, algorithm: str, files_hashes_dict: dict, dirs_files_dict: dict) -> list[list, list, list, list, list]:  # Сравнивает все файлы по указанному хэшу
    list_of_files = os.listdir(path)
    if not list_of_files:  # Проверяю есть ли файлы в папке. Это нужно при рекурсии
        return [[], [], [], [], []]

    matched_files = []  # для файлов, которые совпали
    not_matching_files = []  # для файлов, которые не совпали
    missing_hash_files = []  # для файлов, у которых не было записи про данный хэш
    missing_files = list(set(dirs_files_dict.get(path, [])) - set(list_of_files))  # для отсутсвующих файлов в этой папке
    new_files = list(set(list_of_files) - set(dirs_files_dict.get(path, [])))  # для новых файлов в этой папке
    for name in list_of_files:
        file_path = f"{path}\\{name}"
        if os.path.isdir(file_path):
            temp = match_hashes(file_path, algorithm, files_hashes_dict, dirs_files_dict)
            matched_files.extend(temp[0])
            not_matching_files.extend(temp[1])
            missing_hash_files.extend(temp[2])
            new_files.extend(temp[3])
            missing_files.extend(temp[4])
        elif os.path.isfile(file_path):
            path_exist_in_dict = files_hashes_dict.get(file_path, 0)  # проверяю есть ли запись о таком файле в словаре
            if path_exist_in_dict and path_exist_in_dict.get(algorithm, 0):  # если есть запись о файле и о хеше в нём, то сравниваю
                if files_hashes_dict[file_path][algorithm] == hash_algos(file_path, algorithm):
                    matched_files.append(file_path)
                else:
                    not_matching_files.append(file_path)
            else:
                missing_hash_files.append(file_path)
        else:
            return [[], [], [], [], []]
    return [matched_files, not_matching_files, missing_hash_files, new_files, missing_files]

