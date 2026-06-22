# business_calculator.py - Complete Functional Version with User Registration
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import random
import hashlib

# Global variables
root = None
colors = {}
pages = {}
nav_buttons = {}
page_title = None
current_user = None
current_page = None
history = []
history_file = 'calc_history.json'
users_file = 'calc_users.json'

# Calculator variables
expression = None
result = None
npv_fields = {}
fv_fields = {}
pnl_fields = {}
inv_fields = {}
loan_fields = {}
npv_result = None
fv_result = None
pnl_results = {}
inv_results = {}
loan_results = {}
currency_amount = None
from_currency = None
to_currency = None
currency_result = None
rate_display = None

# Default users
default_users = {
    "users": [
        {
            "name": "John Doe",
            "email": "demo@business.com",
            "password": hashlib.sha256("password123".encode()).hexdigest(),
            "role": "admin",
            "created": datetime.now().isoformat()
        }
    ]
}

# Exchange rates
rates = {
    'USD': 1.0,
    'EUR': 0.85,
    'GBP': 0.73,
    'JPY': 110.5,
    'CAD': 1.25,
    'AUD': 1.35,
    'CHF': 0.92,
    'CNY': 6.45,
    'INR': 74.5,
    'BRL': 5.2,
    'ZAR': 14.8,
    'NGN': 412.0
}

# ==================== DATA FUNCTIONS ====================

def load_users():
    """Load users from file or create default"""
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r') as f:
                return json.load(f)
        except:
            return default_users.copy()
    return default_users.copy()

def save_users(users_data):
    """Save users to file"""
    with open(users_file, 'w') as f:
        json.dump(users_data, f, indent=2)

def load_history():
    """Load calculation history"""
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history_entry(entry):
    """Save calculation to history"""
    global history
    history.append(entry)
    if len(history) > 100:
        history = history[-100:]
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except:
        pass

def clear_history():
    """Clear calculation history"""
    global history
    if messagebox.askyesno("Clear History", "Delete all calculation history?"):
        history = []
        try:
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except:
            pass
        render_history()

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== SETUP FUNCTIONS ====================

def setup_colors():
    """Configure application colors"""
    global colors
    colors = {
        'bg_dark': '#0a0e27',
        'bg_medium': '#141838',
        'bg_light': '#1a1f45',
        'card': '#1e2450',
        'text': '#ffffff',
        'text_secondary': '#8892b0',
        'primary': '#4f46e5',
        'primary_light': '#6366f1',
        'secondary': '#06b6d4',
        'accent': '#f59e0b',
        'success': '#10b981',
        'danger': '#ef4444',
        'gold': '#fbbf24',
        'border': '#2d3566'
    }

def clear_window():
    """Clear all widgets"""
    for widget in root.winfo_children():
        widget.destroy()

# ==================== AUTH FUNCTIONS ====================

