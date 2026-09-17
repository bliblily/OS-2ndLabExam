# OS Simulation Program

A single Python script that simulates:
- CPU Scheduling: **FCFS** (Non-Preemptive) and **Round Robin** (Preemptive)
- **Banker's Algorithm** (deadlock avoidance / safe state check)

## Requirements
- Python 3.x (no external libraries needed)

## How to Run
1. Open a terminal in the folder containing `scheduling_bankers.py`.
2. Run:
   ```
   python3 scheduling_bankers.py
   ```
   (On Windows, use `python scheduling_bankers.py` if `python3` isn't recognized.)
3. Follow the on-screen menu and type your input when prompted.

## Menu Options

```
1. CPU Scheduling Algorithms
2. Banker's Algorithm
3. Exit
```

### 1. CPU Scheduling
Choosing this option asks you to pick an algorithm:
```
1. Non-Preemptive: First Come First Serve (FCFS)
2. Preemptive: Round Robin (RR)
```
You will then be asked for:
- Number of processes
- Arrival time and burst time for each process
- Time Quantum (Round Robin only)

**Output:** a text Gantt chart, a table of AT/BT/CT/TAT/WT per process, and the average Waiting Time and Turnaround Time.

### 2. Banker's Algorithm
You will be asked for:
- Number of processes
- Number of resource types
- Allocation matrix (one row per process)
- Maximum matrix (one row per process)
- Available resources (one row)

**Output:** the computed Need matrix, whether the system is in a **Safe** or **Unsafe** state, and the Safe Sequence if one exists.

## Example: Banker's Algorithm Input
For 5 processes and 3 resource types:
```
Allocation:
0 1 0
2 0 0
3 0 2
2 1 1
0 0 2

Maximum:
7 5 3
3 2 2
9 0 2
2 2 2
4 3 3

Available:
3 3 2
```
Expected result: **Safe State**, Safe Sequence `P1 -> P3 -> P4 -> P0 -> P2`.

## Notes
- All input is entered via the console (no files needed).
- Choosing `3. Exit` from the main menu ends the program.