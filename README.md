## _Package Comparison Tool_
This tool compares packages between two branches of a repository. It retrieves package information from a specified API and provides a detailed comparison, including packages that are unique to each branch and those with higher versions in one branch compared to the other.

## Features
- Fetches package data from an API.
- Compares packages between two branches.
- Outputs results in JSON format and displays them in a readable table format.
- Utilizes multithreading for efficient data retrieval.

## Requirements
- Python 3.6 or higher
- Required libraries listed in requirements.txt

## Installation
Follow these steps to set up the tool on a Linux system:

**1. Clone the repository:**
```bash
git clone https://github.com/romatimon/test_bz.git
cd test_bz/package_comparator
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

## Usage
To use the package comparison tool, run the following command in your terminal:
```bash
python package_comparison.py <branch1> <branch2> [--output <output_file>]
```

- `<branch1>`: The first branch to compare.
- `<branch2>`: The second branch to compare.
- `--output <output_file>`: Optional. Specify the name of the output JSON file (default is `comparison_result.json`).

## Example

```bash
python package_comparison.py sisyphus p10 --output comparison_result.json
```

## Output
The results will be saved to the specified JSON file and displayed in the terminal. The output includes:

- Packages only in branch 1.
- Packages only in branch 2.
- Packages with a higher version in branch 1.

## Logging
The tool logs errors and important information to the console. Make sure to check the logs if you encounter any issues.