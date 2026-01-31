import customtkinter as ctk
from tkinter import messagebox
import database
import logic

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class WageSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Daily Wage Fair Payment System")
        self.geometry("900x600")

        # --- LAYOUT: Grid Configuration ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (Navigation) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FAIR PAY\nSYSTEM",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigation Buttons
        self.btn_add_worker = ctk.CTkButton(self.sidebar_frame, text="Add New Worker", command=self.show_add_worker)
        self.btn_add_worker.grid(row=1, column=0, padx=20, pady=10)

        self.btn_record_work = ctk.CTkButton(self.sidebar_frame, text="Record Daily Work",
                                             command=self.show_record_work)
        self.btn_record_work.grid(row=2, column=0, padx=20, pady=10)

        self.btn_payments = ctk.CTkButton(self.sidebar_frame, text="Pending Payments", command=self.show_payments)
        self.btn_payments.grid(row=3, column=0, padx=20, pady=10)

        # --- MAIN AREA (Right Side) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Initialize with "Add Worker" screen
        self.show_add_worker()

    def clear_main_frame(self):
        """Removes all widgets from the main frame before switching screens."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================
    # SCREEN 1: ADD WORKER
    # ==========================
    def show_add_worker(self):
        self.clear_main_frame()

        # Title
        title = ctk.CTkLabel(self.main_frame, text="Register New Worker", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Inputs
        self.entry_name = ctk.CTkEntry(self.main_frame, placeholder_text="Worker Name", width=300)
        self.entry_name.pack(pady=10)

        self.entry_phone = ctk.CTkEntry(self.main_frame, placeholder_text="Phone Number", width=300)
        self.entry_phone.pack(pady=10)

        # Worker Type (Radio Buttons)
        self.worker_type_var = ctk.StringVar(value="Unskilled")
        radio_frame = ctk.CTkFrame(self.main_frame)
        radio_frame.pack(pady=10)
        r1 = ctk.CTkRadioButton(radio_frame, text="Unskilled Worker", variable=self.worker_type_var, value="Unskilled")
        r1.pack(side="left", padx=10)
        r2 = ctk.CTkRadioButton(radio_frame, text="Skilled Worker", variable=self.worker_type_var, value="Skilled")
        r2.pack(side="left", padx=10)

        self.entry_rate = ctk.CTkEntry(self.main_frame, placeholder_text="Hourly Rate (₹)", width=300)
        self.entry_rate.pack(pady=10)

        # Save Button
        save_btn = ctk.CTkButton(self.main_frame, text="Save to Database", fg_color="green",
                                 command=self.save_worker_logic)
        save_btn.pack(pady=20)

    def save_worker_logic(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()
        w_type = self.worker_type_var.get()
        rate = self.entry_rate.get()

        if not name or not rate:
            messagebox.showerror("Error", "Name and Rate are required!")
            return

        try:
            # Polymorphism Logic Here: creating the object based on type
            if w_type == "Skilled":
                worker = logic.SkilledWorker(name, float(rate))
            else:
                worker = logic.UnskilledWorker(name, float(rate))

            worker.save_to_db(phone)
            messagebox.showinfo("Success", f"{name} added successfully!")
            self.show_add_worker()  # Reset form
        except ValueError:
            messagebox.showerror("Error", "Rate must be a number.")

    # ==========================
    # SCREEN 2: RECORD WORK
    # ==========================
    def show_record_work(self):
        self.clear_main_frame()

        title = ctk.CTkLabel(self.main_frame, text="Record Daily Work", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # 1. Select Worker (Dropdown)
        ctk.CTkLabel(self.main_frame, text="Select Worker ID:").pack(pady=5)

        # Fetch workers from DB for the dropdown
        conn = database.get_connection()
        workers_list = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT worker_id, name FROM workers")
            workers_list = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
            conn.close()

        self.worker_dropdown = ctk.CTkOptionMenu(self.main_frame, values=workers_list, width=300)
        self.worker_dropdown.pack(pady=10)

        # 2. Input Hours
        self.entry_hours = ctk.CTkEntry(self.main_frame, placeholder_text="Hours Worked (e.g. 9.5)", width=300)
        self.entry_hours.pack(pady=10)

        # 3. Calculate Button
        calc_btn = ctk.CTkButton(self.main_frame, text="Calculate Wage & Save", fg_color="orange",
                                 command=self.record_work_logic)
        calc_btn.pack(pady=20)

        # Label to show result
        self.result_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

    def record_work_logic(self):
        selection = self.worker_dropdown.get()
        hours = self.entry_hours.get()

        if not selection or not hours:
            messagebox.showerror("Error", "Select a worker and enter hours.")
            return

        worker_id = selection.split(" - ")[0]  # Extract ID from "1 - Amit"

        try:
            success = logic.add_work_entry(worker_id, hours)
            if success:
                self.result_label.configure(text="✅ Work Recorded! Wage Calculated Automatically.", text_color="green")
            else:
                self.result_label.configure(text="❌ Error recording work.", text_color="red")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # SCREEN 3: PENDING PAYMENTS
    # ==========================
    def show_payments(self):
        self.clear_main_frame()

        title = ctk.CTkLabel(self.main_frame, text="Pending Wages (Unpaid)", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Scrollable Frame for the list
        list_frame = ctk.CTkScrollableFrame(self.main_frame, width=500, height=300)
        list_frame.pack(pady=10)

        # Fetch pending wages
        pending_list = logic.get_pending_wages()

        if not pending_list:
            ctk.CTkLabel(list_frame, text="No pending payments!").pack()
        else:
            # Headers
            headers = ctk.CTkLabel(list_frame, text=f"{'Worker':<20} {'Date':<15} {'Amount':<10}",
                                   font=("Courier", 14, "bold"))
            headers.pack(anchor="w")

            for row in pending_list:
                name, entry_id, date, amount = row
                # Display text
                row_text = f"{name:<20} {str(date):<15} ₹{amount:<10}"

                # Row Container
                row_frame = ctk.CTkFrame(list_frame)
                row_frame.pack(fill="x", pady=2)

                lbl = ctk.CTkLabel(row_frame, text=row_text, font=("Courier", 14))
                lbl.pack(side="left", padx=10)

                # Pay Button (Placeholder for now)
                pay_btn = ctk.CTkButton(row_frame, text="Pay", width=50, height=20, fg_color="green")
                pay_btn.pack(side="right", padx=10)


# --- RUN THE APP ---
if __name__ == "__main__":
    app = WageSystemApp()
    app.mainloop()