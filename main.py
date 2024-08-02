import concurrent
import logging

import requests


def get_packages(url: str) -> list:
    """Получает пакеты из указанного URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.RequestException as e:
        logging.error(f'Ошибка при запросе к серверу: {e}')
        raise ValueError(f'Ошибка при запросе к серверу: {e}')

    packages = response.json().get('packages')
    if packages is None:
        logging.error('Проверьте название ветки или формат ответа API.')
        raise ValueError('Проверьте название ветки или формат ответа API.')

    return packages


def main(branch1: str, branch2: str) -> None:
    """Основная функция для сравнения пакетов двух веток."""
    API_URL = "https://rdb.altlinux.org/api/export/branch_binary_packages/"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_packages, API_URL + branch1),
            executor.submit(get_packages, API_URL + branch2)
        ]

        branch1_packages = futures[0].result()
        branch2_packages = futures[1].result()
