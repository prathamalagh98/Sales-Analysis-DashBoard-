"""Sales Analysis Dashboard - main file (Tkinter GUI).
Run:  python app.py
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import charts
from analyzer import SalesAnalyzer
from generate_data import generate_sales_data, DATA_PATH


# ---- Apni details yahan badal lo (welcome screen par dikhengi) ----
STUDENT_NAME = "Pratham Alagh"
STUDENT_UID = "26MCC20055"
COURSE = "MCC - Python Programming Project"


class WelcomeScreen(tk.Frame):
    """Welcome / splash screen shown before the dashboard opens."""
    BG = "#0f172a"
    CARD = "#1e293b"
    ACCENT = "#3b82f6"

    def __init__(self, master, on_start):
        super().__init__(master, bg=self.BG)
        self.on_start = on_start

        # pack geometry manager: centre card
        card = tk.Frame(self, bg=self.CARD, padx=50, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="\U0001F4CA", font=("Segoe UI Emoji", 42),
                 bg=self.CARD, fg="white").pack()
        tk.Label(card, text="Sales Analysis Dashboard",
                 font=("Segoe UI", 28, "bold"), bg=self.CARD, fg="white").pack(pady=(4, 0))
        tk.Label(card, text="Explore sales trends, categories, regions and customer segments",
                 font=("Segoe UI", 11), bg=self.CARD, fg="#94a3b8").pack(pady=(4, 18))

        features = ["Monthly trend: line and area charts",
                    "Category / Region comparison: bar plots",
                    "Customer segment share: pie chart",
                    "Order distribution: histogram",
                    "Region vs Category: Seaborn heatmap"]
        for f in features:
            tk.Label(card, text="\u2713  " + f, font=("Segoe UI", 11),
                     bg=self.CARD, fg="#e2e8f0", anchor="w").pack(fill="x", pady=1)

        tk.Label(card, text="Python  |  NumPy  |  Pandas  |  Matplotlib  |  Seaborn  |  Tkinter",
                 font=("Segoe UI", 9), bg=self.CARD, fg="#64748b").pack(pady=(18, 14))

        # grid geometry manager: two buttons side by side
        row = tk.Frame(card, bg=self.CARD)
        row.pack()
        self.start_btn = tk.Button(row, text="Start Dashboard  \u2192", font=("Segoe UI", 12, "bold"),
                                   bg=self.ACCENT, fg="white", activebackground="#2563eb",
                                   activeforeground="white", relief="flat", padx=24, pady=8,
                                   cursor="hand2", command=self.on_start)
        self.start_btn.grid(row=0, column=0, padx=6)
        tk.Button(row, text="Exit", font=("Segoe UI", 12), bg="#334155", fg="white",
                  activebackground="#475569", activeforeground="white", relief="flat",
                  padx=24, pady=8, cursor="hand2",
                  command=master.destroy).grid(row=0, column=1, padx=6)

        tk.Label(card, text="Press Enter to start", font=("Segoe UI", 9),
                 bg=self.CARD, fg="#64748b").pack(pady=(10, 0))

        # place geometry manager: footer with student details
        tk.Label(self, text=f"{STUDENT_NAME}   |   {STUDENT_UID}   |   {COURSE}",
                 font=("Segoe UI", 10), bg=self.BG, fg="#94a3b8").place(relx=0.5, rely=0.96, anchor="s")

        master.bind("<Return>", self._enter)
        self.start_btn.focus_set()

    def _enter(self, event=None):
        self.on_start()


class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Analysis Dashboard")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)

        self.analyzer = SalesAnalyzer()
        self.current_chart = charts.line_chart   # function currently shown

        self._build_menu()
        self._build_filters()
        self._build_stats()
        self._build_chart_area()
        self._build_footer()
        self._bind_keys()

        self.load_file(self._ensure_default_data())

    # ------------------------------------------------------------ UI
    def _build_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open CSV...", accelerator="Ctrl+O", command=self.open_csv)
        file_menu.add_command(label="Generate Sample Data", command=self.generate_sample)
        file_menu.add_command(label="Save Chart as PNG...", accelerator="Ctrl+S", command=self.save_chart)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        chart_menu = tk.Menu(menubar, tearoff=0)
        for label, func in self._chart_options():
            chart_menu.add_command(label=label, command=lambda f=func: self.show_chart(f))
        menubar.add_cascade(label="Charts", menu=chart_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Popup (right-click) menu - Unit 3 topic
        self.popup = tk.Menu(self.root, tearoff=0)
        self.popup.add_command(label="Save Chart as PNG...", command=self.save_chart)
        self.popup.add_command(label="Reset Filters", command=self.reset_filters)

    def _chart_options(self):
        return [
            ("Line Plot (Monthly Trend)", charts.line_chart),
            ("Area Chart (Monthly Trend)", charts.area_chart),
            ("Bar Plot (by Category)", self.bar_by_category),
            ("Bar Plot (by Region)", self.bar_by_region),
            ("Pie Chart (by Segment)", lambda fig, df: charts.pie_chart(fig, df, "Segment")),
            ("Pie Chart (by Category)", lambda fig, df: charts.pie_chart(fig, df, "Category")),
            ("Histogram (Order Revenue)", charts.histogram),
            ("Heatmap (Region vs Category)", self.heatmap_all),
        ]

    def _build_filters(self):
        # grid geometry manager
        frame = ttk.LabelFrame(self.root, text="Filters")
        frame.pack(fill="x", padx=10, pady=(10, 4))

        ttk.Label(frame, text="Category:").grid(row=0, column=0, padx=6, pady=8)
        self.category_var = tk.StringVar(value="All")
        self.category_box = ttk.Combobox(frame, textvariable=self.category_var,
                                         state="readonly", width=15, values=["All"])
        self.category_box.grid(row=0, column=1, padx=6)

        ttk.Label(frame, text="Region:").grid(row=0, column=2, padx=6)
        self.region_var = tk.StringVar(value="All")
        self.region_box = ttk.Combobox(frame, textvariable=self.region_var,
                                       state="readonly", width=15, values=["All"])
        self.region_box.grid(row=0, column=3, padx=6)

        ttk.Button(frame, text="Apply", command=self.refresh).grid(row=0, column=4, padx=6)
        ttk.Button(frame, text="Reset", command=self.reset_filters).grid(row=0, column=5, padx=6)

        self.category_box.bind("<<ComboboxSelected>>", lambda e: self.refresh())
        self.region_box.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        # Chart buttons
        btns = ttk.Frame(self.root)
        btns.pack(fill="x", padx=10, pady=4)
        buttons = [
            ("Show Trend", charts.line_chart),
            ("Area Chart", charts.area_chart),
            ("Bar: Category", self.bar_by_category),
            ("Bar: Region", self.bar_by_region),
            ("Pie: Segment", lambda fig, df: charts.pie_chart(fig, df, "Segment")),
            ("Histogram", charts.histogram),
            ("Heatmap", self.heatmap_all),
        ]
        for text, func in buttons:
            ttk.Button(btns, text=text, command=lambda f=func: self.show_chart(f)).pack(side="left", padx=3)

    def _build_stats(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=4)
        self.stat_vars = {}
        for i, name in enumerate(["Total Revenue", "Avg Order", "Units Sold",
                                  "Top Category", "Top Region", "Big Orders (>=30K)"]):
            box = ttk.LabelFrame(frame, text=name)
            box.grid(row=0, column=i, padx=4, sticky="nsew")
            frame.columnconfigure(i, weight=1)
            var = tk.StringVar(value="-")
            ttk.Label(box, textvariable=var, font=("Segoe UI", 12, "bold")).pack(padx=8, pady=6)
            self.stat_vars[name] = var

    def _build_chart_area(self):
        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=4)

        self.fig = Figure(figsize=(8, 4.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        toolbar = NavigationToolbar2Tk(self.canvas, self.chart_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # right click -> popup menu
        self.canvas.get_tk_widget().bind("<Button-3>", self._show_popup)
        self.canvas.get_tk_widget().bind("<Button-2>", self._show_popup)  # macOS

    def _build_footer(self):
        # place geometry manager
        self.footer = tk.Label(self.root, text="", anchor="w", relief="sunken", bd=1)
        self.footer.pack(side="bottom", fill="x")
        self.hint = tk.Label(self.root, text="Tip: chart par right-click karke save kar sakte ho",
                             fg="gray")
        self.hint.place(relx=1.0, rely=1.0, anchor="se", x=-8, y=-3)

    def _bind_keys(self):
        self.root.bind("<Control-o>", lambda e: self.open_csv())
        self.root.bind("<Control-s>", lambda e: self.save_chart())
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    # ------------------------------------------------------------ logic
    def _ensure_default_data(self):
        if not os.path.exists(DATA_PATH):
            generate_sales_data()
        return DATA_PATH

    def load_file(self, path):
        try:
            self.analyzer.load(path)
        except Exception as exc:
            messagebox.showerror("Error", f"File load nahi ho payi:\n{exc}")
            return
        self.category_box["values"] = self.analyzer.unique_values("Category")
        self.region_box["values"] = self.analyzer.unique_values("Region")
        self.reset_filters(redraw=False)
        self.refresh()
        self.footer.config(text=f"  Loaded: {os.path.basename(path)}  |  "
                                f"Rows: {len(self.analyzer.df)}  |  "
                                f"Missing values filled (median): {self.analyzer.missing_filled}")

    def open_csv(self):
        path = filedialog.askopenfilename(title="Open sales CSV",
                                          filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            self.load_file(path)

    def generate_sample(self):
        path = generate_sales_data()
        self.load_file(path)
        messagebox.showinfo("Done", "Naya sample data ban gaya.")

    def current_df(self):
        return self.analyzer.filtered(self.category_var.get(), self.region_var.get())

    def reset_filters(self, redraw=True):
        self.category_var.set("All")
        self.region_var.set("All")
        if redraw:
            self.refresh()

    def refresh(self):
        df = self.current_df()
        a = self.analyzer
        self.stat_vars["Total Revenue"].set(f"{a.total_revenue(df):,.0f}")
        self.stat_vars["Avg Order"].set(f"{a.average_revenue(df):,.0f}")
        self.stat_vars["Units Sold"].set(f"{a.total_quantity(df):,}")
        self.stat_vars["Top Category"].set(a.best(df, "Category"))
        self.stat_vars["Top Region"].set(a.best(df, "Region"))
        count, _ = a.big_orders_total(df)
        self.stat_vars["Big Orders (>=30K)"].set(str(count))
        self.draw()

    # Bar/heatmap charts compare items, so they ignore their own filter
    def bar_by_category(self, fig, df):
        region = self.region_var.get()
        data = self.analyzer.filtered("All", region)
        note = "" if region == "All" else f"Region: {region}"
        charts.bar_chart(fig, data, "Category", note)

    def bar_by_region(self, fig, df):
        category = self.category_var.get()
        data = self.analyzer.filtered(category, "All")
        note = "" if category == "All" else f"Category: {category}"
        charts.bar_chart(fig, data, "Region", note)

    def heatmap_all(self, fig, df):
        charts.heatmap(fig, self.analyzer.df)

    def show_chart(self, func):
        self.current_chart = func
        self.draw()

    def draw(self):
        self.current_chart(self.fig, self.current_df())
        self.canvas.draw()

    def save_chart(self):
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG image", "*.png")])
        if path:
            self.fig.savefig(path, dpi=150)
            messagebox.showinfo("Saved", f"Chart saved:\n{path}")

    def _show_popup(self, event):
        try:
            self.popup.tk_popup(event.x_root, event.y_root)
        finally:
            self.popup.grab_release()

    def about(self):
        messagebox.showinfo("About", "Sales Analysis Dashboard\n"
                                     "Python + NumPy + Pandas + Matplotlib + Seaborn + Tkinter")


def main():
    root = tk.Tk()
    root.title("Sales Analysis Dashboard")
    root.geometry("1100x720")
    root.minsize(900, 600)

    def start():
        root.unbind("<Return>")
        welcome.destroy()
        DashboardApp(root)

    welcome = WelcomeScreen(root, on_start=start)
    welcome.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
