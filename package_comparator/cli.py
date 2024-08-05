import concurrent.futures
import click
from tabulate import tabulate
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

        # Display results
        click.echo("Packages only in branch p10:")
        click.echo(tabulate(result['only_in_branch2'].values(), headers='keys'))

        click.echo("\nPackages only in branch sisyphus:")
        click.echo(tabulate(result['only_in_branch1'].values(), headers='keys'))

        click.echo("\nPackages with higher version in sisyphus:")
        click.echo(tabulate(result['higher_in_branch1'].values(), headers='keys'))


if __name__ == "__main__":
    main()