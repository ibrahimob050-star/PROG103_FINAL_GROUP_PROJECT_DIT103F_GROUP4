# edumaster_app.py - Complete Functional Version
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Global variables
root = None
data_file = 'edumaster_data.json'
db = {}
current_user = None
current_page = None
pages = {}
nav_buttons = {}
colors = {}
login_tab = None
signup_tab = None
login_form = None
signup_form = None
login_email = None
login_password = None
signup_name = None
signup_email = None
signup_role = None
signup_password = None
page_title = None
welcome_text = None

# Treeview references for search
student_tree = None
teacher_tree = None
class_tree = None
attendance_tree = None
grade_tree = None
fee_tree = None

# Default data
default_data = {
    "users": [
        {"name": "School Admin", "email": "admin@school.com", "password": "admin123", "role": "admin"}
    ],
    "students": [
        {"id": "STU001", "name": "Aminata Kamara", "className": "JSS 1", "gender": "Female", "guardian": "Mrs. Kamara"},
        {"id": "STU002", "name": "Mohamed Sesay", "className": "SSS 2", "gender": "Male", "guardian": "Mr. Sesay"}
    ],
    "teachers": [
        {"name": "Mr. Conteh", "subject": "Mathematics", "phone": "076000111"},
        {"name": "Miss Bangura", "subject": "English", "phone": "077000222"}
    ],
    "classes": [
        {"className": "JSS 1", "teacher": "Mr. Conteh", "room": "Room 1"},
        {"className": "SSS 2", "teacher": "Miss Bangura", "room": "Room 5"}
    ],
    "attendance": [
        {"studentId": "STU001", "student": "Aminata Kamara", "className": "JSS 1", "date": "2026-06-16", "status": "Present"}
    ],
    "grades": [
        {"studentId": "STU002", "student": "Mohamed Sesay", "subject": "Mathematics", "score": 82, "grade": "A"}
    ],
    "fees": [
        {"studentId": "STU001", "student": "Aminata Kamara", "amount": 500000, "status": "Paid", "date": "2026-06-16"}
    ]
}

# ==================== DATA FUNCTIONS ====================

def load_data():
    """Load data from file or create default"""
    global db
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                db = json.load(f)
                return
        except:
            db = default_data.copy()
            return
    db = default_data.copy()

def save_data():
    """Save data to file"""
    with open(data_file, 'w') as f:
        json.dump(db, f, indent=2)

# ==================== SETUP FUNCTIONS ====================

def setup_styles():
    """Configure application colors"""
    global colors
    colors = {
        'primary': '#173b7a',
        'secondary': '#f3b21b',
        'bg': '#f4f7fb',
        'dark': '#102033',
        'text': '#4c5a6a',
        'white': '#ffffff',
        'danger': '#d94b4b',
        'success': '#1f9d55',
        'warning': '#f39c12',
        'light_gray': '#edf1f7'
    }
    
    # Configure ttk styles
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure("Treeview", 
                   background=colors['white'],
                   foreground=colors['dark'],
                   rowheight=30,
                   fieldbackground=colors['white'])
    style.map('Treeview', 
             background=[('selected', colors['primary'])],
             foreground=[('selected', 'white')])

def clear_window():
    """Clear all widgets from window"""
    for widget in root.winfo_children():
        widget.destroy()

# ==================== AUTH FUNCTIONS ====================

