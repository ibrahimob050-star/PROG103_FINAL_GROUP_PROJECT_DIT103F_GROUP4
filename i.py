"""
EduManage Pro - Student Management System
Professional Tkinter Application with Modern UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import re

# ============================================================
# CONSTANTS & DATA
# ============================================================

CLASSES = ['Class 10A', 'Class 10B', 'Class 11A', 'Class 11B', 'Class 12A', 'Class 12B']
SUBJECTS = ['Mathematics', 'English', 'Science', 'History', 'Art', 'Physics', 'Chemistry']

STATUSES = [
    {'value': 'active', 'label': 'Active', 'color': '#10b981'},
    {'value': 'inactive', 'label': 'Inactive', 'color': '#ef4444'},
    {'value': 'graduated', 'label': 'Graduated', 'color': '#3b82f6'},
    {'value': 'transferred', 'label': 'Transferred', 'color': '#f59e0b'},
]

GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

COLORS = {
    'bg': '#f1f5f9',
    'card': '#ffffff',
    'primary': '#4f46e5',
    'primary_light': '#818cf8',
    'primary_dark': '#4338ca',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'text': '#0f172a',
    'text_secondary': '#64748b',
    'border': '#e2e8f0',
    'hover': '#f8fafc',
}

# ============================================================
# DATA PERSISTENCE
# ============================================================

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')

def load_data(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_data(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

# ============================================================
# SAMPLE DATA GENERATOR
# ============================================================

def generate_sample_students():
    names = [
        ('John', 'Smith'), ('Emma', 'Johnson'), ('Michael', 'Brown'),
        ('Sophia', 'Davis'), ('William', 'Wilson'), ('Olivia', 'Miller'),
        ('James', 'Taylor'), ('Ava', 'Anderson'), ('Benjamin', 'Thomas'),
        ('Mia', 'Jackson'), ('Lucas', 'White'), ('Charlotte', 'Harris')
    ]
    
    students = []
    for i, (first, last) in enumerate(names):
        grade = GRADES[i % len(GRADES)]
        status = ['active', 'active', 'active', 'active', 'active', 'inactive', 'graduated', 'transferred'][i % 8]
        class_name = CLASSES[i % len(CLASSES)]
        attendance = 65 + (i * 3) % 35
        
        students.append({
            'id': f"STU{str(i+1).zfill(3)}",
            'firstName': first,
            'lastName': last,
            'email': f"{first.lower()}.{last.lower()}@example.com",
            'phone': f"+1 234-567-{str(8900 + i)[:4]}",
            'dob': f"200{3 + (i % 5)}-{str(1 + (i % 12)).zfill(2)}-{str(1 + (i % 28)).zfill(2)}",
            'gender': 'male' if i % 2 == 0 else 'female',
            'class': class_name,
            'enrollmentDate': f"202{2 + (i % 2)}-09-01",
            'grade': grade,
            'status': status,
            'attendance': attendance,
        })
    return students

def generate_sample_users():
    return [
        {'id': 1, 'name': 'Admin User', 'username': 'admin', 'email': 'admin@edumanage.com', 
         'password': 'admin123', 'role': 'Administrator', 'status': 'active'},
        {'id': 2, 'name': 'John Teacher', 'username': 'teacher', 'email': 'teacher@edumanage.com', 
         'password': 'teacher123', 'role': 'Teacher', 'status': 'active'},
    ]

# ============================================================
# TOAST NOTIFICATION
# ============================================================

class Toast:
    def __init__(self, root):
        self.root = root
        self.widget = None
        self.timer = None
    
    def show(self, message, type='info'):
        if self.widget:
            self.widget.destroy()
        
        colors = {
            'success': '#10b981',
            'error': '#ef4444',
            'info': '#3b82f6',
            'warning': '#f59e0b'
        }
        
        self.widget = tk.Toplevel(self.root)
        self.widget.overrideredirect(True)
        self.widget.configure(bg=colors.get(type, '#3b82f6'))
        
        # Position at bottom right
        x = self.root.winfo_x() + self.root.winfo_width() - 420
        y = self.root.winfo_y() + self.root.winfo_height() - 80
        self.widget.geometry(f"400x50+{x}+{y}")
        
        # Keep on top
        self.widget.attributes('-topmost', True)
        
        frame = tk.Frame(self.widget, bg=colors.get(type, '#3b82f6'))
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        
        icon = tk.Label(frame, text='✓' if type == 'success' else 'ℹ', 
                       font=('Segoe UI', 14), bg=colors.get(type, '#3b82f6'), fg='white')
        icon.pack(side=tk.LEFT, padx=(0, 10))
        
        msg = tk.Label(frame, text=message, font=('Segoe UI', 11), 
                      bg=colors.get(type, '#3b82f6'), fg='white')
        msg.pack(side=tk.LEFT)
        
        # Auto close after 3 seconds
        if self.timer:
            self.root.after_cancel(self.timer)
        self.timer = self.root.after(3000, self.hide)
    
    def hide(self):
        if self.widget:
            self.widget.destroy()
            self.widget = None

# ============================================================
# MODERN ROUNDED BUTTON
# ============================================================

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color='#4f46e5', fg_color='white', 
                 hover_color='#4338ca', font=('Segoe UI', 11, 'bold'), width=200, height=44):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.text = text
        self.font = font
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
        self.draw_button()
    
    def draw_button(self):
        self.delete('all')
        # Rounded rectangle
        radius = 10
        self.create_rounded_rect(0, 0, self.winfo_width(), self.winfo_height(), radius, fill=self.current_color, outline='')
        # Text
        self.create_text(self.winfo_width()//2, self.winfo_height()//2, 
                        text=self.text, font=self.font, fill=self.fg_color)
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, e):
        self.current_color = self.hover_color
        self.draw_button()
    
    def on_leave(self, e):
        self.current_color = self.bg_color
        self.draw_button()
    
    def on_click(self, e):
        if self.command:
            self.command()

# ============================================================
# MAIN APPLICATION CLASS
# ============================================================

class EduManageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EduManage Pro - Student Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg='white')
        
        # Load data
        self.students = load_data(STUDENTS_FILE, generate_sample_students())
        self.users = load_data(USERS_FILE, generate_sample_users())
        self.current_user = None
        self.current_page = 'dashboard'
        
        # Toast
        self.toast = Toast(root)
        
        # State
        self.current_page_num = 1
        self.per_page = 6
        
        # Show login
        self.show_login()
    
    # ============================================================
    # TOAST HELPER
    # ============================================================
    def show_toast(self, message, type='info'):
        self.toast.show(message, type)
    
    # ============================================================
    # LOGIN PAGE
    # ============================================================
    def show_login(self):
        self.clear_window()
        self.root.configure(bg='white')
        
        # Main container - centered
        container = tk.Frame(self.root, bg='white')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo Section
        logo_frame = tk.Frame(container, bg='white')
        logo_frame.pack(pady=(0, 30))
        
        # Icon with gradient effect (using emoji)
        icon_label = tk.Label(logo_frame, text='🎓', font=('Segoe UI', 48), bg='white')
        icon_label.pack()
        
        title_label = tk.Label(logo_frame, text='EduManage Pro', 
                              font=('Segoe UI', 28, 'bold'), bg='white', fg='#1e293b')
        title_label.pack()
        
        subtitle_label = tk.Label(logo_frame, text='Sign in to your account', 
                                 font=('Segoe UI', 14), bg='white', fg='#64748b')
        subtitle_label.pack(pady=(4, 0))
        
        # Form Card
        card = tk.Frame(container, bg='white', highlightbackground='#e2e8f0', 
                       highlightthickness=1, relief=tk.FLAT)
        card.pack(pady=10)
        
        inner_card = tk.Frame(card, bg='white')
        inner_card.pack(padx=40, pady=30)
        
        # Username Field
        username_label = tk.Label(inner_card, text='Username *', font=('Segoe UI', 11, 'bold'),
                                 bg='white', fg='#334155')
        username_label.pack(anchor='w', pady=(0, 4))
        
        self.login_username = tk.Entry(inner_card, font=('Segoe UI', 12), 
                                       bg='#f8fafc', relief=tk.FLAT,
                                       highlightthickness=2, highlightcolor='#4f46e5',
                                       highlightbackground='#e2e8f0', width=30)
        self.login_username.pack(pady=(0, 16), ipady=6)
        self.login_username.insert(0, 'admin')
        
        # Password Field
        password_label = tk.Label(inner_card, text='Password *', font=('Segoe UI', 11, 'bold'),
                                 bg='white', fg='#334155')
        password_label.pack(anchor='w', pady=(0, 4))
        
        self.login_password = tk.Entry(inner_card, font=('Segoe UI', 12), 
                                       bg='#f8fafc', relief=tk.FLAT,
                                       highlightthickness=2, highlightcolor='#4f46e5',
                                       highlightbackground='#e2e8f0', width=30, show='•')
        self.login_password.pack(pady=(0, 16), ipady=6)
        self.login_password.insert(0, 'admin123')
        
        # Remember me & Create Account
        options_frame = tk.Frame(inner_card, bg='white')
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Remember me (left)
        remember_frame = tk.Frame(options_frame, bg='white')
        remember_frame.pack(side=tk.LEFT)
        
        self.remember_var = tk.IntVar(value=1)
        remember_check = tk.Checkbutton(remember_frame, text='Remember me', 
                                        variable=self.remember_var,
                                        bg='white', font=('Segoe UI', 10),
                                        fg='#64748b', selectcolor='white',
                                        activebackground='white')
        remember_check.pack(side=tk.LEFT)
        
        # Create Account (right)
        create_account_label = tk.Label(options_frame, text='Create Account', 
                                        font=('Segoe UI', 10, 'bold'),
                                        bg='white', fg='#4f46e5', cursor='hand2')
        create_account_label.pack(side=tk.RIGHT)
        create_account_label.bind('<Button-1>', lambda e: self.show_register())
        
        # Sign In Button
        login_btn = ModernButton(inner_card, 'Sign In', self.handle_login,
                                 bg_color='#4f46e5', hover_color='#4338ca',
                                 font=('Segoe UI', 12, 'bold'), width=280)
        login_btn.pack(pady=(0, 12))
        
        # Demo hint
        demo_label = tk.Label(inner_card, text='Demo: admin / admin123', 
                             font=('Segoe UI', 10), bg='white', fg='#94a3b8')
        demo_label.pack()
        
        # Bind Enter key
        self.login_username.bind('<Return>', lambda e: self.login_password.focus())
        self.login_password.bind('<Return>', lambda e: self.handle_login())
    
    # ============================================================
    # REGISTER PAGE
    # ============================================================
    def show_register(self):
        self.clear_window()
        self.root.configure(bg='white')
        
        # Main container - centered
        container = tk.Frame(self.root, bg='white')
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Logo Section
        logo_frame = tk.Frame(container, bg='white')
        logo_frame.pack(pady=(0, 20))
        
        icon_label = tk.Label(logo_frame, text='📝', font=('Segoe UI', 40), bg='white')
        icon_label.pack()
        
        title_label = tk.Label(logo_frame, text='Create Account', 
                              font=('Segoe UI', 26, 'bold'), bg='white', fg='#1e293b')
        title_label.pack()
        
        # Form Card
        card = tk.Frame(container, bg='white', highlightbackground='#e2e8f0', 
                       highlightthickness=1, relief=tk.FLAT)
        card.pack(pady=10)
        
        inner_card = tk.Frame(card, bg='white')
        inner_card.pack(padx=40, pady=25)
        
        # Full Name
        tk.Label(inner_card, text='Full Name *', font=('Segoe UI', 10, 'bold'),
                bg='white', fg='#334155').pack(anchor='w', pady=(0, 4))
        self.reg_name = tk.Entry(inner_card, font=('Segoe UI', 11), 
                                bg='#f8fafc', relief=tk.FLAT,
                                highlightthickness=2, highlightcolor='#4f46e5',
                                highlightbackground='#e2e8f0', width=30)
        self.reg_name.pack(pady=(0, 12), ipady=5)
        
        # Email
        tk.Label(inner_card, text='Email *', font=('Segoe UI', 10, 'bold'),
                bg='white', fg='#334155').pack(anchor='w', pady=(0, 4))
        self.reg_email = tk.Entry(inner_card, font=('Segoe UI', 11), 
                                 bg='#f8fafc', relief=tk.FLAT,
                                 highlightthickness=2, highlightcolor='#4f46e5',
                                 highlightbackground='#e2e8f0', width=30)
        self.reg_email.pack(pady=(0, 12), ipady=5)
        
        # Username
        tk.Label(inner_card, text='Username *', font=('Segoe UI', 10, 'bold'),
                bg='white', fg='#334155').pack(anchor='w', pady=(0, 4))
        self.reg_username = tk.Entry(inner_card, font=('Segoe UI', 11), 
                                    bg='#f8fafc', relief=tk.FLAT,
                                    highlightthickness=2, highlightcolor='#4f46e5',
                                    highlightbackground='#e2e8f0', width=30)
        self.reg_username.pack(pady=(0, 12), ipady=5)
        
        # Password
        tk.Label(inner_card, text='Password *', font=('Segoe UI', 10, 'bold'),
                bg='white', fg='#334155').pack(anchor='w', pady=(0, 4))
        self.reg_password = tk.Entry(inner_card, font=('Segoe UI', 11), 
                                    bg='#f8fafc', relief=tk.FLAT,
                                    highlightthickness=2, highlightcolor='#4f46e5',
                                    highlightbackground='#e2e8f0', width=30, show='•')
        self.reg_password.pack(pady=(0, 8), ipady=5)
        
        # Password strength indicator
        self.pw_strength = tk.Label(inner_card, text='', font=('Segoe UI', 9),
                                   bg='white', fg='#64748b')
        self.pw_strength.pack(anchor='w', pady=(0, 12))
        self.reg_password.bind('<KeyRelease>', self.check_password_strength)
        
        # Confirm Password
        tk.Label(inner_card, text='Confirm Password *', font=('Segoe UI', 10, 'bold'),
                bg='white', fg='#334155').pack(anchor='w', pady=(0, 4))
        self.reg_confirm = tk.Entry(inner_card, font=('Segoe UI', 11), 
                                   bg='#f8fafc', relief=tk.FLAT,
                                   highlightthickness=2, highlightcolor='#4f46e5',
                                   highlightbackground='#e2e8f0', width=30, show='•')
        self.reg_confirm.pack(pady=(0, 12), ipady=5)
        self.reg_confirm.bind('<KeyRelease>', self.check_password_match)
        
        # Terms
        terms_frame = tk.Frame(inner_card, bg='white')
        terms_frame.pack(fill=tk.X, pady=(0, 16))
        
        self.terms_var = tk.IntVar(value=1)
        terms_check = tk.Checkbutton(terms_frame, text='I agree to the Terms of Service', 
                                    variable=self.terms_var,
                                    bg='white', font=('Segoe UI', 10),
                                    fg='#64748b', selectcolor='white',
                                    activebackground='white')
        terms_check.pack(side=tk.LEFT)
        
        # Create Account Button
        register_btn = ModernButton(inner_card, 'Create Account', self.handle_register,
                                   bg_color='#10b981', hover_color='#059669',
                                   font=('Segoe UI', 12, 'bold'), width=280)
        register_btn.pack(pady=(0, 10))
        
        # Back to login
        back_frame = tk.Frame(inner_card, bg='white')
        back_frame.pack()
        
        tk.Label(back_frame, text='Already have an account?', font=('Segoe UI', 10),
                bg='white', fg='#64748b').pack(side=tk.LEFT)
        
        back_link = tk.Label(back_frame, text='Sign In', font=('Segoe UI', 10, 'bold'),
                            bg='white', fg='#4f46e5', cursor='hand2')
        back_link.pack(side=tk.LEFT, padx=(5, 0))
        back_link.bind('<Button-1>', lambda e: self.show_login())
    
    def check_password_strength(self, event=None):
        password = self.reg_password.get()
        strength = ''
        color = '#64748b'
        
        if len(password) >= 8 and any(c.isupper() for c in password) and any(c.isdigit() for c in password):
            strength = '✓ Strong password'
            color = '#10b981'
        elif len(password) >= 6:
            strength = '⚠️ Medium password'
            color = '#f59e0b'
        elif password:
            strength = '❌ Weak password'
            color = '#ef4444'
        
        self.pw_strength.config(text=strength, fg=color)
    
    def check_password_match(self, event=None):
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if confirm and password != confirm:
            self.reg_confirm.config(highlightbackground='#ef4444')
        elif confirm:
            self.reg_confirm.config(highlightbackground='#10b981')
        else:
            self.reg_confirm.config(highlightbackground='#e2e8f0')
    
    # ============================================================
    # AUTH HANDLERS
    # ============================================================
    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        user = None
        for u in self.users:
            if u['username'] == username and u['password'] == password:
                user = u
                break
        
        if user:
            self.current_user = user
            self.show_toast(f"Welcome back, {user['name']}!", 'success')
            self.show_dashboard()
        else:
            self.show_toast('Invalid credentials. Try admin/admin123', 'error')
    
    def handle_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        terms = self.terms_var.get()
        
        if not all([name, email, username, password]):
            self.show_toast('Please fill in all fields.', 'error')
            return
        
        if password != confirm:
            self.show_toast('Passwords do not match.', 'error')
            return
        
        if len(password) < 6:
            self.show_toast('Password must be at least 6 characters.', 'error')
            return
        
        if not terms:
            self.show_toast('Please agree to the Terms of Service.', 'error')
            return
        
        # Check if username exists
        for u in self.users:
            if u['username'] == username:
                self.show_toast('Username already exists.', 'error')
                return
        
        # Create user
        new_id = max([u['id'] for u in self.users]) + 1 if self.users else 1
        new_user = {
            'id': new_id,
            'name': name,
            'username': username,
            'email': email,
            'password': password,
            'role': 'Staff',
            'status': 'active'
        }
        self.users.append(new_user)
        save_data(USERS_FILE, self.users)
        
        self.show_toast('Account created successfully! Please sign in.', 'success')
        self.show_login()
        self.login_username.delete(0, tk.END)
        self.login_username.insert(0, username)
        self.login_password.delete(0, tk.END)
        self.login_password.insert(0, password)
    
    # ============================================================
    # DASHBOARD
    # ============================================================
    def show_dashboard(self):
        self.clear_window()
        self.root.geometry("1200x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Create sidebar
        self.create_sidebar()
        
        # Main content
        self.main_frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Top bar
        self.create_topbar()
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)
        
        # Show dashboard page
        self.show_page('dashboard')
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg='white', width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Brand
        brand = tk.Frame(sidebar, bg='white')
        brand.pack(fill=tk.X, pady=(20, 16), padx=16)
        
        icon = tk.Label(brand, text='🎓', font=('Segoe UI', 20), bg='white')
        icon.pack(side=tk.LEFT)
        
        brand_text = tk.Frame(brand, bg='white')
        brand_text.pack(side=tk.LEFT, padx=(10, 0))
        
        tk.Label(brand_text, text='EduManage Pro', font=('Segoe UI', 16, 'bold'), 
                bg='white', fg=COLORS['text']).pack(anchor='w')
        tk.Label(brand_text, text='Administrator', font=('Segoe UI', 9), 
                bg='white', fg=COLORS['text_secondary']).pack(anchor='w')
        
        # Navigation
        nav_frame = tk.Frame(sidebar, bg='white')
        nav_frame.pack(fill=tk.X, pady=10)
        
        nav_items = [
            ('dashboard', '📊 Dashboard'),
            ('students', '👥 Students'),
            ('analytics', '📈 Analytics'),
            ('attendance', '✅ Attendance'),
            ('grades', '🎓 Grades'),
            ('courses', '📚 Courses'),
            ('users', '👤 Users'),
            ('settings', '⚙️ Settings'),
        ]
        
        self.nav_buttons = {}
        
        for page, label in nav_items:
            btn = tk.Button(nav_frame, text=label, font=('Segoe UI', 11),
                           bg='white', fg=COLORS['text_secondary'],
                           relief=tk.FLAT, anchor='w', padx=20, pady=8,
                           cursor='hand2', command=lambda p=page: self.show_page(p))
            btn.pack(fill=tk.X, padx=8, pady=1)
            self.nav_buttons[page] = btn
            
            def on_enter(e, b=btn): 
                if b.cget('bg') != '#eef2ff':
                    b.config(bg=COLORS['hover'])
            def on_leave(e, b=btn): 
                if b.cget('bg') != '#eef2ff':
                    b.config(bg='white')
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Logout at bottom
        logout_frame = tk.Frame(sidebar, bg='white')
        logout_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=16, padx=16)
        
        logout_btn = tk.Button(logout_frame, text='🚪 Logout', font=('Segoe UI', 11),
                              bg='white', fg=COLORS['danger'], relief=tk.FLAT,
                              anchor='w', padx=12, pady=8, cursor='hand2',
                              command=self.handle_logout)
        logout_btn.pack(fill=tk.X)
    
    def create_topbar(self):
        topbar = tk.Frame(self.main_frame, bg='white', height=60)
        topbar.pack(fill=tk.X)
        topbar.pack_propagate(False)
        
        # Page title
        self.page_title = tk.Label(topbar, text='Dashboard', font=('Segoe UI', 18, 'bold'),
                                  bg='white', fg=COLORS['text'])
        self.page_title.pack(side=tk.LEFT, padx=24)
        
        # Right side actions
        actions = tk.Frame(topbar, bg='white')
        actions.pack(side=tk.RIGHT, padx=24)
        
        # Search
        search_frame = tk.Frame(actions, bg='white')
        search_frame.pack(side=tk.LEFT, padx=(0, 12))
        
        self.search_entry = tk.Entry(search_frame, font=('Segoe UI', 11), bg=COLORS['bg'],
                                     relief=tk.FLAT, width=20, highlightthickness=0)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 8))
        self.search_entry.bind('<KeyRelease>', self.handle_search)
        
        search_icon = tk.Label(search_frame, text='🔍', font=('Segoe UI', 12), bg='white')
        search_icon.pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(actions, bg='white')
        user_frame.pack(side=tk.LEFT)
        
        if self.current_user:
            tk.Label(user_frame, text=f"👤 {self.current_user['name']}", 
                    font=('Segoe UI', 11), bg='white').pack(side=tk.LEFT, padx=(0, 8))
    
    # ============================================================
    # PAGE NAVIGATION
    # ============================================================
    def show_page(self, page):
        self.current_page = page
        
        # Update nav buttons
        for p, btn in self.nav_buttons.items():
            if p == page:
                btn.config(bg='#eef2ff', fg=COLORS['primary'])
            else:
                btn.config(bg='white', fg=COLORS['text_secondary'])
        
        # Update title
        titles = {
            'dashboard': '📊 Dashboard',
            'students': '👥 Student Management',
            'analytics': '📈 Analytics',
            'attendance': '✅ Attendance',
            'grades': '🎓 Grades',
            'courses': '📚 Courses',
            'users': '👤 User Management',
            'settings': '⚙️ Settings'
        }
        self.page_title.config(text=titles.get(page, 'Dashboard'))
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show selected page
        page_methods = {
            'dashboard': self.render_dashboard,
            'students': self.render_students,
            'analytics': self.render_analytics,
            'attendance': self.render_attendance,
            'grades': self.render_grades,
            'courses': self.render_courses,
            'users': self.render_users,
            'settings': self.render_settings,
        }
        
        if page in page_methods:
            page_methods[page]()
    
    # ============================================================
    # RENDER: DASHBOARD
    # ============================================================
    def render_dashboard(self):
        # Stats grid
        stats_frame = tk.Frame(self.content_frame, bg=COLORS['bg'])
        stats_frame.pack(fill=tk.X, pady=(0, 16))
        
        total = len(self.students)
        active = len([s for s in self.students if s['status'] == 'active'])
        avg_grade = sum([self.grade_to_score(s['grade']) for s in self.students]) / max(total, 1)
        avg_attendance = sum([s['attendance'] for s in self.students]) / max(total, 1)
        
        stats = [
            ('Total Students', str(total), '👥', COLORS['primary']),
            ('Active Students', str(active), '✅', COLORS['success']),
            ('Avg Grade', f"{avg_grade:.1f}%", '📊', COLORS['warning']),
            ('Attendance', f"{avg_attendance:.1f}%", '📈', COLORS['info']),
        ]
        
        for i, (label, value, icon, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg='white', relief=tk.FLAT, bd=1,
                           highlightbackground=COLORS['border'], highlightthickness=1)
            card.grid(row=0, column=i, padx=8, sticky='ew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            inner = tk.Frame(card, bg='white')
            inner.pack(padx=16, pady=14, fill=tk.X)
            
            tk.Label(inner, text=icon, font=('Segoe UI', 20), bg='white').pack(side=tk.RIGHT)
            
            tk.Label(inner, text=label, font=('Segoe UI', 11), 
                    bg='white', fg=COLORS['text_secondary']).pack(anchor='w')
            tk.Label(inner, text=value, font=('Segoe UI', 24, 'bold'), 
                    bg='white', fg=color).pack(anchor='w')
        
        # Recent students table
        table_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        header = tk.Frame(table_frame, bg='white')
        header.pack(fill=tk.X, padx=16, pady=(12, 8))
        tk.Label(header, text='📋 Recent Students', font=('Segoe UI', 14, 'bold'), 
                bg='white').pack(side=tk.LEFT)
        
        # Table
        self.create_student_table(table_frame, self.students[:5])
    
    def grade_to_score(self, grade):
        scores = {'A+': 95, 'A': 90, 'A-': 85, 'B+': 82, 'B': 78, 'B-': 75, 'C+': 72, 'C': 68}
        return scores.get(grade, 70)
    
    # ============================================================
    # RENDER: STUDENTS
    # ============================================================
    def render_students(self):
        # Toolbar
        toolbar = tk.Frame(self.content_frame, bg=COLORS['bg'])
        toolbar.pack(fill=tk.X, pady=(0, 12))
        
        tk.Button(toolbar, text='➕ Add Student', font=('Segoe UI', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=16, pady=6,
                 cursor='hand2', command=self.open_add_student).pack(side=tk.LEFT)
        
        tk.Button(toolbar, text='📤 Export', font=('Segoe UI', 11),
                 bg='white', fg=COLORS['text'], relief=tk.FLAT, padx=16, pady=6,
                 cursor='hand2', command=self.export_data).pack(side=tk.LEFT, padx=(8, 0))
        
        # Filters
        filter_frame = tk.Frame(self.content_frame, bg=COLORS['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 12))
        
        tk.Label(filter_frame, text='🔍 Search:', font=('Segoe UI', 10), 
                bg=COLORS['bg']).pack(side=tk.LEFT, padx=(0, 6))
        
        self.search_student = tk.Entry(filter_frame, font=('Segoe UI', 11), bg='white',
                                       relief=tk.FLAT, width=20)
        self.search_student.pack(side=tk.LEFT, padx=(0, 12))
        self.search_student.bind('<KeyRelease>', self.filter_students)
        
        tk.Label(filter_frame, text='Class:', font=('Segoe UI', 10), 
                bg=COLORS['bg']).pack(side=tk.LEFT, padx=(0, 6))
        
        self.filter_class = ttk.Combobox(filter_frame, values=['All'] + CLASSES, 
                                         font=('Segoe UI', 11), width=12)
        self.filter_class.pack(side=tk.LEFT, padx=(0, 12))
        self.filter_class.set('All')
        self.filter_class.bind('<<ComboboxSelected>>', self.filter_students)
        
        tk.Label(filter_frame, text='Status:', font=('Segoe UI', 10), 
                bg=COLORS['bg']).pack(side=tk.LEFT, padx=(0, 6))
        
        self.filter_status = ttk.Combobox(filter_frame, values=['All'] + [s['label'] for s in STATUSES],
                                          font=('Segoe UI', 11), width=12)
        self.filter_status.pack(side=tk.LEFT)
        self.filter_status.set('All')
        self.filter_status.bind('<<ComboboxSelected>>', self.filter_students)
        
        # Table
        table_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.student_table_frame = table_frame
        self.render_student_table()
    
    def render_student_table(self):
        # Clear table frame
        for widget in self.student_table_frame.winfo_children():
            widget.destroy()
        
        # Get filtered data
        data = self.get_filtered_students()
        total = len(data)
        total_pages = max(1, (total + self.per_page - 1) // self.per_page)
        
        if self.current_page_num > total_pages:
            self.current_page_num = total_pages
        
        start = (self.current_page_num - 1) * self.per_page
        end = min(start + self.per_page, total)
        page_data = data[start:end]
        
        # Table header
        header = tk.Frame(self.student_table_frame, bg='white')
        header.pack(fill=tk.X, padx=16, pady=(12, 8))
        tk.Label(header, text='📋 All Students', font=('Segoe UI', 14, 'bold'), 
                bg='white').pack(side=tk.LEFT)
        
        # Create table
        self.create_student_table(self.student_table_frame, page_data)
        
        # Pagination
        pagination = tk.Frame(self.student_table_frame, bg='white')
        pagination.pack(fill=tk.X, padx=16, pady=(8, 12))
        
        tk.Label(pagination, text=f"Showing {start+1 if total > 0 else 0} to {end} of {total} students",
                font=('Segoe UI', 10), bg='white', fg=COLORS['text_secondary']).pack(side=tk.LEFT)
        
        page_frame = tk.Frame(pagination, bg='white')
        page_frame.pack(side=tk.RIGHT)
        
        # Previous button
        prev_btn = tk.Button(page_frame, text='◀', font=('Segoe UI', 10),
                            bg='white', relief=tk.FLAT, padx=8,
                            command=lambda: self.go_to_page(self.current_page_num - 1))
        prev_btn.pack(side=tk.LEFT)
        if self.current_page_num <= 1:
            prev_btn.config(state=tk.DISABLED)
        
        # Page numbers
        for i in range(1, total_pages + 1):
            if i == self.current_page_num:
                btn = tk.Button(page_frame, text=str(i), font=('Segoe UI', 10),
                               bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=8)
            else:
                btn = tk.Button(page_frame, text=str(i), font=('Segoe UI', 10),
                               bg='white', relief=tk.FLAT, padx=8,
                               command=lambda p=i: self.go_to_page(p))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Next button
        next_btn = tk.Button(page_frame, text='▶', font=('Segoe UI', 10),
                            bg='white', relief=tk.FLAT, padx=8,
                            command=lambda: self.go_to_page(self.current_page_num + 1))
        next_btn.pack(side=tk.LEFT)
        if self.current_page_num >= total_pages:
            next_btn.config(state=tk.DISABLED)
    
    def create_student_table(self, parent, data):
        # Treeview for table
        columns = ('ID', 'Name', 'Class', 'Grade', 'Status', 'Attendance')
        
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=32)
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=6)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column('Name', width=180)
        
        for student in data:
            status = next((s for s in STATUSES if s['value'] == student['status']), None)
            status_label = status['label'] if status else student['status']
            
            tree.insert('', tk.END, values=(
                student['id'],
                f"{student['firstName']} {student['lastName']}",
                student['class'],
                student['grade'],
                status_label,
                f"{student['attendance']}%"
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 12))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=0.92, anchor='ne')
    
    def get_filtered_students(self):
        search = self.search_student.get().strip().lower() if hasattr(self, 'search_student') else ''
        class_filter = self.filter_class.get() if hasattr(self, 'filter_class') else 'All'
        status_filter = self.filter_status.get() if hasattr(self, 'filter_status') else 'All'
        
        data = self.students.copy()
        
        if search:
            data = [s for s in data if search in f"{s['firstName']} {s['lastName']}".lower() or search in s['id'].lower()]
        
        if class_filter != 'All':
            data = [s for s in data if s['class'] == class_filter]
        
        if status_filter != 'All':
            data = [s for s in data if next((st for st in STATUSES if st['label'] == status_filter), {}).get('value') == s['status']]
        
        return data
    
    def filter_students(self, event=None):
        self.current_page_num = 1
        self.render_student_table()
    
    def go_to_page(self, page):
        data = self.get_filtered_students()
        total_pages = max(1, (len(data) + self.per_page - 1) // self.per_page)
        if 1 <= page <= total_pages:
            self.current_page_num = page
            self.render_student_table()
    
    # ============================================================
    # RENDER: ANALYTICS
    # ============================================================
    def render_analytics(self):
        # Grade distribution chart
        chart_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        tk.Label(chart_frame, text='📊 Grade Distribution', font=('Segoe UI', 14, 'bold'),
                bg='white').pack(anchor='w', padx=16, pady=(12, 8))
        
        chart_inner = tk.Frame(chart_frame, bg='white')
        chart_inner.pack(fill=tk.X, padx=16, pady=(0, 16))
        
        grade_counts = {}
        for g in GRADES:
            grade_counts[g] = len([s for s in self.students if s['grade'] == g])
        
        max_count = max(grade_counts.values()) if grade_counts else 1
        
        for grade, count in grade_counts.items():
            height = int((count / max_count) * 150) + 10
            
            bar_frame = tk.Frame(chart_inner, bg='white')
            bar_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
            
            # Bar
            bar = tk.Frame(bar_frame, bg=COLORS['primary'], height=height)
            bar.pack(side=tk.BOTTOM, fill=tk.X, padx=4)
            
            # Label
            tk.Label(bar_frame, text=f"{grade}\n{count}", font=('Segoe UI', 9),
                    bg='white', fg=COLORS['text_secondary']).pack(side=tk.BOTTOM, pady=(4, 0))
    
    # ============================================================
    # RENDER: ATTENDANCE
    # ============================================================
    def render_attendance(self):
        table_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(table_frame, text='✅ Attendance Records', font=('Segoe UI', 14, 'bold'),
                bg='white').pack(anchor='w', padx=16, pady=(12, 8))
        
        columns = ('Name', 'Class', 'Present', 'Absent', 'Attendance %', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column('Name', width=150)
        
        for s in self.students[:10]:
            present = int(s['attendance'] * 0.95)
            absent = int(s['attendance'] * 0.05)
            status = 'Good' if s['attendance'] >= 90 else 'Average' if s['attendance'] >= 75 else 'Poor'
            
            tree.insert('', tk.END, values=(
                f"{s['firstName']} {s['lastName']}",
                s['class'],
                present,
                absent,
                f"{s['attendance']}%",
                status
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
    
    # ============================================================
    # RENDER: GRADES
    # ============================================================
    def render_grades(self):
        table_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(table_frame, text='🎓 Grade Records', font=('Segoe UI', 14, 'bold'),
                bg='white').pack(anchor='w', padx=16, pady=(12, 8))
        
        columns = ('Student', 'Class', 'Subject', 'Score', 'Grade', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        tree.column('Student', width=150)
        
        import random
        for i, s in enumerate(self.students[:10]):
            subject = SUBJECTS[i % len(SUBJECTS)]
            score = random.randint(60, 95)
            grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D' if score >= 60 else 'F'
            status = 'Pass' if score >= 70 else 'Fail'
            
            tree.insert('', tk.END, values=(
                f"{s['firstName']} {s['lastName']}",
                s['class'],
                subject,
                f"{score}%",
                grade,
                status
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
    
    # ============================================================
    # RENDER: COURSES
    # ============================================================
    def render_courses(self):
        courses = [
            ('Mathematics 101', 'Dr. Sarah Chen', '32', 'Mon/Wed 10:00 AM'),
            ('English Literature', 'Prof. James Wilson', '28', 'Tue/Thu 11:00 AM'),
            ('Computer Science', 'Ms. Emily Davis', '35', 'Mon/Wed 2:00 PM'),
            ('Physics', 'Dr. Robert Kim', '25', 'Tue/Thu 9:00 AM'),
            ('Chemistry', 'Prof. Maria Garcia', '30', 'Mon/Wed 1:00 PM'),
            ('History', 'Mr. David Brown', '22', 'Fri 10:00 AM'),
        ]
        
        grid = tk.Frame(self.content_frame, bg=COLORS['bg'])
        grid.pack(fill=tk.BOTH, expand=True)
        
        for i, (name, teacher, students, schedule) in enumerate(courses):
            row, col = i // 3, i % 3
            card = tk.Frame(grid, bg='white', relief=tk.FLAT, bd=1,
                           highlightbackground=COLORS['border'], highlightthickness=1)
            card.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
            grid.grid_rowconfigure(row, weight=1)
            grid.grid_columnconfigure(col, weight=1)
            
            inner = tk.Frame(card, bg='white')
            inner.pack(padx=16, pady=16, fill=tk.BOTH, expand=True)
            
            tk.Label(inner, text='📚', font=('Segoe UI', 24), bg='white').pack(anchor='ne')
            
            tk.Label(inner, text=name, font=('Segoe UI', 13, 'bold'), 
                    bg='white', fg=COLORS['text']).pack(anchor='w')
            tk.Label(inner, text=teacher, font=('Segoe UI', 10), 
                    bg='white', fg=COLORS['text_secondary']).pack(anchor='w', pady=(2, 8))
            
            info = tk.Frame(inner, bg='white')
            info.pack(fill=tk.X)
            tk.Label(info, text=f"👥 {students} students", font=('Segoe UI', 10),
                    bg='white', fg=COLORS['text_secondary']).pack(side=tk.LEFT)
            tk.Label(info, text=f"🕐 {schedule}", font=('Segoe UI', 10),
                    bg='white', fg=COLORS['text_secondary']).pack(side=tk.RIGHT)
    
    # ============================================================
    # RENDER: USERS
    # ============================================================
    def render_users(self):
        toolbar = tk.Frame(self.content_frame, bg=COLORS['bg'])
        toolbar.pack(fill=tk.X, pady=(0, 12))
        
        tk.Button(toolbar, text='➕ Add User', font=('Segoe UI', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=16, pady=6,
                 cursor='hand2', command=self.open_add_user).pack(side=tk.LEFT)
        
        table_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                               highlightbackground=COLORS['border'], highlightthickness=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(table_frame, text='👤 User Management', font=('Segoe UI', 14, 'bold'),
                bg='white').pack(anchor='w', padx=16, pady=(12, 8))
        
        columns = ('Name', 'Username', 'Email', 'Role', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor='center')
        tree.column('Name', width=160)
        
        for u in self.users:
            tree.insert('', tk.END, values=(
                u['name'],
                u['username'],
                u['email'],
                u['role'],
                u['status']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
    
    # ============================================================
    # RENDER: SETTINGS
    # ============================================================
    def render_settings(self):
        settings_frame = tk.Frame(self.content_frame, bg='white', relief=tk.FLAT, bd=1,
                                  highlightbackground=COLORS['border'], highlightthickness=1)
        settings_frame.pack(fill=tk.X, pady=20, padx=40)
        
        inner = tk.Frame(settings_frame, bg='white')
        inner.pack(padx=32, pady=32, fill=tk.X)
        
        tk.Label(inner, text='⚙️ System Settings', font=('Segoe UI', 18, 'bold'),
                bg='white').pack(anchor='w', pady=(0, 16))
        
        # Settings fields
        fields = [
            ('School Name', 'EduManage Pro Academy'),
            ('School Code', 'EMP-2024'),
            ('Academic Year', '2024-2025'),
            ('Semester', 'Semester 2'),
        ]
        
        for label, value in fields:
            row = tk.Frame(inner, bg='white')
            row.pack(fill=tk.X, pady=6)
            
            tk.Label(row, text=label, font=('Segoe UI', 11), 
                    bg='white', fg=COLORS['text_secondary'], width=16, anchor='w').pack(side=tk.LEFT)
            
            if label == 'Academic Year':
                combo = ttk.Combobox(row, values=['2024-2025', '2023-2024'], font=('Segoe UI', 11), width=20)
                combo.pack(side=tk.LEFT)
                combo.set(value)
            elif label == 'Semester':
                combo = ttk.Combobox(row, values=['Semester 1', 'Semester 2'], font=('Segoe UI', 11), width=20)
                combo.pack(side=tk.LEFT)
                combo.set(value)
            else:
                entry = tk.Entry(row, font=('Segoe UI', 11), bg=COLORS['bg'], relief=tk.FLAT, width=25)
                entry.pack(side=tk.LEFT)
                entry.insert(0, value)
        
        btn_frame = tk.Frame(inner, bg='white')
        btn_frame.pack(fill=tk.X, pady=(16, 0))
        
        tk.Button(btn_frame, text='Save Settings', font=('Segoe UI', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=lambda: self.show_toast('Settings saved!', 'success')).pack(side=tk.LEFT)
        
        tk.Button(btn_frame, text='Reset', font=('Segoe UI', 11),
                 bg='white', fg=COLORS['text_secondary'], relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=lambda: self.show_toast('Settings reset!', 'info')).pack(side=tk.LEFT, padx=(8, 0))
    
    # ============================================================
    # STUDENT CRUD OPERATIONS
    # ============================================================
    def open_add_student(self):
        modal = tk.Toplevel(self.root)
        modal.title("Add New Student")
        modal.geometry("600x550")
        modal.configure(bg='white')
        modal.transient(self.root)
        modal.grab_set()
        
        # Center modal
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 300
        y = (modal.winfo_screenheight() // 2) - 275
        modal.geometry(f"600x550+{x}+{y}")
        
        # Header
        header = tk.Frame(modal, bg='white')
        header.pack(fill=tk.X, padx=24, pady=(20, 12))
        tk.Label(header, text='➕ Add New Student', font=('Segoe UI', 18, 'bold'),
                bg='white').pack(side=tk.LEFT)
        
        tk.Button(header, text='✕', font=('Segoe UI', 14), bg='white', relief=tk.FLAT,
                 cursor='hand2', command=modal.destroy).pack(side=tk.RIGHT)
        
        # Form
        form = tk.Frame(modal, bg='white')
        form.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))
        
        entries = {}
        fields = [
            ('First Name *', 'firstName'),
            ('Last Name *', 'lastName'),
            ('Email *', 'email'),
            ('Phone', 'phone'),
            ('Date of Birth *', 'dob'),
            ('Gender', 'gender'),
            ('Class *', 'class'),
            ('Enrollment Date *', 'enrollmentDate'),
        ]
        
        for i, (label, key) in enumerate(fields):
            row, col = i // 2, i % 2
            frame = tk.Frame(form, bg='white')
            frame.grid(row=row, column=col, padx=8, pady=6, sticky='ew')
            form.grid_columnconfigure(col, weight=1)
            
            tk.Label(frame, text=label, font=('Segoe UI', 10), 
                    bg='white', fg=COLORS['text_secondary']).pack(anchor='w')
            
            if key == 'gender':
                entry = ttk.Combobox(frame, values=['male', 'female', 'other'], font=('Segoe UI', 11))
            elif key == 'class':
                entry = ttk.Combobox(frame, values=CLASSES, font=('Segoe UI', 11))
            elif key == 'dob' or key == 'enrollmentDate':
                entry = tk.Entry(frame, font=('Segoe UI', 11), bg='#f8fafc', relief=tk.FLAT)
                entry.insert(0, '2005-01-01')
            else:
                entry = tk.Entry(frame, font=('Segoe UI', 11), bg='#f8fafc', relief=tk.FLAT)
            
            entry.pack(fill=tk.X, pady=(2, 0))
            entries[key] = entry
        
        # Address field
        addr_frame = tk.Frame(form, bg='white')
        addr_frame.grid(row=4, column=0, columnspan=2, padx=8, pady=6, sticky='ew')
        tk.Label(addr_frame, text='Address', font=('Segoe UI', 10), 
                bg='white', fg=COLORS['text_secondary']).pack(anchor='w')
        addr_entry = tk.Text(addr_frame, font=('Segoe UI', 11), height=2, bg='#f8fafc', relief=tk.FLAT)
        addr_entry.pack(fill=tk.X, pady=(2, 0))
        
        # Buttons
        btn_frame = tk.Frame(modal, bg='white')
        btn_frame.pack(fill=tk.X, padx=24, pady=(0, 20))
        
        tk.Button(btn_frame, text='Cancel', font=('Segoe UI', 11),
                 bg='white', fg=COLORS['text_secondary'], relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=modal.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        
        def save_student():
            data = {k: entries[k].get().strip() for k in entries}
            address = addr_entry.get('1.0', tk.END).strip()
            
            if not all([data['firstName'], data['lastName'], data['email'], data['dob'], data['class'], data['enrollmentDate']]):
                self.show_toast('Please fill in all required fields.', 'error')
                return
            
            new_id = f"STU{str(len(self.students) + 1).zfill(3)}"
            new_student = {
                'id': new_id,
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'email': data['email'],
                'phone': data.get('phone', ''),
                'dob': data['dob'],
                'gender': data.get('gender', 'male'),
                'class': data['class'],
                'enrollmentDate': data['enrollmentDate'],
                'grade': 'B',
                'status': 'active',
                'attendance': 85,
                'address': address,
            }
            
            self.students.append(new_student)
            save_data(STUDENTS_FILE, self.students)
            modal.destroy()
            self.show_toast(f"Student {data['firstName']} {data['lastName']} added!", 'success')
            self.render_student_table()
        
        tk.Button(btn_frame, text='Save Student', font=('Segoe UI', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=save_student).pack(side=tk.RIGHT)
    
    def open_add_user(self):
        modal = tk.Toplevel(self.root)
        modal.title("Add New User")
        modal.geometry("450x450")
        modal.configure(bg='white')
        modal.transient(self.root)
        modal.grab_set()
        
        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - 225
        y = (modal.winfo_screenheight() // 2) - 225
        modal.geometry(f"450x450+{x}+{y}")
        
        header = tk.Frame(modal, bg='white')
        header.pack(fill=tk.X, padx=24, pady=(20, 12))
        tk.Label(header, text='➕ Add New User', font=('Segoe UI', 18, 'bold'),
                bg='white').pack(side=tk.LEFT)
        tk.Button(header, text='✕', font=('Segoe UI', 14), bg='white', relief=tk.FLAT,
                 cursor='hand2', command=modal.destroy).pack(side=tk.RIGHT)
        
        form = tk.Frame(modal, bg='white')
        form.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))
        
        entries = {}
        fields = [
            ('Full Name *', 'name'),
            ('Username *', 'username'),
            ('Email *', 'email'),
            ('Password *', 'password'),
            ('Role', 'role'),
        ]
        
        for i, (label, key) in enumerate(fields):
            frame = tk.Frame(form, bg='white')
            frame.pack(fill=tk.X, pady=6)
            
            tk.Label(frame, text=label, font=('Segoe UI', 10), 
                    bg='white', fg=COLORS['text_secondary']).pack(anchor='w')
            
            if key == 'role':
                entry = ttk.Combobox(frame, values=['Administrator', 'Teacher', 'Staff', 'Viewer'], font=('Segoe UI', 11))
                entry.set('Staff')
            elif key == 'password':
                entry = tk.Entry(frame, font=('Segoe UI', 11), bg='#f8fafc', relief=tk.FLAT, show='•')
            else:
                entry = tk.Entry(frame, font=('Segoe UI', 11), bg='#f8fafc', relief=tk.FLAT)
            
            entry.pack(fill=tk.X, pady=(2, 0))
            entries[key] = entry
        
        btn_frame = tk.Frame(modal, bg='white')
        btn_frame.pack(fill=tk.X, padx=24, pady=(0, 20))
        
        tk.Button(btn_frame, text='Cancel', font=('Segoe UI', 11),
                 bg='white', fg=COLORS['text_secondary'], relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=modal.destroy).pack(side=tk.RIGHT, padx=(0, 8))
        
        def save_user():
            data = {k: entries[k].get().strip() for k in entries}
            
            if not all([data['name'], data['username'], data['email'], data['password']]):
                self.show_toast('Please fill in all required fields.', 'error')
                return
            
            if len(data['password']) < 6:
                self.show_toast('Password must be at least 6 characters.', 'error')
                return
            
            for u in self.users:
                if u['username'] == data['username']:
                    self.show_toast('Username already exists.', 'error')
                    return
            
            new_id = max([u['id'] for u in self.users]) + 1 if self.users else 1
            new_user = {
                'id': new_id,
                'name': data['name'],
                'username': data['username'],
                'email': data['email'],
                'password': data['password'],
                'role': data.get('role', 'Staff'),
                'status': 'active'
            }
            
            self.users.append(new_user)
            save_data(USERS_FILE, self.users)
            modal.destroy()
            self.show_toast(f"User {data['name']} added!", 'success')
            self.render_users()
        
        tk.Button(btn_frame, text='Save User', font=('Segoe UI', 11, 'bold'),
                 bg=COLORS['primary'], fg='white', relief=tk.FLAT, padx=24, pady=8,
                 cursor='hand2', command=save_user).pack(side=tk.RIGHT)
    
    # ============================================================
    # EXPORT DATA
    # ============================================================
    def export_data(self):
        import csv
        filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Class', 'Grade', 'Status', 'Attendance'])
                for s in self.students:
                    writer.writerow([
                        s['id'], s['firstName'], s['lastName'], s['email'],
                        s['phone'], s['class'], s['grade'], s['status'], s['attendance']
                    ])
            self.show_toast(f'Data exported to {filename}', 'success')
        except Exception as e:
            self.show_toast(f'Export failed: {str(e)}', 'error')
    
    # ============================================================
    # SEARCH
    # ============================================================
    def handle_search(self, event=None):
        query = self.search_entry.get().strip().lower()
        if query:
            self.show_page('students')
            self.search_student.delete(0, tk.END)
            self.search_student.insert(0, query)
            self.filter_students()
    
    # ============================================================
    # LOGOUT
    # ============================================================
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_toast('Logged out successfully', 'info')
            self.show_login()
    
    # ============================================================
    # CLEAR WINDOW
    # ============================================================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = EduManageApp(root)
    root.mainloop()