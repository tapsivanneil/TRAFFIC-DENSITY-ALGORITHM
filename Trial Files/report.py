import mysql.connector
import tkinter as tk
from tkinter import ttk

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cavitestateuniversity",
    database="traffic_density"
)
sql = mydb.cursor()

root = tk.Tk()
root.title("Traffic Report Dashboard")
root.geometry("1200x800")

group_frame = ttk.LabelFrame(root, text="Grouped Averages", padding=10)
group_frame.pack(fill="x", padx=10, pady=(10, 5))

ttk.Label(group_frame, text="Group by:").pack(side="left")
group_var = tk.StringVar(value="day")
group_options = ["hour", "day", "date", "week", "month", "year"]
group_menu = ttk.Combobox(group_frame, textvariable=group_var, values=group_options, state="readonly", width=10)
group_menu.pack(side="left", padx=5)

ttk.Label(group_frame, text="Limit:").pack(side="left")
group_limit_var = tk.StringVar(value="50")
group_limit_entry = ttk.Entry(group_frame, width=5, textvariable=group_limit_var)
group_limit_entry.pack(side="left", padx=5)

def convert_hour(hour):
    hour = int(hour)
    suffix = "AM" if hour < 12 else "PM"
    hour = hour % 12
    return f"{hour or 12} {suffix}"

def convert_day(day):
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return days[int(day)] if 0 <= int(day) <= 6 else str(day)

def convert_month(month):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[int(month) - 1] if 1 <= int(month) <= 12 else str(month)

def load_grouped_data():
    group_by = group_var.get()
    try:
        limit = int(group_limit_var.get())
    except ValueError:
        limit = 50

    query = f"""
        SELECT 
            {group_by} AS group_value,
            lane,
            AVG(density) AS avg_density
        FROM report
        GROUP BY {group_by}, lane
        ORDER BY {group_by}, lane
        LIMIT {limit}
    """
    sql.execute(query)
    rows = sql.fetchall()

    grouped_tree.delete(*grouped_tree.get_children())
    for row in rows:
        group_val = row[0]
        if group_by == "hour":
            group_val = convert_hour(group_val)
        elif group_by == "day":
            group_val = convert_day(group_val)
        elif group_by == "month":
            group_val = convert_month(group_val)
        grouped_tree.insert("", "end", values=(group_val, row[1], row[2]))

ttk.Button(group_frame, text="Refresh", command=load_grouped_data).pack(side="left", padx=10)

grouped_columns = ["group", "lane", "avg_density"]

grouped_tree_frame = ttk.Frame(root, padding=10)
grouped_tree_frame.pack(fill="both", expand=False)

grouped_tree = ttk.Treeview(grouped_tree_frame, columns=grouped_columns, show="headings")
for col in grouped_columns:
    grouped_tree.heading(col, text=col.upper())
    grouped_tree.column(col, width=180, anchor="center")
grouped_tree.pack(fill="x")

raw_frame = ttk.LabelFrame(root, text="Raw Report Data", padding=10)
raw_frame.pack(fill="x", padx=10, pady=(20, 5))

ttk.Label(raw_frame, text="Show last:").pack(side="left")
raw_limit_var = tk.StringVar(value="50")
raw_limit_entry = ttk.Entry(raw_frame, width=5, textvariable=raw_limit_var)
raw_limit_entry.pack(side="left", padx=5)

def load_raw_data():
    try:
        limit = int(raw_limit_var.get())
    except ValueError:
        limit = 50

    sql.execute(f"""
        SELECT minute, hour, day, date, week, month, year, lane,
               density, class_1, class_2, class_3, class_4
        FROM report
        ORDER BY id DESC
        LIMIT {limit}
    """)
    rows = sql.fetchall()

    raw_tree.delete(*raw_tree.get_children())
    for row in rows:
        row = list(row)
        row[1] = convert_hour(row[1])    # hour
        row[2] = convert_day(row[2])     # day
        row[5] = convert_month(row[5])   # month
        raw_tree.insert("", "end", values=row)

ttk.Button(raw_frame, text="Refresh", command=load_raw_data).pack(side="left", padx=10)

raw_columns = [
    "minute", "hour", "day", "date", "week", "month", "year", "lane",
    "density", "class_1", "class_2", "class_3", "class_4"
]

raw_tree_frame = ttk.Frame(root, padding=10)
raw_tree_frame.pack(fill="both", expand=True)

raw_tree = ttk.Treeview(raw_tree_frame, columns=raw_columns, show="headings")
for col in raw_columns:
    raw_tree.heading(col, text=col.upper())
    raw_tree.column(col, width=100, anchor="center")
raw_tree.pack(fill="both", expand=True)

load_grouped_data()
load_raw_data()

root.mainloop()
