import tkinter as tk
from tkinter import ttk, messagebox
import math

class BusinessCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Business Calculator Pro')
        self.window.geometry('900x700')
        self.window.configure(bg='#F0F4F8')
        self.window.resizable(False, False)
        
        # Main calculator variables
        self.current_input = ''
        self.result = ''
        self.operation = ''
        self.first_number = None
        self.new_operation = True
        
        self.create_main_interface()
        
    def create_main_interface(self):
        """Create the main calculator interface"""
        # Title bar
        title_bar = tk.Frame(self.window, bg='#1E293B', height=80)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        
        tk.Label(title_bar, text='💼 Business Calculator Pro', 
                font=('Segoe UI', 20, 'bold'), 
                bg='#1E293B', fg='white').pack(pady=(15, 0))
        tk.Label(title_bar, text='Profit • Margin • Markup • Tax • ROI', 
                font=('Segoe UI', 11), 
                bg='#1E293B', fg='#94A3B8').pack()
        
        # Main content
        main_frame = tk.Frame(self.window, bg='#F0F4F8')
        main_frame.pack(expand=True, fill='both', padx=15, pady=15)
        
        # Left side - Calculator
        calc_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        calc_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Display
        display_frame = tk.Frame(calc_frame, bg='white', padx=15, pady=15)
        display_frame.pack(fill='x')
        
        self.expression_var = tk.StringVar()
        self.expression_var.set('')
        tk.Label(display_frame, textvariable=self.expression_var,
                font=('Segoe UI', 12), bg='white', fg='#64748B',
                anchor='e').pack(fill='x')
        
        self.display_var = tk.StringVar()
        self.display_var.set('0')
        tk.Label(display_frame, textvariable=self.display_var,
                font=('Segoe UI', 36, 'bold'), bg='white',
                fg='#0F172A', anchor='e', height=1).pack(fill='x')
        
        # Buttons
        self.create_calculator_buttons(calc_frame)
        
        # Right side - Business Tools
        tools_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1, width=350)
        tools_frame.pack(side='right', fill='both', expand=True)
        tools_frame.pack_propagate(False)
        
        self.create_business_tools(tools_frame)
    
    def create_calculator_buttons(self, parent):
        """Create calculator buttons"""
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        buttons = [
            ['C', '⌫', '÷', '%'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            btn_row = tk.Frame(buttons_frame, bg='white')
            btn_row.pack(expand=True, fill='both', pady=3)
            
            for j, text in enumerate(row):
                # Style
                if text in ['C', '⌫']:
                    bg, fg = '#FEF2F2', '#DC2626'
                elif text in ['÷', '×', '−', '+', '=', '%']:
                    bg, fg = '#EFF6FF', '#2563EB' if text == '=' else '#1E293B'
                elif text in ['±']:
                    bg, fg = '#F1F5F9', '#1E293B'
                else:
                    bg, fg = '#FFFFFF', '#0F172A'
                
                btn = tk.Button(btn_row, text=text, font=('Segoe UI', 16, 'bold' if text == '=' else 'normal'),
                              bg=bg, fg=fg, relief='flat', borderwidth=0,
                              padx=10, pady=15, cursor='hand2',
                              command=lambda t=text: self.button_click(t))
                
                if text == '=':
                    btn.configure(bg='#2563EB', fg='white')
                    btn.bind('<Enter>', lambda e, b=btn: b.configure(bg='#1D4ED8'))
                    btn.bind('<Leave>', lambda e, b=btn: b.configure(bg='#2563EB'))
                
                btn.pack(side='left', expand=True, fill='both', padx=2)
    
    def create_business_tools(self, parent):
        """Create business tools section"""
        # Title
        tk.Label(parent, text='📊 Business Tools', 
                font=('Segoe UI', 16, 'bold'),
                bg='white', fg='#0F172A').pack(pady=(20, 10))
        
        # Notebook for tools
        notebook = ttk.Notebook(parent)
        notebook.pack(expand=True, fill='both', padx=15, pady=10)
        
        # Profit Calculator
        profit_frame = tk.Frame(notebook, bg='white')
        notebook.add(profit_frame, text='💰 Profit')
        self.create_profit_tool(profit_frame)
        
        # Margin Calculator
        margin_frame = tk.Frame(notebook, bg='white')
        notebook.add(margin_frame, text='📈 Margin')
        self.create_margin_tool(margin_frame)
        
        # Tax Calculator
        tax_frame = tk.Frame(notebook, bg='white')
        notebook.add(tax_frame, text='🧾 Tax')
        self.create_tax_tool(tax_frame)
        
        # ROI Calculator
        roi_frame = tk.Frame(notebook, bg='white')
        notebook.add(roi_frame, text='📊 ROI')
        self.create_roi_tool(roi_frame)
    
    def create_profit_tool(self, parent):
        """Create profit calculator"""
        frame = tk.Frame(parent, bg='white', padx=15, pady=15)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text='Revenue ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        revenue = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                          relief='solid', bd=1)
        revenue.pack(fill='x', pady=(0, 12), ipady=6)
        revenue.insert(0, '10000')
        
        tk.Label(frame, text='Costs ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        costs = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                        relief='solid', bd=1)
        costs.pack(fill='x', pady=(0, 12), ipady=6)
        costs.insert(0, '6500')
        
        self.profit_result = tk.Label(frame, text='', font=('Segoe UI', 12),
                                     bg='white', justify='left')
        self.profit_result.pack(pady=10)
        
        def calc_profit():
            try:
                r = float(revenue.get())
                c = float(costs.get())
                profit = r - c
                margin = (profit / r * 100) if r > 0 else 0
                
                self.profit_result.config(
                    text=f'📈 Profit: ${profit:,.2f}\n📊 Margin: {margin:.1f}%\n💹 Revenue: ${r:,.2f}',
                    fg='#0F172A'
                )
            except:
                messagebox.showerror('Error', 'Enter valid numbers')
        
        tk.Button(frame, text='Calculate Profit', command=calc_profit,
                 bg='#2563EB', fg='white', font=('Segoe UI', 11, 'bold'),
                 relief='flat', padx=20, pady=10).pack(pady=10)
    
    def create_margin_tool(self, parent):
        """Create margin calculator"""
        frame = tk.Frame(parent, bg='white', padx=15, pady=15)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text='Cost ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        cost = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                       relief='solid', bd=1)
        cost.pack(fill='x', pady=(0, 12), ipady=6)
        cost.insert(0, '100')
        
        tk.Label(frame, text='Desired Margin (%)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        margin = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                         relief='solid', bd=1)
        margin.pack(fill='x', pady=(0, 12), ipady=6)
        margin.insert(0, '40')
        
        self.margin_result = tk.Label(frame, text='', font=('Segoe UI', 12),
                                     bg='white', justify='left')
        self.margin_result.pack(pady=10)
        
        def calc_margin():
            try:
                c = float(cost.get())
                m = float(margin.get()) / 100
                
                if m >= 1:
                    messagebox.showerror('Error', 'Margin must be < 100%')
                    return
                
                price = c / (1 - m)
                markup = ((price - c) / c) * 100
                
                self.margin_result.config(
                    text=f'💰 Price: ${price:,.2f}\n📈 Markup: {markup:.1f}%\n💵 Cost: ${c:,.2f}',
                    fg='#0F172A'
                )
            except:
                messagebox.showerror('Error', 'Enter valid numbers')
        
        tk.Button(frame, text='Calculate Price', command=calc_margin,
                 bg='#2563EB', fg='white', font=('Segoe UI', 11, 'bold'),
                 relief='flat', padx=20, pady=10).pack(pady=10)
    
    def create_tax_tool(self, parent):
        """Create tax calculator"""
        frame = tk.Frame(parent, bg='white', padx=15, pady=15)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text='Amount ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        amount = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                         relief='solid', bd=1)
        amount.pack(fill='x', pady=(0, 12), ipady=6)
        amount.insert(0, '1000')
        
        tk.Label(frame, text='Tax Rate (%)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        rate = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                       relief='solid', bd=1)
        rate.pack(fill='x', pady=(0, 12), ipady=6)
        rate.insert(0, '15')
        
        self.tax_result = tk.Label(frame, text='', font=('Segoe UI', 12),
                                  bg='white', justify='left')
        self.tax_result.pack(pady=10)
        
        def calc_tax():
            try:
                a = float(amount.get())
                r = float(rate.get()) / 100
                
                tax = a * r
                total = a + tax
                
                self.tax_result.config(
                    text=f'🧾 Tax: ${tax:,.2f}\n💰 Total: ${total:,.2f}\n📊 Rate: {r*100:.1f}%',
                    fg='#0F172A'
                )
            except:
                messagebox.showerror('Error', 'Enter valid numbers')
        
        tk.Button(frame, text='Calculate Tax', command=calc_tax,
                 bg='#2563EB', fg='white', font=('Segoe UI', 11, 'bold'),
                 relief='flat', padx=20, pady=10).pack(pady=10)
    
    def create_roi_tool(self, parent):
        """Create ROI calculator"""
        frame = tk.Frame(parent, bg='white', padx=15, pady=15)
        frame.pack(expand=True, fill='both')
        
        tk.Label(frame, text='Initial Investment ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        investment = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                             relief='solid', bd=1)
        investment.pack(fill='x', pady=(0, 12), ipady=6)
        investment.insert(0, '50000')
        
        tk.Label(frame, text='Final Value ($)', font=('Segoe UI', 11),
                bg='white').pack(anchor='w', pady=(0, 5))
        final = tk.Entry(frame, font=('Segoe UI', 12), bg='#F8FAFC',
                        relief='solid', bd=1)
        final.pack(fill='x', pady=(0, 12), ipady=6)
        final.insert(0, '75000')
        
        self.roi_result = tk.Label(frame, text='', font=('Segoe UI', 12),
                                  bg='white', justify='left')
        self.roi_result.pack(pady=10)
        
        def calc_roi():
            try:
                inv = float(investment.get())
                fin = float(final.get())
                
                profit = fin - inv
                roi = (profit / inv) * 100 if inv > 0 else 0
                
                self.roi_result.config(
                    text=f'📈 ROI: {roi:.1f}%\n💰 Profit: ${profit:,.2f}\n💵 Investment: ${inv:,.2f}',
                    fg='#0F172A'
                )
            except:
                messagebox.showerror('Error', 'Enter valid numbers')
        
        tk.Button(frame, text='Calculate ROI', command=calc_roi,
                 bg='#2563EB', fg='white', font=('Segoe UI', 11, 'bold'),
                 relief='flat', padx=20, pady=10).pack(pady=10)
    
    # Calculator functions
    def button_click(self, value):
        """Handle button clicks"""
        if value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value in ['÷', '×', '−', '+']:
            self.set_operation(value)
        elif value == '=':
            self.calculate()
        elif value == '%':
            self.percentage()
        elif value == '±':
            self.negate()
        elif value == '.':
            self.add_decimal()
        else:
            self.add_number(value)
    
    def clear(self):
        self.current_input = ''
        self.expression_var.set('')
        self.display_var.set('0')
        self.first_number = None
        self.operation = ''
        self.new_operation = True
    
    def backspace(self):
        if len(self.current_input) > 0:
            self.current_input = self.current_input[:-1]
            self.display_var.set(self.current_input or '0')
    
    def add_number(self, num):
        if self.new_operation:
            self.current_input = ''
            self.new_operation = False
        
        if len(self.current_input) < 15:
            self.current_input += num
            self.display_var.set(self.current_input)
    
    def add_decimal(self):
        if '.' not in self.current_input:
            if self.current_input == '':
                self.current_input = '0'
            self.current_input += '.'
            self.display_var.set(self.current_input)
    
    def negate(self):
        if self.current_input:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
    
    def set_operation(self, op):
        if self.first_number is not None and not self.new_operation:
            self.calculate()
        
        if self.current_input:
            self.first_number = float(self.current_input)
            self.operation = op
            self.new_operation = True
            self.expression_var.set(f"{self.current_input} {op}")
    
    def calculate(self):
        if self.first_number is not None and self.current_input and not self.new_operation:
            try:
                second_number = float(self.current_input)
                
                if self.operation == '+':
                    result = self.first_number + second_number
                elif self.operation == '−':
                    result = self.first_number - second_number
                elif self.operation == '×':
                    result = self.first_number * second_number
                elif self.operation == '÷':
                    if second_number == 0:
                        messagebox.showerror('Error', 'Cannot divide by zero!')
                        self.clear()
                        return
                    result = self.first_number / second_number
                else:
                    return
                
                self.display_var.set(self.format_number(result))
                self.expression_var.set(f"{self.first_number} {self.operation} {second_number} =")
                
                self.current_input = str(result)
                self.first_number = None
                self.operation = ''
                self.new_operation = True
                
            except:
                messagebox.showerror('Error', 'Invalid calculation')
                self.clear()
    
    def percentage(self):
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                self.display_var.set(self.format_number(value))
                self.current_input = str(value)
            except:
                pass
    
    def format_number(self, num):
        if num == int(num):
            return str(int(num))
        return str(num)

if __name__ == '__main__':
    app = BusinessCalculator()
    app.window.mainloop()
    
