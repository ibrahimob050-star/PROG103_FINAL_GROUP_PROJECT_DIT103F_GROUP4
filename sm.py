# clinic_queue_system.py - Complete Clinic Management System with Classes
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime, timedelta
import hashlib
import random

# ==================== DATA MANAGER CLASS ====================

class DataManager:
    """Handles all data operations"""
    
    def __init__(self):
        self.users_file = 'clinic_users.json'
        self.patients_file = 'clinic_patients.json'
        self.appointments_file = 'clinic_appointments.json'
        self.queue_file = 'clinic_queue.json'
        self.doctors_file = 'clinic_doctors.json'
        
        self.default_users = {
            "users": [
                {
                    "id": "USR001",
                    "name": "Admin Doctor",
                    "email": "admin@clinic.com",
                    "password": self.hash_password("admin123"),
                    "role": "admin",
                    "department": "Administration",
                    "created": datetime.now().isoformat()
                },
                {
                    "id": "USR002",
                    "name": "Dr. Sarah Johnson",
                    "email": "doctor@clinic.com",
                    "password": self.hash_password("doctor123"),
                    "role": "doctor",
                    "department": "Cardiology",
                    "created": datetime.now().isoformat()
                },
                {
                    "id": "USR003",
                    "name": "Nurse Mary",
                    "email": "nurse@clinic.com",
                    "password": self.hash_password("nurse123"),
                    "role": "nurse",
                    "department": "Nursing",
                    "created": datetime.now().isoformat()
                },
                {
                    "id": "PAT001",
                    "name": "John Smith",
                    "email": "john@patient.com",
                    "password": self.hash_password("patient123"),
                    "role": "patient",
                    "department": "Patient",
                    "created": datetime.now().isoformat(),
                    "patient_id": "PAT001"
                }
            ]
        }
        
        self.default_doctors = {
            "doctors": [
                {
                    "id": "DOC001",
                    "name": "Dr. Sarah Johnson",
                    "specialty": "Cardiology",
                    "available": True,
                    "room": "101",
                    "schedule": {
                        "Monday": "09:00-17:00",
                        "Tuesday": "09:00-17:00",
                        "Wednesday": "09:00-17:00",
                        "Thursday": "09:00-17:00",
                        "Friday": "09:00-17:00"
                    }
                },
                {
                    "id": "DOC002",
                    "name": "Dr. Michael Chen",
                    "specialty": "Neurology",
                    "available": True,
                    "room": "202",
                    "schedule": {
                        "Monday": "08:00-16:00",
                        "Tuesday": "08:00-16:00",
                        "Wednesday": "08:00-16:00",
                        "Thursday": "08:00-16:00",
                        "Friday": "08:00-16:00"
                    }
                },
                {
                    "id": "DOC003",
                    "name": "Dr. Emily Williams",
                    "specialty": "Pediatrics",
                    "available": True,
                    "room": "303",
                    "schedule": {
                        "Monday": "10:00-18:00",
                        "Tuesday": "10:00-18:00",
                        "Wednesday": "10:00-18:00",
                        "Thursday": "10:00-18:00",
                        "Friday": "10:00-18:00"
                    }
                }
            ]
        }
        
        self.default_patients = {
            "patients": [
                {
                    "id": "PAT001",
                    "name": "John Smith",
                    "age": "45",
                    "gender": "Male",
                    "phone": "555-0101",
                    "email": "john@patient.com",
                    "address": "123 Main St",
                    "blood_type": "A+",
                    "allergies": "None",
                    "medical_history": "High blood pressure",
                    "registered_date": datetime.now().isoformat()
                },
                {
                    "id": "PAT002",
                    "name": "Mary Johnson",
                    "age": "32",
                    "gender": "Female",
                    "phone": "555-0102",
                    "email": "mary@email.com",
                    "address": "456 Oak Ave",
                    "blood_type": "O-",
                    "allergies": "Penicillin",
                    "medical_history": "Asthma",
                    "registered_date": datetime.now().isoformat()
                }
            ]
        }
        
        self.default_appointments = {
            "appointments": [
                {
                    "id": "APP001",
                    "patient_id": "PAT001",
                    "patient_name": "John Smith",
                    "doctor_id": "DOC001",
                    "doctor_name": "Dr. Sarah Johnson",
                    "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "time": "09:30",
                    "status": "Scheduled",
                    "reason": "Annual checkup",
                    "notes": ""
                }
            ]
        }
        
        self.default_queue = {
            "queue": [
                {
                    "id": "QUE001",
                    "patient_id": "PAT001",
                    "patient_name": "John Smith",
                    "doctor_id": "DOC001",
                    "doctor_name": "Dr. Sarah Johnson",
                    "priority": "Normal",
                    "status": "Waiting",
                    "arrival_time": datetime.now().isoformat(),
                    "start_time": None,
                    "end_time": None,
                    "estimated_wait": "15 min"
                }
            ]
        }
    
    def hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_data(self, filename, default_data):
        """Load data from file or create default"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except:
                return default_data.copy()
        return default_data.copy()
    
    def save_data(self, filename, data):
        """Save data to file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_users(self):
        return self.load_data(self.users_file, self.default_users)
    
    def save_users(self, users_data):
        self.save_data(self.users_file, users_data)
    
    def load_patients(self):
        return self.load_data(self.patients_file, self.default_patients)
    
    def save_patients(self, patients_data):
        self.save_data(self.patients_file, patients_data)
    
    def load_appointments(self):
        return self.load_data(self.appointments_file, self.default_appointments)
    
    def save_appointments(self, appointments_data):
        self.save_data(self.appointments_file, appointments_data)
    
    def load_queue(self):
        return self.load_data(self.queue_file, self.default_queue)
    
    def save_queue(self, queue_data):
        self.save_data(self.queue_file, queue_data)
    
    def load_doctors(self):
        return self.load_data(self.doctors_file, self.default_doctors)
    
    def save_doctors(self, doctors_data):
        self.save_data(self.doctors_file, doctors_data)
    
    def generate_id(self, prefix, existing_ids):
        """Generate unique ID with prefix"""
        max_num = 0
        for id_str in existing_ids:
            if id_str.startswith(prefix):
                try:
                    num = int(id_str[len(prefix):])
                    max_num = max(max_num, num)
                except:
                    pass
        return f"{prefix}{max_num + 1:03d}"
    
    def get_available_doctors(self):
        """Get list of available doctors"""
        doctors_data = self.load_doctors()
        return [d for d in doctors_data['doctors'] if d.get('available', True)]
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        doctors_data = self.load_doctors()
        return next((d for d in doctors_data['doctors'] if d['id'] == doctor_id), None)
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        patients_data = self.load_patients()
        return next((p for p in patients_data['patients'] if p['id'] == patient_id), None)
    
    def get_patient_by_email(self, email):
        """Get patient by email"""
        patients_data = self.load_patients()
        return next((p for p in patients_data['patients'] if p['email'] == email), None)
    
    def get_patient_appointments(self, patient_id):
        """Get all appointments for a patient"""
        appointments_data = self.load_appointments()
        return [a for a in appointments_data['appointments'] if a['patient_id'] == patient_id]
    
    def get_doctor_appointments(self, doctor_id, date=None):
        """Get appointments for a doctor on a specific date"""
        appointments_data = self.load_appointments()
        appointments = [a for a in appointments_data['appointments'] if a['doctor_id'] == doctor_id]
        if date:
            appointments = [a for a in appointments if a['date'] == date]
        return appointments
    
    def check_appointment_conflict(self, doctor_id, date, time):
        """Check if appointment time conflicts with existing appointments"""
        appointments = self.get_doctor_appointments(doctor_id, date)
        for app in appointments:
            if app['time'] == time:
                return True
        return False
    
    def book_appointment(self, patient_id, doctor_id, date, time, reason, notes=""):
        """Book a new appointment"""
        appointments_data = self.load_appointments()
        existing_ids = [a['id'] for a in appointments_data['appointments']]
        app_id = self.generate_id("APP", existing_ids)
        
        patient = self.get_patient_by_id(patient_id)
        doctor = self.get_doctor_by_id(doctor_id)
        
        if not patient or not doctor:
            return None, "Patient or Doctor not found"
        
        if self.check_appointment_conflict(doctor_id, date, time):
            return None, "Time slot already booked"
        
        appointment = {
            "id": app_id,
            "patient_id": patient_id,
            "patient_name": patient['name'],
            "doctor_id": doctor_id,
            "doctor_name": doctor['name'],
            "date": date,
            "time": time,
            "status": "Scheduled",
            "reason": reason,
            "notes": notes
        }
        
        appointments_data['appointments'].append(appointment)
        self.save_appointments(appointments_data)
        return appointment, "Appointment booked successfully"

