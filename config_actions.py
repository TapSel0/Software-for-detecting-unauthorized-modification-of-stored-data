from const import *
import configparser
import os


def create_config(path: str):
    """
    Создание конфига со стандартными путями
    """
    config = configparser.ConfigParser()
    config.add_section("Paths")
    config.set("Paths", "files_hashes_dict", DEFAULT_PATH_TO_HASH)
    config.set("Paths", "dirs_files_dict", DEFAULT_PATH_TO_DIRS_FILES)
    config.set("Paths", "audit", DEFAULT_PATH_TO_AUDIT)
    config.set("Paths", "tracked_file", "")

    with open(path, "w") as config_file:
        config.write(config_file)


def read_config(path: str):  # Возвращает путь к аудиту, хешам, расположению файлов и последнему отслеживаемому файлу
    """
    Считывания конфига путей
    """
    if not os.path.exists(path):  # Если не существует, то создаётся новый со стандартными настройками
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)

    # Читаем некоторые значения из конфига
    audit_path = config.get("Paths", "audit")
    hashes_path = config.get("Paths", "files_hashes_dict")
    path_to_dirs_files = config.get("Paths", "dirs_files_dict")
    tracked_file_path = config.get("Paths", "tracked_file")

    return audit_path, hashes_path, path_to_dirs_files, tracked_file_path


def set_config(path: str, audit_path: str, hashes_path: str, path_to_dirs_files: str, tracked_file_path: str):
    """
    Запись новых путей в конфиг
    """
    config = configparser.ConfigParser()
    config.read(path)

    # Меняем значения из конфиг
    config.set("Paths", "audit", audit_path)
    config.set("Paths", "files_hashes_dict", hashes_path)
    config.set("Paths", "dirs_files_dict", path_to_dirs_files)
    config.set("Paths", "tracked_file", tracked_file_path)

    # Вносим изменения в конфиг
    with open(path, "w") as config_file:
        config.write(config_file)
