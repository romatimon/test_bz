import concurrent.futures
import json
import logging
import re
import time

import click
import requests
from tabulate import tabulate
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def normalize_version(version: str) -> str:
    """Нормализует версию, извлекая основную часть."""
    match = re.match(r'(\d+(\.\d+){0,2})', version)
    return match.group(0) if match else version


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


def compare_packages(branch1_packages: list, branch2_packages: list) -> dict:
    """Сравнивает пакеты между двумя ветками и возвращает результаты."""
    branch1_dict = {pkg['name']: pkg for pkg in branch1_packages}
    branch2_dict = {pkg['name']: pkg for pkg in branch2_packages}

    only_in_branch1 = {pkg['name']: pkg for pkg in branch1_dict.values() if pkg['name'] not in branch2_dict}
    only_in_branch2 = {pkg['name']: pkg for pkg in branch2_dict.values() if pkg['name'] not in branch1_dict}

    higher_in_branch1 = {}

    for name, branch1_pkg in branch1_dict.items():
        if name in branch2_dict:
            branch2_pkg = branch2_dict[name]
            branch1_version = normalize_version(branch1_pkg['version'])
            branch2_version = normalize_version(branch2_pkg['version'])

            # Сравнение версий
            if (branch1_version > branch2_version or
                    (branch1_version == branch2_version and branch1_pkg['release'] > branch2_pkg['release'])):
                higher_in_branch1[name] = {
                    'name': name,
                    'version': branch1_pkg['version'],
                    'release': branch1_pkg['release'],
                    'arch': branch1_pkg['arch'],
                    'disttag': branch1_pkg['disttag'],
                    'buildtime': branch1_pkg['buildtime'],
                    'source': branch1_pkg['source']
                }

    return {
        'only_in_branch1': only_in_branch1,
        'only_in_branch2': only_in_branch2,
        'higher_in_branch1': higher_in_branch1,
    }


def save_results_to_json(result: dict, filename: str = 'comparison_result.json') -> None:
    """Сохраняет результаты сравнения в JSON файл."""
    with open(filename, 'w') as json_file:
        json.dump(result, json_file, indent=4)


@click.command()
@click.argument('branch1')
@click.argument('branch2')
@click.option('--output', default='comparison_result.json',
              help='Имя выходного файла для сохранения результата в формате JSON.')
def main(branch1: str, branch2: str, output: str) -> None:
    """Основная функция для сравнения пакетов двух веток."""
    API_URL = "https://rdb.altlinux.org/api/export/branch_binary_packages/"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_packages, API_URL + branch1),
            executor.submit(get_packages, API_URL + branch2)
        ]

        # Используем tqdm для отображения прогресса
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Загрузка пакетов"):
            future.result()  # Просто ждем завершения

        branch1_packages = futures[0].result()
        branch2_packages = futures[1].result()

        result = compare_packages(branch1_packages, branch2_packages)

        save_results_to_json(result, output)
        click.echo(f'Результаты сохранены в файл: {output}')

        # Вывод результатов
        click.echo("Пакеты только в ветке 1:")
        time.sleep(2)
        click.echo(tabulate(result['only_in_branch1'].values(), headers='keys'))

        click.echo("\nПакеты только в ветке 2:")
        time.sleep(2)
        click.echo(tabulate(result['only_in_branch2'].values(), headers='keys'))

        click.echo("\nПакеты с более высокой версией в ветке 1:")
        time.sleep(2)
        click.echo(tabulate(result['higher_in_branch1'].values(), headers='keys'))


if __name__ == "__main__":
    main()