# ==================== COLOR MANAGER CLASS ====================

class ColorManager:
    """Manages application colors"""
    
    def __init__(self):
        self.colors = {
            'bg_dark': '#f0f0f0',
            'bg_medium': '#e8e8e8',
            'bg_light': '#ffffff',
            'card': '#ffffff',
            'text': '#1a1a1a',
            'text_secondary': '#555555',
            'primary': '#2563eb',
            'primary_light': '#3b82f6',
            'secondary': '#059669',
            'success': '#059669',
            'danger': '#dc2626',
            'warning': '#d97706',
            'gold': '#d97706',
            'border': '#d1d5db',
            'purple': '#7c3aed',
            'pink': '#db2777',
            'indigo': '#4f46e5',
            'queue_waiting': '#f59e0b',
            'queue_in_progress': '#3b82f6',
            'queue_completed': '#10b981'
        }
    
    def get(self, key):
        return self.colors.get(key, '#ffffff')

# ==================== APP CLASS ====================

class ClinicApp:
    """Main Application Class"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Clinic Queue Pro - Advanced Patient Management System")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg='#f0f0f0')
        
        self.data = DataManager()
        self.colors = ColorManager()
        self.current_user = None
        self.current_page = None
        self.pages = {}
        self.nav_buttons = {}
        self.page_title = None
        
        # Ensure data files exist
        self.initialize_data()
        
        self.show_login()
        self.root.mainloop()
    
    def initialize_data(self):
        """Initialize data files if they don't exist"""
        if not os.path.exists(self.data.users_file):
            self.data.save_users(self.data.default_users)
        if not os.path.exists(self.data.patients_file):
            self.data.save_patients(self.data.default_patients)
        if not os.path.exists(self.data.appointments_file):
            self.data.save_appointments(self.data.default_appointments)
        if not os.path.exists(self.data.queue_file):
            self.data.save_queue(self.data.default_queue)
        if not os.path.exists(self.data.doctors_file):
            self.data.save_doctors(self.data.default_doctors)
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Show login screen"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.colors.get('bg_dark'))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main card
        card = tk.Frame(main_frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=780)
        
        # Header
        header_frame = tk.Frame(card, bg=self.colors.get('card'))
        header_frame.pack(fill=tk.X, pady=(10, 5))
        
        logo_frame = tk.Frame(header_frame, bg=self.colors.get('primary'), width=45, height=45)
        logo_frame.pack(pady=3)
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, text="🏥", font=('Segoe UI', 22),
                             bg=self.colors.get('primary'), fg='white')
        logo_label.pack(expand=True)
        
        tk.Label(header_frame, text="Clinic Queue Pro",
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack()
        tk.Label(header_frame, text="Patient & Staff Management System",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack()
        
        # Tabs
        tab_frame = tk.Frame(card, bg=self.colors.get('bg_medium'), padx=5, pady=5)
        tab_frame.pack(fill=tk.X, padx=25, pady=8)
        
        login_tab = tk.Button(tab_frame, text="Staff Login", font=('Segoe UI', 9, 'bold'),
                             bg=self.colors.get('primary'), fg='white',
                             relief=tk.FLAT, cursor='hand2',
                             command=lambda: self.switch_auth('login'))
        login_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        patient_login_tab = tk.Button(tab_frame, text="Patient Login", font=('Segoe UI', 9, 'bold'),
                                     bg=self.colors.get('bg_medium'), fg=self.colors.get('text'),
                                     relief=tk.FLAT, cursor='hand2',
                                     command=lambda: self.switch_auth('patient_login'))
        patient_login_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        signup_tab = tk.Button(tab_frame, text="Patient Sign Up", font=('Segoe UI', 9, 'bold'),
                              bg=self.colors.get('bg_medium'), fg=self.colors.get('text'),
                              relief=tk.FLAT, cursor='hand2',
                              command=lambda: self.switch_auth('signup'))
        signup_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Staff Login Form
        login_form = self.create_staff_login_form(card)
        
        # Patient Login Form
        patient_login_form = self.create_patient_login_form(card)
        
        # Patient Signup Form
        signup_form = self.create_patient_signup_form(card)
        
        # Store form references for tab switching
        self.auth_forms = {
            'login': {'form': login_form, 'tab': login_tab},
            'patient_login': {'form': patient_login_form, 'tab': patient_login_tab},
            'signup': {'form': signup_form, 'tab': signup_tab}
        }
        
        info_frame = tk.Frame(card, bg=self.colors.get('card'))
        info_frame.pack(fill=tk.X, pady=3)
        
        tk.Label(info_frame, text="Staff: admin@clinic.com / admin123 | Patient: john@patient.com / patient123",
                font=('Segoe UI', 8),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack()
        tk.Label(info_frame, text="v1.0 Clinic Queue Pro",
                font=('Segoe UI', 7),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack()
    
    def create_staff_login_form(self, parent):
        """Create staff login form"""
        form = tk.Frame(parent, bg=self.colors.get('card'))
        form.pack(fill=tk.BOTH, expand=True, padx=35, pady=8)
        
        tk.Label(form, text="Staff Login",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack(pady=(3, 8))
        
        tk.Label(form, text="Email Address",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(3, 2))
        email_entry = tk.Entry(form, font=('Segoe UI', 11),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1)
        email_entry.pack(fill=tk.X, pady=(0, 10))
        email_entry.insert(0, "admin@clinic.com")
        
        tk.Label(form, text="Password",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(3, 2))
        password_entry = tk.Entry(form, font=('Segoe UI', 11),
                                 bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                                 relief=tk.SOLID, bd=1,
                                 show='•')
        password_entry.pack(fill=tk.X, pady=(0, 12))
        password_entry.insert(0, "admin123")
        
        def handle_login():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            users_data = self.data.load_users()
            user = next((u for u in users_data['users'] 
                        if u['email'] == email and u['password'] == self.data.hash_password(password) and u['role'] != 'patient'), None)
            
            if not user:
                messagebox.showerror("Login Failed", "Invalid email or password for staff")
                return
            
            self.current_user = user
            self.show_dashboard()
        
        login_btn = tk.Button(form, text="Access Dashboard",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.colors.get('primary'), fg='white',
                             relief=tk.FLAT, cursor='hand2',
                             height=2, command=handle_login)
        login_btn.pack(fill=tk.X, pady=(3, 8))
        
        return form
    
    def create_patient_login_form(self, parent):
        """Create patient login form"""
        form = tk.Frame(parent, bg=self.colors.get('card'))
        form.pack(fill=tk.BOTH, expand=True, padx=35, pady=8)
        form.pack_forget()
        
        tk.Label(form, text="Patient Login",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack(pady=(3, 8))
        
        tk.Label(form, text="Email Address",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(3, 2))
        email_entry = tk.Entry(form, font=('Segoe UI', 11),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1)
        email_entry.pack(fill=tk.X, pady=(0, 10))
        email_entry.insert(0, "john@patient.com")
        
        tk.Label(form, text="Password",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(3, 2))
        password_entry = tk.Entry(form, font=('Segoe UI', 11),
                                 bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                                 relief=tk.SOLID, bd=1,
                                 show='•')
        password_entry.pack(fill=tk.X, pady=(0, 12))
        password_entry.insert(0, "patient123")
        
        def handle_patient_login():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            users_data = self.data.load_users()
            user = next((u for u in users_data['users'] 
                        if u['email'] == email and u['password'] == self.data.hash_password(password) and u['role'] == 'patient'), None)
            
            if not user:
                messagebox.showerror("Login Failed", "Invalid email or password for patient")
                return
            
            self.current_user = user
            self.show_patient_dashboard()
        
        login_btn = tk.Button(form, text="Access Patient Portal",
                             font=('Segoe UI', 11, 'bold'),
                             bg=self.colors.get('secondary'), fg='white',
                             relief=tk.FLAT, cursor='hand2',
                             height=2, command=handle_patient_login)
        login_btn.pack(fill=tk.X, pady=(3, 8))
        
        return form
    
    def create_patient_signup_form(self, parent):
        """Create patient signup form"""
        form = tk.Frame(parent, bg=self.colors.get('card'))
        form.pack(fill=tk.BOTH, expand=True, padx=35, pady=5)
        form.pack_forget()
        
        tk.Label(form, text="Patient Registration",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack(pady=(3, 6))
        
        # Full Name
        tk.Label(form, text="Full Name *",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(2, 2))
        name_entry = tk.Entry(form, font=('Segoe UI', 10),
                             bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                             relief=tk.SOLID, bd=1)
        name_entry.pack(fill=tk.X, pady=(0, 6))
        
        # Email
        tk.Label(form, text="Email Address *",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(2, 2))
        email_entry = tk.Entry(form, font=('Segoe UI', 10),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1)
        email_entry.pack(fill=tk.X, pady=(0, 6))
        
        # Phone
        tk.Label(form, text="Phone Number *",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(2, 2))
        phone_entry = tk.Entry(form, font=('Segoe UI', 10),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1)
        phone_entry.pack(fill=tk.X, pady=(0, 6))
        
        # Age and Gender
        row_frame = tk.Frame(form, bg=self.colors.get('card'))
        row_frame.pack(fill=tk.X, pady=(0, 6))
        
        age_frame = tk.Frame(row_frame, bg=self.colors.get('card'))
        age_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Label(age_frame, text="Age",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X)
        age_entry = tk.Entry(age_frame, font=('Segoe UI', 10),
                            bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                            relief=tk.SOLID, bd=1)
        age_entry.pack(fill=tk.X, pady=(2, 0))
        
        gender_frame = tk.Frame(row_frame, bg=self.colors.get('card'))
        gender_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        tk.Label(gender_frame, text="Gender",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X)
        gender_combo = ttk.Combobox(gender_frame, font=('Segoe UI', 10),
                                   values=['Male', 'Female', 'Other'],
                                   state='readonly')
        gender_combo.pack(fill=tk.X, pady=(2, 0))
        gender_combo.set('Male')
        
        # Password
        tk.Label(form, text="Password (min 6 characters) *",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(2, 2))
        password_entry = tk.Entry(form, font=('Segoe UI', 10),
                                 bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                                 relief=tk.SOLID, bd=1,
                                 show='•')
        password_entry.pack(fill=tk.X, pady=(0, 6))
        
        # Confirm Password
        tk.Label(form, text="Confirm Password *",
                font=('Segoe UI', 9),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                anchor=tk.W).pack(fill=tk.X, pady=(2, 2))
        confirm_entry = tk.Entry(form, font=('Segoe UI', 10),
                                bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                                relief=tk.SOLID, bd=1,
                                show='•')
        confirm_entry.pack(fill=tk.X, pady=(0, 10))
        
        def handle_signup():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            age = age_entry.get().strip()
            gender = gender_combo.get()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            if not all([name, email, phone, password, confirm]):
                messagebox.showerror("Error", "Name, Email, Phone, and Password are required")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return
            
            users_data = self.data.load_users()
            
            if any(u['email'] == email for u in users_data['users']):
                messagebox.showerror("Error", "Email already registered")
                return
            
            # Check if patient already exists
            patients_data = self.data.load_patients()
            existing_patient = next((p for p in patients_data['patients'] if p['email'] == email), None)
            
            if existing_patient:
                patient_id = existing_patient['id']
            else:
                existing_ids = [p['id'] for p in patients_data['patients']]
                patient_id = self.data.generate_id("PAT", existing_ids)
                
                new_patient = {
                    "id": patient_id,
                    "name": name,
                    "age": age if age else "Not specified",
                    "gender": gender,
                    "phone": phone,
                    "email": email,
                    "address": "",
                    "blood_type": "Not specified",
                    "allergies": "None",
                    "medical_history": "None",
                    "registered_date": datetime.now().isoformat()
                }
                patients_data['patients'].append(new_patient)
                self.data.save_patients(patients_data)
            
            # Create user account
            existing_ids = [u['id'] for u in users_data['users']]
            user_id = self.data.generate_id("USR", existing_ids)
            
            users_data['users'].append({
                "id": user_id,
                "name": name,
                "email": email,
                "password": self.data.hash_password(password),
                "role": "patient",
                "department": "Patient",
                "created": datetime.now().isoformat(),
                "patient_id": patient_id
            })
            self.data.save_users(users_data)
            
            messagebox.showinfo("Success", f"Patient account created!\nPatient ID: {patient_id}\nYou can now login.")
            
            # Switch to patient login
            self.switch_auth('patient_login')
            # Get the email entry from patient login form
            for child in self.auth_forms['patient_login']['form'].winfo_children():
                if isinstance(child, tk.Entry):
                    child.delete(0, tk.END)
                    child.insert(0, email)
                    break
        
        signup_btn = tk.Button(form, text="Register as Patient",
                              font=('Segoe UI', 11, 'bold'),
                              bg=self.colors.get('success'), fg='white',
                              relief=tk.FLAT, cursor='hand2',
                              height=2, command=handle_signup)
        signup_btn.pack(fill=tk.X, pady=(5, 8))
        
        # Store entries for later use
        self.signup_entries = {
            'name': name_entry,
            'email': email_entry,
            'phone': phone_entry,
            'age': age_entry,
            'gender': gender_combo,
            'password': password_entry,
            'confirm': confirm_entry
        }
        
        return form
    
    def switch_auth(self, mode):
        """Switch between auth forms"""
        for key, data in self.auth_forms.items():
            if key == mode:
                data['tab'].config(bg=self.colors.get('primary'), fg='white')
                data['form'].pack(fill=tk.BOTH, expand=True, padx=35, pady=8)
            else:
                data['tab'].config(bg=self.colors.get('bg_medium'), fg=self.colors.get('text'))
                data['form'].pack_forget()
    
    def show_dashboard(self):
        """Show staff dashboard"""
        self.clear_window()
        
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        
        main_container = tk.Frame(self.root, bg=self.colors.get('bg_dark'))
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        sidebar = self.create_sidebar(main_container, is_staff=True)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors.get('bg_dark'))
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Topbar
        topbar = tk.Frame(content_frame, bg=self.colors.get('card'), height=50, relief=tk.RAISED, bd=1)
        topbar.pack(fill=tk.X, pady=0)
        topbar.pack_propagate(False)
        
        self.page_title = tk.Label(topbar, text="Dashboard",
                                  font=('Segoe UI', 16, 'bold'),
                                  bg=self.colors.get('card'), fg=self.colors.get('text'))
        self.page_title.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Pages
        self.pages = {}
        for page in ['dashboard', 'patients', 'add_patient', 'queue', 'appointments', 'doctors', 'reports', 'users']:
            frame = tk.Frame(content_frame, bg=self.colors.get('bg_dark'))
            self.pages[page] = frame
        
        self.switch_page('dashboard')
    
    def show_patient_dashboard(self):
        """Show patient dashboard"""
        self.clear_window()
        
        self.root.geometry("1000x650")
        self.root.minsize(800, 550)
        
        main_container = tk.Frame(self.root, bg=self.colors.get('bg_dark'))
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        sidebar = self.create_sidebar(main_container, is_staff=False)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=self.colors.get('bg_dark'))
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Topbar
        topbar = tk.Frame(content_frame, bg=self.colors.get('card'), height=50, relief=tk.RAISED, bd=1)
        topbar.pack(fill=tk.X, pady=0)
        topbar.pack_propagate(False)
        
        self.page_title = tk.Label(topbar, text="Patient Dashboard",
                                  font=('Segoe UI', 16, 'bold'),
                                  bg=self.colors.get('card'), fg=self.colors.get('text'))
        self.page_title.pack(side=tk.LEFT, padx=20, pady=12)
        
        # Pages
        self.pages = {}
        for page in ['dashboard', 'appointments', 'book_appointment', 'queue', 'profile']:
            frame = tk.Frame(content_frame, bg=self.colors.get('bg_dark'))
            self.pages[page] = frame
        
        self.switch_patient_page('dashboard')
    
    def create_sidebar(self, parent, is_staff=True):
        """Create sidebar with navigation"""
        sidebar = tk.Frame(parent, bg=self.colors.get('bg_medium'), width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        header_frame = tk.Frame(sidebar, bg=self.colors.get('bg_medium'))
        header_frame.pack(fill=tk.X, pady=12)
        
        tk.Label(header_frame, text="🏥", font=('Segoe UI', 24),
                bg=self.colors.get('bg_medium'), fg=self.colors.get('primary')).pack()
        tk.Label(header_frame, text="Clinic Pro" if is_staff else "Patient Portal",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors.get('bg_medium'), fg=self.colors.get('text')).pack()
        
        nav_frame = tk.Frame(sidebar, bg=self.colors.get('bg_medium'))
        nav_frame.pack(fill=tk.X, pady=8)
        
        if is_staff:
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("👥 Patients", "patients"),
                ("➕ Add Patient", "add_patient"),
                ("🔄 Queue", "queue"),
                ("📅 Appointments", "appointments"),
                ("👨‍⚕️ Doctors", "doctors"),
                ("📈 Reports", "reports"),
                ("👤 Users", "users")
            ]
            page_switch = self.switch_page
        else:
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("📅 My Appointments", "appointments"),
                ("📝 Book Appointment", "book_appointment"),
                ("🔄 Queue Status", "queue"),
                ("👤 My Profile", "profile")
            ]
            page_switch = self.switch_patient_page
        
        self.nav_buttons = {}
        for text, page in nav_items:
            btn = tk.Button(nav_frame, text=text, font=('Segoe UI', 9),
                          bg=self.colors.get('bg_medium'), fg=self.colors.get('text'),
                          relief=tk.FLAT, anchor=tk.W, padx=15, pady=8,
                          cursor='hand2', bd=0,
                          command=lambda p=page: page_switch(p))
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[page] = btn
        
        # User info at bottom
        user_frame = tk.Frame(sidebar, bg=self.colors.get('bg_medium'))
        user_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=12)
        
        tk.Label(user_frame, text=f"👤 {self.current_user.get('name', 'User')}",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('bg_medium'), fg=self.colors.get('text')).pack()
        tk.Label(user_frame, text=self.current_user.get('role', 'staff').title(),
                font=('Segoe UI', 9),
                bg=self.colors.get('bg_medium'), fg=self.colors.get('text_secondary')).pack()
        
        logout_btn = tk.Button(user_frame, text="Logout",
                              font=('Segoe UI', 9),
                              bg=self.colors.get('danger'), fg='white',
                              relief=tk.FLAT, cursor='hand2',
                              padx=15, pady=4,
                              command=self.logout)
        logout_btn.pack(pady=8)
        
        return sidebar
    
    def switch_page(self, page):
        """Switch between staff pages"""
        for p in self.pages.values():
            p.pack_forget()
        
        if page in self.pages:
            self.pages[page].pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        page_names = {
            'dashboard': 'Dashboard',
            'patients': 'Patient Management',
            'add_patient': 'Register New Patient',
            'queue': 'Patient Queue',
            'appointments': 'Appointments',
            'doctors': 'Doctor Management',
            'reports': 'Reports & Analytics',
            'users': 'User Management'
        }
        
        for p, btn in self.nav_buttons.items():
            if p == page:
                btn.config(bg=self.colors.get('primary'), fg='white')
            else:
                btn.config(bg=self.colors.get('bg_medium'), fg=self.colors.get('text'))
        
        self.page_title.config(text=page_names.get(page, 'Dashboard'))
        
        if page == 'dashboard':
            self.render_dashboard()
        elif page == 'patients':
            self.render_patients()
        elif page == 'add_patient':
            self.render_add_patient()
        elif page == 'queue':
            self.render_queue()
        elif page == 'appointments':
            self.render_appointments()
        elif page == 'doctors':
            self.render_doctors()
        elif page == 'reports':
            self.render_reports()
        elif page == 'users':
            self.render_users()
    
    def switch_patient_page(self, page):
        """Switch between patient pages"""
        for p in self.pages.values():
            p.pack_forget()
        
        if page in self.pages:
            self.pages[page].pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        page_names = {
            'dashboard': 'Patient Dashboard',
            'appointments': 'My Appointments',
            'book_appointment': 'Book Appointment',
            'queue': 'Queue Status',
            'profile': 'My Profile'
        }
        
        for p, btn in self.nav_buttons.items():
            if p == page:
                btn.config(bg=self.colors.get('primary'), fg='white')
            else:
                btn.config(bg=self.colors.get('bg_medium'), fg=self.colors.get('text'))
        
        self.page_title.config(text=page_names.get(page, 'Patient Dashboard'))
        
        if page == 'dashboard':
            self.render_patient_dashboard()
        elif page == 'appointments':
            self.render_patient_appointments()
        elif page == 'book_appointment':
            self.render_book_appointment()
        elif page == 'queue':
            self.render_patient_queue()
        elif page == 'profile':
            self.render_patient_profile()
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login()
    
    # ==================== STAFF RENDER METHODS ====================
    
    def render_dashboard(self):
        """Render staff dashboard"""
        frame = self.pages['dashboard']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patients_data = self.data.load_patients()
        queue_data = self.data.load_queue()
        appointments_data = self.data.load_appointments()
        doctors_data = self.data.load_doctors()
        
        stats_frame = tk.Frame(frame, bg=self.colors.get('bg_dark'))
        stats_frame.pack(fill=tk.X, pady=8)
        
        waiting = len([q for q in queue_data['queue'] if q['status'] == 'Waiting'])
        in_progress = len([q for q in queue_data['queue'] if q['status'] == 'In Progress'])
        today_appointments = len([a for a in appointments_data['appointments'] 
                                if a['date'] == datetime.now().strftime("%Y-%m-%d")])
        
        stats = [
            ("Total Patients", len(patients_data['patients']), self.colors.get('primary')),
            ("Waiting", waiting, self.colors.get('warning')),
            ("In Progress", in_progress, self.colors.get('secondary')),
            ("Today's Appointments", today_appointments, self.colors.get('success'))
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.grid(row=0, column=i, padx=8, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=str(value), font=('Segoe UI', 24, 'bold'),
                    bg=self.colors.get('card'), fg=color).pack(pady=(12, 3))
            tk.Label(card, text=label, font=('Segoe UI', 10),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(pady=(0, 12))
    
    def render_patients(self):
        """Render patients page"""
        frame = self.pages['patients']
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Search bar
        search_frame = tk.Frame(frame, bg=self.colors.get('bg_dark'))
        search_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(search_frame, text="Search Patients:", font=('Segoe UI', 9),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=4)
        search_entry = tk.Entry(search_frame, font=('Segoe UI', 10),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1, width=25)
        search_entry.pack(side=tk.LEFT, padx=4)
        
        def search_patients():
            query = search_entry.get().strip().lower()
            patients_data = self.data.load_patients()
            if query:
                filtered = [p for p in patients_data['patients'] 
                           if query in p['name'].lower() or 
                              query in p['id'].lower() or
                              query in p['phone']]
            else:
                filtered = patients_data['patients']
            update_patient_table(filtered)
        
        search_btn = tk.Button(search_frame, text="Search", font=('Segoe UI', 9),
                              bg=self.colors.get('primary'), fg='white',
                              relief=tk.FLAT, cursor='hand2',
                              command=search_patients)
        search_btn.pack(side=tk.LEFT, padx=4)
        
        tk.Button(search_frame, text="➕ Add Patient", font=('Segoe UI', 9),
                 bg=self.colors.get('success'), fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=lambda: self.switch_page('add_patient')).pack(side=tk.RIGHT, padx=4)
        
        # Patient table
        table_frame = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        
        columns = ('ID', 'Name', 'Age', 'Gender', 'Phone', 'Blood Type', 'Registered')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=4)
        
        def update_patient_table(patients):
            for item in tree.get_children():
                tree.delete(item)
            
            for patient in patients:
                registered = patient.get('registered_date', '')[:10]
                tree.insert('', tk.END, values=(
                    patient['id'],
                    patient['name'],
                    patient['age'],
                    patient['gender'],
                    patient['phone'],
                    patient['blood_type'],
                    registered
                ))
        
        update_patient_table(self.data.load_patients()['patients'])
    
    def render_add_patient(self):
        """Render add patient page"""
        frame = self.pages['add_patient']
        for widget in frame.winfo_children():
            widget.destroy()
        
        form_card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        tk.Label(form_card, text="Register New Patient",
                font=('Segoe UI', 16, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack(pady=(15, 10))
        
        # Simplified form - similar to signup but for staff
        form_frame = tk.Frame(form_card, bg=self.colors.get('card'))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=8)
        
        # Create form fields (reuse from signup but without password)
        fields = {}
        field_labels = [
            ("Full Name:", "name"),
            ("Age:", "age"),
            ("Gender:", "gender"),
            ("Phone:", "phone"),
            ("Email:", "email"),
            ("Address:", "address"),
            ("Blood Type:", "blood_type")
        ]
        
        for i, (label, key) in enumerate(field_labels):
            row = tk.Frame(form_frame, bg=self.colors.get('card'))
            row.pack(fill=tk.X, pady=6)
            tk.Label(row, text=label, font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                    width=12, anchor=tk.W).pack(side=tk.LEFT)
            
            if key == 'gender':
                entry = ttk.Combobox(row, values=['Male', 'Female', 'Other'],
                                    font=('Segoe UI', 10), state='readonly')
                entry.set('Male')
            elif key == 'blood_type':
                entry = ttk.Combobox(row, values=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
                                    font=('Segoe UI', 10), state='readonly')
                entry.set('A+')
            else:
                entry = tk.Entry(row, font=('Segoe UI', 10),
                               bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                               relief=tk.SOLID, bd=1)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            fields[key] = entry
        
        def save_patient():
            data = {}
            for key, entry in fields.items():
                if isinstance(entry, ttk.Combobox):
                    data[key] = entry.get()
                else:
                    data[key] = entry.get().strip()
            
            if not data['name'] or not data['age'] or not data['phone']:
                messagebox.showerror("Error", "Name, Age, and Phone are required")
                return
            
            patients_data = self.data.load_patients()
            existing_ids = [p['id'] for p in patients_data['patients']]
            patient_id = self.data.generate_id("PAT", existing_ids)
            
            patient = {
                "id": patient_id,
                "name": data['name'],
                "age": data['age'],
                "gender": data['gender'],
                "phone": data['phone'],
                "email": data.get('email', ''),
                "address": data.get('address', ''),
                "blood_type": data['blood_type'],
                "allergies": "None",
                "medical_history": "None",
                "registered_date": datetime.now().isoformat()
            }
            
            patients_data['patients'].append(patient)
            self.data.save_patients(patients_data)
            
            messagebox.showinfo("Success", f"Patient {data['name']} registered with ID: {patient_id}")
            self.switch_page('patients')
        
        btn_frame = tk.Frame(form_card, bg=self.colors.get('card'))
        btn_frame.pack(fill=tk.X, pady=15)
        
        tk.Button(btn_frame, text="Register Patient", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors.get('success'), fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 padx=25, pady=8,
                 command=save_patient).pack(side=tk.LEFT, padx=4)
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'),
                 bg=self.colors.get('danger'), fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 padx=25, pady=8,
                 command=lambda: self.switch_page('patients')).pack(side=tk.LEFT, padx=4)
    
    def render_queue(self):
        """Render queue page"""
        frame = self.pages['queue']
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Simplified queue display - same as before but using class methods
        toolbar = tk.Frame(frame, bg=self.colors.get('bg_dark'))
        toolbar.pack(fill=tk.X, pady=8)
        
        tk.Label(toolbar, text="Patient Queue Management",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(side=tk.LEFT, padx=4)
        
        queue_data = self.data.load_queue()
        
        # Display queue entries
        for i, entry in enumerate(queue_data['queue']):
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=4)
            
            status_colors = {
                'Waiting': self.colors.get('warning'),
                'In Progress': self.colors.get('secondary'),
                'Completed': self.colors.get('success')
            }
            status_color = status_colors.get(entry['status'], self.colors.get('text_secondary'))
            
            row = tk.Frame(card, bg=self.colors.get('card'))
            row.pack(fill=tk.X, padx=12, pady=8)
            
            tk.Label(row, text=f"#{entry['id']} - {entry['patient_name']}",
                    font=('Segoe UI', 10, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT, padx=4)
            
            tk.Label(row, text=f"👨‍⚕️ {entry['doctor_name']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=10)
            
            tk.Label(row, text=f"Priority: {entry['priority']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=10)
            
            status_label = tk.Label(row, text=entry['status'], font=('Segoe UI', 9, 'bold'),
                                   bg=status_color, fg='white', padx=8, pady=2)
            status_label.pack(side=tk.RIGHT, padx=4)
    
    def render_appointments(self):
        """Render staff appointments page"""
        frame = self.pages['appointments']
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="All Appointments",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 8))
        
        appointments_data = self.data.load_appointments()
        
        if not appointments_data['appointments']:
            tk.Label(frame, text="No appointments found.",
                    font=('Segoe UI', 11),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('text_secondary')).pack(pady=30)
            return
        
        for app in appointments_data['appointments']:
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=4)
            
            status_colors = {
                'Scheduled': self.colors.get('primary'),
                'Completed': self.colors.get('success'),
                'Cancelled': self.colors.get('danger')
            }
            status_color = status_colors.get(app['status'], self.colors.get('text_secondary'))
            
            row1 = tk.Frame(card, bg=self.colors.get('card'))
            row1.pack(fill=tk.X, padx=12, pady=(8, 4))
            
            tk.Label(row1, text=f"📅 {app['date']} at {app['time']} - {app['patient_name']}",
                    font=('Segoe UI', 10, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT)
            
            tk.Label(row1, text=app['status'],
                    font=('Segoe UI', 9, 'bold'),
                    bg=status_color, fg='white',
                    padx=8, pady=2).pack(side=tk.RIGHT)
            
            row2 = tk.Frame(card, bg=self.colors.get('card'))
            row2.pack(fill=tk.X, padx=12, pady=(0, 8))
            
            tk.Label(row2, text=f"👨‍⚕️ {app['doctor_name']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=(0, 15))
            
            tk.Label(row2, text=f"📝 {app['reason']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT)
    
    def render_doctors(self):
        """Render doctors page"""
        frame = self.pages['doctors']
        for widget in frame.winfo_children():
            widget.destroy()
        
        tk.Label(frame, text="Doctor Management",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 8))
        
        doctors_data = self.data.load_doctors()
        
        for doctor in doctors_data['doctors']:
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=4)
            
            status_color = self.colors.get('success') if doctor.get('available', True) else self.colors.get('danger')
            status_text = "✅ Available" if doctor.get('available', True) else "❌ Unavailable"
            
            row = tk.Frame(card, bg=self.colors.get('card'))
            row.pack(fill=tk.X, padx=12, pady=10)
            
            tk.Label(row, text=f"👨‍⚕️ {doctor['name']}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT)
            
            tk.Label(row, text=f"Specialty: {doctor['specialty']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=15)
            
            tk.Label(row, text=f"Room: {doctor.get('room', 'N/A')}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=15)
            
            tk.Label(row, text=status_text,
                    font=('Segoe UI', 9, 'bold'),
                    bg=status_color, fg='white',
                    padx=8, pady=2).pack(side=tk.RIGHT)
    
    def render_reports(self):
        """Render reports page"""
        frame = self.pages['reports']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patients_data = self.data.load_patients()
        queue_data = self.data.load_queue()
        appointments_data = self.data.load_appointments()
        doctors_data = self.data.load_doctors()
        
        stats_frame = tk.Frame(frame, bg=self.colors.get('bg_dark'))
        stats_frame.pack(fill=tk.X, pady=8)
        
        stats = [
            ("Total Patients", len(patients_data['patients']), self.colors.get('primary')),
            ("Total Appointments", len(appointments_data['appointments']), self.colors.get('secondary')),
            ("Active Doctors", len(doctors_data['doctors']), self.colors.get('success')),
            ("Completed Visits", len([q for q in queue_data['queue'] if q['status'] == 'Completed']), self.colors.get('gold'))
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.grid(row=0, column=i, padx=8, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=str(value), font=('Segoe UI', 22, 'bold'),
                    bg=self.colors.get('card'), fg=color).pack(pady=(12, 3))
            tk.Label(card, text=label, font=('Segoe UI', 10),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(pady=(0, 12))
    
    def render_users(self):
        """Render users page"""
        frame = self.pages['users']
        for widget in frame.winfo_children():
            widget.destroy()
        
        if self.current_user['role'] != 'admin':
            tk.Label(frame, text="⚠️ Access Denied",
                    font=('Segoe UI', 22, 'bold'),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('danger')).pack(pady=30)
            return
        
        tk.Label(frame, text="User Management",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 8))
        
        users_data = self.data.load_users()
        
        for user in users_data['users']:
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=3)
            
            row = tk.Frame(card, bg=self.colors.get('card'))
            row.pack(fill=tk.X, padx=12, pady=8)
            
            tk.Label(row, text=f"{user['name']} ({user['email']})",
                    font=('Segoe UI', 10),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT)
            
            tk.Label(row, text=f"Role: {user['role'].title()}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=15)
            
            tk.Label(row, text=f"Department: {user.get('department', 'N/A')}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=15)
    
    # ==================== PATIENT RENDER METHODS ====================
    
    def render_patient_dashboard(self):
        """Render patient dashboard"""
        frame = self.pages['dashboard']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patient_id = self.current_user.get('patient_id')
        patient = self.data.get_patient_by_id(patient_id)
        
        if not patient:
            tk.Label(frame, text="Patient data not found", font=('Segoe UI', 14),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('danger')).pack(pady=30)
            return
        
        # Welcome message
        welcome = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        welcome.pack(fill=tk.X, pady=8)
        
        tk.Label(welcome, text=f"Welcome, {patient['name']}!",
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text')).pack(pady=12, padx=15, anchor=tk.W)
        tk.Label(welcome, text=f"Patient ID: {patient['id']} | Email: {patient['email']}",
                font=('Segoe UI', 10),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(pady=(0, 12), padx=15, anchor=tk.W)
        
        # Stats
        stats_frame = tk.Frame(frame, bg=self.colors.get('bg_dark'))
        stats_frame.pack(fill=tk.X, pady=15)
        
        appointments = self.data.get_patient_appointments(patient_id)
        queue_data = self.data.load_queue()
        patient_queue = [q for q in queue_data['queue'] if q['patient_id'] == patient_id]
        
        stats = [
            ("Total Appointments", len(appointments), self.colors.get('primary')),
            ("Upcoming", len([a for a in appointments if a['status'] == 'Scheduled']), self.colors.get('secondary')),
            ("Queue Status", "In Queue" if patient_queue else "Not in queue", self.colors.get('warning'))
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.grid(row=0, column=i, padx=8, sticky='nsew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            tk.Label(card, text=str(value), font=('Segoe UI', 22, 'bold'),
                    bg=self.colors.get('card'), fg=color).pack(pady=(12, 3))
            tk.Label(card, text=label, font=('Segoe UI', 10),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(pady=(0, 12))
    
    def render_patient_appointments(self):
        """Render patient appointments"""
        frame = self.pages['appointments']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patient_id = self.current_user.get('patient_id')
        
        tk.Label(frame, text="My Appointments",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 8))
        
        appointments = self.data.get_patient_appointments(patient_id)
        
        if not appointments:
            tk.Label(frame, text="No appointments found.",
                    font=('Segoe UI', 11),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('text_secondary')).pack(pady=30)
            return
        
        for app in appointments:
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=4)
            
            status_colors = {
                'Scheduled': self.colors.get('primary'),
                'Completed': self.colors.get('success'),
                'Cancelled': self.colors.get('danger')
            }
            status_color = status_colors.get(app['status'], self.colors.get('text_secondary'))
            
            row1 = tk.Frame(card, bg=self.colors.get('card'))
            row1.pack(fill=tk.X, padx=12, pady=(8, 4))
            
            tk.Label(row1, text=f"📅 {app['date']} at {app['time']}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT)
            
            tk.Label(row1, text=app['status'],
                    font=('Segoe UI', 9, 'bold'),
                    bg=status_color, fg='white',
                    padx=8, pady=2).pack(side=tk.RIGHT)
            
            row2 = tk.Frame(card, bg=self.colors.get('card'))
            row2.pack(fill=tk.X, padx=12, pady=(0, 8))
            
            tk.Label(row2, text=f"👨‍⚕️ Doctor: {app['doctor_name']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=(0, 15))
            
            tk.Label(row2, text=f"📝 Reason: {app['reason']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT)
    
    def render_book_appointment(self):
        """Render book appointment page - NEW FEATURE"""
        frame = self.pages['book_appointment']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patient_id = self.current_user.get('patient_id')
        patient = self.data.get_patient_by_id(patient_id)
        
        if not patient:
            tk.Label(frame, text="Patient data not found", font=('Segoe UI', 14),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('danger')).pack(pady=30)
            return
        
        tk.Label(frame, text="Book New Appointment",
                font=('Segoe UI', 18, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(pady=(0, 15))
        
        # Form card
        form_card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        form_card.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        form_frame = tk.Frame(form_card, bg=self.colors.get('card'))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=15)
        
        # Patient name (readonly)
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Patient:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(row, text=patient['name'], font=('Segoe UI', 10),
                bg=self.colors.get('card'), fg=self.colors.get('text'),
                anchor=tk.W).pack(side=tk.LEFT, padx=10)
        
        # Patient ID (readonly)
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Patient ID:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(row, text=patient['id'], font=('Segoe UI', 10),
                bg=self.colors.get('card'), fg=self.colors.get('text'),
                anchor=tk.W).pack(side=tk.LEFT, padx=10)
        
        # Doctor selection
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Select Doctor:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        doctors = self.data.get_available_doctors()
        doctor_names = [f"{d['id']} - {d['name']} ({d['specialty']})" for d in doctors]
        
        doctor_combo = ttk.Combobox(row, values=doctor_names,
                                   font=('Segoe UI', 10), state='readonly', width=30)
        doctor_combo.pack(side=tk.LEFT, padx=10)
        if doctor_names:
            doctor_combo.set(doctor_names[0])
        
        # Date
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Date:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        date_entry = tk.Entry(row, font=('Segoe UI', 10),
                             bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                             relief=tk.SOLID, bd=1, width=20)
        date_entry.pack(side=tk.LEFT, padx=10)
        # Set default to tomorrow
        default_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_entry.insert(0, default_date)
        
        tk.Label(row, text="(YYYY-MM-DD)", font=('Segoe UI', 8),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=5)
        
        # Time
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Time:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        time_combo = ttk.Combobox(row, values=['09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                                              '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'],
                                 font=('Segoe UI', 10), state='readonly', width=20)
        time_combo.pack(side=tk.LEFT, padx=10)
        time_combo.set('09:00')
        
        # Reason
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Reason:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        reason_entry = tk.Entry(row, font=('Segoe UI', 10),
                               bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                               relief=tk.SOLID, bd=1, width=40)
        reason_entry.pack(side=tk.LEFT, padx=10)
        reason_entry.insert(0, "General checkup")
        
        # Notes
        row = tk.Frame(form_frame, bg=self.colors.get('card'))
        row.pack(fill=tk.X, pady=8)
        tk.Label(row, text="Notes:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                width=15, anchor=tk.W).pack(side=tk.LEFT)
        
        notes_entry = tk.Entry(row, font=('Segoe UI', 10),
                              bg=self.colors.get('bg_light'), fg=self.colors.get('text'),
                              relief=tk.SOLID, bd=1, width=40)
        notes_entry.pack(side=tk.LEFT, padx=10)
        
        def book_appointment():
            doctor_str = doctor_combo.get()
            date = date_entry.get().strip()
            time = time_combo.get()
            reason = reason_entry.get().strip()
            notes = notes_entry.get().strip()
            
            if not doctor_str or not date or not time or not reason:
                messagebox.showerror("Error", "All fields are required")
                return
            
            doctor_id = doctor_str.split(' - ')[0]
            doctor = self.data.get_doctor_by_id(doctor_id)
            
            if not doctor:
                messagebox.showerror("Error", "Doctor not found")
                return
            
            # Check if doctor is available
            if not doctor.get('available', True):
                messagebox.showerror("Error", "Selected doctor is not available")
                return
            
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            
            # Check if date is in the past
            if datetime.strptime(date, "%Y-%m-%d") < datetime.now():
                if not messagebox.askyesno("Past Date", "The selected date is in the past. Continue?"):
                    return
            
            # Book appointment
            appointment, message = self.data.book_appointment(
                patient_id, doctor_id, date, time, reason, notes
            )
            
            if appointment:
                messagebox.showinfo("Success", f"Appointment booked successfully!\nID: {appointment['id']}")
                self.switch_patient_page('appointments')
            else:
                messagebox.showerror("Error", message)
        
        # Buttons
        btn_frame = tk.Frame(form_card, bg=self.colors.get('card'))
        btn_frame.pack(fill=tk.X, pady=15)
        
        tk.Button(btn_frame, text="📅 Book Appointment", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors.get('success'), fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 padx=30, pady=10,
                 command=book_appointment).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors.get('danger'), fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 padx=30, pady=10,
                 command=lambda: self.switch_patient_page('dashboard')).pack(side=tk.LEFT, padx=5)
    
    def render_patient_queue(self):
        """Render patient queue status"""
        frame = self.pages['queue']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patient_id = self.current_user.get('patient_id')
        
        tk.Label(frame, text="My Queue Status",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 8))
        
        queue_data = self.data.load_queue()
        patient_queue = [q for q in queue_data['queue'] if q['patient_id'] == patient_id]
        
        if not patient_queue:
            tk.Label(frame, text="You are not currently in the queue.",
                    font=('Segoe UI', 11),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('text_secondary')).pack(pady=30)
            return
        
        for entry in patient_queue:
            card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
            card.pack(fill=tk.X, pady=4)
            
            status_colors = {
                'Waiting': self.colors.get('warning'),
                'In Progress': self.colors.get('secondary'),
                'Completed': self.colors.get('success')
            }
            status_color = status_colors.get(entry['status'], self.colors.get('text_secondary'))
            
            row1 = tk.Frame(card, bg=self.colors.get('card'))
            row1.pack(fill=tk.X, padx=12, pady=(8, 4))
            
            tk.Label(row1, text=f"Queue ID: {entry['id']}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text')).pack(side=tk.LEFT)
            
            tk.Label(row1, text=entry['status'],
                    font=('Segoe UI', 9, 'bold'),
                    bg=status_color, fg='white',
                    padx=8, pady=2).pack(side=tk.RIGHT)
            
            row2 = tk.Frame(card, bg=self.colors.get('card'))
            row2.pack(fill=tk.X, padx=12, pady=(0, 8))
            
            tk.Label(row2, text=f"👨‍⚕️ Doctor: {entry['doctor_name']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=(0, 12))
            
            tk.Label(row2, text=f"Priority: {entry['priority']}",
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary')).pack(side=tk.LEFT, padx=(0, 12))
            
            if entry['status'] == 'Waiting':
                arrival = datetime.fromisoformat(entry['arrival_time'])
                wait_minutes = int((datetime.now() - arrival).total_seconds() / 60)
                tk.Label(row2, text=f"⏱️ Waiting: {wait_minutes} min",
                        font=('Segoe UI', 9),
                        bg=self.colors.get('card'), fg=self.colors.get('warning')).pack(side=tk.LEFT)
    
    def render_patient_profile(self):
        """Render patient profile"""
        frame = self.pages['profile']
        for widget in frame.winfo_children():
            widget.destroy()
        
        patient_id = self.current_user.get('patient_id')
        patient = self.data.get_patient_by_id(patient_id)
        
        if not patient:
            tk.Label(frame, text="Patient data not found", font=('Segoe UI', 14),
                    bg=self.colors.get('bg_dark'), fg=self.colors.get('danger')).pack(pady=30)
            return
        
        tk.Label(frame, text="My Profile",
                font=('Segoe UI', 15, 'bold'),
                bg=self.colors.get('bg_dark'), fg=self.colors.get('text')).pack(anchor=tk.W, pady=(0, 10))
        
        card = tk.Frame(frame, bg=self.colors.get('card'), relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True, pady=8)
        
        info_items = [
            ("Patient ID", patient['id']),
            ("Name", patient['name']),
            ("Age", patient['age']),
            ("Gender", patient['gender']),
            ("Phone", patient['phone']),
            ("Email", patient['email']),
            ("Blood Type", patient['blood_type']),
            ("Allergies", patient['allergies']),
            ("Medical History", patient['medical_history'])
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = tk.Frame(card, bg=self.colors.get('card'))
            row.pack(fill=tk.X, padx=15, pady=4)
            
            tk.Label(row, text=f"{label}:",
                    font=('Segoe UI', 9, 'bold'),
                    bg=self.colors.get('card'), fg=self.colors.get('text_secondary'),
                    width=14, anchor=tk.W).pack(side=tk.LEFT)
            
            tk.Label(row, text=str(value),
                    font=('Segoe UI', 9),
                    bg=self.colors.get('card'), fg=self.colors.get('text'),
                    anchor=tk.W).pack(side=tk.LEFT, padx=8)

# ==================== MAIN ====================

if __name__ == "__main__":
    app = ClinicApp()