def show_login_page():
    """Display login/signup page"""
    global login_tab, signup_tab, login_form, signup_form
    global login_email, login_password, signup_name, signup_email, signup_role, signup_password
    
    clear_window()
    
    # Main container
    main_frame = tk.Frame(root, bg=colors['primary'])
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Center card
    card = tk.Frame(main_frame, bg=colors['white'], padx=40, pady=30)
    card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450)
    
    # Brand
    brand_frame = tk.Frame(card, bg=colors['white'])
    brand_frame.pack(fill=tk.X, pady=(0, 20))
    
    logo = tk.Label(brand_frame, text="EM", font=('Arial', 32, 'bold'),
                   bg=colors['secondary'], fg=colors['primary'],
                   width=4, height=2)
    logo.pack(side=tk.LEFT, padx=(0, 15))
    
    brand_text = tk.Frame(brand_frame, bg=colors['white'])
    brand_text.pack(side=tk.LEFT)
    tk.Label(brand_text, text="EduMaster", font=('Arial', 24, 'bold'),
            bg=colors['white'], fg=colors['primary']).pack(anchor=tk.W)
    tk.Label(brand_text, text="Standard School Management System",
            font=('Arial', 10), bg=colors['white'], fg=colors['text']).pack(anchor=tk.W)
    
    # Tabs
    tab_frame = tk.Frame(card, bg=colors['light_gray'], padx=6, pady=6)
    tab_frame.pack(fill=tk.X, pady=(0, 20))
    
    login_tab = tk.Button(tab_frame, text="Login", font=('Arial', 10, 'bold'),
                         bg=colors['primary'], fg='white',
                         padx=20, pady=8, relief=tk.FLAT,
                         command=lambda: switch_auth('login'))
    login_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    signup_tab = tk.Button(tab_frame, text="Sign Up", font=('Arial', 10, 'bold'),
                          bg=colors['light_gray'], fg=colors['text'],
                          padx=20, pady=8, relief=tk.FLAT,
                          command=lambda: switch_auth('signup'))
    signup_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # Login Form
    login_form = tk.Frame(card, bg=colors['white'])
    login_form.pack(fill=tk.X)
    
    tk.Label(login_form, text="Welcome Back", font=('Arial', 16, 'bold'),
            bg=colors['white'], fg=colors['dark']).pack(anchor=tk.W, pady=(0, 15))
    
    tk.Label(login_form, text="Email", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    login_email = tk.Entry(login_form, font=('Arial', 11), relief=tk.FLAT,
                          bg='#f8fafc', highlightthickness=1, highlightcolor=colors['primary'])
    login_email.pack(fill=tk.X, pady=(5, 15))
    login_email.insert(0, "admin@school.com")
    
    tk.Label(login_form, text="Password", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    login_password = tk.Entry(login_form, font=('Arial', 11), relief=tk.FLAT,
                             bg='#f8fafc', highlightthickness=1, highlightcolor=colors['primary'],
                             show='*')
    login_password.pack(fill=tk.X, pady=(5, 15))
    login_password.insert(0, "admin123")
    
    login_btn = tk.Button(login_form, text="Login", font=('Arial', 11, 'bold'),
                         bg=colors['primary'], fg='white', padx=20, pady=12,
                         relief=tk.FLAT, cursor='hand2',
                         command=handle_login)
    login_btn.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(login_form, text="Demo admin: admin@school.com / admin123",
            font=('Arial', 9), bg=colors['white'], fg=colors['text']).pack()
    
    # Signup Form
    signup_form = tk.Frame(card, bg=colors['white'])
    
    tk.Label(signup_form, text="Create Account", font=('Arial', 16, 'bold'),
            bg=colors['white'], fg=colors['dark']).pack(anchor=tk.W, pady=(0, 15))
    
    tk.Label(signup_form, text="Full Name", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    signup_name = tk.Entry(signup_form, font=('Arial', 11), relief=tk.FLAT,
                          bg='#f8fafc', highlightthickness=1, highlightcolor=colors['primary'])
    signup_name.pack(fill=tk.X, pady=(5, 15))
    
    tk.Label(signup_form, text="Email", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    signup_email = tk.Entry(signup_form, font=('Arial', 11), relief=tk.FLAT,
                           bg='#f8fafc', highlightthickness=1, highlightcolor=colors['primary'])
    signup_email.pack(fill=tk.X, pady=(5, 15))
    
    tk.Label(signup_form, text="Role", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    signup_role = ttk.Combobox(signup_form, font=('Arial', 11),
                              values=['Student', 'Teacher', 'Parent'],
                              state='readonly')
    signup_role.pack(fill=tk.X, pady=(5, 15))
    
    tk.Label(signup_form, text="Password", bg=colors['white'],
            font=('Arial', 10), fg=colors['text']).pack(anchor=tk.W)
    signup_password = tk.Entry(signup_form, font=('Arial', 11), relief=tk.FLAT,
                              bg='#f8fafc', highlightthickness=1, highlightcolor=colors['primary'],
                              show='*')
    signup_password.pack(fill=tk.X, pady=(5, 15))
    
    signup_btn = tk.Button(signup_form, text="Create Account", font=('Arial', 11, 'bold'),
                          bg=colors['primary'], fg='white', padx=20, pady=12,
                          relief=tk.FLAT, cursor='hand2',
                          command=handle_signup)
    signup_btn.pack(fill=tk.X)

def switch_auth(mode):
    """Switch between login and signup forms"""
    global login_tab, signup_tab, login_form, signup_form
    if mode == 'login':
        login_tab.config(bg=colors['primary'], fg='white')
        signup_tab.config(bg=colors['light_gray'], fg=colors['text'])
        login_form.pack(fill=tk.X)
        signup_form.pack_forget()
    else:
        signup_tab.config(bg=colors['primary'], fg='white')
        login_tab.config(bg=colors['light_gray'], fg=colors['text'])
        signup_form.pack(fill=tk.X)
        login_form.pack_forget()

def handle_login():
    """Process login"""
    global current_user
    email = login_email.get().strip()
    password = login_password.get().strip()
    
    user = next((u for u in db['users'] 
                 if u['email'] == email and u['password'] == password), None)
    
    if not user:
        messagebox.showerror("Login Failed", "Wrong email or password")
        return
    
    current_user = user
    show_dashboard()

def handle_signup():
    """Process signup - Adds student to students collection with ID"""
    name = signup_name.get().strip()
    email = signup_email.get().strip()
    role = signup_role.get().lower()
    password = signup_password.get().strip()
    
    if not all([name, email, role, password]):
        messagebox.showerror("Error", "All fields are required")
        return
    
    if any(u['email'] == email for u in db['users']):
        messagebox.showerror("Error", "Email already exists")
        return
    
    # Add user to users collection
    db['users'].append({
        'name': name,
        'email': email,
        'role': role,
        'password': password
    })
    
    # If role is student, also add to students collection with generated ID
    if role == 'student':
        student_id = f"STU{len(db['students']) + 1:03d}"
        db['students'].append({
            'id': student_id,
            'name': name,
            'className': 'Not Assigned',
            'gender': 'Not Specified',
            'guardian': 'Not Specified'
        })
        messagebox.showinfo("Success", f"Student {name} registered with ID: {student_id}")
    else:
        messagebox.showinfo("Success", f"Account created for {name}!")
    
    save_data()
    switch_auth('login')
    signup_name.delete(0, tk.END)
    signup_email.delete(0, tk.END)
    signup_role.set('')
    signup_password.delete(0, tk.END)

# ==================== DASHBOARD FUNCTIONS ====================

def show_dashboard():
    """Display main dashboard"""
    global page_title, welcome_text, pages, nav_buttons
    global student_tree, teacher_tree, class_tree, attendance_tree, grade_tree, fee_tree
    
    clear_window()
    
    # Main container
    main_container = tk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Sidebar
    sidebar = tk.Frame(main_container, bg=colors['primary'], width=260)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    
    # Brand in sidebar
    brand_frame = tk.Frame(sidebar, bg=colors['primary'], pady=20)
    brand_frame.pack(fill=tk.X)
    
    logo = tk.Label(brand_frame, text="EM", font=('Arial', 24, 'bold'),
                   bg=colors['secondary'], fg=colors['primary'],
                   width=3, height=1)
    logo.pack(side=tk.LEFT, padx=15)
    
    tk.Label(brand_frame, text="EduMaster", font=('Arial', 18, 'bold'),
            bg=colors['primary'], fg='white').pack(side=tk.LEFT, padx=5)
    
    # Navigation buttons
    nav_frame = tk.Frame(sidebar, bg=colors['primary'])
    nav_frame.pack(fill=tk.X, pady=20)
    
    nav_items = [
        ("Dashboard", "dashboard"),
        ("Students", "students"),
        ("Teachers", "teachers"),
        ("Classes", "classes"),
        ("Attendance", "attendance"),
        ("Grades", "grades"),
        ("Fees", "fees")
    ]
    
    if current_user['role'] == 'admin':
        nav_items.append(("Admin Users", "users"))
    
    nav_buttons = {}
    for text, page in nav_items:
        btn = tk.Button(nav_frame, text=text, font=('Arial', 11, 'bold'),
                       bg=colors['primary'], fg='white',
                       relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                       cursor='hand2',
                       command=lambda p=page: switch_page(p))
        btn.pack(fill=tk.X, padx=10, pady=2)
        nav_buttons[page] = btn
    
    # Logout button
    logout_btn = tk.Button(sidebar, text="Logout", font=('Arial', 11, 'bold'),
                          bg=colors['danger'], fg='white',
                          relief=tk.FLAT, padx=20, pady=12,
                          cursor='hand2',
                          command=logout)
    logout_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=20)
    
    # Content area
    content_frame = tk.Frame(main_container, bg=colors['bg'])
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Top bar
    topbar = tk.Frame(content_frame, bg=colors['white'], height=80)
    topbar.pack(fill=tk.X, padx=20, pady=20)
    topbar.pack_propagate(False)
    
    title_frame = tk.Frame(topbar, bg=colors['white'])
    title_frame.pack(side=tk.LEFT, padx=20, pady=15)
    
    page_title = tk.Label(title_frame, text="Dashboard",
                         font=('Arial', 20, 'bold'),
                         bg=colors['white'], fg=colors['dark'])
    page_title.pack(anchor=tk.W)
    
    welcome_text = tk.Label(title_frame, text=f"Welcome, {current_user['name']}",
                           font=('Arial', 11),
                           bg=colors['white'], fg=colors['text'])
    welcome_text.pack(anchor=tk.W)
    
    profile_frame = tk.Frame(topbar, bg=colors['white'])
    profile_frame.pack(side=tk.RIGHT, padx=20)
    
    role_badge = tk.Label(profile_frame, text=current_user['role'].title(),
                         font=('Arial', 10, 'bold'),
                         bg=colors['light_gray'], fg=colors['primary'],
                         padx=15, pady=5)
    role_badge.pack(side=tk.RIGHT, padx=5)
    
    tk.Label(profile_frame, text=current_user['name'],
            font=('Arial', 11, 'bold'),
            bg=colors['white'], fg=colors['dark']).pack(side=tk.RIGHT, padx=10)
    
    # Pages container
    pages = {}
    for page in ['dashboard', 'students', 'teachers', 'classes', 'attendance', 'grades', 'fees', 'users']:
        frame = tk.Frame(content_frame, bg=colors['bg'])
        pages[page] = frame
    
    # Initialize dashboard
    switch_page('dashboard')

def switch_page(page):
    """Switch between pages"""
    global page_title, pages, nav_buttons
    
    # Hide all pages
    for p in pages.values():
        p.pack_forget()
    
    # Show selected page
    if page in pages:
        pages[page].pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    # Update nav buttons
    for p, btn in nav_buttons.items():
        if p == page:
            btn.config(bg=colors['secondary'], fg=colors['primary'])
        else:
            btn.config(bg=colors['primary'], fg='white')
    
    # Update page title
    page_titles = {
        'dashboard': 'Dashboard',
        'students': 'Students',
        'teachers': 'Teachers',
        'classes': 'Classes',
        'attendance': 'Attendance',
        'grades': 'Grades',
        'fees': 'Fees',
        'users': 'Admin Users'
    }
    page_title.config(text=page_titles.get(page, 'Dashboard'))
    
    # Render page content
    if page == 'dashboard':
        render_dashboard()
    elif page == 'students':
        render_students()
    elif page == 'teachers':
        render_teachers()
    elif page == 'classes':
        render_classes()
    elif page == 'attendance':
        render_attendance()
    elif page == 'grades':
        render_grades()
    elif page == 'fees':
        render_fees()
    elif page == 'users':
        render_users()

# ==================== DASHBOARD RENDER FUNCTIONS ====================

def render_dashboard():
    """Render dashboard page"""
    frame = pages['dashboard']
    
    # Clear frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Stats cards
    stats_frame = tk.Frame(frame, bg=colors['bg'])
    stats_frame.pack(fill=tk.X, pady=(0, 20))
    
    stats = [
        ("Total Students", len(db['students'])),
        ("Total Teachers", len(db['teachers'])),
        ("Classes", len(db['classes'])),
        ("Total Fees", f"Le {sum(float(f['amount']) for f in db['fees']):,.0f}")
    ]
    
    for i, (label, value) in enumerate(stats):
        card = tk.Frame(stats_frame, bg=colors['white'], relief=tk.RAISED, bd=1)
        card.grid(row=0, column=i, padx=10, sticky='nsew')
        stats_frame.grid_columnconfigure(i, weight=1)
        
        tk.Label(card, text=label, font=('Arial', 11),
                bg=colors['white'], fg=colors['text']).pack(pady=(15, 5))
        tk.Label(card, text=str(value), font=('Arial', 28, 'bold'),
                bg=colors['white'], fg=colors['primary']).pack(pady=(0, 15))
    
    # Overview panel
    overview = tk.Frame(frame, bg=colors['white'], padx=20, pady=20)
    overview.pack(fill=tk.BOTH, expand=True)
    
    tk.Label(overview, text="School Overview", font=('Arial', 16, 'bold'),
            bg=colors['white'], fg=colors['dark']).pack(anchor=tk.W)
    
    tk.Label(overview, text="This dashboard helps the school manage learners, staff, classes, "
                           "attendance, grades, payments, and user accounts from one place.",
            font=('Arial', 11), bg=colors['white'], fg=colors['text'],
            wraplength=800, justify=tk.LEFT).pack(pady=10, anchor=tk.W)

# ==================== TABLE FUNCTIONS ====================

def create_table(parent, columns, data, actions=True):
    """Create a table with scrollbar"""
    # Frame for table
    table_frame = tk.Frame(parent, bg=colors['white'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Treeview
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
    
    # Scrollbars
    v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
    
    # Pack scrollbars
    v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Configure columns
    for col in columns:
        heading = col.replace('_', ' ').title()
        tree.heading(col, text=heading)
        tree.column(col, width=120, anchor=tk.W)
    
    # Insert data
    for i, row in enumerate(data):
        values = []
        for col in columns:
            value = row.get(col, '')
            # Format the value
            if col == 'amount' and isinstance(value, (int, float)):
                value = f"Le {value:,.0f}"
            values.append(value)
        
        # Insert the row
        tree.insert('', tk.END, values=values, tags=(str(i),))
        
        # Color coding for status
        if 'status' in row:
            status = row['status'].lower()
            if status in ['paid', 'present']:
                tree.tag_configure('paid', background='#e9f9ef')
            elif status in ['unpaid', 'absent']:
                tree.tag_configure('unpaid', background='#fff0f0')
            elif status in ['pending', 'late']:
                tree.tag_configure('pending', background='#fff8df')
    
    return tree

def search_table(tree, query):
    """Search and filter table"""
    if not tree:
        return
        
    # Get all items
    all_items = tree.get_children()
    
    if not query:
        # Show all items
        for item in all_items:
            try:
                tree.reattach(item, '', tk.END)
            except:
                pass
        return
    
    # Search and filter
    for item in all_items:
        values = tree.item(item)['values']
        # Check if query matches any value
        if any(query.lower() in str(v).lower() for v in values):
            try:
                tree.reattach(item, '', tk.END)
            except:
                pass
        else:
            try:
                tree.detach(item)
            except:
                pass

def on_tree_click(event, tree, collection):
    """Handle click on tree item"""
    if not tree:
        return
        
    # Get selected item
    item = tree.selection()
    if not item:
        return
    
    # Only admin can delete
    if current_user['role'] != 'admin':
        return
    
    # Show delete option
    if messagebox.askyesno("Delete Record", "Delete this record?"):
        # Get the index from the item
        index = tree.index(item[0])
        if 0 <= index < len(db[collection]):
            del db[collection][index]
            save_data()
            # Refresh current page
            current_page_name = page_title.cget('text').lower()
            switch_page(current_page_name)
            messagebox.showinfo("Success", "Record deleted successfully")

# ==================== PAGE RENDER FUNCTIONS ====================

def render_students():
    """Render students page with ID column"""
    global student_tree
    frame = pages['students']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Header
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Students", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Add Student", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_student)
        add_btn.pack(side=tk.RIGHT)
    
    # Search
    search_frame = tk.Frame(frame, bg=colors['bg'])
    search_frame.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(search_frame, text="Search:", bg=colors['bg'],
            font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_entry.bind('<KeyRelease>', lambda e: search_table(student_tree, search_entry.get()))
    
    # Table with ID column
    columns = ['id', 'name', 'className', 'gender', 'guardian']
    student_tree = create_table(frame, columns, db['students'])
    student_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, student_tree, 'students'))

def render_teachers():
    """Render teachers page"""
    global teacher_tree
    frame = pages['teachers']
    for widget in frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Teachers", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Add Teacher", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_teacher)
        add_btn.pack(side=tk.RIGHT)
    
    columns = ['name', 'subject', 'phone']
    teacher_tree = create_table(frame, columns, db['teachers'])
    teacher_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, teacher_tree, 'teachers'))

def render_classes():
    """Render classes page"""
    global class_tree
    frame = pages['classes']
    for widget in frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Classes", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Add Class", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_class)
        add_btn.pack(side=tk.RIGHT)
    
    columns = ['className', 'teacher', 'room']
    class_tree = create_table(frame, columns, db['classes'])
    class_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, class_tree, 'classes'))

