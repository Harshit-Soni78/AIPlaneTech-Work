import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import sys
from datetime import datetime

# --- Configuration ---
# Determine the absolute path for the database file
# It will be in the same directory as the script
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle/frozen executable (e.g., PyInstaller)
    APPLICATION_PATH = os.path.dirname(sys.executable)
else:
    # If run as a normal .py script
    APPLICATION_PATH = os.path.dirname(os.path.abspath(__file__))

DB_FILENAME = "app_parameters.db"
DB_ABSOLUTE_PATH = os.path.join(APPLICATION_PATH, DB_FILENAME)
TABLE_NAME = "settings"

# --- Database Functions ---
def initialize_database():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DB_ABSOLUTE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                bias_parameter TEXT,
                description_bias_parameter TEXT
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}\nDatabase path: {DB_ABSOLUTE_PATH}")
    finally:
        if conn:
            conn.close()

def save_parameters_to_db(bias_param, desc_bias_param):
    """Saves the provided parameters to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_ABSOLUTE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (bias_parameter, description_bias_parameter, timestamp)
            VALUES (?, ?, ?)
        """, (bias_param, desc_bias_param, datetime.now()))
        conn.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save parameters: {e}")
        return False
    finally:
        if conn:
            conn.close()

def check_if_parameters_exist(bias_param, desc_bias_param):
    """Checks if the given parameter combination already exists in the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_ABSOLUTE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 1 FROM {TABLE_NAME}
            WHERE bias_parameter = ? AND description_bias_parameter = ?
        """, (bias_param, desc_bias_param))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to check parameters: {e}")
        return False # Assume not found on error to prevent accidental overwrite, or handle differently
    finally:
        if conn:
            conn.close()


def fetch_all_parameters_from_db():
    """Fetches all parameters from the database, ordered by ID descending."""
    conn = None
    try:
        conn = sqlite3.connect(DB_ABSOLUTE_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, timestamp, bias_parameter, description_bias_parameter
            FROM {TABLE_NAME}
            ORDER BY id DESC
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to fetch parameters: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- GUI Functions ---
def on_save_button_click():
    """Handles the save button click event."""
    # Get values from entry fields
    bias_param_val = bias_param_entry.get()
    desc_bias_param_val = desc_bias_param_entry.get()

    # Check for missing entries
    if not bias_param_val:
        messagebox.showerror("Input Error", "Bias Parameter cannot be empty.")
        status_var.set("Error: Bias Parameter is missing.")
        return

    if not desc_bias_param_val:
        messagebox.showerror("Input Error", "Description Bias Parameter cannot be empty.")
        status_var.set("Error: Description Bias Parameter is missing.")
        return

    # Check if the entry already exists
    if check_if_parameters_exist(bias_param_val, desc_bias_param_val):
        messagebox.showerror("Input Error", "This parameter combination already exists in the database.")
        status_var.set("Error: Parameter combination already exists.")
        return

    # Save to database
    if save_parameters_to_db(bias_param_val, desc_bias_param_val):
        status_var.set("Parameters saved successfully!")
        bias_param_entry.delete(0, tk.END)
        desc_bias_param_entry.delete(0, tk.END)
    else:
        status_var.set("Failed to save parameters.")

def open_database_viewer_window():
    """Opens a new window to display database contents."""
    viewer_window = tk.Toplevel(root)
    viewer_window.title("Database Viewer - Stored Parameters")
    viewer_window.geometry("900x500") # Adjusted size for better viewing

    viewer_frame = ttk.Frame(viewer_window, padding="10 10 10 10")
    viewer_frame.pack(expand=True, fill=tk.BOTH)

    cols = ("ID", "Timestamp", "Bias Parameter Code", "Description of Bias Parameter")
    tree = ttk.Treeview(viewer_frame, columns=cols, show='headings', selectmode="browse")

    # Define headings and column properties
    col_widths = {
        "ID": 50, "Timestamp": 160, "Bias Parameter Code": 250, "Description of Bias Parameter": 300
    }
    for col_name in cols:
        tree.heading(col_name, text=col_name, command=lambda _col=col_name: treeview_sort_column(tree, _col, False))
        tree.column(col_name, width=col_widths.get(col_name, 100), anchor=tk.W)

    # Scrollbars
    vsb = ttk.Scrollbar(viewer_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(viewer_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    viewer_frame.grid_rowconfigure(0, weight=1)
    viewer_frame.grid_columnconfigure(0, weight=1)

    def refresh_treeview_data():
        # Clear existing items
        for i in tree.get_children():
            tree.delete(i)
        # Fetch and insert new data
        records = fetch_all_parameters_from_db()
        for record in records:
            # Format timestamp for better readability if needed
            # record_list = list(record)
            # if record_list[1]: # Assuming timestamp is at index 1
            #     try:
            #         dt_obj = datetime.fromisoformat(record_list[1].split('.')[0]) # Handle potential microseconds
            #         record_list[1] = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
            #     except ValueError:
            #         pass # Keep original if parsing fails
            tree.insert("", tk.END, values=record)

    refresh_button = ttk.Button(viewer_frame, text="Refresh Data", command=refresh_treeview_data)
    refresh_button.grid(row=2, column=0, pady=10, sticky='ew')

    refresh_treeview_data() # Initial data load

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(key=lambda t: (t[0] is None, t[0] == '', float(t[0]) if str(t[0]).replace('.', '', 1).isdigit() else str(t[0]).lower()), reverse=reverse)
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

# --- Main Application Setup ---
if __name__ == "__main__":
    # Initialize database first
    initialize_database()

    # Create main window
    root = tk.Tk()
    root.title("Defination of Bias Parameters")

    # Create a frame for input fields
    input_frame = ttk.Frame(root, padding="20 20 20 20")
    input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Parameter: Bias_parameter (Text)
    ttk.Label(input_frame, text="Bias Parameter Code:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
    bias_param_entry = ttk.Entry(input_frame, width=40)
    bias_param_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

    # Parameter: Description_Bias_parameter (Text)
    ttk.Label(input_frame, text="Description of Bias Parameter:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
    desc_bias_param_entry = ttk.Entry(input_frame, width=40)
    desc_bias_param_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

    # Save Button
    save_button = ttk.Button(input_frame, text="Save Parameters", command=on_save_button_click)
    save_button.grid(row=2, column=0, pady=(20,5), padx=5, sticky=tk.EW)

    # View Database Button
    view_db_button = ttk.Button(input_frame, text="View Database", command=open_database_viewer_window)
    view_db_button.grid(row=2, column=1, pady=(20,5), padx=5, sticky=tk.EW)

    # Status Label
    status_var = tk.StringVar()
    status_label = ttk.Label(input_frame, textvariable=status_var, foreground="green")
    status_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Configure column weights for resizing
    input_frame.columnconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Start the GUI event loop
    root.mainloop()