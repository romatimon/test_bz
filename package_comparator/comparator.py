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

def parse_version(version):
    """Parses a version string and returns a tuple for comparison."""
    version = version.replace('_', '-')  #  1.26.0_alt1 convert to 1.26.0-alt1
    if '-' in version:
        base_version, release = version.split('-', 1)  #  base_version = 1.26.0, release = alt1
    else:
        base_version, release = version, ''

    parts = base_version.split('.')  #  1.26.0 convert to ['1', '26', '0']

    return [int(part) if part.isdigit() else part for part in parts], release

def compare_versions(pkg1, pkg2):
    """Compares two package versions without external libraries."""
    evr1 = f"{pkg1.get('epoch', '0')}:{pkg1['version']}-{pkg1['release']}"  # str: 0:1.26.0-alt1
    evr2 = f"{pkg2.get('epoch', '0')}:{pkg2['version']}-{pkg2['release']}"

    epoch1, version1 = evr1.split(':', 1)  # epoch1: 0, version1: 1.26.0-alt1
    epoch2, version2 = evr2.split(':', 1)

    if int(epoch1) != int(epoch2):
        return int(epoch1) - int(epoch2)

    version_parts1, release1 = parse_version(version1)  # [1, 26, 0], alt1
    version_parts2, release2 = parse_version(version2)

    for part1, part2 in zip(version_parts1, version_parts2):  # [1, 26, 0, 1, 26, 0]
        if isinstance(part1, int) and isinstance(part2, int):
            if part1 != part2:
                return part1 - part2
        else:
            if isinstance(part1, str) and isinstance(part2, str):
                if part1 != part2:
                    return (part1 > part2) - (part1 < part2)
            elif isinstance(part1, int):
                return 1
            else:
                return -1

    return (release1 > release2) - (release1 < release2)  # bool

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
