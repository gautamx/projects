import tkinter as tk
from tkinter import ttk, messagebox
import re

class QValueCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Q-Value Calculator")
        self.geometry("500x600")
        self.configure(padx=20, pady=20)
        
        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create input section
        input_frame = ttk.LabelFrame(main_frame, text="Input")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Decimal input
        ttk.Label(input_frame, text="Decimal Value:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.decimal_value = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.decimal_value, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Q-format specifications
        format_frame = ttk.Frame(input_frame)
        format_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(format_frame, text="Q-Format:").pack(side=tk.LEFT)
        
        ttk.Label(format_frame, text="Q").pack(side=tk.LEFT)
        self.integer_bits = tk.StringVar(value="8")
        ttk.Entry(format_frame, textvariable=self.integer_bits, width=3).pack(side=tk.LEFT)
        
        ttk.Label(format_frame, text=".").pack(side=tk.LEFT)
        self.fractional_bits = tk.StringVar(value="8")
        ttk.Entry(format_frame, textvariable=self.fractional_bits, width=3).pack(side=tk.LEFT)
        
        # Calculate buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Decimal to Q-Value", command=self.decimal_to_q).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Q-Value to Decimal", command=self.q_to_decimal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Binary representation
        ttk.Label(results_frame, text="Binary Representation:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.binary_result = tk.StringVar()
        binary_entry = ttk.Entry(results_frame, textvariable=self.binary_result, width=40)
        binary_entry.grid(row=0, column=1, padx=5, pady=5)
        binary_entry.config(state="readonly")
        
        # Hexadecimal representation
        ttk.Label(results_frame, text="Hexadecimal:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.hex_result = tk.StringVar()
        hex_entry = ttk.Entry(results_frame, textvariable=self.hex_result, width=40)
        hex_entry.grid(row=1, column=1, padx=5, pady=5)
        hex_entry.config(state="readonly")
        
        # Decimal representation
        ttk.Label(results_frame, text="Decimal Value:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.decimal_result = tk.StringVar()
        decimal_entry = ttk.Entry(results_frame, textvariable=self.decimal_result, width=40)
        decimal_entry.grid(row=2, column=1, padx=5, pady=5)
        decimal_entry.config(state="readonly")
        
        # Range information
        range_frame = ttk.LabelFrame(main_frame, text="Q-Format Information")
        range_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(range_frame, text="Range:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.range_info = tk.StringVar()
        range_entry = ttk.Entry(range_frame, textvariable=self.range_info, width=40)
        range_entry.grid(row=0, column=1, padx=5, pady=5)
        range_entry.config(state="readonly")
        
        ttk.Label(range_frame, text="Resolution:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.resolution_info = tk.StringVar()
        resolution_entry = ttk.Entry(range_frame, textvariable=self.resolution_info, width=40)
        resolution_entry.grid(row=1, column=1, padx=5, pady=5)
        resolution_entry.config(state="readonly")
        
        # Instructions section
        instruction_frame = ttk.LabelFrame(main_frame, text="Instructions")
        instruction_frame.pack(fill=tk.X, pady=10)
        
        instructions = """
1. For Decimal to Q-Value conversion:
   - Enter a decimal number (e.g. 3.75 or -2.5)
   - Set the Q-format (e.g. Q8.8)
   - Click "Decimal to Q-Value"

2. For Q-Value to Decimal conversion:
   - Enter a binary or hexadecimal value
     (e.g. 0b0011110000 or 0x3C0)
   - Set the Q-format
   - Click "Q-Value to Decimal"
        """
        
        ttk.Label(instruction_frame, text=instructions, justify=tk.LEFT).pack(padx=5, pady=5)
        
        # Calculate initial range and resolution
        self.update_format_info()
        
        # Bind events to update format info when Q-format changes
        self.integer_bits.trace_add("write", lambda *args: self.update_format_info())
        self.fractional_bits.trace_add("write", lambda *args: self.update_format_info())

    def update_format_info(self):
        try:
            i_bits = int(self.integer_bits.get() or 0)
            f_bits = int(self.fractional_bits.get() or 0)
            
            total_bits = i_bits + f_bits
            
            # For signed numbers
            min_val = -(2 ** (i_bits - 1))
            max_val = (2 ** (i_bits - 1)) - (2 ** -f_bits)
            resolution = 2 ** -f_bits
            
            self.range_info.set(f"{min_val} to {max_val}")
            self.resolution_info.set(f"{resolution}")
        except ValueError:
            self.range_info.set("Invalid format")
            self.resolution_info.set("Invalid format")

    def decimal_to_q(self):
        try:
            decimal_str = self.decimal_value.get().strip()
            if not decimal_str:
                messagebox.showerror("Error", "Please enter a decimal value")
                return
                
            decimal_val = float(decimal_str)
            i_bits = int(self.integer_bits.get() or 0)
            f_bits = int(self.fractional_bits.get() or 0)
            
            total_bits = i_bits + f_bits
            
            # Check if value is within range
            min_val = -(2 ** (i_bits - 1))
            max_val = (2 ** (i_bits - 1)) - (2 ** -f_bits)
            
            if decimal_val < min_val or decimal_val > max_val:
                messagebox.showerror("Error", f"Value out of range for Q{i_bits}.{f_bits} format.\nRange: {min_val} to {max_val}")
                return
            
            # Convert to fixed-point representation
            scaled = int(decimal_val * (2 ** f_bits))
            
            # Handle negative numbers with two's complement
            if scaled < 0:
                scaled = (1 << total_bits) + scaled
                
            # Format results
            binary = bin(scaled)
            if len(binary) - 2 > total_bits:  # -2 for '0b' prefix
                binary = binary[-total_bits:]
            else:
                binary = '0b' + binary[2:].zfill(total_bits)
                
            hex_val = hex(scaled & ((1 << total_bits) - 1))
            
            self.binary_result.set(binary)
            self.hex_result.set(hex_val)
            self.decimal_result.set(str(decimal_val))
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def q_to_decimal(self):
        try:
            q_value = self.decimal_value.get().strip()
            if not q_value:
                messagebox.showerror("Error", "Please enter a binary (0b...) or hexadecimal (0x...) Q-value")
                return
                
            i_bits = int(self.integer_bits.get() or 0)
            f_bits = int(self.fractional_bits.get() or 0)
            total_bits = i_bits + f_bits
            
            # Parse the input value
            if q_value.startswith("0b"):
                int_val = int(q_value, 2)
            elif q_value.startswith("0x"):
                int_val = int(q_value, 16)
            else:
                # Try to interpret as decimal integer
                int_val = int(q_value)
                
            # Handle two's complement for signed numbers
            if int_val & (1 << (total_bits - 1)):
                int_val = int_val - (1 << total_bits)
                
            # Convert to decimal
            decimal_val = int_val / (2 ** f_bits)
            
            # Format results
            binary = bin(int_val & ((1 << total_bits) - 1))
            binary = '0b' + binary[2:].zfill(total_bits)
            
            hex_val = hex(int_val & ((1 << total_bits) - 1))
            
            self.binary_result.set(binary)
            self.hex_result.set(hex_val)
            self.decimal_result.set(str(decimal_val))
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")

    def clear_fields(self):
        self.decimal_value.set("")
        self.binary_result.set("")
        self.hex_result.set("")
        self.decimal_result.set("")

if __name__ == "__main__":
    app = QValueCalculator()
    app.mainloop()