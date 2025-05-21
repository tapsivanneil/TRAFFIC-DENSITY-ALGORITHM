import mysql.connector
import tkinter as tk
from tkinter import ttk

# --- Database Connection ---
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cavitestateuniversity",
    database="traffic_density"
)
sql = mydb.cursor()

# --- Main Window ---
root = tk.Tk()
root.title("Traffic Report Dashboard")
root.geometry("1200x800")

# =========================
# 🔼 TOP: GROUPED AVERAGES
# =========================

# --- Top Controls ---
group_frame = ttk.LabelFrame(root, text="Grouped Averages", padding=10)
group_frame.pack(fill="x", padx=10, pady=(10, 5))

ttk.Label(group_frame, text="Group by:").pack(side="left")
group_var = tk.StringVar(value="hour")
group_options = ["hour", "day", "date", "week", "month", "year"]
group_menu = ttk.Combobox(group_frame, textvariable=group_var, values=group_options, state="readonly", width=10)
group_menu.pack(side="left", padx=5)

ttk.Label(group_frame, text="Limit:").pack(side="left")
group_limit_var = tk.StringVar(value="50")
group_limit_entry = ttk.Entry(group_frame, width=5, textvariable=group_limit_var)
group_limit_entry.pack(side="left", padx=5)

def load_grouped_data():
    group_by = group_var.get()
    try:
        limit = int(group_limit_var.get())
    except ValueError:
        limit = 50

    query = f"""
        SELECT 
            {group_by} AS group_value,
            AVG(density) AS avg_density,
            AVG(class_1) AS avg_class_1,
            AVG(class_2) AS avg_class_2,
            AVG(class_3) AS avg_class_3,
            AVG(class_4) AS avg_class_4
        FROM report
        GROUP BY {group_by}
        ORDER BY {group_by}
        LIMIT {limit}
    """
    sql.execute(query)
    rows = sql.fetchall()

    grouped_tree.delete(*grouped_tree.get_children())
    for row in rows:
        grouped_tree.insert("", "end", values=row)

ttk.Button(group_frame, text="Refresh", command=load_grouped_data).pack(side="left", padx=10)

# --- Treeview for Grouped Averages ---
grouped_columns = [
    "group", "avg_density", "avg_class_1", "avg_class_2", "avg_class_3", "avg_class_4"
]

grouped_tree_frame = ttk.Frame(root, padding=10)
grouped_tree_frame.pack(fill="both", expand=False)

grouped_tree = ttk.Treeview(grouped_tree_frame, columns=grouped_columns, show="headings")
for col in grouped_columns:
    grouped_tree.heading(col, text=col.upper())
    grouped_tree.column(col, width=150, anchor="center")
grouped_tree.pack(fill="x")

# ============================
# 🔽 BOTTOM: RAW REPORT RECORDS
# ============================

# --- Bottom Controls ---
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
        raw_tree.insert("", "end", values=row)

ttk.Button(raw_frame, text="Refresh", command=load_raw_data).pack(side="left", padx=10)

# --- Treeview for Raw Data ---
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

# --- Load initial data ---
load_grouped_data()
load_raw_data()

# --- Run App ---
root.mainloop()
