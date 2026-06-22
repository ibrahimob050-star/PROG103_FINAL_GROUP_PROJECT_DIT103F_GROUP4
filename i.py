"""
Student Academic Portal - SDG 4 Quality Education
Professional UI Version with Modern Design
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# =========================================================
# 1. CONSTANTS AND DATA CONFIGURATION
# =========================================================
EXCELLENT = "Excellent"
GOOD = "Good"
CREDIT = "Credit"
PASS = "Pass"
FAIL = "Fail"

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "student_data.json")
student_records = []
selected_student_id = None

# Professional Color Scheme
COLORS = {
    "bg": "#0a0e17",
    "bg_secondary": "#111927",
    "bg_tertiary": "#1a2332",
    "bg_card": "#0f1a2e",
    "border": "#1e3a5f",
    "text_primary": "#e8edf5",
    "text_secondary": "#8899bb",
    "text_muted": "#4a5a7a",
    "accent_cyan": "#00d4ff",
    "accent_blue": "#4a9eff",
    "accent_green": "#00e676",
    "accent_gold": "#ffd700",
    "accent_purple": "#b388ff",
    "accent_orange": "#ff9100",
    "accent_red": "#ff5252",
    "accent_pink": "#ff4081",
    "gradient_1": "#00d4ff",
    "gradient_2": "#7c4dff",
}

# =========================================================
# 2. FILE PERSISTENCE FUNCTIONS
# =========================================================
def load_data_from_file():
    global student_records
    if not os.path.exists(DATA_FILE):
        student_records = []
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            student_records = data if isinstance(data, list) else []
    except json.JSONDecodeError:
        student_records = []
        messagebox.showwarning(
            "Data Warning",
            "The data file is damaged or empty. The system will start with no records."
        )
    except Exception as error:
        student_records = []
        messagebox.showerror("Load Error", f"Could not load records:\n{error}")


def save_data_to_file():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(student_records, file, indent=4)
        return True
    except Exception as error:
        messagebox.showerror("Storage Error", f"Could not save records:\n{error}")
        return False

# =========================================================
# 3. BACKEND FUNCTIONS
# =========================================================
def calculate_grade(mark):
    if mark >= 80:
        return "A", EXCELLENT
    if mark >= 70:
        return "B", GOOD
    if mark >= 60:
        return "C", CREDIT
    if mark >= 50:
        return "D", PASS
    return "F", FAIL


def validate_student_input(student_id, name, course_mark):
    if not student_id or not name or not course_mark:
        return False, "All fields are required."

    if len(student_id) < 2:
        return False, "Student ID is too short."

    if len(name) < 3:
        return False, "Full name must be at least 3 characters."

    try:
        mark = float(course_mark)
    except ValueError:
        return False, "Course mark must be a valid number."

    if mark < 0 or mark > 100:
        return False, "Course mark must be between 0 and 100."

    return True, mark


def add_student_record(student_id, name, course_mark):
    valid, result = validate_student_input(student_id, name, course_mark)
    if not valid:
        return False, result

    mark = result

    for student in student_records:
        if student["ID"].lower() == student_id.lower():
            return False, f"A student with ID '{student_id}' already exists."

    letter_grade, classification = calculate_grade(mark)
    record = {
        "ID": student_id,
        "Name": name.title(),
        "Mark": mark,
        "Grade": letter_grade,
        "Status": classification,
        "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    student_records.append(record)

    if save_data_to_file():
        return True, f"Record for {name.title()} was added successfully."
    return False, "The record was not saved."


def update_student_record(old_id, new_id, name, course_mark):
    valid, result = validate_student_input(new_id, name, course_mark)
    if not valid:
        return False, result

    mark = result

    for student in student_records:
        if student["ID"].lower() == new_id.lower() and student["ID"].lower() != old_id.lower():
            return False, f"Another student already uses ID '{new_id}'."

    for student in student_records:
        if student["ID"].lower() == old_id.lower():
            letter_grade, classification = calculate_grade(mark)
            student["ID"] = new_id
            student["Name"] = name.title()
            student["Mark"] = mark
            student["Grade"] = letter_grade
            student["Status"] = classification
            student["Date_Added"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_data_to_file()
            return True, "Selected record was updated successfully."

    return False, "Selected record was not found."


def delete_student_record(student_id):
    global student_records
    original_count = len(student_records)
    student_records = [s for s in student_records if s["ID"].lower() != student_id.lower()]

    if len(student_records) == original_count:
        return False, "Record was not found."

    save_data_to_file()
    return True, "Record was deleted successfully."


def generate_summary_report():
    if not student_records:
        return "No records available to summarize."

    total_students = len(student_records)
    total_marks = 0
    passed_students = 0
    failed_students = 0
    highest = student_records[0]
    lowest = student_records[0]
    
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for student in student_records:
        total_marks += student["Mark"]
        grade_distribution[student["Grade"]] += 1
        
        if student["Grade"] != "F":
            passed_students += 1
        else:
            failed_students += 1

        if student["Mark"] > highest["Mark"]:
            highest = student
        if student["Mark"] < lowest["Mark"]:
            lowest = student

    average_mark = total_marks / total_students
    pass_rate = (passed_students / total_students) * 100

    return (
        "═" * 50 + "\n"
        "  📊 STUDENT ACADEMIC PORTAL SUMMARY  \n"
        "═" * 50 + "\n\n"
        f"  📚 Total Students    : {total_students}\n"
        f"  📈 Class Average     : {average_mark:.2f}%\n"
        f"  ✅ Passed Students   : {passed_students}\n"
        f"  ❌ Failed Students   : {failed_students}\n"
        f"  🎯 Pass Rate         : {pass_rate:.1f}%\n\n"
        "  ── Grade Distribution ──\n"
        f"  🟢 A (Excellent)     : {grade_distribution['A']}\n"
        f"  🔵 B (Good)          : {grade_distribution['B']}\n"
        f"  🟡 C (Credit)        : {grade_distribution['C']}\n"
        f"  🟠 D (Pass)          : {grade_distribution['D']}\n"
        f"  🔴 F (Fail)          : {grade_distribution['F']}\n\n"
        "  ── Top & Bottom ──\n"
        f"  🏆 Highest Mark      : {highest['Name']} - {highest['Mark']:.1f}%\n"
        f"  📉 Lowest Mark       : {lowest['Name']} - {lowest['Mark']:.1f}%\n"
        "═" * 50
    )

# =========================================================
# 4. GUI CLASS - MODERN PROFESSIONAL UI
# =========================================================
class StudentPortalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Academic Portal - SDG 4 Quality Education")
        self.root.geometry("1000x720")
        self.root.minsize(900, 650)
        self.root.configure(bg=COLORS["bg"])
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Set application icon (if available)
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
            
        # Load data
        load_data_from_file()
        
        # Build UI
        self.create_header()
        self.create_input_panel()
        self.create_action_buttons()
        self.create_search_panel()
        self.create_table_panel()
        self.create_status_bar()
        
        # Refresh display
        self.refresh_records_display()
    
    def create_header(self):
        """Create modern header with gradient effect"""
        header_frame = tk.Frame(self.root, bg=COLORS["bg_secondary"], height=80)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        # Title with icon
        title_label = tk.Label(
            header_frame,
            text="🎓 STUDENT ACADEMIC PORTAL",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["bg_secondary"],
            fg=COLORS["accent_cyan"],
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="SDG 4: Quality Education | Structured Programming Project",
            font=("Segoe UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"],
        )
        subtitle_label.pack(side=tk.LEFT, padx=20)
        
        # Stats badge
        self.stats_label = tk.Label(
            header_frame,
            text="📊 0 Students",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["bg_tertiary"],
            fg=COLORS["accent_green"],
            padx=15,
            pady=5,
            relief=tk.FLAT,
        )
        self.stats_label.pack(side=tk.RIGHT, padx=30)
        
        # Decorative line
        line = tk.Frame(self.root, bg=COLORS["border"], height=2)
        line.grid(row=1, column=0, sticky="ew")
    
    def create_input_panel(self):
        """Create modern input panel with card design"""
        input_frame = tk.Frame(self.root, bg=COLORS["bg_card"], relief=tk.FLAT, bd=0)
        input_frame.grid(row=2, column=0, padx=25, pady=15, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)
        input_frame.grid_columnconfigure(5, weight=1)
        
        # Inner padding
        inner_frame = tk.Frame(input_frame, bg=COLORS["bg_card"])
        inner_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        inner_frame.grid_columnconfigure(1, weight=1)
        inner_frame.grid_columnconfigure(3, weight=1)
        
        # Title
        title_label = tk.Label(
            inner_frame,
            text="📝 Student Record Input",
            font=("Segoe UI", 13, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["accent_cyan"],
        )
        title_label.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 15))
        
        # Row 1: ID and Name
        # ID
        id_label = tk.Label(
            inner_frame,
            text="Student ID:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        )
        id_label.grid(row=1, column=0, sticky="w", padx=(0, 5))
        
        self.entry_id = tk.Entry(
            inner_frame,
            font=("Segoe UI", 11),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
        )
        self.entry_id.grid(row=1, column=1, sticky="ew", padx=(0, 20))
        
        # Name
        name_label = tk.Label(
            inner_frame,
            text="Full Name:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        )
        name_label.grid(row=1, column=2, sticky="w", padx=(0, 5))
        
        self.entry_name = tk.Entry(
            inner_frame,
            font=("Segoe UI", 11),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
        )
        self.entry_name.grid(row=1, column=3, sticky="ew", padx=(0, 20))
        
        # Row 2: Mark and Buttons
        mark_label = tk.Label(
            inner_frame,
            text="Course Mark (%):",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        )
        mark_label.grid(row=2, column=0, sticky="w", padx=(0, 5), pady=(10, 0))
        
        self.entry_mark = tk.Entry(
            inner_frame,
            font=("Segoe UI", 11),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
        )
        self.entry_mark.grid(row=2, column=1, sticky="ew", padx=(0, 20), pady=(10, 0))
        
        # Action buttons in input panel
        btn_frame = tk.Frame(inner_frame, bg=COLORS["bg_card"])
        btn_frame.grid(row=2, column=2, columnspan=4, sticky="e", pady=(10, 0))
        
        self.btn_add = self.create_modern_button(
            btn_frame, "➕ Add", COLORS["accent_green"], self.handle_add_student, 0
        )
        self.btn_update = self.create_modern_button(
            btn_frame, "✏️ Update", COLORS["accent_blue"], self.handle_update_student, 1, state=tk.DISABLED
        )
        self.btn_clear = self.create_modern_button(
            btn_frame, "🗑️ Clear", COLORS["accent_orange"], self.clear_entries, 2
        )
        
        # Hint
        hint_label = tk.Label(
            inner_frame,
            text="💡 Tip: Enter mark from 0 to 100. Select a row in the table to update or delete.",
            font=("Segoe UI", 9),
            bg=COLORS["bg_card"],
            fg=COLORS["text_muted"],
        )
        hint_label.grid(row=3, column=0, columnspan=6, sticky="w", pady=(12, 0))
    
    def create_modern_button(self, parent, text, color, command, column, state=tk.NORMAL):
        """Create a modern styled button"""
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg=COLORS["text_primary"],
            activebackground=color,
            activeforeground=COLORS["text_primary"],
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            command=command,
            state=state,
        )
        btn.grid(row=0, column=column, padx=5)
        
        # Add hover effect
        def on_enter(e):
            btn.config(bg=self.adjust_brightness(color, 1.2))
        def on_leave(e):
            btn.config(bg=color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def adjust_brightness(self, hex_color, factor):
        """Adjust brightness of a hex color"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def create_action_buttons(self):
        """Create action buttons panel"""
        action_frame = tk.Frame(self.root, bg=COLORS["bg"])
        action_frame.grid(row=3, column=0, padx=25, pady=(0, 10), sticky="ew")
        
        # Center the buttons
        center_frame = tk.Frame(action_frame, bg=COLORS["bg"])
        center_frame.pack(anchor="center")
        
        buttons = [
            ("📊 Summary", COLORS["accent_purple"], self.handle_show_summary),
            ("🗑️ Delete Selected", COLORS["accent_red"], self.handle_delete_selected),
            ("🧹 Clear All", COLORS["accent_orange"], self.handle_clear_all),
            ("🚪 Exit", COLORS["accent_pink"], self.root.destroy),
        ]
        
        for i, (text, color, command) in enumerate(buttons):
            btn = self.create_modern_button(center_frame, text, color, command, i)
            btn.config(padx=20, pady=6)
    
    def create_search_panel(self):
        """Create modern search panel"""
        search_frame = tk.Frame(self.root, bg=COLORS["bg_card"], relief=tk.FLAT)
        search_frame.grid(row=4, column=0, padx=25, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(1, weight=1)
        
        inner_frame = tk.Frame(search_frame, bg=COLORS["bg_card"])
        inner_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        inner_frame.grid_columnconfigure(1, weight=1)
        
        # Search icon and label
        search_label = tk.Label(
            inner_frame,
            text="🔍 Search:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["text_secondary"],
        )
        search_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.entry_search = tk.Entry(
            inner_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["accent_cyan"],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=COLORS["border"],
            highlightbackground=COLORS["border"],
        )
        self.entry_search.grid(row=0, column=1, sticky="ew")
        self.entry_search.bind("<KeyRelease>", lambda event: self.handle_search())
        
        show_all_btn = tk.Button(
            inner_frame,
            text="Show All",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["accent_blue"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["accent_blue"],
            activeforeground=COLORS["text_primary"],
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor="hand2",
            command=lambda: [self.search_var.set(""), self.refresh_records_display()],
        )
        show_all_btn.grid(row=0, column=2, padx=(10, 0))
    
    def create_table_panel(self):
        """Create modern table with professional styling"""
        table_frame = tk.LabelFrame(
            self.root,
            text=" 📋 Registered Students ",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["bg_card"],
            fg=COLORS["accent_cyan"],
            relief=tk.FLAT,
            bd=0,
        )
        table_frame.grid(row=5, column=0, padx=25, pady=(0, 15), sticky="nsew")
        self.root.grid_rowconfigure(5, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Custom styles for Treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure the treeview style
        style.configure(
            "Custom.Treeview",
            background=COLORS["bg_secondary"],
            foreground=COLORS["text_primary"],
            fieldbackground=COLORS["bg_secondary"],
            rowheight=30,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=COLORS["bg_tertiary"],
            foreground=COLORS["accent_cyan"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="solid",
        )
        style.map("Custom.Treeview",
            background=[("selected", COLORS["accent_blue"])],
            foreground=[("selected", COLORS["text_primary"])],
        )
        
        # Create treeview
        columns = ("ID", "Name", "Mark", "Grade", "Status", "Date Added")
        self.records_tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            style="Custom.Treeview",
            height=15,
        )
        
        # Configure columns
        column_widths = {
            "ID": 120,
            "Name": 250,
            "Mark": 100,
            "Grade": 100,
            "Status": 150,
            "Date Added": 180,
        }
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=column_widths[col], anchor="center" if col != "Name" else "w")
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.records_tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.records_tree.xview)
        self.records_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Grid layout
        self.records_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.records_tree.bind("<<TreeviewSelect>>", self.fill_selected_record)
    
    def create_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.root, bg=COLORS["bg_secondary"], height=30)
        status_frame.grid(row=6, column=0, sticky="ew")
        status_frame.grid_propagate(False)
        
        self.status_var = tk.StringVar(value="✅ Ready")
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_secondary"],
            anchor="w",
            padx=20,
        )
        status_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Record count on status bar
        self.record_count_label = tk.Label(
            status_frame,
            text="📊 0 records",
            font=("Segoe UI", 9),
            bg=COLORS["bg_secondary"],
            fg=COLORS["text_muted"],
            padx=20,
        )
        self.record_count_label.pack(side=tk.RIGHT)
    
    # =========================================================
    # 5. GUI EVENT HANDLERS
    # =========================================================
    def clear_entries(self):
        global selected_student_id
        selected_student_id = None
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_mark.delete(0, tk.END)
        self.btn_update.config(state=tk.DISABLED)
        self.btn_add.config(state=tk.NORMAL)
        self.status_var.set("✅ Ready")
        self.entry_id.focus_set()
    
    def refresh_records_display(self, records=None):
        if records is None:
            records = student_records
        
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        
        for student in records:
            self.records_tree.insert(
                "",
                tk.END,
                values=(
                    student["ID"],
                    student["Name"],
                    f"{student['Mark']:.1f}",
                    student["Grade"],
                    student["Status"],
                    student.get("Date_Added", "N/A"),
                ),
            )
        
        self.status_var.set(f"✅ Showing {len(records)} record(s)")
        self.stats_label.config(text=f"📊 {len(records)} Students")
        self.record_count_label.config(text=f"📊 {len(records)} records")
    
    def fill_selected_record(self, event=None):
        global selected_student_id
        selected = self.records_tree.selection()
        if not selected:
            return
        
        values = self.records_tree.item(selected[0], "values")
        selected_student_id = values[0]
        
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, values[0])
        
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])
        
        self.entry_mark.delete(0, tk.END)
        self.entry_mark.insert(0, values[2])
        
        self.btn_add.config(state=tk.DISABLED)
        self.btn_update.config(state=tk.NORMAL)
        self.status_var.set(f"✏️ Editing record: {values[0]} - {values[1]}")
    
    def handle_add_student(self):
        s_id = self.entry_id.get().strip()
        s_name = self.entry_name.get().strip()
        s_mark = self.entry_mark.get().strip()
        
        success, message = add_student_record(s_id, s_name, s_mark)
        if success:
            messagebox.showinfo("✅ Success", message, parent=self.root)
            self.clear_entries()
            self.refresh_records_display()
        else:
            messagebox.showerror("❌ Error", message, parent=self.root)
    
    def handle_update_student(self):
        if not selected_student_id:
            messagebox.showwarning("⚠️ No Selection", "Please select a record from the table first.", parent=self.root)
            return
        
        success, message = update_student_record(
            selected_student_id,
            self.entry_id.get().strip(),
            self.entry_name.get().strip(),
            self.entry_mark.get().strip(),
        )
        
        if success:
            messagebox.showinfo("✅ Updated", message, parent=self.root)
            self.clear_entries()
            self.refresh_records_display()
        else:
            messagebox.showerror("❌ Error", message, parent=self.root)
    
    def handle_delete_selected(self):
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ No Selection", "Please select a record to delete.", parent=self.root)
            return
        
        values = self.records_tree.item(selected[0], "values")
        student_id = values[0]
        student_name = values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Delete record for {student_name}?", parent=self.root):
            success, message = delete_student_record(student_id)
            if success:
                messagebox.showinfo("✅ Deleted", message, parent=self.root)
                self.clear_entries()
                self.refresh_records_display()
            else:
                messagebox.showerror("❌ Error", message, parent=self.root)
    
    def handle_show_summary(self):
        summary = generate_summary_report()
        messagebox.showinfo("📊 Portal Summary", summary, parent=self.root)
    
    def handle_search(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.refresh_records_display()
            return
        
        filtered = []
        for student in student_records:
            if (query in student["ID"].lower() or 
                query in student["Name"].lower() or 
                query in student["Grade"].lower() or
                query in student["Status"].lower()):
                filtered.append(student)
        
        self.refresh_records_display(filtered)
    
    def handle_clear_all(self):
        global student_records
        if not student_records:
            messagebox.showinfo("ℹ️ No Data", "There are no records to clear.", parent=self.root)
            return
        
        if messagebox.askyesno("⚠️ Confirm Clear", "Are you sure you want to delete ALL stored records?\nThis action cannot be undone!", parent=self.root):
            student_records = []
            save_data_to_file()
            self.clear_entries()
            self.refresh_records_display()
            messagebox.showinfo("✅ Cleared", "All records have been deleted.", parent=self.root)

# =========================================================
# 6. MAIN APPLICATION LAUNCH
# =========================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentPortalApp(root)
    root.mainloop()