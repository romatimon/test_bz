## _Package Comparison Tool_
This tool compares packages between two branches of a repository. It retrieves package information from a specified API and provides a detailed comparison, including packages that are unique to each branch and those with higher versions in one branch compared to the other.

## Features
- Fetches package data from an API.
- Compares packages between two branches.
- Utilizes multithreading for efficient data retrieval.

## Requirements
- Python 3.6 or higher
- Required libraries listed in requirements.txt

## Installation
Follow these steps to set up the tool on a Linux system:

**1. Clone the repository:**
```bash
git clone https://github.com/romatimon/test_bz.git
cd test_bz
```
**2. Update package lists:**
```bash
sudo apt update
```

**3. Install Python 3 and pip (if not already installed):**
```bash
sudo apt install python3-pip
```

**4. Install required libraries:**
```bash
pip install -r requirements.txt
```

**5. Install RPM Python bindings:**
```bash
sudo apt install python3-rpm
```

## Usage

To use the package comparison tool, go to the `package_comparator` folder and run the following command in a terminal:
```bash
cd package_comparator
python3 cli.py <branch1> <branch2>
```

- `<branch1>`: The first branch to compare.
- `<branch2>`: The second branch to compare.

## Example

```bash
python3 cli.py sisyphus p10
```

## Output
The results will be converted to the terminal. The output includes:

- Packages only in branch 1.
- Packages only in branch 2.
- Packages with a higher version in branch 1.