def render_attendance():
    """Render attendance page with student ID and class"""
    global attendance_tree
    frame = pages['attendance']
    for widget in frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Attendance", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Mark Attendance", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_attendance)
        add_btn.pack(side=tk.RIGHT)
    
    columns = ['studentId', 'student', 'className', 'date', 'status']
    attendance_tree = create_table(frame, columns, db['attendance'])
    attendance_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, attendance_tree, 'attendance'))

def render_grades():
    """Render grades page"""
    global grade_tree
    frame = pages['grades']
    for widget in frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Grades", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Add Grade", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_grade)
        add_btn.pack(side=tk.RIGHT)
    
    columns = ['studentId', 'student', 'subject', 'score', 'grade']
    grade_tree = create_table(frame, columns, db['grades'])
    grade_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, grade_tree, 'grades'))

def render_fees():
    """Render fees page"""
    global fee_tree
    frame = pages['fees']
    for widget in frame.winfo_children():
        widget.destroy()
    
    header = tk.Frame(frame, bg=colors['bg'])
    header.pack(fill=tk.X, pady=(0, 10))
    
    tk.Label(header, text="Fees", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(side=tk.LEFT)
    
    if current_user['role'] in ['admin', 'teacher']:
        add_btn = tk.Button(header, text="Add Payment", font=('Arial', 10, 'bold'),
                           bg=colors['primary'], fg='white', padx=20, pady=8,
                           relief=tk.FLAT, cursor='hand2',
                           command=add_fee)
        add_btn.pack(side=tk.RIGHT)
    
    columns = ['studentId', 'student', 'amount', 'status', 'date']
    fee_tree = create_table(frame, columns, db['fees'])
    fee_tree.bind('<ButtonRelease-1>', lambda e: on_tree_click(e, fee_tree, 'fees'))

def render_users():
    """Render users page (admin only)"""
    frame = pages['users']
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame, text="Admin Users", font=('Arial', 18, 'bold'),
            bg=colors['bg'], fg=colors['dark']).pack(anchor=tk.W, pady=(0, 10))
    
    tk.Label(frame, text="Only admin can view registered users.",
            font=('Arial', 10), bg=colors['bg'], fg=colors['text']).pack(anchor=tk.W, pady=(0, 10))
    
    columns = ['name', 'email', 'role']
    create_table(frame, columns, db['users'], actions=False)

