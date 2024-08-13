# js redos finder
* This project is designed to automatically detect ReDoS (Regular Expression Denial of Service) vulnerabilities within npm packages. The tool depends on recheck and nodejs.
* Based on the programme https://github.com/makenowjust-labs/recheck.
* korean translate: https://github.com/yuhano/js-redos-finder/readme_kr.md


## Key Features
* Regex Pattern Extraction: Extracts regular expression patterns from JavaScript and TypeScript files.
* Generate an attackable regular expression (Attack string) with `recheck` on the extracted regular expression (found_regex) 
* Performance Measurement: Measures the actual execution time of the regex patterns using nodeJS with the generated attack strings.
* Result Export: Saves the inspection results in a CSV file.


## Project Structure
```
project_root/
│
├── input/                     # Folder containing files to be analyzed
│   ├── example npm folder 1
│   └── example npm folder 2
│
├── src/                       # Package and source code location
│   ├── __init__.py            # Package initialization file
│   ├── constants.py           # Configuration and constants file
│   ├── log_utils.py           # Log utility functions
│   ├── file_utils.py          # File handling utility functions
│   ├── regex_utils.py         # Regex inspection utility functions
│   └── main.py                # Main execution script
│
├── scripts/                   # External regex checker program location
│   └── recheck-windows-x64.exe
│
├── logs/                      # Folder for storing log files
│   └── (Log files are created here)
│
└── output/                    # Folder for storing the result CSV file
    └── regex_search_results_output.csv
```


## Installation and Usage
### Prerequisites
* Python 3.x
* Node.js (Required for executing JavaScript code)
* Windows OS

### Installation
1. Clone this repository:
    ```
    git clone https://github.com/yuhano/js-redos-finder.git
    ```

2. Place the packages you want to inspect in the `input` folder.
    ```
    mkdir input
    cp [npmProject] input
    ```

3. Modify the ROOT_DIRECTORY and PROGRAM_PATH values in the src/constants.py file as appropriate.
Run the tool with the following command:
```
python src/main.py
```

# License
This project is licensed under the MIT License. For more details, see the LICENSE file.

# Contributing
Contributions are welcome! You can contribute by reporting bugs, requesting features, or submitting pull requests.