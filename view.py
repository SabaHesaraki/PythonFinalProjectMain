import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from controller import Controller


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.controller = Controller()

        self.BG_MAIN = "#F2F7F2"
        self.BG_CARD = "#E7EFE6"
        self.PRIMARY_OLIVE = "#607254"
        self.ACCENT_MINT = "#86A789"
        self.ACCENT_WARM = "#D27D7D"
        self.TEXT_COLOR = "#2D3748"

        self.title("🌱 Saba Data Entry & Plant Management System")
        self.geometry("980x680")
        self.configure(bg=self.BG_MAIN)
        self.minsize(900, 600)

        self.selected_record_id = None
        self.logged_in_user_id = 1  # Default demo admin user ID

        self.setup_styles()
        self.show_login_window()

    def setup_styles(self):
        """Configure ttk styles with pastel olive theme."""
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview styling
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground=self.TEXT_COLOR,
            rowheight=25,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Treeview.Heading",
            background=self.PRIMARY_OLIVE,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", self.ACCENT_MINT)])

    def show_login_window(self):
        """Create a clean, focused login dialog."""
        self.login_window = tk.Toplevel(self)
        self.login_window.title("User Login")
        self.login_window.geometry("340x360")
        self.login_window.configure(bg=self.BG_MAIN)
        self.login_window.resizable(False, False)
        self.login_window.grab_set()

        # Header
        lbl_title = tk.Label(
            self.login_window,
            text="🌿 Welcome Back",
            font=("Segoe UI", 16, "bold"),
            bg=self.BG_MAIN,
            fg=self.PRIMARY_OLIVE,
        )
        lbl_title.pack(pady=(25, 5))

        lbl_sub = tk.Label(
            self.login_window,
            text="Please enter your credentials",
            font=("Segoe UI", 9),
            bg=self.BG_MAIN,
            fg="#718096",
        )
        lbl_sub.pack(pady=(0, 20))

        frame_inputs = tk.Frame(self.login_window, bg=self.BG_MAIN)
        frame_inputs.pack(padx=30, fill="x")

        # Username
        tk.Label(
            frame_inputs,
            text="Username",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_MAIN,
            fg=self.TEXT_COLOR,
        ).pack(anchor="w")
        self.entry_user = tk.Entry(
            frame_inputs, font=("Segoe UI", 10), relief="groove", bd=1
        )
        self.entry_user.pack(fill="x", pady=(2, 10), ipady=3)
        self.entry_user.insert(0, "admin")

        # Password
        tk.Label(
            frame_inputs,
            text="Password",
            font=("Segoe UI", 9, "bold"),
            bg=self.BG_MAIN,
            fg=self.TEXT_COLOR,
        ).pack(anchor="w")
        self.entry_pass = tk.Entry(
            frame_inputs,
            show="•",
            font=("Segoe UI", 10),
            relief="groove",
            bd=1,
        )
        self.entry_pass.pack(fill="x", pady=(2, 20), ipady=3)
        self.entry_pass.insert(0, "GAPGPTMASKTOKENj0xiz5uv11X1X")

        # Login button
        btn_login = tk.Button(
            self.login_window,
            text="Login",
            font=("Segoe UI", 10, "bold"),
            bg=self.PRIMARY_OLIVE,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.handle_login,
        )
        btn_login.pack(fill="x", padx=30, ipady=5)

        self.login_window.protocol("WM_DELETE_WINDOW", self.destroy)

    def handle_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        success, msg = self.controller.login(user, pwd)

        if success:
            self.login_window.destroy()
            self.build_main_gui()
        else:
            messagebox.showerror("Login Failed", msg)

    def build_main_gui(self):
        """Construct the main application layout with pastel panels."""
        self.build_menu()

        # Top Bar
        top_bar = tk.Frame(self, bg=self.PRIMARY_OLIVE, height=45)
        top_bar.pack(fill="x")

        lbl_header = tk.Label(
            top_bar,
            text="🌿 SABA DATA ENTRY APP - PLANT RECORDS",
            font=("Segoe UI", 12, "bold"),
            bg=self.PRIMARY_OLIVE,
            fg="white",
        )
        lbl_header.pack(side="left", padx=15, pady=8)


        main_frame = tk.Frame(self, bg=self.BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        left_card = tk.LabelFrame(
            main_frame,
            text=" Record Details ",
            bg=self.BG_CARD,
            fg=self.PRIMARY_OLIVE,
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=10,
        )
        left_card.pack(side="left", fill="y", padx=(0, 10))

        # Form Inputs
        self.inputs = {}
        fields = [
            ("Plot Name:", "plot_name"),
            ("Plot Location:", "plot_loc"),
            ("Plant Name:", "plant_name"),
            ("Plant Type:", "plant_type"),
            ("Soil Type:", "soil_type"),
            ("pH Level (0-14):", "ph"),
            ("Temperature (°C):", "temp"),
            ("Humidity (%):", "humidity"),
            ("Notes / Remarks:", "notes"),
        ]

        for i, (label_text, key) in enumerate(fields):
            tk.Label(
                left_card,
                text=label_text,
                font=("Segoe UI", 8, "bold"),
                bg=self.BG_CARD,
                fg=self.TEXT_COLOR,
            ).pack(anchor="w", pady=(2, 0))

            if key == "notes":
                ent = tk.Entry(left_card, font=("Segoe UI", 9), width=28)
            else:
                ent = tk.Entry(left_card, font=("Segoe UI", 9), width=28)

            ent.pack(fill="x", pady=(0, 4), ipady=2)
            self.inputs[key] = ent

        # Form Buttons
        btn_frame = tk.Frame(left_card, bg=self.BG_CARD)
        btn_frame.pack(fill="x", pady=(10, 0))

        self.btn_save = tk.Button(
            btn_frame,
            text=" Save",
            bg=self.ACCENT_MINT,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.save_data,
        )
        self.btn_save.pack(side="left", expand=True, fill="x", padx=2, ipady=4)

        self.btn_update = tk.Button(
            btn_frame,
            text=" Update",
            bg=self.PRIMARY_OLIVE,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.update_data,
        )
        self.btn_update.pack(
            side="left", expand=True, fill="x", padx=2, ipady=4
        )

        self.btn_clear = tk.Button(
            btn_frame,
            text=" Clear",
            bg="#A0AEC0",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            command=self.clear_form,
        )
        self.btn_clear.pack(
            side="left", expand=True, fill="x", padx=2, ipady=4
        )


        right_card = tk.LabelFrame(
            main_frame,
            text=" Saved Records ",
            bg=self.BG_CARD,
            fg=self.PRIMARY_OLIVE,
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
        )
        right_card.pack(side="right", fill="both", expand=True)

        # Treeview definition
        cols = (
            "id",
            "date",
            "plot",
            "loc",
            "plant",
            "type",
            "soil",
            "ph",
            "temp",
            "hum",
            "notes",
        )
        self.tree = ttk.Treeview(
            right_card, columns=cols, show="headings", selectmode="browse"
        )

        headers = {
            "id": ("ID", 35),
            "date": ("Date", 75),
            "plot": ("Plot", 80),
            "loc": ("Location", 80),
            "plant": ("Plant", 85),
            "type": ("Type", 75),
            "soil": ("Soil", 65),
            "ph": ("pH", 40),
            "temp": ("Temp", 45),
            "hum": ("Hum%", 45),
            "notes": ("Notes", 110),
        }

        for col_name, (heading_text, width) in headers.items():
            self.tree.heading(col_name, text=heading_text)
            self.tree.column(col_name, width=width, anchor="center")

        # Scrollbars
        scroll_y = ttk.Scrollbar(
            right_card, orient="vertical", command=self.tree.yview
        )
        scroll_x = ttk.Scrollbar(
            right_card, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Bottom Action Bar
        action_bar = tk.Frame(right_card, bg=self.BG_CARD)
        action_bar.pack(fill="x", pady=(10, 0))

        btn_delete = tk.Button(
            action_bar,
            text=" Delete Selected",
            bg=self.ACCENT_WARM,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.delete_data,
        )
        btn_delete.pack(side="left", padx=5, ipady=3)

        btn_refresh = tk.Button(
            action_bar,
            text="Refresh Table",
            bg=self.PRIMARY_OLIVE,
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            command=self.refresh_table,
        )
        btn_refresh.pack(side="left", padx=5, ipady=3)

        btn_open = tk.Button(
            action_bar,
            text=" Open Saved File",
            bg=self.ACCENT_MINT,
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            command=self.open_saved_file,
        )
        btn_open.pack(side="right", padx=5, ipady=3)

        self.refresh_table()

    def build_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="Export to CSV...", command=self.export_csv_dialog
        )
        file_menu.add_command(
            label="Open CSV File...", command=self.open_saved_file
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About", "Saba Data Entry App\nMVC Architecture & PostgreSQL"
            ),
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)


    def clear_form(self):

        for ent in self.inputs.values():
            ent.delete(0, tk.END)
        self.selected_record_id = None
        self.tree.selection_remove(self.tree.selection())

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]
        if not values:
            return

        self.selected_record_id = values[0]

        keys = [
            "plot_name",
            "plot_loc",
            "plant_name",
            "plant_type",
            "soil_type",
            "ph",
            "temp",
            "humidity",
            "notes",
        ]
        row_data = values[2:]

        for key, val in zip(keys, row_data):
            self.inputs[key].delete(0, tk.END)
            self.inputs[key].insert(0, str(val))

    def save_data(self):
        success, msg = self.controller.save_new_entry(
            user_id=self.logged_in_user_id,
            plot_name=self.inputs["plot_name"].get(),
            plot_loc=self.inputs["plot_loc"].get(),
            plant_name=self.inputs["plant_name"].get(),
            plant_type=self.inputs["plant_type"].get(),
            soil_type=self.inputs["soil_type"].get(),
            ph=self.inputs["ph"].get(),
            temp=self.inputs["temp"].get(),
            humidity=self.inputs["humidity"].get(),
            notes=self.inputs["notes"].get(),
        )

        if success:
            messagebox.showinfo("Success", msg)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def update_data(self):
        """Update selected record."""
        if not self.selected_record_id:
            messagebox.showwarning(
                "Warning", "Please select a record from the table first!"
            )
            return

        success, msg = self.controller.update_entry(
            record_id=self.selected_record_id,
            plot_name=self.inputs["plot_name"].get(),
            plot_loc=self.inputs["plot_loc"].get(),
            plant_name=self.inputs["plant_name"].get(),
            plant_type=self.inputs["plant_type"].get(),
            soil_type=self.inputs["soil_type"].get(),
            ph=self.inputs["ph"].get(),
            temp=self.inputs["temp"].get(),
            humidity=self.inputs["humidity"].get(),
            notes=self.inputs["notes"].get(),
        )

        if success:
            messagebox.showinfo("Updated", msg)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def delete_data(self):
        """Delete selected row from database."""
        if not self.selected_record_id:
            messagebox.showwarning(
                "Warning", "Please select a record from the table to delete!"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete record #{self.selected_record_id}?",
        )
        if confirm:
            success, msg = self.controller.delete_record(
                self.selected_record_id
            )
            if success:
                messagebox.showinfo("Deleted", msg)
                self.clear_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def refresh_table(self):
        """Reload records into the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.controller.load_table_data()
        for row in records:
            self.tree.insert("", tk.END, values=row)

    def export_csv_dialog(self):
        """Save data as CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Records to CSV",
        )
        if file_path:
            success, msg = self.controller.export_to_csv(file_path)
            if success:
                messagebox.showinfo("Exported", msg)
            else:
                messagebox.showerror("Error", msg)

    def open_saved_file(self):
        """Open an existing CSV file with default system application."""
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Open Saved CSV File",
        )
        if file_path and os.path.exists(file_path):
            os.startfile(file_path)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
