"""
============================================================
 OS Simulation Program
 1. CPU Scheduling Algorithms
    - Non-Preemptive: First Come First Serve (FCFS)
    - Preemptive: Round Robin (RR)
 2. Banker's Algorithm (Deadlock Avoidance)

 Language: Python 3
============================================================
"""

# ------------------------------------------------------------
# SECTION 1: CPU SCHEDULING
# ------------------------------------------------------------

def input_processes():
    """Reads number of processes, their arrival and burst times from console."""
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        print(f"\n--- Process P{i} ---")
        at = int(input(f"Arrival time of P{i}: "))
        bt = int(input(f"Burst time of P{i}: "))
        processes.append({"pid": f"P{i}", "at": at, "bt": bt})
    return processes


def print_gantt_chart(timeline):
    """
    Prints a simple text-based Gantt chart.
    timeline: list of tuples (pid, start_time, end_time)
    """
    print("\nGantt Chart:")
    top = "|"
    for pid, start, end in timeline:
        width = max(len(pid) + 2, len(str(end)) + 1)
        top += f" {pid} ".center(width - 1) + "|"
    print(top)

    # Print time markers under each block boundary
    line = f"{timeline[0][1]}"
    for pid, start, end in timeline:
        width = max(len(pid) + 2, len(str(end)) + 1)
        line += str(end).rjust(width)
    print(line)