def show_login_splash():
    """Show login and registration screen.
    Fixed version: the registration form has a clear button, the card is taller,
    and all text/entry areas are padded so the content fits properly.
    """
    global root
    clear_window()

    main_frame = tk.Frame(root, bg=colors['bg_dark'])
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Simple background dots
    for i in range(18):
        x = random.randint(0, 1100)
        y = random.randint(0, 780)
        size = random.randint(2, 6)
        shade = random.randint(35, 85)
        tk.Label(main_frame, text='•', font=('Arial', size),
                 fg=f'#{shade:02x}{shade:02x}{shade:02x}',
                 bg=colors['bg_dark']).place(x=x, y=y)

    # Larger card so signup form and buttons do not disappear
    card = tk.Frame(main_frame, bg=colors['card'], relief=tk.FLAT, bd=0)
    card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=520, height=690)

    tk.Frame(card, bg=colors['primary'], height=3).pack(fill=tk.X, side=tk.TOP)

    title_frame = tk.Frame(card, bg=colors['card'])
    title_frame.pack(fill=tk.X, pady=(18, 8))

    logo_frame = tk.Frame(title_frame, bg=colors['primary'], width=58, height=58)
    logo_frame.pack(pady=(0, 8))
    logo_frame.pack_propagate(False)
    tk.Label(logo_frame, text="$$", font=('Segoe UI', 24, 'bold'),
             bg=colors['primary'], fg='white').pack(expand=True)

    tk.Label(title_frame, text="Business Calculator Pro",
             font=('Segoe UI', 20, 'bold'), bg=colors['card'], fg='white').pack()
    tk.Label(title_frame, text="Enterprise Financial Suite",
             font=('Segoe UI', 10), bg=colors['card'],
             fg=colors['text_secondary']).pack()

    tab_frame = tk.Frame(card, bg=colors['bg_medium'], padx=5, pady=5)
    tab_frame.pack(fill=tk.X, padx=35, pady=(8, 10))

    form_holder = tk.Frame(card, bg=colors['card'])
    form_holder.pack(fill=tk.BOTH, expand=True, padx=35, pady=(0, 5))

    def style_entry(parent, show=None):
        ent = tk.Entry(parent, font=('Segoe UI', 12), bg=colors['bg_light'], fg='white',
                       relief=tk.FLAT, insertbackground='white', highlightthickness=1,
                       highlightcolor=colors['primary'], highlightbackground=colors['border'],
                       show=show if show else '')
        ent.pack(fill=tk.X, pady=(0, 10), ipady=8)
        return ent

    def field(parent, label, show=None):
        tk.Label(parent, text=label, font=('Segoe UI', 10, 'bold'), bg=colors['card'],
                 fg=colors['text_secondary'], anchor=tk.W).pack(fill=tk.X, pady=(4, 4))
        return style_entry(parent, show=show)

    login_tab = tk.Button(tab_frame, text="Login", font=('Segoe UI', 10, 'bold'),
                          bg=colors['primary'], fg='white', relief=tk.FLAT,
                          cursor='hand2', command=lambda: switch_auth_tab('login'))
    login_tab.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

    signup_tab = tk.Button(tab_frame, text="Register", font=('Segoe UI', 10, 'bold'),
                           bg=colors['bg_medium'], fg=colors['text_secondary'],
                           relief=tk.FLAT, cursor='hand2',
                           command=lambda: switch_auth_tab('signup'))
    signup_tab.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

    # LOGIN FORM
    login_form = tk.Frame(form_holder, bg=colors['card'])
    login_form.pack(fill=tk.BOTH, expand=True)

    tk.Label(login_form, text="Login to your account", font=('Segoe UI', 15, 'bold'),
             bg=colors['card'], fg='white').pack(anchor=tk.W, pady=(2, 10))

    login_email = field(login_form, "Email Address")
    login_email.insert(0, "demo@business.com")
    login_password = field(login_form, "Password", show='•')
    login_password.insert(0, "password123")

    def handle_login():
        email = login_email.get().strip()
        password = login_password.get().strip()

        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter your email and password")
            return

        users_data = load_users()
        user = next((u for u in users_data['users']
                    if u['email'].lower() == email.lower() and u['password'] == hash_password(password)), None)

        if not user:
            messagebox.showerror("Login Failed", "Invalid email or password")
            return

        global current_user
        current_user = user
        show_dashboard()

    tk.Button(login_form, text="Access Dashboard", font=('Segoe UI', 12, 'bold'),
              bg=colors['primary'], fg='white', relief=tk.FLAT, cursor='hand2',
              command=handle_login).pack(fill=tk.X, pady=(10, 10), ipady=10)

    # This is the clear button the user asked for
    tk.Button(login_form, text="Create New Account / Register", font=('Segoe UI', 11, 'bold'),
              bg=colors['gold'], fg='#0a0e27', relief=tk.FLAT, cursor='hand2',
              command=lambda: switch_auth_tab('signup')).pack(fill=tk.X, pady=(0, 10), ipady=9)

    tk.Label(login_form, text="Demo account: demo@business.com / password123",
             font=('Segoe UI', 9), bg=colors['card'],
             fg=colors['text_secondary'], wraplength=430).pack(pady=(8, 0))

    # SIGNUP FORM
    signup_form = tk.Frame(form_holder, bg=colors['card'])

    tk.Label(signup_form, text="Register new account", font=('Segoe UI', 15, 'bold'),
             bg=colors['card'], fg='white').pack(anchor=tk.W, pady=(2, 8))

    signup_name = field(signup_form, "Full Name")
    signup_email = field(signup_form, "Email Address")
    signup_password = field(signup_form, "Password (minimum 6 characters)", show='•')
    signup_confirm = field(signup_form, "Confirm Password", show='•')

    def handle_signup():
        name = signup_name.get().strip()
        email = signup_email.get().strip()
        password = signup_password.get().strip()
        confirm = signup_confirm.get().strip()

        if not all([name, email, password, confirm]):
            messagebox.showerror("Registration Error", "All fields are required")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Registration Error", "Please enter a valid email address")
            return
        if password != confirm:
            messagebox.showerror("Registration Error", "Passwords do not match")
            return
        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters")
            return

        users_data = load_users()
        if any(u['email'].lower() == email.lower() for u in users_data['users']):
            messagebox.showerror("Registration Error", "Email already registered")
            return

        users_data['users'].append({
            "name": name,
            "email": email,
            "password": hash_password(password),
            "role": "user",
            "created": datetime.now().isoformat()
        })
        save_users(users_data)

        messagebox.showinfo("Registration Successful", f"Account created for {name}. You can now login.")
        switch_auth_tab('login')
        login_email.delete(0, tk.END)
        login_email.insert(0, email)
        login_password.delete(0, tk.END)

    tk.Button(signup_form, text="Register Account", font=('Segoe UI', 12, 'bold'),
              bg=colors['gold'], fg='#0a0e27', relief=tk.FLAT, cursor='hand2',
              command=handle_signup).pack(fill=tk.X, pady=(12, 8), ipady=10)

    tk.Button(signup_form, text="Back to Login", font=('Segoe UI', 10, 'bold'),
              bg=colors['bg_light'], fg='white', relief=tk.FLAT, cursor='hand2',
              command=lambda: switch_auth_tab('login')).pack(fill=tk.X, pady=(0, 5), ipady=8)

    def switch_auth_tab(mode):
        if mode == 'login':
            login_tab.config(bg=colors['primary'], fg='white')
            signup_tab.config(bg=colors['bg_medium'], fg=colors['text_secondary'])
            signup_form.pack_forget()
            login_form.pack(fill=tk.BOTH, expand=True)
        else:
            signup_tab.config(bg=colors['primary'], fg='white')
            login_tab.config(bg=colors['bg_medium'], fg=colors['text_secondary'])
            login_form.pack_forget()
            signup_form.pack(fill=tk.BOTH, expand=True)

    tk.Label(card, text="v3.2.1 Enterprise Edition",
             font=('Segoe UI', 8), bg=colors['card'],
             fg=colors['text_secondary']).pack(pady=(0, 8))

# ==================== DASHBOARD FUNCTIONS ====================


