# SmartSudokuSolver
This is a project I have done for AI class to solve a 9x9 sudoku board

## Description 🧐

This is a program that is designed to solve the 9X9 sudoku game through a **backtracking** search algorithm using minimum remaining value heuristic and applying forward checking to reduce the variable's domains

This program solves 400 boards for: 
* Minimum time (8.197784423828125 ms)
* Maximum time (1011.6868019104004 ms) 
* Mean of (96.73954844474792 ms)
* Standard_deviation: (132.05955555187012 ms)

## Getting Started 🚀

### Dependencies

* Language/Version: python 3.9
* Libraries: Numpy ,math, time, operator, random, statistics

### Executing program 👩🏻‍💻

* The program can be executed in two ways:
* 1. by including a .txt file that has several boards of string format, the algorithm will be applied to all of them.
* 2. by running the algorithm in one board configuration as follow: 
```
$ python3 sudoku.py <input_string>
```
* Example:
```
$ python3 sudoku.py 000000009024059003750000060000000000070030890000065742800002000000006010043008000
```

## Acknowledgments ❇️

* This program has been done as a project for an AI class.
