import requests
import rpm


def get_packages(url: str) -> list:
    """Fetch packages from the specified URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f'Error while requesting the server: {e}')

    packages = response.json().get('packages')
    if packages is None:
        raise ValueError('Check the branch name or the API response format.')

    return packages

def compare_versions(pkg1, pkg2):
    """Compares two package versions without external libraries."""
    evr1 = f"{pkg1['epoch']}:{pkg1['version']}-{pkg1['release']}" if 'epoch' in pkg1 else f"0:{pkg1['version']}-{pkg1['release']}"
    evr2 = f"{pkg2['epoch']}:{pkg2['version']}-{pkg2['release']}" if 'epoch' in pkg2 else f"0:{pkg2['version']}-{pkg2['release']}"

    return rpm.labelCompare(evr1, evr2)

def compare_packages(branch1_packages: list, branch2_packages: list) -> dict:
    """Compare packages between two branches and return the results."""
    branch1_dict = {pkg['name']: pkg for pkg in branch1_packages}
    branch2_dict = {pkg['name']: pkg for pkg in branch2_packages}

    only_in_branch1 = {pkg['name']: pkg for pkg in branch1_dict.values() if pkg['name'] not in branch2_dict}
    only_in_branch2 = {pkg['name']: pkg for pkg in branch2_dict.values() if pkg['name'] not in branch1_dict}

    higher_in_branch1 = {}

    for name, branch1_pkg in branch1_dict.items():
        if name in branch2_dict:
            branch2_pkg = branch2_dict[name]
            comparison_result = compare_versions(branch1_pkg, branch2_pkg)

            if comparison_result > 0:
                higher_in_branch1[name] = {
                    'name': name,
                    'epoch': branch1_pkg['epoch'],
                    'version': branch1_pkg['version'],
                    'release': branch1_pkg['release'],
                    'arch': branch1_pkg['arch'],
                }

    return {
        'only_in_branch1': only_in_branch1,
        'only_in_branch2': only_in_branch2,
        'higher_in_branch1': higher_in_branch1,
    }
