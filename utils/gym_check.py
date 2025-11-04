from rich import print
import csv
from collections import defaultdict
import datetime
from rich.table import Table
from rich.console import Console
import math

filename = "stronglifts/StrongLifts20251030.csv"
rows = []

with open(filename, "r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Read the header row
    for row in csvreader:
        rows.append(row)


def check_gym_frequency(start_date, end_date, rows):
    """
    Checks if the user has gone to the gym at least 3 times in the last 7 days (including end_date).
    Returns True if workouts >= 3 in that window, False otherwise.
    """
    unique_dates = set()
    for row in rows:
        try:
            row_date = datetime.datetime.strptime(row[0], "%Y/%m/%d").date()
            if start_date <= row_date <= end_date:
                unique_dates.add(row_date)
        except ValueError:
            continue

    if not unique_dates:
        return True

    window_start = end_date - datetime.timedelta(days=6)
    recent_workouts = [d for d in unique_dates if window_start <= d <= end_date]

    return len(recent_workouts) >= 3


def print_banner():
    """
    Prints a big red blinking banner using ANSI escape codes.
    Note: Blinking may not work in all terminals.
    """
    banner_text = """
GGGG   OOO        TTTTT  OOO        TTTTT H   H EEEEE       GGGG  Y   Y M   M 
G     O   O         T   O   O         T   H   H E           G      Y Y  MM MM 
G GG  O   O         T   O   O         T   HHHHH EEE         G GG    Y   M M M 
G  G  O   O         T   O   O         T   H   H E           G  G    Y   M   M 
GGGG   OOO          T    OOO          T   H   H EEEEE       GGGG    Y   M   M 
    """
    print(banner_text)


def strength_gains_since(start_date_str):
    """
    Prints a table showing strength gain stats since the given date using rich.
    If gym frequency is less than 3x/week, prints a banner first.

    Parameters:
    start_date_str (str): The start date in 'yyyy/mm/dd' format.
    """
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y/%m/%d").date()
    except ValueError:
        print("Invalid date format. Please use 'yyyy/mm/dd'.")
        return

    # Assume end date is current date; adjust if needed
    end_date = datetime.date.today()

    # Filter rows since the start date
    filtered_rows = []
    for row in rows:
        try:
            row_date = datetime.datetime.strptime(row[0], "%Y/%m/%d").date()
            if row_date >= start_date:
                filtered_rows.append(row)
        except ValueError:
            continue  # Skip rows with invalid dates

    if not filtered_rows:
        print("No data available since the given date.")
        return

    # Check frequency and print banner if needed
    if not check_gym_frequency(start_date, end_date, filtered_rows):
        print_banner()

    # Collect stats: exercise -> list of (date, e1RM)
    stats = defaultdict(list)
    for row in filtered_rows:
        if row[9]:  # Check if e1RM is present
            try:
                date = datetime.datetime.strptime(row[0], "%Y/%m/%d").date()
                e1rm = float(row[9])
                exercise = row[5]
                stats[exercise].append((date, e1rm))
            except ValueError:
                continue  # Skip invalid e1RM

    if not stats:
        print("No valid e1RM data found.")
        return

    # Prepare table
    table = Table(title=f"Strength Gains Since {start_date_str}")
    table.border_style = "bright_green"
    table.header_style = "bold white on blue"
    columns = [
        "Exercise",
        "Start Date",
        "Start e1RM (KG)",
        "End Date",
        "End e1RM (KG)",
        "Gain (KG)",
        "Gain (%)",
        "Last 5 Sess Gain (%)",
    ]
    column_styles = [
        "bold cyan",
        "dim white",
        "yellow",
        "dim white",
        "yellow",
        "green",
        "green",
        "magenta",
    ]
    for col, style in zip(columns, column_styles):
        table.add_column(col, justify="center", style=style)

    for exercise in sorted(stats.keys()):
        lst = sorted(stats[exercise])  # Sort by date
        if lst:
            start_d, start_e = lst[0]
            end_d, end_e = lst[-1]
            gain = end_e - start_e
            percent = (gain / start_e * 100) if start_e > 0 else 0

            last = 3
            if len(lst) >= last:
                old_e = lst[-last][1]
                gain_last5 = end_e - old_e
                percent_last5 = (gain_last5 / old_e * 100) if old_e > 0 else 0
            else:
                percent_last5 = f"N/A (<{last -1} sess)"

            gain_kg_str = f"{gain:.1f}kg"
            gain_pct_str = f"{percent:.1f}%"
            last_pct_str = (
                f"{percent_last5:.1f}%"
                if isinstance(percent_last5, (int, float))
                else percent_last5
            )

            table.add_row(
                exercise,
                str(start_d),
                f"{start_e:.1f}",
                str(end_d),
                f"{end_e:.1f}",
                gain_kg_str,
                gain_pct_str,
                last_pct_str,
            )

    console = Console()
    console.print(table)


# strength_gains_since("2025/09/20")