# ==================== ADD FUNCTIONS ====================

def add_student():
    """Add new student with ID"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Student")
    dialog.geometry("450x400")
    dialog.transient(root)
    dialog.grab_set()
    
    # Generate next student ID
    next_id = f"STU{len(db['students']) + 1:03d}"
    
    fields = [
        ("Student ID:", tk.Entry(dialog, font=('Arial', 11))),
        ("Name:", tk.Entry(dialog, font=('Arial', 11))),
        ("Class:", tk.Entry(dialog, font=('Arial', 11))),
        ("Gender:", ttk.Combobox(dialog, values=['Male', 'Female'], state='readonly')),
        ("Guardian:", tk.Entry(dialog, font=('Arial', 11)))
    ]
    
    # Set the ID field with generated value and make it read-only
    fields[0][1].insert(0, next_id)
    fields[0][1].config(state='readonly', bg='#f0f0f0')
    
    for i, (label, widget) in enumerate(fields):
        tk.Label(dialog, text=label, font=('Arial', 10)).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        widget.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        dialog.grid_columnconfigure(1, weight=1)
    
    def save():
        data = {
            'id': fields[0][1].get().strip(),
            'name': fields[1][1].get().strip(),
            'className': fields[2][1].get().strip(),
            'gender': fields[3][1].get(),
            'guardian': fields[4][1].get().strip()
        }
        
        if not all([data['name'], data['className'], data['gender'], data['guardian']]):
            messagebox.showerror("Error", "All fields except ID are required")
            return
        
        # Check if ID already exists
        if any(s['id'] == data['id'] for s in db['students']):
            messagebox.showerror("Error", f"Student ID {data['id']} already exists!")
            return
        
        db['students'].append(data)
        save_data()
        dialog.destroy()
        switch_page('students')
        messagebox.showinfo("Success", f"Student {data['name']} (ID: {data['id']}) added successfully!")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    tk.Button(btn_frame, text="Save", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def add_teacher():
    """Add new teacher"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Teacher")
    dialog.geometry("400x300")
    dialog.transient(root)
    dialog.grab_set()
    
    fields = [
        ("Name:", tk.Entry(dialog, font=('Arial', 11))),
        ("Subject:", tk.Entry(dialog, font=('Arial', 11))),
        ("Phone:", tk.Entry(dialog, font=('Arial', 11)))
    ]
    
    for i, (label, widget) in enumerate(fields):
        tk.Label(dialog, text=label, font=('Arial', 10)).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        widget.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        dialog.grid_columnconfigure(1, weight=1)
    
    def save():
        data = {
            'name': fields[0][1].get().strip(),
            'subject': fields[1][1].get().strip(),
            'phone': fields[2][1].get().strip()
        }
        
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required")
            return
        
        db['teachers'].append(data)
        save_data()
        dialog.destroy()
        switch_page('teachers')
        messagebox.showinfo("Success", "Teacher added successfully")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    tk.Button(btn_frame, text="Save", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def add_class():
    """Add new class"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Class")
    dialog.geometry("400x300")
    dialog.transient(root)
    dialog.grab_set()
    
    fields = [
        ("Class Name:", tk.Entry(dialog, font=('Arial', 11))),
        ("Teacher:", tk.Entry(dialog, font=('Arial', 11))),
        ("Room:", tk.Entry(dialog, font=('Arial', 11)))
    ]
    
    for i, (label, widget) in enumerate(fields):
        tk.Label(dialog, text=label, font=('Arial', 10)).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        widget.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        dialog.grid_columnconfigure(1, weight=1)
    
    def save():
        data = {
            'className': fields[0][1].get().strip(),
            'teacher': fields[1][1].get().strip(),
            'room': fields[2][1].get().strip()
        }
        
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required")
            return
        
        db['classes'].append(data)
        save_data()
        dialog.destroy()
        switch_page('classes')
        messagebox.showinfo("Success", "Class added successfully")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
    
    tk.Button(btn_frame, text="Save", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def add_attendance():
    """Mark attendance with student search by ID, name, or class"""
    dialog = tk.Toplevel(root)
    dialog.title("Mark Attendance")
    dialog.geometry("500x450")
    dialog.transient(root)
    dialog.grab_set()
    
    # Search frame
    search_frame = tk.LabelFrame(dialog, text="Search Student", font=('Arial', 10, 'bold'))
    search_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(search_frame, text="Search (ID, Name, or Class):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 11), width=30)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Student listbox with scrollbar
    list_frame = tk.Frame(search_frame)
    list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    student_listbox = tk.Listbox(list_frame, height=6, font=('Arial', 10), yscrollcommand=scrollbar.set)
    student_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=student_listbox.yview)
    
    # Populate student list
    students = db['students']
    for s in students:
        student_listbox.insert(tk.END, f"{s['id']} - {s['name']} ({s['className']})")
    
    def search_students():
        query = search_entry.get().strip().lower()
        student_listbox.delete(0, tk.END)
        for s in students:
            if (query in s['id'].lower() or 
                query in s['name'].lower() or 
                query in s['className'].lower()):
                student_listbox.insert(tk.END, f"{s['id']} - {s['name']} ({s['className']})")
    
    search_entry.bind('<KeyRelease>', lambda e: search_students())
    
    # Selected student display
    selected_frame = tk.LabelFrame(dialog, text="Selected Student", font=('Arial', 10, 'bold'))
    selected_frame.pack(fill=tk.X, padx=10, pady=10)
    
    selected_label = tk.Label(selected_frame, text="No student selected", font=('Arial', 11), fg='red')
    selected_label.pack(pady=5)
    
    # Attendance fields
    fields_frame = tk.Frame(dialog)
    fields_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(fields_frame, text="Date:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    date_entry = tk.Entry(fields_frame, font=('Arial', 11), width=25)
    date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    tk.Label(fields_frame, text="Status:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    status_combo = ttk.Combobox(fields_frame, values=['Present', 'Absent', 'Late'], state='readonly', width=23)
    status_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    status_combo.set('Present')
    
    # Store selected student data
    selected_student = {'id': '', 'name': '', 'class': ''}
    
    def select_student():
        selection = student_listbox.curselection()
        if not selection:
            return
        selected_text = student_listbox.get(selection[0])
        # Parse the selection
        parts = selected_text.split(' - ')
        if len(parts) == 2:
            student_id = parts[0]
            name_class = parts[1].split(' (')
            if len(name_class) == 2:
                selected_student['id'] = student_id
                selected_student['name'] = name_class[0]
                selected_student['class'] = name_class[1].replace(')', '')
                selected_label.config(text=f"{selected_student['id']} - {selected_student['name']} ({selected_student['class']})", fg='green')
    
    student_listbox.bind('<<ListboxSelect>>', lambda e: select_student())
    
    def save_attendance():
        if not selected_student['id']:
            messagebox.showerror("Error", "Please select a student")
            return
        
        date = date_entry.get().strip()
        status = status_combo.get()
        
        if not date or not status:
            messagebox.showerror("Error", "Date and Status are required")
            return
        
        # Check if attendance already exists for this student on this date
        existing = next((a for a in db['attendance'] 
                       if a['studentId'] == selected_student['id'] and a['date'] == date), None)
        if existing:
            if not messagebox.askyesno("Duplicate", f"Attendance for {selected_student['name']} on {date} already exists. Update?"):
                return
            # Remove existing
            db['attendance'].remove(existing)
        
        # Add new attendance record
        db['attendance'].append({
            'studentId': selected_student['id'],
            'student': selected_student['name'],
            'className': selected_student['class'],
            'date': date,
            'status': status
        })
        save_data()
        dialog.destroy()
        switch_page('attendance')
        messagebox.showinfo("Success", f"Attendance marked for {selected_student['name']}")
    
    # Buttons
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Save Attendance", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save_attendance).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def add_grade():
    """Add new grade with student search"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Grade")
    dialog.geometry("450x400")
    dialog.transient(root)
    dialog.grab_set()
    
    # Search frame
    search_frame = tk.LabelFrame(dialog, text="Search Student", font=('Arial', 10, 'bold'))
    search_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(search_frame, text="Search (ID or Name):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 11), width=25)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Student listbox
    list_frame = tk.Frame(search_frame)
    list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    student_listbox = tk.Listbox(list_frame, height=4, font=('Arial', 10), yscrollcommand=scrollbar.set)
    student_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=student_listbox.yview)
    
    students = db['students']
    for s in students:
        student_listbox.insert(tk.END, f"{s['id']} - {s['name']}")
    
    def search_students():
        query = search_entry.get().strip().lower()
        student_listbox.delete(0, tk.END)
        for s in students:
            if query in s['id'].lower() or query in s['name'].lower():
                student_listbox.insert(tk.END, f"{s['id']} - {s['name']}")
    
    search_entry.bind('<KeyRelease>', lambda e: search_students())
    
    selected_student = {'id': '', 'name': ''}
    
    def select_student():
        selection = student_listbox.curselection()
        if not selection:
            return
        selected_text = student_listbox.get(selection[0])
        parts = selected_text.split(' - ')
        if len(parts) == 2:
            selected_student['id'] = parts[0]
            selected_student['name'] = parts[1]
    
    student_listbox.bind('<<ListboxSelect>>', lambda e: select_student())
    
    # Grade fields
    fields_frame = tk.Frame(dialog)
    fields_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(fields_frame, text="Subject:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    subject_entry = tk.Entry(fields_frame, font=('Arial', 11), width=25)
    subject_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    
    tk.Label(fields_frame, text="Score:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    score_entry = tk.Entry(fields_frame, font=('Arial', 11), width=25)
    score_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    
    def get_grade(score):
        if score >= 80: return 'A'
        if score >= 70: return 'B'
        if score >= 60: return 'C'
        if score >= 50: return 'D'
        return 'F'
    
    def save_grade():
        if not selected_student['id']:
            messagebox.showerror("Error", "Please select a student")
            return
        
        subject = subject_entry.get().strip()
        try:
            score = float(score_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid score")
            return
        
        if not subject:
            messagebox.showerror("Error", "Subject is required")
            return
        
        if score < 0 or score > 100:
            messagebox.showerror("Error", "Score must be between 0 and 100")
            return
        
        data = {
            'studentId': selected_student['id'],
            'student': selected_student['name'],
            'subject': subject,
            'score': score,
            'grade': get_grade(score)
        }
        
        db['grades'].append(data)
        save_data()
        dialog.destroy()
        switch_page('grades')
        messagebox.showinfo("Success", f"Grade added for {selected_student['name']}")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Save Grade", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save_grade).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

def add_fee():
    """Add new fee payment with student search"""
    dialog = tk.Toplevel(root)
    dialog.title("Add Fee Payment")
    dialog.geometry("450x420")
    dialog.transient(root)
    dialog.grab_set()
    
    # Search frame
    search_frame = tk.LabelFrame(dialog, text="Search Student", font=('Arial', 10, 'bold'))
    search_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(search_frame, text="Search (ID or Name):", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(search_frame, font=('Arial', 11), width=25)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    
    # Student listbox
    list_frame = tk.Frame(search_frame)
    list_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    student_listbox = tk.Listbox(list_frame, height=4, font=('Arial', 10), yscrollcommand=scrollbar.set)
    student_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=student_listbox.yview)
    
    students = db['students']
    for s in students:
        student_listbox.insert(tk.END, f"{s['id']} - {s['name']}")
    
    def search_students():
        query = search_entry.get().strip().lower()
        student_listbox.delete(0, tk.END)
        for s in students:
            if query in s['id'].lower() or query in s['name'].lower():
                student_listbox.insert(tk.END, f"{s['id']} - {s['name']}")
    
    search_entry.bind('<KeyRelease>', lambda e: search_students())
    
    selected_student = {'id': '', 'name': ''}
    
    def select_student():
        selection = student_listbox.curselection()
        if not selection:
            return
        selected_text = student_listbox.get(selection[0])
        parts = selected_text.split(' - ')
        if len(parts) == 2:
            selected_student['id'] = parts[0]
            selected_student['name'] = parts[1]
    
    student_listbox.bind('<<ListboxSelect>>', lambda e: select_student())
    
    # Fee fields
    fields_frame = tk.Frame(dialog)
    fields_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(fields_frame, text="Amount:", font=('Arial', 10)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    amount_entry = tk.Entry(fields_frame, font=('Arial', 11), width=25)
    amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    
    tk.Label(fields_frame, text="Status:", font=('Arial', 10)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    status_combo = ttk.Combobox(fields_frame, values=['Paid', 'Pending', 'Unpaid'], state='readonly', width=23)
    status_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    status_combo.set('Paid')
    
    tk.Label(fields_frame, text="Date:", font=('Arial', 10)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    date_entry = tk.Entry(fields_frame, font=('Arial', 11), width=25)
    date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
    date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    
    def save_fee():
        if not selected_student['id']:
            messagebox.showerror("Error", "Please select a student")
            return
        
        try:
            amount = float(amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        
        status = status_combo.get()
        date = date_entry.get().strip()
        
        if not status or not date:
            messagebox.showerror("Error", "All fields are required")
            return
        
        data = {
            'studentId': selected_student['id'],
            'student': selected_student['name'],
            'amount': amount,
            'status': status,
            'date': date
        }
        
        db['fees'].append(data)
        save_data()
        dialog.destroy()
        switch_page('fees')
        messagebox.showinfo("Success", f"Payment added for {selected_student['name']}")
    
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Button(btn_frame, text="Save Payment", font=('Arial', 10, 'bold'),
             bg=colors['primary'], fg='white', padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=save_fee).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", font=('Arial', 10, 'bold'),
             bg='#e0e0e0', fg=colors['dark'], padx=20, pady=8,
             relief=tk.FLAT, cursor='hand2', command=dialog.destroy).pack(side=tk.LEFT, padx=5)

# ==================== LOGOUT FUNCTION ====================

def logout():
    """Logout user"""
    global current_user
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        current_user = None
        show_login_page()

# ==================== MAIN ====================

def main():
    global root
    root = tk.Tk()
    root.title("EduMaster School Management System")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    
    # Load data and setup
    load_data()
    setup_styles()
    
    # Show login page
    show_login_page()
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()