def fcfs_scheduling(processes):
    """
    Non-Preemptive First Come First Serve (FCFS) scheduling.
    Processes are executed strictly in order of arrival time.
    """
    # Sort by arrival time (and pid as tie-breaker)
    procs = sorted(processes, key=lambda p: (p["at"], p["pid"]))

    time = 0
    timeline = []          # for Gantt chart: (pid, start, end)
    completion = {}

    for p in procs:
        # If CPU is idle before this process arrives, jump time forward
        if time < p["at"]:
            time = p["at"]
        start = time
        time += p["bt"]     # run process to completion (non-preemptive)
        end = time
        timeline.append((p["pid"], start, end))
        completion[p["pid"]] = end

    # Calculate waiting time and turnaround time for each process
    results = []
    total_wt = 0
    total_tat = 0
    for p in procs:
        ct = completion[p["pid"]]
        tat = ct - p["at"]          # Turnaround time = Completion - Arrival
        wt = tat - p["bt"]          # Waiting time = Turnaround - Burst
        total_tat += tat
        total_wt += wt
        results.append({"pid": p["pid"], "at": p["at"], "bt": p["bt"],
                         "ct": ct, "tat": tat, "wt": wt})

    avg_wt = total_wt / len(procs)
    avg_tat = total_tat / len(procs)

    print_gantt_chart(timeline)
    print_results_table(results)
    print(f"\nAverage Waiting Time   : {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


def round_robin_scheduling(processes, quantum):
    """
    Preemptive Round Robin scheduling.
    Each process gets a fixed time quantum; if it doesn't finish,
    it goes to the back of the ready queue.
    """
    # Work on copies so original burst times remain untouched
    remaining = {p["pid"]: p["bt"] for p in processes}
    procs_sorted = sorted(processes, key=lambda p: (p["at"], p["pid"]))

    timeline = []
    queue = []
    completion = {}
    i = 0                     # pointer into procs_sorted for arrivals
    n = len(procs_sorted)

    def add_new_arrivals(current_time):
        nonlocal i
        while i < n and procs_sorted[i]["at"] <= current_time:
            queue.append(procs_sorted[i])
            i += 1

    # Initialize time to the first arrival
    time = procs_sorted[0]["at"]
    add_new_arrivals(time)

    while queue:
        p = queue.pop(0)
        pid = p["pid"]

        if time < p["at"]:
            time = p["at"]

        start = time
        run_time = min(quantum, remaining[pid])
        time += run_time
        remaining[pid] -= run_time
        end = time
        timeline.append((pid, start, end))

        # Add any processes that arrived during this execution slice
        add_new_arrivals(time)

        if remaining[pid] > 0:
            queue.append(p)          # not finished -> back of queue
        else:
            completion[pid] = end    # finished

        # If queue becomes empty but not all processes have arrived yet,
        # jump time forward to the next arrival.
        if not queue and i < n:
            time = max(time, procs_sorted[i]["at"])
            add_new_arrivals(time)

    # Calculate waiting time and turnaround time
    results = []
    total_wt = 0
    total_tat = 0
    for p in procs_sorted:
        ct = completion[p["pid"]]
        tat = ct - p["at"]
        wt = tat - p["bt"]
        total_tat += tat
        total_wt += wt
        results.append({"pid": p["pid"], "at": p["at"], "bt": p["bt"],
                         "ct": ct, "tat": tat, "wt": wt})

    avg_wt = total_wt / len(procs_sorted)
    avg_tat = total_tat / len(procs_sorted)

    print_gantt_chart(timeline)
    print_results_table(results)
    print(f"\nAverage Waiting Time   : {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


def print_results_table(results):
    """Prints a table of AT, BT, CT, TAT, WT for each process."""
    print("\nProcess Details:")
    print(f"{'PID':<6}{'AT':<6}{'BT':<6}{'CT':<6}{'TAT':<6}{'WT':<6}")
    for r in results:
        print(f"{r['pid']:<6}{r['at']:<6}{r['bt']:<6}{r['ct']:<6}{r['tat']:<6}{r['wt']:<6}")


def run_fcfs():
    """Menu handler for FCFS scheduling."""
    processes = input_processes()
    fcfs_scheduling(processes)


def run_round_robin():
    """Menu handler for Round Robin scheduling."""
    processes = input_processes()
    quantum = int(input("Enter Time Quantum: "))
    round_robin_scheduling(processes, quantum)


def run_cpu_scheduling():
    """Submenu handler for CPU scheduling algorithms."""
    print("\nChoose Scheduling Algorithm:")
    print("1. Non-Preemptive: First Come First Serve (FCFS)")
    print("2. Preemptive: Round Robin (RR)")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        run_fcfs()
    elif choice == "2":
        run_round_robin()
    else:
        print("Invalid choice.")


# ------------------------------------------------------------
# SECTION 2: BANKER'S ALGORITHM
# ------------------------------------------------------------

def input_bankers_data():
    """Reads number of processes/resources, Allocation, Max, and Available."""
    n = int(input("Enter number of processes: "))
    m = int(input("Enter number of resource types: "))

    print("\nEnter Allocation Matrix:")
    allocation = []
    for i in range(n):
        row = list(map(int, input(f"P{i} (space-separated, {m} values): ").split()))
        allocation.append(row)

    print("\nEnter Maximum Matrix:")
    maximum = []
    for i in range(n):
        row = list(map(int, input(f"P{i} (space-separated, {m} values): ").split()))
        maximum.append(row)

    print("\nEnter Available Resources:")
    available = list(map(int, input(f"Available (space-separated, {m} values): ").split()))

    return n, m, allocation, maximum, available


def bankers_algorithm(n, m, allocation, maximum, available):
    """
    Implements the Banker's Algorithm safety check.
    Returns (is_safe, safe_sequence).
    """
    # Need matrix = Maximum - Allocation (resources still needed by each process)
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    work = available.copy()        # resources currently available
    finish = [False] * n           # tracks which processes have finished
    safe_sequence = []

    print("\nNeed Matrix:")
    for i in range(n):
        print(f"P{i}: {need[i]}")

    # Repeatedly look for a process whose need can be satisfied by 'work'
    count = 0
    while count < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                # Process i can finish: reclaim its allocated resources
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(f"P{i}")
                found = True
                count += 1

        if not found:
            # No process could be satisfied this pass -> unsafe state
            break

    is_safe = all(finish)
    return is_safe, safe_sequence


def run_bankers_algorithm():
    """Menu handler for Banker's Algorithm."""
    n, m, allocation, maximum, available = input_bankers_data()
    is_safe, safe_sequence = bankers_algorithm(n, m, allocation, maximum, available)

    if is_safe:
        print("\nSystem is in a Safe State.")
        print("Safe Sequence: " + " -> ".join(safe_sequence))
    else:
        print("\nSystem is in an UNSAFE State (deadlock may occur).")


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

def main():
    while True:
        print("\n" + "=" * 50)
        print("OS SIMULATION MENU")
        print("=" * 50)
        print("1. CPU Scheduling Algorithms")
        print("2. Banker's Algorithm")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            run_cpu_scheduling()
        elif choice == "2":
            run_bankers_algorithm()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()