def show_dashboard():
    """Show main dashboard"""
    global pages, nav_buttons, page_title, current_page, history
    clear_window()
    
    history = load_history()
    
    # Main container
    main_container = tk.Frame(root, bg=colors['bg_dark'])
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Sidebar
    sidebar = tk.Frame(main_container, bg=colors['bg_medium'], width=240)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    
    # Sidebar header
    header_frame = tk.Frame(sidebar, bg=colors['bg_medium'])
    header_frame.pack(fill=tk.X, pady=20)
    
    tk.Label(header_frame, text="$$", font=('Segoe UI', 24, 'bold'),
            bg=colors['bg_medium'], fg=colors['gold']).pack()
    tk.Label(header_frame, text="Business Pro",
            font=('Segoe UI', 14, 'bold'),
            bg=colors['bg_medium'], fg='white').pack()
    
    # Navigation
    nav_frame = tk.Frame(sidebar, bg=colors['bg_medium'])
    nav_frame.pack(fill=tk.X, pady=20)
    
    nav_items = [
        ("📊 Dashboard", "dashboard"),
        ("🧮 Standard", "standard"),
        ("💹 Financial", "financial"),
        ("💰 Profit & Loss", "pnl"),
        ("📈 Investment", "investment"),
        ("🏦 Loan Calculator", "loan"),
        ("💵 Currency", "currency"),
        ("📋 History", "history"),
        ("👤 Users", "users")
    ]
    
    nav_buttons = {}
    for text, page in nav_items:
        btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 10),
                      bg=colors['bg_medium'], fg=colors['text_secondary'],
                      relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                      cursor='hand2', bd=0,
                      command=lambda p=page: switch_page(p))
        btn.pack(fill=tk.X, pady=2)
        nav_buttons[page] = btn
    
    # User info at bottom
    user_frame = tk.Frame(sidebar, bg=colors['bg_medium'])
    user_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
    
    tk.Label(user_frame, text=f"👤 {current_user.get('name', 'User')}",
            font=('Segoe UI', 10, 'bold'),
            bg=colors['bg_medium'], fg='white').pack()
    tk.Label(user_frame, text=current_user.get('role', 'user').title(),
            font=('Segoe UI', 9),
            bg=colors['bg_medium'], fg=colors['text_secondary']).pack()
    
    logout_btn = tk.Button(user_frame, text="Logout",
                          font=('Segoe UI', 9),
                          bg=colors['danger'], fg='white',
                          relief=tk.FLAT, cursor='hand2',
                          padx=20, pady=5,
                          command=logout)
    logout_btn.pack(pady=10)
    
    # Content area
    content_frame = tk.Frame(main_container, bg=colors['bg_dark'])
    content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Header
    header = tk.Frame(content_frame, bg=colors['bg_medium'], height=70)
    header.pack(fill=tk.X, pady=0)
    header.pack_propagate(False)
    
    page_title = tk.Label(header, text="Dashboard",
                         font=('Segoe UI', 20, 'bold'),
                         bg=colors['bg_medium'], fg='white')
    page_title.pack(side=tk.LEFT, padx=30, pady=20)
    
    # Quick stats
    stats_frame = tk.Frame(content_frame, bg=colors['bg_dark'])
    stats_frame.pack(fill=tk.X, padx=20, pady=20)
    
    # Pages container
    pages = {}
    for page in ['dashboard', 'standard', 'financial', 'pnl', 'investment', 'loan', 'currency', 'history', 'users']:
        frame = tk.Frame(content_frame, bg=colors['bg_dark'])
        pages[page] = frame
    
    current_page = 'dashboard'
    switch_page('dashboard')

def switch_page(page):
    """Switch between pages"""
    global current_page, pages, nav_buttons, page_title
    
    # Hide all pages
    for p in pages.values():
        p.pack_forget()
    
    # Show selected page
    if page in pages:
        pages[page].pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Update nav buttons
    page_names = {
        'dashboard': 'Dashboard',
        'standard': 'Standard Calculator',
        'financial': 'Financial Calculator',
        'pnl': 'Profit & Loss',
        'investment': 'Investment Calculator',
        'loan': 'Loan Calculator',
        'currency': 'Currency Converter',
        'history': 'History',
        'users': 'User Management'
    }
    
    for p, btn in nav_buttons.items():
        if p == page:
            btn.config(bg=colors['primary'], fg='white')
        else:
            btn.config(bg=colors['bg_medium'], fg=colors['text_secondary'])
    
    page_title.config(text=page_names.get(page, 'Dashboard'))
    current_page = page
    
    # Render page
    if page == 'dashboard':
        render_dashboard()
    elif page == 'standard':
        render_standard_calculator()
    elif page == 'financial':
        render_financial_calculator()
    elif page == 'pnl':
        render_pnl_calculator()
    elif page == 'investment':
        render_investment_calculator()
    elif page == 'loan':
        render_loan_calculator()
    elif page == 'currency':
        render_currency_converter()
    elif page == 'history':
        render_history()
    elif page == 'users':
        render_users()

def logout():
    """Logout user"""
    global current_user
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        current_user = None
        show_login_splash()

# ==================== DASHBOARD RENDER ====================

