# 🧮 Professional Calculator

A robust, command-line calculator application built in Python. This project features a continuous Read-Eval-Print Loop (REPL), advanced history tracking using Pandas, and state traversal (Undo/Redo) using the Memento design pattern.

---

## ✨ Features & Architecture

* **Advanced Mathematics:** Perform Addition, Subtraction, Multiplication, Division, Power, and Root operations.
* **Pandas Data Management:** Calculations are seamlessly saved to a Pandas DataFrame and automatically synchronized to a CSV file for persistent storage.
* **Robust Error Handling:** Utilizes both **LBYL** (Look Before You Leap) and **EAFP** (Easier to Ask Forgiveness than Permission) paradigms to gracefully handle invalid inputs and prevent application crashes.

### 🧩 Design Patterns Implemented
* **Facade:** Simplifies complex internal subsystems into a single, easy-to-use interface.
* **Strategy & Factory:** Dynamically routes user input and executes mathematical operations without rigid `if/else` chains.
* **Observer:** Automatically monitors calculation events in the background to trigger data auto-saves.
* **Memento:** Safely stores deep copies of the history state, enabling flawless `undo` and `redo` time-travel capabilities.

---

## 🚀 Setup Instructions

1. **Clone the repository:**
```bash
git clone [https://github.com/Reyesfrancisp/midterm_calculator_project.git](https://github.com/Reyesfrancisp/midterm_calculator_project.git)
cd enhanced_calculator_example
```

2. **Create and activate a virtual environment:**

```bash
# Windows
python -m venv venv
source venv/Scripts/activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```Bash
pip install -r requirements.txt
```

4. **Setup Environment Variables**:

The application relies on environment variables for safe and flexible configuration, particularly for file paths and system logging.

Create a .env file in the root directory to configure the application:

```Plaintext

# .env file

ENVIRONMENT=development
HISTORY_FILE=data/history.csv

# Logging Configuration
# Set the desired threshold for system logs: DEBUG, INFO, WARNING, ERROR, or CRITICAL
LOG_LEVEL=INFO
```
5. **Usage Instructions**:

Start the application by running:

```Bash
python main.py
```

## Available Commands
Once the REPL starts, you can use the following commands:

| Command | Usage Example | Description |
| :--- | :--- | :--- |
| **`add`** | `add 5 10` | Adds two numbers together. |
| **`subtract`** | `subtract 10 4` | Subtracts the second number from the first. |
| **`multiply`** | `multiply 6 7` | Multiplies two numbers. |
| **`divide`** | `divide 8 2` | Divides the first number by the second. |
| **`power`** | `power 2 3` | Raises the first number to the power of the second. |
| **`root`** | `root 9 2` | Calculates the nth root of the first number. |
| **`log`** | `log 100 10` | Calculates the logarithm of the first number with the specified base. |
| **`mean`** | `mean 2 4 6 8` | Calculates the average (mean) of a list of numbers. |
| **`median`** | `median 1 3 5` | Finds the middle value (median) of a list of numbers. |
| **`stddev`** | `stddev 1 2 3 4` | Calculates the standard deviation of a dataset. |
| **`variance`** | `variance 1 2 3` | Calculates the variance of a dataset. |
| **`history`** | `history` | Displays a clean Pandas table of your past calculations. |
| **`clear`** | `clear` | Wipes the current calculation history session. |
| **`undo`** | `undo` | Reverts the calculation history to the previous state. |
| **`redo`** | `redo` | Restores a previously undone history state. |
| **`save`** | `save` | Manually forces a save of the current history to the CSV file. |
| **`load`** | `load` | Manually loads calculation history from the CSV file. |
| **`export`** | `export` | Exports the current history to a specific file format or location. |
| **`filter`** | `filter add` | Filters the Pandas history to show only specific operations. |
| **`help`** | `help` | Displays the available command menu. |
| **`exit`** | `exit` | Safely exits the application. |

## 🧪 Testing Instructions

This application is tested and maintains 90%+ test coverage to ensure production-level stability. The tests cover both positive execution paths and negative error-handling branches.

To run the automated unit tests and view the coverage report in your terminal, run:

```Bash
python -m pytest --cov=app --cov-report=term-missing tests/
```

## 🔄 CI/CD Information (GitHub Actions)
This project utilizes GitHub Actions for Continuous Integration (CI).

Whenever code is pushed or a Pull Request is opened against the main branch, the .github/workflows/python-app.yml workflow is automatically triggered.

Workflow Purpose:

Spins up an Ubuntu environment with Python 3.11.

Installs all required dependencies from requirements.txt.

Runs the full pytest suite.

Enforces Quality: Analyzes the coverage report and will intentionally fail the build if the test coverage drops below exactly 100% (--fail-under=100). This ensures that no undocumented or untested code is ever merged into the production branch.