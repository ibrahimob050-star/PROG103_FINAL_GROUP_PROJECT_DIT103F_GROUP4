import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class ClinicQueueManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Queue Management System")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f4f7fc')
        self.root.resizable(True, True)
        
        # User data file
        self.users_file = "users.json"
        self.load_users()
        
        # Queue data
        self.queue = []
        self.queue_counter = 1
        self.current_serving = None
        self.current_user = None
        
        # Sample doctors
        self.doctors = [
            {"id": 1, "name": "Dr. Patricia Hill", "specialty": "Cardiology", "room": "304", "status": "Available"},
            {"id": 2, "name": "Dr. Alan Chen", "specialty": "Orthopedics", "room": "210", "status": "Available"},
            {"id": 3, "name": "Dr. Lisa Park", "specialty": "Dermatology", "room": "112", "status": "Available"},
            {"id": 4, "name": "Dr. Mark Rivera", "specialty": "Neurology", "room": "407", "status": "Available"}
        ]
        
        # Initialize sample queue
        self.initialize_sample_queue()
        
        # Main container
        self.main_container = tk.Frame(root, bg='#ffffff', highlightthickness=1, 
                                      highlightcolor='#eef2f6', highlightbackground='#eef2f6')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show login page
        self.show_login()
        
        # Auto-refresh every 5 seconds
        self.auto_refresh()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            # Default users
            self.users = {
                "admin@clinic.com": {"password": "admin123", "name": "Admin"},
                "doctor@clinic.com": {"password": "doctor123", "name": "Dr. Sarah Chen"}
            }
            self.save_users()
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)
    
    def initialize_sample_queue(self):
        """Initialize with sample patients"""
        sample_patients = [
            {"name": "James Delaney", "priority": "Normal", "doctor": "Dr. Patricia Hill", "department": "Cardiology"},
            {"name": "Maria Rodriguez", "priority": "Urgent", "doctor": "Dr. Alan Chen", "department": "Orthopedics"},
            {"name": "Thomas Webb", "priority": "Normal", "doctor": "Dr. Lisa Park", "department": "Dermatology"},
            {"name": "Sarah Finley", "priority": "Normal", "doctor": "Dr. Mark Rivera", "department": "Neurology"},
            {"name": "Emma Johnson", "priority": "Urgent", "doctor": "Dr. Patricia Hill", "department": "Cardiology"}
        ]
        
        for patient in sample_patients:
            self.queue.append({
                "ticket": f"Q{self.queue_counter:04d}",
                "name": patient["name"],
                "priority": patient["priority"],
                "doctor": patient["doctor"],
                "department": patient["department"],
                "status": "Waiting",
                "time": datetime.now().strftime("%I:%M %p"),
                "wait_time": "5 min"
            })
            self.queue_counter += 1
    
    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def auto_refresh(self):
        """Auto-refresh the dashboard every 5 seconds"""
        if hasattr(self, 'current_page') and self.current_page == 'dashboard':
            self.update_queue_display()
        self.root.after(5000, self.auto_refresh)
    
    def create_rounded_frame(self, parent, bg='white', **kwargs):
        """Helper to create a frame with rounded corners appearance"""
        frame = tk.Frame(parent, bg=bg, **kwargs)
        frame.config(highlightthickness=1, highlightcolor='#eef2f6', highlightbackground='#eef2f6')
        return frame
    
    def get_priority_color(self, priority):
        """Get color based on priority"""
        colors = {
            "Urgent": "#dc2626",
            "High": "#eab308", 
            "Normal": "#2563eb",
            "Low": "#64748b"
        }
        return colors.get(priority, "#64748b")
    
    def get_status_color(self, status):
        """Get color based on status"""
        colors = {
            "Waiting": "#eab308",
            "In Progress": "#2563eb",
            "Completed": "#22c55e",
            "Cancelled": "#dc2626"
        }
        return colors.get(status, "#64748b")
    
    # ==================== LOGIN PAGE ====================
    def show_login(self):
        self.current_page = 'login'
        self.clear_container()
        
        # Header
        header = tk.Frame(self.main_container, bg='#f4f7fc', height=70)
        header.pack(fill=tk.X, pady=(15, 20))
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg='#f4f7fc')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#f4f7fc')
        logo_text.pack(side=tk.LEFT)
        
        # Login form
        form_container = tk.Frame(self.main_container, bg='#f4f7fc')
        form_container.pack(expand=True)
        
        form_frame = self.create_rounded_frame(form_container, bg='white', width=450, height=400)
        form_frame.pack(pady=30)
        form_frame.pack_propagate(False)
        
        tk.Label(form_frame, text="Welcome back", font=('Segoe UI', 24, 'bold'), 
                fg='#0b1e3a', bg='white').pack(pady=(35, 5))
        tk.Label(form_frame, text="Sign in to manage the clinic queue", font=('Segoe UI', 12), 
                fg='#64748b', bg='white').pack(pady=(0, 25))
        
        # Email
        tk.Label(form_frame, text="Email", font=('Segoe UI', 10, 'bold'), 
                fg='#334155', bg='white').pack(anchor='w', padx=40)
        self.login_email = tk.Entry(form_frame, font=('Segoe UI', 12), bg='#f8fafc',
                             relief='solid', bd=1, highlightcolor='#2563eb')
        self.login_email.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=4)
        self.login_email.insert(0, "admin@clinic.com")
        
        # Password
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                fg='#334155', bg='white').pack(anchor='w', padx=40)
        self.login_password = tk.Entry(form_frame, font=('Segoe UI', 12), bg='#f8fafc',
                                relief='solid', bd=1, show='•')
        self.login_password.pack(fill=tk.X, padx=40, pady=(5, 20), ipady=4)
        self.login_password.insert(0, "admin123")
        
        # Login button
        login_btn = tk.Button(form_frame, text="Sign in", font=('Segoe UI', 12, 'bold'),
                            bg='#2563eb', fg='white', relief='flat', cursor='hand2',
                            activebackground='#1d4ed8', activeforeground='white',
                            command=self.handle_login)
        login_btn.pack(fill=tk.X, padx=40, pady=10, ipady=6)
        
        # Toggle to signup
        toggle_frame = tk.Frame(form_frame, bg='white')
        toggle_frame.pack(pady=15)
        tk.Label(toggle_frame, text="Don't have an account?", font=('Segoe UI', 11),
                fg='#475569', bg='white').pack(side=tk.LEFT)
        signup_link = tk.Label(toggle_frame, text="Sign up", font=('Segoe UI', 11, 'bold'),
                             fg='#2563eb', bg='white', cursor='hand2')
        signup_link.pack(side=tk.LEFT, padx=(5, 0))
        signup_link.bind('<Button-1>', lambda e: self.show_signup())
        signup_link.bind('<Enter>', lambda e: signup_link.config(fg='#1d4ed8'))
        signup_link.bind('<Leave>', lambda e: signup_link.config(fg='#2563eb'))
    
    def handle_login(self):
        email = self.login_email.get().strip()
        password = self.login_password.get().strip()
        
        if not email or not password:
            messagebox.showwarning("Warning", "Please enter both email and password")
            return
        
        if email in self.users and self.users[email]['password'] == password:
            self.current_user = self.users[email]['name']
            messagebox.showinfo("Success", f"✅ Welcome back, {self.current_user}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "❌ Invalid email or password")
    
    # ==================== SIGNUP PAGE ====================
    def show_signup(self):
        self.current_page = 'signup'
        self.clear_container()
        
        # Header
        header = tk.Frame(self.main_container, bg='#f4f7fc', height=70)
        header.pack(fill=tk.X, pady=(15, 20))
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg='#f4f7fc')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#f4f7fc')
        logo_text.pack(side=tk.LEFT)
        
        # Signup form
        form_container = tk.Frame(self.main_container, bg='#f4f7fc')
        form_container.pack(expand=True)
        
        form_frame = self.create_rounded_frame(form_container, bg='white', width=450, height=480)
        form_frame.pack(pady=20)
        form_frame.pack_propagate(False)
        
        tk.Label(form_frame, text="Create account", font=('Segoe UI', 24, 'bold'), 
                fg='#0b1e3a', bg='white').pack(pady=(30, 5))
        tk.Label(form_frame, text="Start managing your clinic queue", 
                font=('Segoe UI', 12), fg='#64748b', bg='white').pack(pady=(0, 20))
        
        # Full name
        tk.Label(form_frame, text="Full name", font=('Segoe UI', 10, 'bold'), 
                fg='#334155', bg='white').pack(anchor='w', padx=40)
        self.signup_name = tk.Entry(form_frame, font=('Segoe UI', 12), bg='#f8fafc',
                            relief='solid', bd=1)
        self.signup_name.pack(fill=tk.X, padx=40, pady=(5, 10), ipady=4)
        self.signup_name.insert(0, "Dr. Sarah Chen")
        
        # Email
        tk.Label(form_frame, text="Email", font=('Segoe UI', 10, 'bold'), 
                fg='#334155', bg='white').pack(anchor='w', padx=40)
        self.signup_email = tk.Entry(form_frame, font=('Segoe UI', 12), bg='#f8fafc',
                            relief='solid', bd=1)
        self.signup_email.pack(fill=tk.X, padx=40, pady=(5, 10), ipady=4)
        self.signup_email.insert(0, "sarah@clinic.com")
        
        # Password
        tk.Label(form_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                fg='#334155', bg='white').pack(anchor='w', padx=40)
        self.signup_password = tk.Entry(form_frame, font=('Segoe UI', 12), bg='#f8fafc',
                                relief='solid', bd=1, show='•')
        self.signup_password.pack(fill=tk.X, padx=40, pady=(5, 15), ipady=4)
        self.signup_password.insert(0, "securepass123")
        
        # Signup button
        signup_btn = tk.Button(form_frame, text="Create account", font=('Segoe UI', 12, 'bold'),
                             bg='#2563eb', fg='white', relief='flat', cursor='hand2',
                             activebackground='#1d4ed8', activeforeground='white',
                             command=self.handle_signup)
        signup_btn.pack(fill=tk.X, padx=40, pady=10, ipady=6)
        
        # Toggle to login
        toggle_frame = tk.Frame(form_frame, bg='white')
        toggle_frame.pack(pady=10)
        tk.Label(toggle_frame, text="Already have an account?", font=('Segoe UI', 11),
                fg='#475569', bg='white').pack(side=tk.LEFT)
        login_link = tk.Label(toggle_frame, text="Sign in", font=('Segoe UI', 11, 'bold'),
                            fg='#2563eb', bg='white', cursor='hand2')
        login_link.pack(side=tk.LEFT, padx=(5, 0))
        login_link.bind('<Button-1>', lambda e: self.show_login())
        login_link.bind('<Enter>', lambda e: login_link.config(fg='#1d4ed8'))
        login_link.bind('<Leave>', lambda e: login_link.config(fg='#2563eb'))
    
    def handle_signup(self):
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get().strip()
        
        if not name or not email or not password:
            messagebox.showwarning("Warning", "Please fill in all fields")
            return
        
        if email in self.users:
            messagebox.showerror("Error", "❌ Email already registered")
            return
        
        # Add new user
        self.users[email] = {"password": password, "name": name}
        self.save_users()
        
        messagebox.showinfo("Success", f"✅ Account created successfully for {name}!\nPlease sign in.")
        self.show_login()
    
    # ==================== DASHBOARD ====================
    def show_dashboard(self):
        self.current_page = 'dashboard'
        self.clear_container()
        
        # Header with logo and nav
        header = tk.Frame(self.main_container, bg='#ffffff', height=80)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(header, bg='#ffffff')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#ffffff')
        logo_text.pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(header, bg='#ffffff')
        user_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(user_frame, text=f"👤 {self.current_user}", font=('Segoe UI', 11, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(user_frame, text="Logout", font=('Segoe UI', 10, 'bold'),
                             bg='#dc2626', fg='white', relief='flat', padx=15, pady=5,
                             cursor='hand2', command=self.logout)
        logout_btn.pack(side=tk.LEFT, padx=5)
        
        # Navigation
        nav_frame = tk.Frame(header, bg='#f1f5f9', relief='flat', bd=0)
        nav_frame.pack(side=tk.LEFT, padx=30)
        nav_frame.config(highlightthickness=0)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Check-in Patient", self.show_checkin),
            ("🎫 Queue Management", self.show_queue_management),
            ("👨‍⚕️ Doctors", self.show_doctors)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 11, 'bold'),
                          bg='white' if i == 0 else '#f1f5f9', 
                          fg='#0b1e3a' if i == 0 else '#475569',
                          relief='flat', bd=0, padx=20, pady=8, cursor='hand2',
                          activebackground='#e5e9f0',
                          command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Stats cards
        stats_frame = tk.Frame(self.main_container, bg='#f4f7fc')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        waiting = len([p for p in self.queue if p["status"] == "Waiting"])
        in_progress = len([p for p in self.queue if p["status"] == "In Progress"])
        completed = len([p for p in self.queue if p["status"] == "Completed"])
        total = len(self.queue)
        
        stats_data = [
            {"label": "Total Patients", "value": str(total), "icon": "👥", "color": "#2563eb"},
            {"label": "Waiting", "value": str(waiting), "icon": "⏳", "color": "#eab308"},
            {"label": "In Progress", "value": str(in_progress), "icon": "🔄", "color": "#2563eb"},
            {"label": "Completed Today", "value": str(completed), "icon": "✅", "color": "#22c55e"}
        ]
        
        for stat in stats_data:
            card = self.create_rounded_frame(stats_frame, bg='#f8fafc')
            card.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            
            inner = tk.Frame(card, bg='#f8fafc')
            inner.pack(fill=tk.X, padx=20, pady=15)
            
            info = tk.Frame(inner, bg='#f8fafc')
            info.pack(side=tk.LEFT)
            
            tk.Label(info, text=stat['label'], font=('Segoe UI', 10), fg='#64748b', 
                    bg='#f8fafc').pack(anchor='w')
            tk.Label(info, text=stat['value'], font=('Segoe UI', 28, 'bold'), 
                    fg=stat['color'], bg='#f8fafc').pack(anchor='w')
            
            icon = tk.Label(inner, text=stat['icon'], font=('Segoe UI', 28), 
                          bg='#f8fafc')
            icon.pack(side=tk.RIGHT)
        
        # Main content - 3 columns with fixed proportions
        main_content = tk.Frame(self.main_container, bg='#f4f7fc')
        main_content.pack(fill=tk.BOTH, expand=True)
        
        # Column 1: Now Serving (25% width)
        col1 = tk.Frame(main_content, bg='#f4f7fc')
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        col1.pack_propagate(False)
        col1.config(width=320)
        
        serving_panel = self.create_rounded_frame(col1, bg='#ffffff')
        serving_panel.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(serving_panel, text="🔄 Now Serving", font=('Segoe UI', 14, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(anchor='w', padx=20, pady=(15, 10))
        
        # Current serving display - fixed height with proper centering
        serving_display = tk.Frame(serving_panel, bg='#dbeafe', height=150)
        serving_display.pack(fill=tk.X, padx=20, pady=10)
        serving_display.pack_propagate(False)
        
        current = next((p for p in self.queue if p["status"] == "In Progress"), None)
        
        if current:
            # Patient info container
            info_container = tk.Frame(serving_display, bg='#dbeafe')
            info_container.pack(expand=True, fill=tk.BOTH)
            
            tk.Label(info_container, text=f"🎫 {current['ticket']}", 
                    font=('Segoe UI', 36, 'bold'), fg='#1d4ed8', bg='#dbeafe').pack(pady=(10, 0))
            tk.Label(info_container, text=current['name'], 
                    font=('Segoe UI', 18, 'bold'), fg='#0b1e3a', bg='#dbeafe').pack()
            tk.Label(info_container, text=f"👨‍⚕️ {current['doctor']} · {current['department']}", 
                    font=('Segoe UI', 13), fg='#475569', bg='#dbeafe').pack()
            tk.Label(info_container, text=f"Priority: {current['priority']}", 
                    font=('Segoe UI', 11), fg='#64748b', bg='#dbeafe').pack()
        else:
            # No one serving - properly centered
            empty_container = tk.Frame(serving_display, bg='#dbeafe')
            empty_container.pack(expand=True, fill=tk.BOTH)
            
            tk.Label(empty_container, text="⏳", 
                    font=('Segoe UI', 48), fg='#94a3b8', bg='#dbeafe').pack(pady=(5, 0))
            tk.Label(empty_container, text="No one currently", 
                    font=('Segoe UI', 18, 'bold'), fg='#64748b', bg='#dbeafe').pack()
            tk.Label(empty_container, text="being served", 
                    font=('Segoe UI', 18, 'bold'), fg='#64748b', bg='#dbeafe').pack()
        
        # Quick actions
        actions_frame = tk.Frame(serving_panel, bg='#ffffff')
        actions_frame.pack(fill=tk.X, padx=20, pady=(15, 20))
        
        next_btn = tk.Button(actions_frame, text="▶ Next Patient", font=('Segoe UI', 11, 'bold'),
                           bg='#2563eb', fg='white', relief='flat', padx=20, pady=8,
                           cursor='hand2', command=self.next_patient)
        next_btn.pack(side=tk.LEFT, padx=5)
        
        complete_btn = tk.Button(actions_frame, text="✅ Complete", font=('Segoe UI', 11, 'bold'),
                               bg='#22c55e', fg='white', relief='flat', padx=20, pady=8,
                               cursor='hand2', command=self.complete_current)
        complete_btn.pack(side=tk.LEFT, padx=5)
        
        # Column 2: Queue List (50% width)
        col2 = tk.Frame(main_content, bg='#f4f7fc')
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10))
        
        queue_panel = self.create_rounded_frame(col2, bg='#ffffff')
        queue_panel.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(queue_panel, text="🎫 Queue List", font=('Segoe UI', 14, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(anchor='w', padx=20, pady=(15, 10))
        
        # Queue list with scrollbar
        queue_frame = tk.Frame(queue_panel, bg='#ffffff')
        queue_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        canvas = tk.Canvas(queue_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = tk.Scrollbar(queue_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display queue items
        self.update_queue_list()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Column 3: Doctor Status (25% width)
        col3 = tk.Frame(main_content, bg='#f4f7fc')
        col3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
        col3.pack_propagate(False)
        col3.config(width=320)
        
        doctor_panel = self.create_rounded_frame(col3, bg='#ffffff')
        doctor_panel.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(doctor_panel, text="👨‍⚕️ Doctor Status", font=('Segoe UI', 14, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(anchor='w', padx=20, pady=(15, 10))
        
        # Doctor list with scrollbar
        doc_frame = tk.Frame(doctor_panel, bg='#ffffff')
        doc_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        doc_canvas = tk.Canvas(doc_frame, bg='#ffffff', highlightthickness=0)
        doc_scrollbar = tk.Scrollbar(doc_frame, orient="vertical", command=doc_canvas.yview)
        self.doc_scrollable_frame = tk.Frame(doc_canvas, bg='#ffffff')
        
        self.doc_scrollable_frame.bind(
            "<Configure>",
            lambda e: doc_canvas.configure(scrollregion=doc_canvas.bbox("all"))
        )
        
        doc_canvas.create_window((0, 0), window=self.doc_scrollable_frame, anchor="nw")
        doc_canvas.configure(yscrollcommand=doc_scrollbar.set)
        
        # Update doctor list
        self.update_doctor_list_in_dashboard()
        
        doc_canvas.pack(side="left", fill="both", expand=True)
        doc_scrollbar.pack(side="right", fill="y")
    
    def update_queue_list(self):
        """Update the queue list display"""
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        waiting_patients = [p for p in self.queue if p["status"] in ["Waiting", "In Progress"]]
        
        if waiting_patients:
            # Sort by priority (Urgent first)
            priority_order = {"Urgent": 0, "High": 1, "Normal": 2, "Low": 3}
            waiting_patients.sort(key=lambda x: priority_order.get(x['priority'], 3))
            
            for i, patient in enumerate(waiting_patients[:20]):
                bg_color = '#f8fafc' if i % 2 == 0 else '#ffffff'
                item = tk.Frame(self.scrollable_frame, bg=bg_color)
                item.pack(fill=tk.X, pady=2, padx=5)
                
                # Priority indicator
                priority_color = self.get_priority_color(patient['priority'])
                priority_dot = tk.Frame(item, bg=priority_color, width=4, height=40)
                priority_dot.pack(side=tk.LEFT, padx=(0, 10))
                priority_dot.pack_propagate(False)
                
                # Ticket and name
                info_frame = tk.Frame(item, bg=bg_color)
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                ticket_label = tk.Label(info_frame, text=f"🎫 {patient['ticket']}", 
                                      font=('Segoe UI', 11, 'bold'), 
                                      fg='#0b1e3a', bg=bg_color)
                ticket_label.pack(anchor='w')
                
                name_label = tk.Label(info_frame, text=f"{patient['name']} - {patient['department']}", 
                                    font=('Segoe UI', 10), fg='#475569', bg=bg_color)
                name_label.pack(anchor='w')
                
                # Status badge
                status_color = self.get_status_color(patient['status'])
                status_bg = '#fef3c7' if patient['status'] == 'Waiting' else '#dbeafe'
                
                status_label = tk.Label(item, text=patient['status'], font=('Segoe UI', 9, 'bold'),
                                      fg=status_color, bg=status_bg, padx=10, pady=3)
                status_label.pack(side=tk.RIGHT, padx=5)
                
                # Priority badge
                priority_label = tk.Label(item, text=patient['priority'], font=('Segoe UI', 9, 'bold'),
                                        fg='white', bg=priority_color, padx=8, pady=3)
                priority_label.pack(side=tk.RIGHT, padx=5)
        else:
            tk.Label(self.scrollable_frame, text="No patients in queue", 
                    font=('Segoe UI', 14), fg='#94a3b8', bg='#ffffff').pack(pady=30)
    
    def update_doctor_list_in_dashboard(self):
        """Update the doctor list in dashboard"""
        # Clear existing items
        for widget in self.doc_scrollable_frame.winfo_children():
            widget.destroy()
        
        for doc in self.doctors:
            doc_frame = tk.Frame(self.doc_scrollable_frame, bg='#ffffff')
            doc_frame.pack(fill=tk.X, pady=4)
            
            # Doctor info
            info_frame = tk.Frame(doc_frame, bg='#ffffff')
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Status indicator
            status_color = '#22c55e' if doc['status'] == 'Available' else '#eab308'
            status_dot = tk.Label(info_frame, text="●", font=('Segoe UI', 14), 
                                fg=status_color, bg='#ffffff')
            status_dot.pack(side=tk.LEFT, padx=(0, 8))
            
            name_frame = tk.Frame(info_frame, bg='#ffffff')
            name_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(name_frame, text=doc['name'], font=('Segoe UI', 10, 'bold'),
                    fg='#0b1e3a', bg='#ffffff').pack(anchor='w')
            tk.Label(name_frame, text=f"{doc['specialty']} · Room {doc['room']}", 
                    font=('Segoe UI', 9), fg='#64748b', bg='#ffffff').pack(anchor='w')
            
            # Status badge
            status_bg = '#dcfce7' if doc['status'] == 'Available' else '#fef3c7'
            status_color = '#15803d' if doc['status'] == 'Available' else '#b45309'
            
            status_label = tk.Label(doc_frame, text=doc['status'], font=('Segoe UI', 8, 'bold'),
                                  fg=status_color, bg=status_bg, padx=8, pady=2)
            status_label.pack(side=tk.RIGHT)
            
            # Current patient count
            patient_count = len([p for p in self.queue if p["doctor"] == doc['name'] and p["status"] != "Completed"])
            count_label = tk.Label(doc_frame, text=f"{patient_count}", 
                                 font=('Segoe UI', 10, 'bold'), fg='#2563eb', bg='#ffffff')
            count_label.pack(side=tk.RIGHT, padx=5)
    
    def update_queue_display(self):
        """Update queue display (called by auto-refresh)"""
        if hasattr(self, 'current_page') and self.current_page == 'dashboard':
            # Only update the dynamic parts without rebuilding everything
            self.update_queue_list()
            self.update_doctor_list_in_dashboard()
            # Update the now serving display
            self.update_now_serving()
    
    def update_now_serving(self):
        """Update only the now serving display"""
        # Find the serving display frame
        serving_display = None
        for child in self.main_container.winfo_children():
            if isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Frame) and subchild.winfo_children():
                        # Check if this is the serving panel
                        for grandchild in subchild.winfo_children():
                            if isinstance(grandchild, tk.Frame) and grandchild.winfo_children():
                                # Look for the blue serving display
                                if grandchild.winfo_children() and grandchild.winfo_children()[0].winfo_class() == 'Frame':
                                    if grandchild.cget('bg') == '#dbeafe':
                                        serving_display = grandchild
                                        break
        
        if serving_display:
            # Clear the serving display
            for widget in serving_display.winfo_children():
                widget.destroy()
            
            current = next((p for p in self.queue if p["status"] == "In Progress"), None)
            
            if current:
                info_container = tk.Frame(serving_display, bg='#dbeafe')
                info_container.pack(expand=True, fill=tk.BOTH)
                
                tk.Label(info_container, text=f"🎫 {current['ticket']}", 
                        font=('Segoe UI', 36, 'bold'), fg='#1d4ed8', bg='#dbeafe').pack(pady=(10, 0))
                tk.Label(info_container, text=current['name'], 
                        font=('Segoe UI', 18, 'bold'), fg='#0b1e3a', bg='#dbeafe').pack()
                tk.Label(info_container, text=f"👨‍⚕️ {current['doctor']} · {current['department']}", 
                        font=('Segoe UI', 13), fg='#475569', bg='#dbeafe').pack()
                tk.Label(info_container, text=f"Priority: {current['priority']}", 
                        font=('Segoe UI', 11), fg='#64748b', bg='#dbeafe').pack()
            else:
                empty_container = tk.Frame(serving_display, bg='#dbeafe')
                empty_container.pack(expand=True, fill=tk.BOTH)
                
                tk.Label(empty_container, text="⏳", 
                        font=('Segoe UI', 48), fg='#94a3b8', bg='#dbeafe').pack(pady=(5, 0))
                tk.Label(empty_container, text="No one currently", 
                        font=('Segoe UI', 18, 'bold'), fg='#64748b', bg='#dbeafe').pack()
                tk.Label(empty_container, text="being served", 
                        font=('Segoe UI', 18, 'bold'), fg='#64748b', bg='#dbeafe').pack()
    
    # ==================== CHECK-IN PATIENT ====================
    def show_checkin(self):
        self.current_page = 'checkin'
        self.clear_container()
        
        # Header with navigation
        header = tk.Frame(self.main_container, bg='#ffffff', height=80)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(header, bg='#ffffff')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue Pro", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#ffffff')
        logo_text.pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(header, bg='#ffffff')
        user_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(user_frame, text=f"👤 {self.current_user}", font=('Segoe UI', 11, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(user_frame, text="Logout", font=('Segoe UI', 10, 'bold'),
                             bg='#dc2626', fg='white', relief='flat', padx=15, pady=5,
                             cursor='hand2', command=self.logout)
        logout_btn.pack(side=tk.LEFT, padx=5)
        
        # Navigation
        nav_frame = tk.Frame(header, bg='#f1f5f9', relief='flat', bd=0)
        nav_frame.pack(side=tk.LEFT, padx=30)
        nav_frame.config(highlightthickness=0)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Check-in Patient", self.show_checkin),
            ("🎫 Queue Management", self.show_queue_management),
            ("👨‍⚕️ Doctors", self.show_doctors)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 11, 'bold'),
                          bg='white' if i == 1 else '#f1f5f9', 
                          fg='#0b1e3a' if i == 1 else '#475569',
                          relief='flat', bd=0, padx=20, pady=8, cursor='hand2',
                          activebackground='#e5e9f0',
                          command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Check-in form
        form_panel = self.create_rounded_frame(self.main_container, bg='#ffffff')
        form_panel.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Title
        title_frame = tk.Frame(form_panel, bg='#ffffff')
        title_frame.pack(fill=tk.X, padx=40, pady=(30, 10))
        
        tk.Label(title_frame, text="➕ Patient Check-in", font=('Segoe UI', 24, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(anchor='w')
        tk.Label(title_frame, text="Register a new patient to the queue", 
                font=('Segoe UI', 12), fg='#64748b', bg='#ffffff').pack(anchor='w')
        
        # Form fields - 2 columns
        fields_frame = tk.Frame(form_panel, bg='#ffffff')
        fields_frame.pack(fill=tk.BOTH, padx=40, pady=20)
        
        left_col = tk.Frame(fields_frame, bg='#ffffff')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        right_col = tk.Frame(fields_frame, bg='#ffffff')
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Left column
        tk.Label(left_col, text="Patient Name *", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_name = tk.Entry(left_col, font=('Segoe UI', 12), bg='#f8fafc',
                            relief='solid', bd=1)
        self.checkin_name.pack(fill=tk.X, pady=(0, 20), ipady=6)
        
        tk.Label(left_col, text="Phone Number", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_phone = tk.Entry(left_col, font=('Segoe UI', 12), bg='#f8fafc',
                             relief='solid', bd=1)
        self.checkin_phone.pack(fill=tk.X, pady=(0, 20), ipady=6)
        
        tk.Label(left_col, text="Priority *", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_priority = tk.StringVar(value="Normal")
        priority_dropdown = ttk.Combobox(left_col, textvariable=self.checkin_priority,
                                       values=["Urgent", "High", "Normal", "Low"],
                                       font=('Segoe UI', 12), state='readonly')
        priority_dropdown.pack(fill=tk.X, pady=(0, 20), ipady=4)
        
        # Right column
        tk.Label(right_col, text="Department *", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_department = tk.StringVar(value="Cardiology")
        dept_dropdown = ttk.Combobox(right_col, textvariable=self.checkin_department,
                                   values=["Cardiology", "Orthopedics", "Dermatology", "Neurology", 
                                          "Pediatrics", "ENT", "Ophthalmology", "General"],
                                   font=('Segoe UI', 12), state='readonly')
        dept_dropdown.pack(fill=tk.X, pady=(0, 20), ipady=4)
        
        tk.Label(right_col, text="Assigned Doctor *", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_doctor = tk.StringVar(value="Dr. Patricia Hill")
        doctor_dropdown = ttk.Combobox(right_col, textvariable=self.checkin_doctor,
                                     values=[doc["name"] for doc in self.doctors],
                                     font=('Segoe UI', 12), state='readonly')
        doctor_dropdown.pack(fill=tk.X, pady=(0, 20), ipady=4)
        
        tk.Label(right_col, text="Notes", font=('Segoe UI', 10, 'bold'),
                fg='#334155', bg='#ffffff').pack(anchor='w', pady=(0, 5))
        self.checkin_notes = tk.Entry(right_col, font=('Segoe UI', 12), bg='#f8fafc',
                             relief='solid', bd=1)
        self.checkin_notes.pack(fill=tk.X, pady=(0, 20), ipady=6)
        
        # Buttons
        btn_frame = tk.Frame(form_panel, bg='#ffffff')
        btn_frame.pack(fill=tk.X, padx=40, pady=(10, 30))
        
        checkin_btn = tk.Button(btn_frame, text="✅ Check-in Patient", 
                              font=('Segoe UI', 12, 'bold'),
                              bg='#2563eb', fg='white', relief='flat', 
                              padx=40, pady=12, cursor='hand2',
                              activebackground='#1d4ed8', activeforeground='white',
                              command=self.handle_checkin)
        checkin_btn.pack(side=tk.LEFT)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 12),
                             bg='#f1f5f9', fg='#1e293b', relief='flat',
                             padx=30, pady=12, cursor='hand2',
                             command=self.show_dashboard)
        cancel_btn.pack(side=tk.LEFT, padx=10)
    
    def handle_checkin(self):
        name = self.checkin_name.get().strip()
        phone = self.checkin_phone.get().strip()
        priority = self.checkin_priority.get()
        department = self.checkin_department.get()
        doctor = self.checkin_doctor.get()
        
        if not name:
            messagebox.showwarning("Warning", "Please enter patient name")
            return
        
        # Create new patient entry
        ticket = f"Q{self.queue_counter:04d}"
        self.queue_counter += 1
        
        patient = {
            "ticket": ticket,
            "name": name,
            "phone": phone,
            "priority": priority,
            "department": department,
            "doctor": doctor,
            "status": "Waiting",
            "time": datetime.now().strftime("%I:%M %p"),
            "wait_time": "0 min"
        }
        
        self.queue.append(patient)
        
        messagebox.showinfo("Success", f"✅ Patient {name} checked in successfully!\nTicket: {ticket}")
        self.show_dashboard()
    
    # ==================== QUEUE MANAGEMENT ====================
    def show_queue_management(self):
        self.current_page = 'queue_management'
        self.clear_container()
        
        # Header with navigation
        header = tk.Frame(self.main_container, bg='#ffffff', height=80)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg='#ffffff')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#ffffff')
        logo_text.pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(header, bg='#ffffff')
        user_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(user_frame, text=f"👤 {self.current_user}", font=('Segoe UI', 11, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(user_frame, text="Logout", font=('Segoe UI', 10, 'bold'),
                             bg='#dc2626', fg='white', relief='flat', padx=15, pady=5,
                             cursor='hand2', command=self.logout)
        logout_btn.pack(side=tk.LEFT, padx=5)
        
        nav_frame = tk.Frame(header, bg='#f1f5f9', relief='flat', bd=0)
        nav_frame.pack(side=tk.LEFT, padx=30)
        nav_frame.config(highlightthickness=0)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Check-in Patient", self.show_checkin),
            ("🎫 Queue Management", self.show_queue_management),
            ("👨‍⚕️ Doctors", self.show_doctors)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 11, 'bold'),
                          bg='white' if i == 2 else '#f1f5f9', 
                          fg='#0b1e3a' if i == 2 else '#475569',
                          relief='flat', bd=0, padx=20, pady=8, cursor='hand2',
                          activebackground='#e5e9f0',
                          command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Queue management content
        management_panel = self.create_rounded_frame(self.main_container, bg='#ffffff')
        management_panel.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Title and actions
        top_frame = tk.Frame(management_panel, bg='#ffffff')
        top_frame.pack(fill=tk.X, padx=30, pady=(20, 15))
        
        tk.Label(top_frame, text="🎫 Queue Management", font=('Segoe UI', 20, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = tk.Frame(top_frame, bg='#ffffff')
        action_frame.pack(side=tk.RIGHT)
        
        tk.Button(action_frame, text="🔄 Refresh", font=('Segoe UI', 11),
                 bg='#f1f5f9', fg='#1e293b', relief='flat', padx=20, pady=8,
                 cursor='hand2', command=self.show_queue_management).pack(side=tk.LEFT, padx=5)
        
        tk.Button(action_frame, text="🗑️ Clear Completed", font=('Segoe UI', 11),
                 bg='#dc2626', fg='white', relief='flat', padx=20, pady=8,
                 cursor='hand2', command=self.clear_completed).pack(side=tk.LEFT, padx=5)
        
        # Queue table
        table_frame = tk.Frame(management_panel, bg='#fafcff')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Create Treeview with scrollbars
        columns = ('Ticket', 'Name', 'Priority', 'Department', 'Doctor', 'Status', 'Time')
        tree_frame = tk.Frame(table_frame, bg='#fafcff')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.queue_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                     yscrollcommand=tree_scroll.set, height=15)
        self.queue_tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.queue_tree.yview)
        
        # Configure columns
        for col in columns:
            self.queue_tree.heading(col, text=col)
            self.queue_tree.column(col, width=120)
        
        self.queue_tree.column('Ticket', width=80)
        self.queue_tree.column('Name', width=150)
        self.queue_tree.column('Priority', width=100)
        self.queue_tree.column('Department', width=120)
        self.queue_tree.column('Doctor', width=150)
        self.queue_tree.column('Status', width=120)
        self.queue_tree.column('Time', width=80)
        
        # Insert data
        self.update_queue_tree()
        
        # Right-click menu for actions
        def show_context_menu(event):
            item = self.queue_tree.selection()
            if not item:
                return
            
            menu = tk.Menu(self.queue_tree, tearoff=0)
            menu.add_command(label="Mark as In Progress", 
                           command=lambda: self.update_patient_status(item, "In Progress"))
            menu.add_command(label="Complete", 
                           command=lambda: self.update_patient_status(item, "Completed"))
            menu.add_command(label="Cancel", 
                           command=lambda: self.update_patient_status(item, "Cancelled"))
            menu.add_separator()
            menu.add_command(label="Remove from Queue", 
                           command=lambda: self.remove_patient(item))
            menu.post(event.x_root, event.y_root)
        
        self.queue_tree.bind("<Button-3>", show_context_menu)
    
    def update_queue_tree(self):
        """Update the queue treeview"""
        # Clear existing items
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # Insert data
        for patient in self.queue:
            tags = ()
            if patient['priority'] == 'Urgent':
                tags = ('urgent',)
            elif patient['priority'] == 'High':
                tags = ('high',)
            
            self.queue_tree.insert('', tk.END, values=(
                patient['ticket'],
                patient['name'],
                patient['priority'],
                patient['department'],
                patient['doctor'],
                patient['status'],
                patient['time']
            ), tags=tags)
        
        # Color tags
        self.queue_tree.tag_configure('urgent', background='#fee2e2')
        self.queue_tree.tag_configure('high', background='#fef3c7')
    
    def update_patient_status(self, item, status):
        """Update patient status from queue management"""
        values = self.queue_tree.item(item, 'values')
        ticket = values[0]
        
        for patient in self.queue:
            if patient['ticket'] == ticket:
                patient['status'] = status
                break
        
        self.update_queue_tree()
        self.update_queue_display()
    
    def remove_patient(self, item):
        """Remove patient from queue"""
        if messagebox.askyesno("Confirm", "Remove this patient from the queue?"):
            values = self.queue_tree.item(item, 'values')
            ticket = values[0]
            
            self.queue = [p for p in self.queue if p['ticket'] != ticket]
            self.update_queue_tree()
            self.update_queue_display()
    
    def clear_completed(self):
        """Clear all completed patients"""
        if messagebox.askyesno("Confirm", "Remove all completed patients from the queue?"):
            self.queue = [p for p in self.queue if p['status'] != 'Completed']
            self.update_queue_tree()
            self.update_queue_display()
    
    # ==================== DOCTORS PAGE ====================
    def show_doctors(self):
        self.current_page = 'doctors'
        self.clear_container()
        
        # Header
        header = tk.Frame(self.main_container, bg='#ffffff', height=80)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        logo_frame = tk.Frame(header, bg='#ffffff')
        logo_frame.pack(side=tk.LEFT, padx=10)
        
        icon_bg = tk.Frame(logo_frame, bg='#2563eb', width=44, height=44)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        logo_icon = tk.Label(icon_bg, text="🏥", font=('Segoe UI', 22), bg='#2563eb', fg='white')
        logo_icon.pack(expand=True)
        
        logo_text = tk.Label(logo_frame, text="ClinicQueue Pro", font=('Segoe UI', 22, 'bold'), 
                           fg='#0b1e3a', bg='#ffffff')
        logo_text.pack(side=tk.LEFT)
        
        # User info
        user_frame = tk.Frame(header, bg='#ffffff')
        user_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(user_frame, text=f"👤 {self.current_user}", font=('Segoe UI', 11, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(user_frame, text="Logout", font=('Segoe UI', 10, 'bold'),
                             bg='#dc2626', fg='white', relief='flat', padx=15, pady=5,
                             cursor='hand2', command=self.logout)
        logout_btn.pack(side=tk.LEFT, padx=5)
        
        nav_frame = tk.Frame(header, bg='#f1f5f9', relief='flat', bd=0)
        nav_frame.pack(side=tk.LEFT, padx=30)
        nav_frame.config(highlightthickness=0)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Check-in Patient", self.show_checkin),
            ("🎫 Queue Management", self.show_queue_management),
            ("👨‍⚕️ Doctors", self.show_doctors)
        ]
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 11, 'bold'),
                          bg='white' if i == 3 else '#f1f5f9', 
                          fg='#0b1e3a' if i == 3 else '#475569',
                          relief='flat', bd=0, padx=20, pady=8, cursor='hand2',
                          activebackground='#e5e9f0',
                          command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Doctors content
        doctors_panel = self.create_rounded_frame(self.main_container, bg='#ffffff')
        doctors_panel.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(doctors_panel, text="👨‍⚕️ Doctor Management", font=('Segoe UI', 20, 'bold'),
                fg='#0b1e3a', bg='#ffffff').pack(anchor='w', padx=30, pady=(20, 15))
        
        # Doctor cards
        cards_frame = tk.Frame(doctors_panel, bg='#ffffff')
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        for doc in self.doctors:
            card = self.create_rounded_frame(cards_frame, bg='#f8fafc')
            card.pack(fill=tk.X, pady=8)
            
            inner = tk.Frame(card, bg='#f8fafc')
            inner.pack(fill=tk.X, padx=20, pady=15)
            
            # Left: Doctor info
            info_frame = tk.Frame(inner, bg='#f8fafc')
            info_frame.pack(side=tk.LEFT)
            
            # Status indicator
            status_color = '#22c55e' if doc['status'] == 'Available' else '#eab308'
            status_dot = tk.Label(info_frame, text="●", font=('Segoe UI', 20), 
                                fg=status_color, bg='#f8fafc')
            status_dot.pack(side=tk.LEFT, padx=(0, 15))
            
            name_frame = tk.Frame(info_frame, bg='#f8fafc')
            name_frame.pack(side=tk.LEFT)
            
            tk.Label(name_frame, text=doc['name'], font=('Segoe UI', 14, 'bold'),
                    fg='#0b1e3a', bg='#f8fafc').pack(anchor='w')
            tk.Label(name_frame, text=f"{doc['specialty']} · Room {doc['room']}", 
                    font=('Segoe UI', 11), fg='#64748b', bg='#f8fafc').pack(anchor='w')
            
            # Right: Stats and actions
            right_frame = tk.Frame(inner, bg='#f8fafc')
            right_frame.pack(side=tk.RIGHT)
            
            # Count patients for this doctor
            patient_count = len([p for p in self.queue if p["doctor"] == doc['name'] and p["status"] != "Completed"])
            
            stats_frame = tk.Frame(right_frame, bg='#f8fafc')
            stats_frame.pack(side=tk.LEFT, padx=(0, 20))
            
            tk.Label(stats_frame, text=f"{patient_count}", font=('Segoe UI', 20, 'bold'),
                    fg='#2563eb', bg='#f8fafc').pack(anchor='e')
            tk.Label(stats_frame, text="Patients in queue", font=('Segoe UI', 10),
                    fg='#64748b', bg='#f8fafc').pack(anchor='e')
            
            # Status toggle button
            status_text = "Set Available" if doc['status'] == 'Busy' else "Set Busy"
            status_cmd = lambda d=doc: self.toggle_doctor_status(d)
            
            status_btn = tk.Button(right_frame, text=status_text, font=('Segoe UI', 10, 'bold'),
                                 bg='#2563eb' if doc['status'] == 'Busy' else '#eab308',
                                 fg='white', relief='flat', padx=15, pady=6,
                                 cursor='hand2', command=status_cmd)
            status_btn.pack(side=tk.LEFT)
    
    def toggle_doctor_status(self, doctor):
        """Toggle doctor status between Available and Busy"""
        doctor['status'] = 'Available' if doctor['status'] == 'Busy' else 'Busy'
        self.show_doctors()
        self.update_queue_display()
    
    # ==================== QUEUE OPERATIONS ====================
    def next_patient(self):
        """Move next waiting patient to In Progress"""
        waiting = [p for p in self.queue if p["status"] == "Waiting"]
        if not waiting:
            messagebox.showinfo("Queue Empty", "No patients waiting in queue")
            return
        
        # Prioritize urgent patients
        urgent = [p for p in waiting if p["priority"] == "Urgent"]
        if urgent:
            next_patient = urgent[0]
        else:
            next_patient = waiting[0]
        
        # Update status
        next_patient["status"] = "In Progress"
        
        # Update doctor status
        for doc in self.doctors:
            if doc["name"] == next_patient["doctor"]:
                doc["status"] = "Busy"
                break
        
        self.update_queue_display()
        messagebox.showinfo("Next Patient", f"Now serving: {next_patient['name']}\nTicket: {next_patient['ticket']}")
        self.show_dashboard()
    
    def complete_current(self):
        """Complete current patient"""
        current = next((p for p in self.queue if p["status"] == "In Progress"), None)
        if not current:
            messagebox.showinfo("No Active Patient", "No patient currently being served")
            return
        
        current["status"] = "Completed"
        
        # Update doctor status
        for doc in self.doctors:
            if doc["name"] == current["doctor"]:
                doc["status"] = "Available"
                break
        
        self.update_queue_display()
        messagebox.showinfo("Complete", f"✅ Patient {current['name']} completed!")
        self.show_dashboard()
    
    # ==================== LOGOUT ====================
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicQueueManagementSystem(root)
    root.mainloop()