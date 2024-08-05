import concurrent.futures
import json

import click
from tqdm import tqdm
from comparator import get_packages, compare_packages


@click.command()
@click.argument('branch1')
@click.argument('branch2')
def main(branch1: str, branch2: str) -> None:
    """Main function to compare packages of two branches."""
    API_URL = "https://rdb.altlinux.org/api/export/branch_binary_packages/"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_packages, API_URL + branch1),
            executor.submit(get_packages, API_URL + branch2)
        ]

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Loading packages"):
            future.result()

        branch1_packages = futures[0].result()
        branch2_packages = futures[1].result()

        result = compare_packages(branch1_packages, branch2_packages)

        print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()