import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    # Настройка базового логгирования
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Настройка файлового обработчика с ротацией
    # Задает название директории, в которой будут храниться логи
    log_dir = 'logs'

    '''Создает указанную директорию (и все промежуточные директории, если необходимо). 
    Параметр exist_ok=True означает, что если директория уже существует, код не выбросит ошибку.'''
    os.makedirs(log_dir, exist_ok=True)

    # Формирует полный путь к файлу с логами, объединяя название директории и имя файла
    log_file = os.path.join(log_dir, 'app.log')

    file_handler = RotatingFileHandler(log_file, maxBytes=512 * 512 * 4, backupCount=2)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Добавление файлового обработчика к корневому логгеру
    logging.getLogger().addHandler(file_handler)
    # Установка уровня для корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = True
