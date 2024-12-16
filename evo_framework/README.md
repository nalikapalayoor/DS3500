# TA Allocation Using Evolutionary Computing

## Project Overview

This project uses evolutionary computing to solve a resource allocation problem for Northeastern University's Khoury College. The goal is to help the college assign Teaching Assistants (TAs) to various lab sections efficiently, minimizing various constraints. The solution uses functional programming techniques as well as test-driven development.

## Features

- Evolutionary Algorithm to assign TAs to lab sections
- Five key objectives:
  - Minimize **overallocation** of TAs
  - Minimize **time conflicts**
  - Minimize **undersupport** in lab sections
  - Minimize TAs assigned to sections they are **unwilling** to support
  - Minimize TAs assigned to sections they are **unpreferred** to support
- Unit tests for objective functions to ensure correctness

## Requirements

- Python 3.x
- `pytest` for unit testing
- `csv` for data formatting
- Evolutionary computing framework (`evo.py`, `profiler.py`, `assignta.py`)

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/nalikapalayoor/evo_framework.git
    cd evo_framework
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the optimizer (with a 5-minute time limit):
    ```bash
    python optimizer.py --time-limit 300
    ```

4. View results in CSV format:
    ```bash
    python result_viewer.py
    ```

## Deliverables

- **Code**: All Python files (`evo.py`, `profiler.py`, `assignta.py`, and unit tests).
- **CSV Summary**: A table of Pareto-optimal solutions.
- **Best Solution Details**: The best solution with section assignments and evaluation scores.
- **Unit Test Report**: `pytest` report showing all tests pass.
- **Profiling Report**: Ensure solutions are generated within the 5-minute time limit.

## Data

- `sections.csv`: Contains lab section details, including min/max TA requirements.
- `tas.csv`: Contains TA availability and preferences for each section.

## Authors

- [Nalika Palayoor](https://github.com/nalikapalayoor)