def render_dashboard():
    """Render dashboard page"""
    frame = pages['dashboard']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Stats cards
    stats_frame = tk.Frame(frame, bg=colors['bg_dark'])
    stats_frame.pack(fill=tk.X, pady=10)
    
    history_data = load_history()
    total_calc = len(history_data)
    
    # Calculate some stats
    financial_count = len([h for h in history_data if h.get('type') in ['npv', 'fv', 'pnl']])
    
    stats = [
        ("Total Calculations", str(total_calc), colors['primary']),
        ("Financial Analysis", str(financial_count), colors['secondary']),
        ("Active Users", str(len(load_users()['users'])), colors['success']),
        ("Status", "Online", colors['gold'])
    ]
    
    for i, (label, value, color) in enumerate(stats):
        card = tk.Frame(stats_frame, bg=colors['bg_medium'], relief=tk.FLAT, bd=0)
        card.grid(row=0, column=i, padx=10, sticky='nsew')
        stats_frame.grid_columnconfigure(i, weight=1)
        
        tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'),
                bg=colors['bg_medium'], fg=color).pack(pady=(15, 5))
        tk.Label(card, text=label, font=('Segoe UI', 11),
                bg=colors['bg_medium'], fg=colors['text_secondary']).pack(pady=(0, 15))
    
    # Quick access grid
    quick_frame = tk.Frame(frame, bg=colors['bg_dark'])
    quick_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
    tk.Label(quick_frame, text="Quick Access Tools",
            font=('Segoe UI', 16, 'bold'),
            bg=colors['bg_dark'], fg='white').pack(anchor=tk.W, pady=(0, 15))
    
    tools = [
        ("🧮 Standard\nCalculator", "standard"),
        ("💰 Profit &\nLoss Analysis", "pnl"),
        ("📈 Investment\nCalculator", "investment"),
        ("🏦 Loan\nCalculator", "loan")
    ]
    
    tools_frame = tk.Frame(quick_frame, bg=colors['bg_dark'])
    tools_frame.pack(fill=tk.BOTH, expand=True)
    
    for i, (text, page) in enumerate(tools):
        btn = tk.Button(tools_frame, text=text,
                      font=('Segoe UI', 11),
                      bg=colors['bg_medium'], fg='white',
                      relief=tk.FLAT, cursor='hand2',
                      height=4, width=20,
                      command=lambda p=page: switch_page(p))
        btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
        tools_frame.grid_rowconfigure(i//2, weight=1)
        tools_frame.grid_columnconfigure(i%2, weight=1)

# ==================== STANDARD CALCULATOR ====================

def render_standard_calculator():
    """Render standard calculator"""
    global expression, result
    frame = pages['standard']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Calculator display
    display_frame = tk.Frame(frame, bg=colors['bg_medium'], height=100)
    display_frame.pack(fill=tk.X, pady=(0, 20))
    display_frame.pack_propagate(False)
    
    expression = tk.StringVar()
    result = tk.StringVar()
    expression.set("0")
    result.set("")
    
    expr_label = tk.Label(display_frame, textvariable=expression,
                         font=('Segoe UI', 14),
                         bg=colors['bg_medium'], fg=colors['text_secondary'],
                         anchor=tk.E)
    expr_label.pack(fill=tk.X, padx=20, pady=(20, 5))
    
    result_label = tk.Label(display_frame, textvariable=result,
                           font=('Segoe UI', 24, 'bold'),
                           bg=colors['bg_medium'], fg='white',
                           anchor=tk.E)
    result_label.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    # Calculator buttons
    buttons_frame = tk.Frame(frame, bg=colors['bg_dark'])
    buttons_frame.pack(fill=tk.BOTH, expand=True)
    
    buttons = [
        ['C', '±', '%', '÷'],
        ['7', '8', '9', '×'],
        ['4', '5', '6', '−'],
        ['1', '2', '3', '+'],
        ['0', '.', '=', '']
    ]
    
    def on_click(value):
        current = expression.get()
        
        if value == 'C':
            expression.set("0")
            result.set("")
        elif value == '±':
            if current.startswith('-'):
                expression.set(current[1:])
            else:
                expression.set('-' + current)
        elif value == '%':
            try:
                num = float(current)
                result.set(f"= {num/100:.4f}")
            except:
                pass
        elif value == '=':
            try:
                expr = current.replace('×', '*').replace('÷', '/').replace('−', '-')
                calc_result = eval(expr)
                result.set(f"= {calc_result:,.2f}")
                save_history_entry({
                    'type': 'standard',
                    'expression': current,
                    'result': calc_result,
                    'timestamp': datetime.now().isoformat()
                })
            except:
                result.set("Error")
        else:
            if current == "0" and value not in ['.', '+', '−', '×', '÷']:
                expression.set(value)
            else:
                if value in ['+', '−', '×', '÷']:
                    if current[-1] in ['+', '−', '×', '÷']:
                        expression.set(current[:-1] + value)
                        return
                expression.set(current + value)
    
    button_colors = {
        'C': colors['danger'],
        '±': colors['secondary'],
        '%': colors['secondary'],
        '÷': colors['primary'],
        '×': colors['primary'],
        '−': colors['primary'],
        '+': colors['primary'],
        '=': colors['gold']
    }
    
    for i, row in enumerate(buttons):
        btn_row = tk.Frame(buttons_frame, bg=colors['bg_dark'])
        btn_row.pack(fill=tk.BOTH, expand=True)
        for j, text in enumerate(row):
            if text == '':
                continue
            color = button_colors.get(text, colors['bg_medium'])
            text_color = '#0a0e27' if text == '=' else 'white'
            font_weight = 'bold' if text in ['=', '+', '−', '×', '÷', 'C'] else 'normal'
            
            btn = tk.Button(btn_row, text=text,
                          font=('Segoe UI', 14, font_weight),
                          bg=color, fg=text_color,
                          relief=tk.FLAT, cursor='hand2',
                          bd=1, highlightthickness=0,
                          command=lambda v=text: on_click(v))
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)

# ==================== FINANCIAL CALCULATOR ====================

def render_financial_calculator():
    """Render financial calculator"""
    global npv_fields, fv_fields, npv_result, fv_result
    frame = pages['financial']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Create two columns
    left_frame = tk.Frame(frame, bg=colors['bg_dark'])
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
    
    right_frame = tk.Frame(frame, bg=colors['bg_dark'])
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    # Left: Net Present Value Calculator
    npv_frame = tk.LabelFrame(left_frame, text="Net Present Value (NPV)",
                             font=('Segoe UI', 12, 'bold'),
                             bg=colors['bg_medium'], fg='white',
                             relief=tk.FLAT, bd=0)
    npv_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    npv_fields = {}
    labels = [
        ("Initial Investment:", "npv_initial"),
        ("Annual Cash Flow:", "npv_cashflow"),
        ("Discount Rate (%):", "npv_rate"),
        ("Number of Years:", "npv_years")
    ]
    
    for i, (label, key) in enumerate(labels):
        row = tk.Frame(npv_frame, bg=colors['bg_medium'])
        row.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(row, text=label, font=('Segoe UI', 10),
                bg=colors['bg_medium'], fg=colors['text_secondary'],
                width=18, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(row, font=('Segoe UI', 11),
                       bg=colors['bg_light'], fg='white',
                       relief=tk.FLAT, insertbackground='white',
                       width=15)
        entry.pack(side=tk.RIGHT)
        if key == 'npv_initial':
            entry.insert(0, "100000")
        elif key == 'npv_cashflow':
            entry.insert(0, "25000")
        elif key == 'npv_rate':
            entry.insert(0, "10")
        elif key == 'npv_years':
            entry.insert(0, "5")
        npv_fields[key] = entry
    
    npv_result = tk.Label(npv_frame, text="NPV: $0.00",
                         font=('Segoe UI', 14, 'bold'),
                         bg=colors['bg_medium'], fg=colors['gold'])
    npv_result.pack(pady=10)
    
    btn = tk.Button(npv_frame, text="Calculate NPV",
                   font=('Segoe UI', 10, 'bold'),
                   bg=colors['primary'], fg='white',
                   relief=tk.FLAT, cursor='hand2',
                   command=calculate_npv)
    btn.pack(pady=10)
    
    # Right: Future Value Calculator
    fv_frame = tk.LabelFrame(right_frame, text="Future Value (FV)",
                            font=('Segoe UI', 12, 'bold'),
                            bg=colors['bg_medium'], fg='white',
                            relief=tk.FLAT, bd=0)
    fv_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    fv_fields = {}
    fv_labels = [
        ("Present Value:", "fv_pv"),
        ("Annual Rate (%):", "fv_rate"),
        ("Number of Years:", "fv_years"),
        ("Compounds/Year:", "fv_compounds")
    ]
    
    for i, (label, key) in enumerate(fv_labels):
        row = tk.Frame(fv_frame, bg=colors['bg_medium'])
        row.pack(fill=tk.X, padx=15, pady=8)
        tk.Label(row, text=label, font=('Segoe UI', 10),
                bg=colors['bg_medium'], fg=colors['text_secondary'],
                width=18, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(row, font=('Segoe UI', 11),
                       bg=colors['bg_light'], fg='white',
                       relief=tk.FLAT, insertbackground='white',
                       width=15)
        entry.pack(side=tk.RIGHT)
        if key == 'fv_pv':
            entry.insert(0, "10000")
        elif key == 'fv_rate':
            entry.insert(0, "8")
        elif key == 'fv_years':
            entry.insert(0, "10")
        elif key == 'fv_compounds':
            entry.insert(0, "12")
        fv_fields[key] = entry
    
    fv_result = tk.Label(fv_frame, text="FV: $0.00",
                        font=('Segoe UI', 14, 'bold'),
                        bg=colors['bg_medium'], fg=colors['gold'])
    fv_result.pack(pady=10)
    
    btn = tk.Button(fv_frame, text="Calculate Future Value",
                   font=('Segoe UI', 10, 'bold'),
                   bg=colors['secondary'], fg='white',
                   relief=tk.FLAT, cursor='hand2',
                   command=calculate_fv)
    btn.pack(pady=10)

def calculate_npv():
    """Calculate Net Present Value"""
    global npv_result
    try:
        initial = float(npv_fields['npv_initial'].get())
        cashflow = float(npv_fields['npv_cashflow'].get())
        rate = float(npv_fields['npv_rate'].get()) / 100
        years = int(npv_fields['npv_years'].get())
        
        npv_val = -initial
        for t in range(1, years + 1):
            npv_val += cashflow / ((1 + rate) ** t)
        
        npv_result.config(text=f"NPV: ${npv_val:,.2f}")
        
        save_history_entry({
            'type': 'npv',
            'initial': initial,
            'cashflow': cashflow,
            'rate': rate * 100,
            'years': years,
            'result': npv_val,
            'timestamp': datetime.now().isoformat()
        })
    except:
        npv_result.config(text="Error: Invalid input")

def calculate_fv():
    """Calculate Future Value"""
    global fv_result
    try:
        pv = float(fv_fields['fv_pv'].get())
        rate = float(fv_fields['fv_rate'].get()) / 100
        years = int(fv_fields['fv_years'].get())
        compounds = int(fv_fields['fv_compounds'].get())
        
        fv_val = pv * ((1 + rate/compounds) ** (compounds * years))
        
        fv_result.config(text=f"FV: ${fv_val:,.2f}")
        
        save_history_entry({
            'type': 'fv',
            'pv': pv,
            'rate': rate * 100,
            'years': years,
            'compounds': compounds,
            'result': fv_val,
            'timestamp': datetime.now().isoformat()
        })
    except:
        fv_result.config(text="Error: Invalid input")

# ==================== PROFIT & LOSS ====================

def render_pnl_calculator():
    """Render Profit & Loss calculator"""
    global pnl_fields, pnl_results
    frame = pages['pnl']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Input section
    input_frame = tk.Frame(frame, bg=colors['bg_dark'])
    input_frame.pack(fill=tk.X, pady=10)
    
    labels = [
        ("Revenue:", "revenue"),
        ("Cost of Goods Sold:", "cogs"),
        ("Operating Expenses:", "opex"),
        ("Tax Rate (%):", "tax_rate")
    ]
    
    pnl_fields = {}
    
    for i, (label, key) in enumerate(labels):
        row = tk.Frame(input_frame, bg=colors['bg_dark'])
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text=label, font=('Segoe UI', 11),
                bg=colors['bg_dark'], fg=colors['text_secondary'],
                width=25, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(row, font=('Segoe UI', 11),
                       bg=colors['bg_medium'], fg='white',
                       relief=tk.FLAT, insertbackground='white',
                       width=20)
        entry.pack(side=tk.RIGHT)
        if key == 'revenue':
            entry.insert(0, "500000")
        elif key == 'cogs':
            entry.insert(0, "200000")
        elif key == 'opex':
            entry.insert(0, "150000")
        elif key == 'tax_rate':
            entry.insert(0, "25")
        pnl_fields[key] = entry
    
    btn = tk.Button(input_frame, text="Calculate P&L",
                   font=('Segoe UI', 11, 'bold'),
                   bg=colors['primary'], fg='white',
                   relief=tk.FLAT, cursor='hand2',
                   command=calculate_pnl)
    btn.pack(pady=15)
    
    # Results section
    results_frame = tk.Frame(frame, bg=colors['bg_medium'])
    results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    pnl_results = {}
    result_labels = [
        ("Gross Profit", "gross", colors['secondary']),
        ("Operating Profit", "operating", colors['primary']),
        ("Net Profit", "net", colors['gold']),
        ("Net Profit Margin", "margin", colors['success'])
    ]
    
    for i, (label, key, color) in enumerate(result_labels):
        card = tk.Frame(results_frame, bg=colors['bg_light'], relief=tk.FLAT, bd=0)
        card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
        results_frame.grid_rowconfigure(i//2, weight=1)
        results_frame.grid_columnconfigure(i%2, weight=1)
        
        tk.Label(card, text=label, font=('Segoe UI', 11),
                bg=colors['bg_light'], fg=colors['text_secondary']).pack(pady=(15, 5))
        result_label = tk.Label(card, text="$0.00", 
                               font=('Segoe UI', 20, 'bold'),
                               bg=colors['bg_light'], fg=color)
        result_label.pack(pady=(0, 15))
        pnl_results[key] = result_label

def calculate_pnl():
    """Calculate Profit & Loss"""
    global pnl_results
    try:
        revenue = float(pnl_fields['revenue'].get())
        cogs = float(pnl_fields['cogs'].get())
        opex = float(pnl_fields['opex'].get())
        tax_rate = float(pnl_fields['tax_rate'].get()) / 100
        
        gross = revenue - cogs
        operating = gross - opex
        net = operating * (1 - tax_rate)
        margin = (net / revenue) * 100 if revenue > 0 else 0
        
        pnl_results['gross'].config(text=f"${gross:,.2f}")
        pnl_results['operating'].config(text=f"${operating:,.2f}")
        pnl_results['net'].config(text=f"${net:,.2f}")
        pnl_results['margin'].config(text=f"{margin:.1f}%")
        
        save_history_entry({
            'type': 'pnl',
            'revenue': revenue,
            'cogs': cogs,
            'opex': opex,
            'tax_rate': tax_rate * 100,
            'gross': gross,
            'operating': operating,
            'net': net,
            'margin': margin,
            'timestamp': datetime.now().isoformat()
        })
    except:
        messagebox.showerror("Error", "Invalid input values")

# ==================== INVESTMENT CALCULATOR ====================

def render_investment_calculator():
    """Render investment calculator"""
    global inv_fields, inv_results
    frame = pages['investment']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Input section
    input_frame = tk.Frame(frame, bg=colors['bg_dark'])
    input_frame.pack(fill=tk.X, pady=10)
    
    labels = [
        ("Initial Investment:", "inv_initial"),
        ("Monthly Contribution:", "inv_monthly"),
        ("Annual Return Rate (%):", "inv_rate"),
        ("Investment Period (Years):", "inv_years")
    ]
    
    inv_fields = {}
    
    for i, (label, key) in enumerate(labels):
        row = tk.Frame(input_frame, bg=colors['bg_dark'])
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text=label, font=('Segoe UI', 11),
                bg=colors['bg_dark'], fg=colors['text_secondary'],
                width=25, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(row, font=('Segoe UI', 11),
                       bg=colors['bg_medium'], fg='white',
                       relief=tk.FLAT, insertbackground='white',
                       width=20)
        entry.pack(side=tk.RIGHT)
        if key == 'inv_initial':
            entry.insert(0, "10000")
        elif key == 'inv_monthly':
            entry.insert(0, "500")
        elif key == 'inv_rate':
            entry.insert(0, "10")
        elif key == 'inv_years':
            entry.insert(0, "20")
        inv_fields[key] = entry
    
    btn = tk.Button(input_frame, text="Calculate Investment Growth",
                   font=('Segoe UI', 11, 'bold'),
                   bg=colors['gold'], fg='#0a0e27',
                   relief=tk.FLAT, cursor='hand2',
                   command=calculate_investment)
    btn.pack(pady=15)
    
    # Results
    results_frame = tk.Frame(frame, bg=colors['bg_medium'])
    results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    inv_results = {}
    result_labels = [
        ("Final Value", "final", colors['gold']),
        ("Total Contributions", "contributions", colors['secondary']),
        ("Total Interest Earned", "interest", colors['success'])
    ]
    
    for i, (label, key, color) in enumerate(result_labels):
        card = tk.Frame(results_frame, bg=colors['bg_light'])
        card.grid(row=i, column=0, padx=15, pady=15, sticky='nsew')
        results_frame.grid_rowconfigure(i, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        tk.Label(card, text=label, font=('Segoe UI', 11),
                bg=colors['bg_light'], fg=colors['text_secondary']).pack(pady=(15, 5))
        result_label = tk.Label(card, text="$0.00",
                               font=('Segoe UI', 20, 'bold'),
                               bg=colors['bg_light'], fg=color)
        result_label.pack(pady=(0, 15))
        inv_results[key] = result_label

def calculate_investment():
    """Calculate investment growth"""
    global inv_results
    try:
        initial = float(inv_fields['inv_initial'].get())
        monthly = float(inv_fields['inv_monthly'].get())
        rate = float(inv_fields['inv_rate'].get()) / 100
        years = int(inv_fields['inv_years'].get())
        
        monthly_rate = rate / 12
        months = years * 12
        
        fv = initial * ((1 + monthly_rate) ** months)
        if monthly > 0:
            fv += monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        
        total_contributions = initial + (monthly * months)
        interest_earned = fv - total_contributions
        
        inv_results['final'].config(text=f"${fv:,.2f}")
        inv_results['contributions'].config(text=f"${total_contributions:,.2f}")
        inv_results['interest'].config(text=f"${interest_earned:,.2f}")
        
        save_history_entry({
            'type': 'investment',
            'initial': initial,
            'monthly': monthly,
            'rate': rate * 100,
            'years': years,
            'final': fv,
            'contributions': total_contributions,
            'interest': interest_earned,
            'timestamp': datetime.now().isoformat()
        })
    except:
        messagebox.showerror("Error", "Invalid input values")

# ==================== LOAN CALCULATOR ====================

def render_loan_calculator():
    """Render loan calculator"""
    global loan_fields, loan_results
    frame = pages['loan']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Input section
    input_frame = tk.Frame(frame, bg=colors['bg_dark'])
    input_frame.pack(fill=tk.X, pady=10)
    
    labels = [
        ("Loan Amount:", "loan_amount"),
        ("Annual Interest Rate (%):", "loan_rate"),
        ("Loan Term (Years):", "loan_years"),
        ("Down Payment:", "loan_down")
    ]
    
    loan_fields = {}
    
    for i, (label, key) in enumerate(labels):
        row = tk.Frame(input_frame, bg=colors['bg_dark'])
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text=label, font=('Segoe UI', 11),
                bg=colors['bg_dark'], fg=colors['text_secondary'],
                width=25, anchor=tk.W).pack(side=tk.LEFT)
        entry = tk.Entry(row, font=('Segoe UI', 11),
                       bg=colors['bg_medium'], fg='white',
                       relief=tk.FLAT, insertbackground='white',
                       width=20)
        entry.pack(side=tk.RIGHT)
        if key == 'loan_amount':
            entry.insert(0, "200000")
        elif key == 'loan_rate':
            entry.insert(0, "6")
        elif key == 'loan_years':
            entry.insert(0, "30")
        elif key == 'loan_down':
            entry.insert(0, "40000")
        loan_fields[key] = entry
    
    btn = tk.Button(input_frame, text="Calculate Loan Payment",
                   font=('Segoe UI', 11, 'bold'),
                   bg=colors['secondary'], fg='white',
                   relief=tk.FLAT, cursor='hand2',
                   command=calculate_loan)
    btn.pack(pady=15)
    
    # Results
    results_frame = tk.Frame(frame, bg=colors['bg_medium'])
    results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    loan_results = {}
    result_labels = [
        ("Monthly Payment", "monthly", colors['gold']),
        ("Total Payment", "total", colors['primary']),
        ("Total Interest", "interest", colors['danger']),
        ("Loan Amount", "amount", colors['success'])
    ]
    
    for i, (label, key, color) in enumerate(result_labels):
        card = tk.Frame(results_frame, bg=colors['bg_light'])
        card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
        results_frame.grid_rowconfigure(i//2, weight=1)
        results_frame.grid_columnconfigure(i%2, weight=1)
        
        tk.Label(card, text=label, font=('Segoe UI', 11),
                bg=colors['bg_light'], fg=colors['text_secondary']).pack(pady=(15, 5))
        result_label = tk.Label(card, text="$0.00",
                               font=('Segoe UI', 20, 'bold'),
                               bg=colors['bg_light'], fg=color)
        result_label.pack(pady=(0, 15))
        loan_results[key] = result_label

def calculate_loan():
    """Calculate loan payments"""
    global loan_results
    try:
        loan_amount = float(loan_fields['loan_amount'].get())
        rate = float(loan_fields['loan_rate'].get()) / 100
        years = int(loan_fields['loan_years'].get())
        down_payment = float(loan_fields['loan_down'].get())
        
        principal = loan_amount - down_payment
        monthly_rate = rate / 12
        months = years * 12
        
        if monthly_rate == 0:
            monthly_payment = principal / months
        else:
            monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        
        total_payment = monthly_payment * months
        total_interest = total_payment - principal
        
        loan_results['monthly'].config(text=f"${monthly_payment:,.2f}")
        loan_results['total'].config(text=f"${total_payment:,.2f}")
        loan_results['interest'].config(text=f"${total_interest:,.2f}")
        loan_results['amount'].config(text=f"${principal:,.2f}")
        
        save_history_entry({
            'type': 'loan',
            'amount': loan_amount,
            'rate': rate * 100,
            'years': years,
            'down_payment': down_payment,
            'principal': principal,
            'monthly_payment': monthly_payment,
            'total_payment': total_payment,
            'total_interest': total_interest,
            'timestamp': datetime.now().isoformat()
        })
    except:
        messagebox.showerror("Error", "Invalid input values")

# ==================== CURRENCY CONVERTER ====================

def render_currency_converter():
    """Render currency converter"""
    global currency_amount, from_currency, to_currency, currency_result, rate_display
    frame = pages['currency']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Main converter
    converter_frame = tk.Frame(frame, bg=colors['bg_medium'])
    converter_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    tk.Label(converter_frame, text="Currency Converter",
            font=('Segoe UI', 18, 'bold'),
            bg=colors['bg_medium'], fg='white').pack(pady=20)
    
    # Amount
    row = tk.Frame(converter_frame, bg=colors['bg_medium'])
    row.pack(pady=10)
    tk.Label(row, text="Amount:", font=('Segoe UI', 12),
            bg=colors['bg_medium'], fg=colors['text_secondary']).pack(side=tk.LEFT, padx=10)
    currency_amount = tk.Entry(row, font=('Segoe UI', 14),
                             bg=colors['bg_light'], fg='white',
                             relief=tk.FLAT, insertbackground='white',
                             width=15)
    currency_amount.pack(side=tk.LEFT, padx=10)
    currency_amount.insert(0, "100")
    
    # From currency
    row = tk.Frame(converter_frame, bg=colors['bg_medium'])
    row.pack(pady=10)
    tk.Label(row, text="From:", font=('Segoe UI', 12),
            bg=colors['bg_medium'], fg=colors['text_secondary']).pack(side=tk.LEFT, padx=10)
    from_currency = ttk.Combobox(row, values=list(rates.keys()),
                               font=('Segoe UI', 12), width=12,
                               state='readonly')
    from_currency.pack(side=tk.LEFT, padx=10)
    from_currency.set('USD')
    
    # To currency
    row = tk.Frame(converter_frame, bg=colors['bg_medium'])
    row.pack(pady=10)
    tk.Label(row, text="To:", font=('Segoe UI', 12),
            bg=colors['bg_medium'], fg=colors['text_secondary']).pack(side=tk.LEFT, padx=10)
    to_currency = ttk.Combobox(row, values=list(rates.keys()),
                             font=('Segoe UI', 12), width=12,
                             state='readonly')
    to_currency.pack(side=tk.LEFT, padx=10)
    to_currency.set('EUR')
    
    # Convert button
    btn = tk.Button(converter_frame, text="Convert",
                   font=('Segoe UI', 12, 'bold'),
                   bg=colors['gold'], fg='#0a0e27',
                   relief=tk.FLAT, cursor='hand2',
                   command=convert_currency)
    btn.pack(pady=20)
    
    # Result
    currency_result = tk.Label(converter_frame, text="Result: $0.00",
                              font=('Segoe UI', 24, 'bold'),
                              bg=colors['bg_medium'], fg=colors['gold'])
    currency_result.pack(pady=20)
    
    # Exchange rate display
    rate_display = tk.Label(converter_frame, text="",
                          font=('Segoe UI', 11),
                          bg=colors['bg_medium'], fg=colors['text_secondary'])
    rate_display.pack(pady=10)

def convert_currency():
    """Convert currency"""
    global currency_result, rate_display
    try:
        amount = float(currency_amount.get())
        from_curr = from_currency.get()
        to_curr = to_currency.get()
        
        if from_curr not in rates or to_curr not in rates:
            messagebox.showerror("Error", "Invalid currency")
            return
        
        usd_amount = amount / rates[from_curr]
        converted = usd_amount * rates[to_curr]
        
        currency_result.config(text=f"{from_curr} {amount:,.2f} = {to_curr} {converted:,.2f}")
        rate_display.config(text=f"1 {from_curr} = {rates[to_curr]/rates[from_curr]:.4f} {to_curr}")
        
        save_history_entry({
            'type': 'currency',
            'from': from_curr,
            'to': to_curr,
            'amount': amount,
            'result': converted,
            'rate': rates[to_curr]/rates[from_curr],
            'timestamp': datetime.now().isoformat()
        })
    except:
        messagebox.showerror("Error", "Invalid input")

# ==================== HISTORY ====================

def render_history():
    """Render calculation history"""
    frame = pages['history']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Header
    header = tk.Frame(frame, bg=colors['bg_dark'])
    header.pack(fill=tk.X, pady=10)
    
    tk.Label(header, text="Calculation History",
            font=('Segoe UI', 16, 'bold'),
            bg=colors['bg_dark'], fg='white').pack(side=tk.LEFT)
    
    clear_btn = tk.Button(header, text="Clear History",
                        font=('Segoe UI', 10),
                        bg=colors['danger'], fg='white',
                        relief=tk.FLAT, cursor='hand2',
                        command=clear_history)
    clear_btn.pack(side=tk.RIGHT)
    
    # History list
    list_frame = tk.Frame(frame, bg=colors['bg_medium'])
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Create Treeview
    columns = ('Type', 'Input', 'Result', 'Timestamp')
    tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Load history
    history_data = load_history()
    for entry in reversed(history_data):
        calc_type = entry.get('type', 'unknown').title()
        if calc_type == 'Standard':
            input_text = entry.get('expression', '')
            result_text = f"{entry.get('result', 0):.2f}"
        elif calc_type == 'Npv':
            input_text = f"${entry.get('initial', 0):,} @ {entry.get('rate', 0):.1f}%"
            result_text = f"${entry.get('result', 0):,.2f}"
        elif calc_type == 'Fv':
            input_text = f"${entry.get('pv', 0):,} @ {entry.get('rate', 0):.1f}%"
            result_text = f"${entry.get('result', 0):,.2f}"
        elif calc_type == 'Pnl':
            input_text = f"Revenue: ${entry.get('revenue', 0):,}"
            result_text = f"${entry.get('net', 0):,.2f}"
        elif calc_type == 'Investment':
            input_text = f"${entry.get('initial', 0):,} + ${entry.get('monthly', 0):,}/mo"
            result_text = f"${entry.get('final', 0):,.2f}"
        elif calc_type == 'Loan':
            input_text = f"${entry.get('amount', 0):,} @ {entry.get('rate', 0):.1f}%"
            result_text = f"${entry.get('monthly_payment', 0):,.2f}/mo"
        elif calc_type == 'Currency':
            input_text = f"{entry.get('amount', 0):.2f} {entry.get('from', '')}"
            result_text = f"{entry.get('result', 0):.2f} {entry.get('to', '')}"
        else:
            input_text = str(entry.get('input', ''))
            result_text = str(entry.get('result', ''))
        
        timestamp = entry.get('timestamp', '')[:19]
        tree.insert('', tk.END, values=(calc_type, input_text, result_text, timestamp))

# ==================== USER MANAGEMENT ====================

def render_users():
    """Render user management page"""
    frame = pages['users']
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Only admin can access
    if current_user.get('role') != 'admin':
        tk.Label(frame, text="⚠️ Access Denied",
                font=('Segoe UI', 24, 'bold'),
                bg=colors['bg_dark'], fg=colors['danger']).pack(pady=50)
        tk.Label(frame, text="Only administrators can access this page.",
                font=('Segoe UI', 14),
                bg=colors['bg_dark'], fg=colors['text_secondary']).pack()
        return
    
    # Header
    header = tk.Frame(frame, bg=colors['bg_dark'])
    header.pack(fill=tk.X, pady=10)
    
    tk.Label(header, text="User Management",
            font=('Segoe UI', 16, 'bold'),
            bg=colors['bg_dark'], fg='white').pack(side=tk.LEFT)
    
    # User list
    list_frame = tk.Frame(frame, bg=colors['bg_medium'])
    list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    columns = ('Name', 'Email', 'Role', 'Created')
    tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)
    
    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    users_data = load_users()
    for user in users_data['users']:
        created = user.get('created', '')[:10]
        tree.insert('', tk.END, values=(user['name'], user['email'], user['role'], created))
    
    # Delete user button
    def delete_user():
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        values = tree.item(selection[0])['values']
        email = values[1]
        
        if email == current_user['email']:
            messagebox.showerror("Error", "Cannot delete your own account")
            return
        
        if messagebox.askyesno("Delete User", f"Delete user {values[0]}?"):
            users_data['users'] = [u for u in users_data['users'] if u['email'] != email]
            save_users(users_data)
            render_users()
            messagebox.showinfo("Success", "User deleted successfully")
    
    btn_frame = tk.Frame(frame, bg=colors['bg_dark'])
    btn_frame.pack(fill=tk.X, pady=10)
    
    tk.Button(btn_frame, text="Delete Selected User",
             font=('Segoe UI', 10, 'bold'),
             bg=colors['danger'], fg='white',
             relief=tk.FLAT, cursor='hand2',
             command=delete_user).pack(side=tk.LEFT, padx=5)

# ==================== MAIN ====================

def main():
    global root
    root = tk.Tk()
    root.title("Business Calculator Pro - Enterprise Suite")
    root.geometry("1150x820")
    root.minsize(1050, 760)
    root.configure(bg='#0a0e27')
    
    setup_colors()
    
    # Ensure users file exists
    if not os.path.exists(users_file):
        save_users(default_users)
    
    show_login_splash()
    root.mainloop()

if __name__ == "__main__":
    main()