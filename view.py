import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import style
from datetime import datetime

class LMSView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.root.title(f"{style.AppConfig.APP_NAME}")
        self.root.geometry(f"{style.AppConfig.WINDOW_WIDTH}x{style.AppConfig.WINDOW_HEIGHT}")
        self.root.configure(bg=style.AppConfig.BG_COLOR)
        self.root.resizable(False, False)
        
        self._setup_tkinter_style()
        self.show_login()

    def _setup_tkinter_style(self):
        style_obj = ttk.Style()
        style_obj.theme_use('clam')
        style_obj.configure("TFrame", background=style.AppConfig.BG_COLOR)
        style_obj.configure("Card.TFrame", background=style.AppConfig.CARD_BG, relief="flat")
        style_obj.configure("TLabel", background=style.AppConfig.BG_COLOR, font=style.AppConfig.FONT_BODY, foreground=style.AppConfig.TEXT_MAIN)
        style_obj.configure("Header.TLabel", background=style.AppConfig.SIDEBAR_COLOR, foreground="white", font=style.AppConfig.FONT_HEADER)
        style_obj.configure("TButton", font=style.AppConfig.FONT_BUTTON, borderwidth=0)
        style_obj.map("TButton", background=[('active', style.AppConfig.HOVER_COLOR)])
        style_obj.configure("TEntry", fieldbackground="white", bordercolor=style.AppConfig.PRIMARY)
        style_obj.configure("Treeview", font=style.AppConfig.FONT_BODY, rowheight=25)
        style_obj.configure("Treeview.Heading", font=style.AppConfig.FONT_BUTTON, background=style.AppConfig.BG_COLOR)

    def clear_container(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_toplevel(self, title, geometry):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(geometry)
        win.resizable(False, False) 
        win.transient(self.root)
        win.grab_set()
        win.lift()
        win.focus_force()
        win.configure(bg=style.AppConfig.BG_COLOR)
        return win

    # --- LOGIN ---
    def show_login(self):
        self.clear_container()
        container = tk.Frame(self.root, bg=style.AppConfig.BG_COLOR)
        container.pack(fill="both", expand=True)
        card = tk.Frame(container, bg=style.AppConfig.CARD_BG, padx=50, pady=50)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(card, text=f"{style.AppConfig.APP_NAME} Login", font=style.AppConfig.FONT_HEADER, 
                 bg=style.AppConfig.CARD_BG, fg=style.AppConfig.PRIMARY).pack(pady=(0, 30))
        
        tk.Label(card, text="Username", font=style.AppConfig.FONT_BODY, bg=style.AppConfig.CARD_BG, fg=style.AppConfig.TEXT_MUTED).pack(anchor="w")
        self.user_entry = ttk.Entry(card, font=style.AppConfig.FONT_BODY)
        self.user_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(card, text="Password", font=style.AppConfig.FONT_BODY, bg=style.AppConfig.CARD_BG, fg=style.AppConfig.TEXT_MUTED).pack(anchor="w")
        self.pass_entry = ttk.Entry(card, show="*", font=style.AppConfig.FONT_BODY)
        self.pass_entry.pack(fill="x", pady=(5, 25))
        
        tk.Button(card, text="LOGIN", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.PRIMARY, 
                        fg="white", activebackground=style.AppConfig.HOVER_COLOR, activeforeground="white",
                        cursor="hand2", relief="flat", height=2, command=self.attempt_login).pack(fill="x")
        self.pass_entry.bind('<Return>', lambda e: self.attempt_login())

    def attempt_login(self):
        u = self.user_entry.get()
        p = self.pass_entry.get()
        if u and p:
            if self.controller.login(u, p):
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")

    # --- DASHBOARD ---
    def show_dashboard(self):
        self.clear_container()
        user = self.controller.current_user
        role = user['role']
        
        main_container = tk.Frame(self.root, bg=style.AppConfig.BG_COLOR)
        main_container.pack(fill="both", expand=True)
        
        sidebar = tk.Frame(main_container, bg=style.AppConfig.SIDEBAR_COLOR, width=style.AppConfig.SIDEBAR_WIDTH)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text=style.AppConfig.APP_NAME, font=style.AppConfig.FONT_HEADER, 
                 bg=style.AppConfig.SIDEBAR_COLOR, fg="white").pack(pady=(40, 20))
        tk.Label(sidebar, text=f"User: {user['full_name']}", font=style.AppConfig.FONT_BODY, 
                 bg=style.AppConfig.SIDEBAR_COLOR, fg="#9CA3AF").pack(pady=(0, 40))
        
        tk.Button(sidebar, text="Logout", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.DANGER, 
                  fg="white", activebackground="#DC2626", activeforeground="white",
                  relief="flat", cursor="hand2", height=2, command=self.logout).pack(side="bottom", fill="x", padx=20, pady=40)

        content_frame = tk.Frame(main_container, bg=style.AppConfig.BG_COLOR)
        content_frame.pack(side="right", fill="both", expand=True)
        
        header = tk.Frame(content_frame, bg=style.AppConfig.BG_COLOR)
        header.pack(fill="x", padx=30, pady=30)
        tk.Label(header, text=f"{role.upper()} DASHBOARD", font=style.AppConfig.FONT_SUBHEADER, 
                 bg=style.AppConfig.BG_COLOR, fg=style.AppConfig.TEXT_MAIN).pack(anchor="w")
        
        self.content_area = tk.Frame(content_frame, bg=style.AppConfig.BG_COLOR)
        self.content_area.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        if role == 'admin': self.render_admin_view()
        elif role == 'teacher': self.render_teacher_view()
        elif role == 'student': self.render_student_view()

    def logout(self):
        self.controller.logout()
        self.show_login()

    # --- ADMIN VIEW ---
    def render_admin_view(self):
        nb = ttk.Notebook(self.content_area)
        nb.pack(fill="both", expand=True)
        
        tab1 = tk.Frame(nb, bg=style.AppConfig.BG_COLOR)
        nb.add(tab1, text="Manage Users")
        
        search_frame = tk.Frame(tab1, bg=style.AppConfig.BG_COLOR)
        search_frame.pack(fill="x", pady=10)
        tk.Label(search_frame, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        self.user_search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.user_search_var, width=20).pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=lambda: self.refresh_users(self.user_search_var.get()), bg=style.AppConfig.PRIMARY, fg="white", relief="flat").pack(side="left")
        tk.Button(search_frame, text="+ Add User", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.SUCCESS, fg="white",
                  cursor="hand2", relief="flat", command=self.popup_add_user).pack(side="right")
        
        self.tree_users = ttk.Treeview(tab1, columns=("ID", "Username", "Name", "Role"), show="headings", height=15)
        self.tree_users.heading("ID", text="ID"); self.tree_users.column("ID", width=40)
        self.tree_users.heading("Username", text="Username"); self.tree_users.column("Username", width=120)
        self.tree_users.heading("Name", text="Full Name"); self.tree_users.column("Name", width=180)
        self.tree_users.heading("Role", text="Role")
        self.tree_users.pack(fill="both", expand=True, pady=10)
        
        btn_frame = tk.Frame(tab1, bg=style.AppConfig.BG_COLOR)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Edit Selected", command=self.popup_edit_user, bg=style.AppConfig.WARNING, fg="white", relief="flat").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_user, bg=style.AppConfig.DANGER, fg="white", relief="flat").pack(side="left")
        self.refresh_users()

        tab2 = tk.Frame(nb, bg=style.AppConfig.BG_COLOR)
        nb.add(tab2, text="Manage Courses")
        
        search_frame_c = tk.Frame(tab2, bg=style.AppConfig.BG_COLOR)
        search_frame_c.pack(fill="x", pady=10)
        tk.Label(search_frame_c, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        self.course_search_var = tk.StringVar()
        tk.Entry(search_frame_c, textvariable=self.course_search_var, width=20).pack(side="left", padx=5)
        tk.Button(search_frame_c, text="Search", command=lambda: self.refresh_courses(self.course_search_var.get()), bg=style.AppConfig.PRIMARY, fg="white", relief="flat").pack(side="left")
        tk.Button(search_frame_c, text="+ Create Course", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.SUCCESS, fg="white",
                  cursor="hand2", relief="flat", command=self.popup_add_course).pack(side="right")
        tk.Button(search_frame_c, text="Enroll Students", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.PRIMARY, fg="white",
                  cursor="hand2", relief="flat", command=self.popup_enroll_students).pack(side="right", padx=5)

        self.tree_courses = ttk.Treeview(tab2, columns=("ID", "Title", "Teacher"), show="headings", height=15)
        self.tree_courses.heading("ID", text="ID"); self.tree_courses.column("ID", width=40)
        self.tree_courses.heading("Title", text="Course Title")
        self.tree_courses.heading("Teacher", text="Teacher")
        self.tree_courses.pack(fill="both", expand=True, pady=10)
        
        btn_frame_c = tk.Frame(tab2, bg=style.AppConfig.BG_COLOR)
        btn_frame_c.pack(fill="x")
        tk.Button(btn_frame_c, text="Delete Course", command=self.delete_course, bg=style.AppConfig.DANGER, fg="white", relief="flat").pack(side="left")
        self.refresh_courses()

    # --- TEACHER VIEW ---
    def render_teacher_view(self):
        paned = tk.PanedWindow(self.content_area, orient=tk.HORIZONTAL, bg=style.AppConfig.BG_COLOR)
        paned.pack(fill="both", expand=True)
        
        left_panel = tk.Frame(paned, bg=style.AppConfig.BG_COLOR)
        paned.add(left_panel, width=400)
        
        ctrl_frame = tk.Frame(left_panel, bg=style.AppConfig.CARD_BG, padx=15, pady=15)
        ctrl_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(ctrl_frame, text="Select Course:", bg=style.AppConfig.CARD_BG, font=style.AppConfig.FONT_BODY).pack(anchor="w")
        self.course_var = tk.StringVar()
        self.course_cb = ttk.Combobox(ctrl_frame, textvariable=self.course_var, state="readonly")
        self.course_cb.pack(fill="x", pady=5)
        self.course_cb.bind("<<ComboboxSelected>>", self.on_teacher_course_select)
        
        tk.Button(ctrl_frame, text="+ Add Assignment", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.SUCCESS, fg="white",
                  relief="flat", cursor="hand2", command=self.popup_add_assignment).pack(fill="x", pady=(10, 0))
        
        tk.Label(left_panel, text="Assignments", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.BG_COLOR).pack(anchor="w", pady=(15, 5))
        
        search_frame_a = tk.Frame(left_panel, bg=style.AppConfig.BG_COLOR)
        search_frame_a.pack(fill="x", pady=(0, 5))
        tk.Label(search_frame_a, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        self.assign_search_var = tk.StringVar()
        tk.Entry(search_frame_a, textvariable=self.assign_search_var, width=15).pack(side="left", padx=5)
        tk.Button(search_frame_a, text="Go", command=lambda: self.on_teacher_course_select(search=self.assign_search_var.get()), bg=style.AppConfig.TEXT_MUTED, fg="white", relief="flat").pack(side="left")

        cols = ("ID", "Title", "Deadline")
        self.tree_assign = ttk.Treeview(left_panel, columns=cols, show="headings", height=15)
        self.tree_assign.heading("ID", text="ID"); self.tree_assign.column("ID", width=40)
        self.tree_assign.heading("Title", text="Title")
        self.tree_assign.heading("Deadline", text="Deadline")
        self.tree_assign.pack(fill="both", expand=True, pady=(0, 10))
        self.tree_assign.bind("<<TreeviewSelect>>", self.on_teacher_assignment_select)
        self.tree_assign.bind("<Double-1>", lambda e: self.open_assignment_manager())

        tk.Button(left_panel, text="Delete Selected", command=self.delete_assignment, bg=style.AppConfig.DANGER, fg="white", relief="flat").pack(fill="x")

        right_panel = tk.Frame(paned, bg=style.AppConfig.BG_COLOR)
        paned.add(right_panel)
        
        tk.Label(right_panel, text="Student Progress", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.BG_COLOR).pack(anchor="w", pady=(0, 5))
        
        search_frame_s = tk.Frame(right_panel, bg=style.AppConfig.BG_COLOR)
        search_frame_s.pack(fill="x", pady=(0, 5))
        tk.Label(search_frame_s, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        self.student_search_var = tk.StringVar()
        e_stud = tk.Entry(search_frame_s, textvariable=self.student_search_var, width=20)
        e_stud.pack(side="left", padx=5)
        e_stud.bind("<Return>", lambda e: self.on_teacher_assignment_select(search=self.student_search_var.get()))
        tk.Button(search_frame_s, text="Go", command=lambda: self.on_teacher_assignment_select(search=self.student_search_var.get()), bg=style.AppConfig.TEXT_MUTED, fg="white", relief="flat").pack(side="left")
        
        s_cols = ("Name", "Status", "Grade")
        self.tree_students = ttk.Treeview(right_panel, columns=s_cols, show="headings", height=15)
        self.tree_students.heading("Name", text="Student Name")
        self.tree_students.heading("Status", text="Status")
        self.tree_students.heading("Grade", text="Grade")
        self.tree_students.pack(fill="both", expand=True, pady=(0, 10))
        self.tree_students.bind("<Double-1>", lambda e: self.open_assignment_manager())

        instr_frame = tk.LabelFrame(right_panel, text="Instructions", bg=style.AppConfig.CARD_BG, font=style.AppConfig.FONT_SUBHEADER, padx=15, pady=15)
        instr_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        instr = ("1. Select an assignment to see student status above.\n"
                 "2. Double-click an assignment to open detailed grading manager.")
        tk.Label(instr_frame, text=instr, bg=style.AppConfig.CARD_BG, fg=style.AppConfig.TEXT_MAIN, justify="left", wraplength=500).pack(anchor="w")

        self.refresh_teacher_courses()

    # --- TEACHER LOGIC ---
    def refresh_teacher_courses(self):
        courses = self.controller.get_teacher_courses_data()
        self.course_cb['values'] = [f"{c['id']} - {c['title']}" for c in courses]
        if courses:
            self.course_cb.current(0)
            self.on_teacher_course_select()

    def on_teacher_course_select(self, event=None, search=""):
        sel = self.course_var.get()
        if not sel: return
        c_id = int(sel.split(" - ")[0])
        
        for i in self.tree_assign.get_children(): self.tree_assign.delete(i)
        for a in self.controller.get_course_assignments_data(c_id, search):
            d_str = a['deadline'].strftime('%Y-%m-%d') if a['deadline'] else "No Deadline"
            self.tree_assign.insert("", "end", values=(a['id'], a['title'], d_str))
            
        for i in self.tree_students.get_children(): self.tree_students.delete(i)

    def on_teacher_assignment_select(self, event=None, search=""):
        sel = self.tree_assign.selection()
        if not sel:
            for i in self.tree_students.get_children(): self.tree_students.delete(i)
            return
            
        aid = self.tree_assign.item(sel[0])['values'][0]
        assign_data = self.controller.model.get_assignment_details(aid)
        if not assign_data: return

        submissions = self.controller.get_assignment_submissions(aid, search)
        
        for i in self.tree_students.get_children(): self.tree_students.delete(i)
        for s in submissions:
            status = "Submitted" if s['content_text'] or s['file_path'] else "Pending"
            grade = f"{s['score']:.1f}/{assign_data['max_score']}" if s['score'] else "-"
            self.tree_students.insert("", "end", values=(s['full_name'], status, grade))

    def popup_add_assignment(self):
        sel = self.course_var.get()
        if not sel: return messagebox.showwarning("Warning", "Select a course first.")
        c_id = int(sel.split(" - ")[0])
        
        win = self.create_toplevel("New Assignment", "600x700")
        
        form_frame = tk.Frame(win, bg=style.AppConfig.BG_COLOR)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(form_frame, text="Title:", bg=style.AppConfig.BG_COLOR).pack(anchor="w")
        e_title = ttk.Entry(form_frame)
        e_title.pack(fill="x", pady=(0, 10))
        
        tk.Label(form_frame, text="Description:", bg=style.AppConfig.BG_COLOR).pack(anchor="w")
        e_desc = tk.Text(form_frame, height=5, font=style.AppConfig.FONT_BODY)
        e_desc.pack(fill="x", pady=(0, 10))
        
        f_details = tk.Frame(form_frame, bg=style.AppConfig.BG_COLOR)
        f_details.pack(fill="x", pady=(0, 10))
        
        tk.Label(f_details, text="Max Score:", bg=style.AppConfig.BG_COLOR).pack(side="left")
        e_max = ttk.Entry(f_details, width=10)
        e_max.insert(0, "100")
        e_max.pack(side="left", padx=(5, 20))
        
        tk.Label(f_details, text="Deadline (YYYY-MM-DD HH:MM):", bg=style.AppConfig.BG_COLOR).pack(side="left")
        e_deadline = ttk.Entry(f_details)
        e_deadline.insert(0, datetime.now().strftime('%Y-%m-%d 23:59'))
        e_deadline.pack(side="left", padx=5)
        
        # FIX: Add File Attachment Option
        f_att = tk.Frame(form_frame, bg=style.AppConfig.BG_COLOR)
        f_att.pack(fill="x", pady=(0, 10))
        att_var = tk.StringVar()
        tk.Button(f_att, text="Upload Attachment", command=lambda: att_var.set(filedialog.askopenfilename()), bg=style.AppConfig.TEXT_MUTED, fg="white", relief="flat").pack(side="left")
        tk.Label(f_att, textvariable=att_var, bg=style.AppConfig.BG_COLOR, fg=style.AppConfig.PRIMARY).pack(side="left", padx=10)
        
        tk.Label(form_frame, text="Assign to Students (Advisors Only):", font=style.AppConfig.FONT_SUBHEADER, 
                 bg=style.AppConfig.BG_COLOR).pack(anchor="w", pady=(15, 5))
        tk.Label(form_frame, text="Uncheck students to exclude them.", 
                 bg=style.AppConfig.BG_COLOR, fg=style.AppConfig.TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w")

        # FIX: Reduced height to 200 and set expand=False to ensure Create button is visible
        container_frame = tk.LabelFrame(form_frame, bg=style.AppConfig.CARD_BG, height=200)
        container_frame.pack(fill="both", expand=False, pady=5)
        container_frame.pack_propagate(False) 

        scrollbar = tk.Scrollbar(container_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        canvas = tk.Canvas(container_frame, yscrollcommand=scrollbar.set, bg=style.AppConfig.CARD_BG, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas, bg=style.AppConfig.CARD_BG)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        stud_list = self.controller.get_course_students(c_id)
        stud_vars = {}
        
        for s in stud_list:
            var = tk.IntVar(value=1)
            stud_vars[s['id']] = var
            chk = tk.Checkbutton(inner_frame, text=f"{s['full_name']}", variable=var, 
                                bg=style.AppConfig.CARD_BG, anchor="w", font=style.AppConfig.FONT_BODY)
            chk.pack(fill="x", padx=5, pady=2)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", on_frame_configure)

        btn_frame = tk.Frame(form_frame, bg=style.AppConfig.BG_COLOR)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        def save():
            title = e_title.get()
            desc = e_desc.get("1.0", tk.END)
            max_s = e_max.get()
            dead = e_deadline.get()
            att_path = att_var.get()
            
            if not title or not dead:
                messagebox.showerror("Error", "Title and Deadline are required")
                return
            
            selected_sids = [sid for sid, var in stud_vars.items() if var.get() == 1]
                
            # Pass attachment path to controller
            if self.controller.add_assignment([c_id, title, desc, max_s, dead], selected_sids, att_path):
                messagebox.showinfo("Success", "Assignment Added")
                self.on_teacher_course_select()
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to save.")
        
        tk.Button(btn_frame, text="Create Assignment", command=save, 
                  bg=style.AppConfig.PRIMARY, fg="white", relief="flat", 
                  cursor="hand2", font=style.AppConfig.FONT_BUTTON, height=2).pack(fill="x")

    def delete_assignment(self):
        sel = self.tree_assign.selection()
        if not sel: return
        aid = self.tree_assign.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this assignment?"):
            self.controller.delete_assignment(aid)
            self.on_teacher_course_select()

    # --- ASSIGNMENT MANAGER ---
    def open_assignment_manager(self):
        aid = None
        sel = self.tree_assign.selection()
        if sel:
            aid = self.tree_assign.item(sel[0])['values'][0]
        
        if not aid:
            return messagebox.showwarning("Warning", "Select an assignment first.")
        
        assign_data = self.controller.model.get_assignment_details(aid)
        if not assign_data: return
        
        win = self.create_toplevel(f"Manage: {assign_data['title']}", "1000x700")
        
        top_frame = tk.Frame(win, bg=style.AppConfig.CARD_BG, padx=20, pady=20)
        top_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(top_frame, text=f"Assignment: {assign_data['title']}", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.CARD_BG).pack(anchor="w")
        tk.Label(top_frame, text=f"Deadline: {assign_data['deadline']}", font=style.AppConfig.FONT_BODY, fg=style.AppConfig.DANGER, bg=style.AppConfig.CARD_BG).pack(anchor="w", pady=5)
        
        mid_pane = tk.PanedWindow(win, orient=tk.HORIZONTAL, bg=style.AppConfig.BG_COLOR)
        mid_pane.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        left = tk.Frame(mid_pane, bg=style.AppConfig.BG_COLOR)
        mid_pane.add(left, width=400)
        
        tk.Label(left, text="Student Submissions", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.BG_COLOR).pack(anchor="w", pady=5)
        
        cols = ("ID", "Name", "Status")
        tree_subs = ttk.Treeview(left, columns=cols, show="headings", height=20)
        tree_subs.heading("ID", text="ID"); tree_subs.column("ID", width=40)
        tree_subs.heading("Name", text="Student Name")
        tree_subs.heading("Status", text="Status")
        tree_subs.pack(fill="both", expand=True)
        
        submissions = self.controller.get_assignment_submissions(aid)
        sub_map = {}
        for s in submissions:
            status = "Submitted" if s['content_text'] or s['file_path'] else "Pending"
            vals = (s['id'], s['full_name'], status)
            item = tree_subs.insert("", "end", values=vals)
            sub_map[item] = s
            
        right = tk.Frame(mid_pane, bg=style.AppConfig.CARD_BG)
        mid_pane.add(right)
        
        lbl_header = tk.Label(right, text="Select a student to grade", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.CARD_BG)
        lbl_header.pack(pady=10)
        
        frame_content = tk.LabelFrame(right, text="Submission Content", bg=style.AppConfig.CARD_BG, font=style.AppConfig.FONT_BODY, padx=10, pady=10)
        frame_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        txt_view = tk.Text(frame_content, height=8, state="disabled", bg="#F9FAFB", font=("Segoe UI", 10), wrap="word")
        txt_view.pack(fill="both", expand=True)
        
        var_file = tk.StringVar()
        lbl_file = tk.Label(frame_content, textvariable=var_file, fg="blue", cursor="hand2", bg=style.AppConfig.CARD_BG)
        lbl_file.pack(pady=5)
        
        frame_grade = tk.LabelFrame(right, text="Grading", bg=style.AppConfig.CARD_BG, font=style.AppConfig.FONT_BODY, padx=10, pady=10)
        frame_grade.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_grade, text="Feedback:", bg=style.AppConfig.CARD_BG).pack(anchor="w")
        txt_feedback = tk.Text(frame_grade, height=3, font=("Segoe UI", 10))
        txt_feedback.pack(fill="x", pady=5)
        
        f_score = tk.Frame(frame_grade, bg=style.AppConfig.CARD_BG)
        f_score.pack(fill="x", pady=5)
        tk.Label(f_score, text="Score:", bg=style.AppConfig.CARD_BG).pack(side="left")
        e_score = ttk.Entry(f_score, width=10)
        e_score.pack(side="left", padx=5)
        lbl_max = tk.Label(f_score, text=f"/ {assign_data['max_score']}", bg=style.AppConfig.CARD_BG)
        lbl_max.pack(side="left")
        
        def on_student_select(event):
            sel = tree_subs.selection()
            if not sel: return
            data = sub_map[sel[0]]
            
            lbl_header.config(text=f"Grading: {data['full_name']}")
            txt_view.config(state="normal")
            txt_view.delete("1.0", tk.END)
            if data['content_text']:
                txt_view.insert(tk.END, data['content_text'])
            else:
                txt_view.insert(tk.END, "[No text submission]")
            txt_view.config(state="disabled")
            
            if data['file_path']:
                var_file.set(f"Attached: {data['file_path']}")
                lbl_file.bind("<Button-1>", lambda e: messagebox.showinfo("File", f"Path: {data['file_path']}"))
            else:
                var_file.set("")
                
            if data['score'] is not None:
                e_score.delete(0, tk.END)
                e_score.insert(0, str(data['score']))
            
            fb = data.get('feedback')
            txt_feedback.delete("1.0", tk.END)
            if fb:
                txt_feedback.insert(tk.END, fb)
        
        tree_subs.bind("<<TreeviewSelect>>", on_student_select)
        
        def submit_grade():
            sel = tree_subs.selection()
            if not sel: return messagebox.showwarning("Warning", "Select a student.")
            s_id = sub_map[sel[0]]['id']
            
            try:
                score = float(e_score.get())
            except ValueError:
                return messagebox.showerror("Error", "Invalid score format.")
            
            if score > assign_data['max_score']:
                return messagebox.showerror("Error", f"Score cannot exceed maximum ({assign_data['max_score']}).")

            fb = txt_feedback.get("1.0", tk.END).strip()
            
            if self.controller.save_grade_and_feedback(s_id, aid, score, fb):
                messagebox.showinfo("Success", "Grade saved.")
                self.on_teacher_assignment_select()
            else:
                messagebox.showerror("Error", "Failed to save.")

        tk.Button(frame_grade, text="Save Grade & Feedback", command=submit_grade, bg=style.AppConfig.PRIMARY, fg="white", relief="flat", cursor="hand2", font=style.AppConfig.FONT_BUTTON).pack(fill="x", pady=5)

    # --- STUDENT VIEW ---
    def render_student_view(self):
        toolbar = tk.Frame(self.content_area, bg=style.AppConfig.BG_COLOR)
        toolbar.pack(fill="x", pady=(0, 10))
        
        tk.Label(toolbar, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        self.stud_assign_search_var = tk.StringVar()
        tk.Entry(toolbar, textvariable=self.stud_assign_search_var, width=20).pack(side="left", padx=5)
        tk.Button(toolbar, text="Search", command=lambda: self.refresh_student_grades(self.stud_assign_search_var.get()), bg=style.AppConfig.PRIMARY, fg="white", relief="flat").pack(side="left")
        tk.Button(toolbar, text="Refresh", command=lambda: self.refresh_student_grades(), bg=style.AppConfig.TEXT_MUTED, fg="white",
                  font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(side="right")
        
        cols = ("ID", "Course", "Assignment", "Deadline", "Max", "Grade")
        self.tree_student = ttk.Treeview(self.content_area, columns=cols, show="headings", height=25)
        
        self.tree_student.heading("ID", text="ID"); self.tree_student.column("ID", width=0, stretch=False)
        self.tree_student.heading("Course", text="Course"); self.tree_student.column("Course", width=200)
        self.tree_student.heading("Assignment", text="Assignment"); self.tree_student.column("Assignment", width=200)
        self.tree_student.heading("Deadline", text="Deadline"); self.tree_student.column("Deadline", width=120)
        self.tree_student.heading("Max", text="Max"); self.tree_student.column("Max", width=50)
        self.tree_student.heading("Grade", text="Grade"); self.tree_student.column("Grade", width=80)
        
        self.tree_student.pack(fill="both", expand=True)
        self.tree_student.bind("<Double-1>", lambda e: self.open_student_submission_page())
        self.refresh_student_grades()

    def refresh_student_grades(self, search=""):
        for i in self.tree_student.get_children(): self.tree_student.delete(i)
        data = self.controller.get_student_report_card(search)
        
        for row in data:
            deadline_str = row[5].strftime('%Y-%m-%d') if row[5] else "No Deadline"
            grade = f"{row[4]:.1f}" if row[4] else "-"
            
            vals = (row[1], row[0], row[2], deadline_str, row[3], grade)
            self.tree_student.insert("", "end", values=vals)

    def open_student_submission_page(self):
        sel = self.tree_student.selection()
        if not sel: return
        
        vals = self.tree_student.item(sel[0])['values']
        aid = vals[0]
        c_name, a_name = vals[1], vals[2]
        
        # FIX: Resized to 1100x680
        win = self.create_toplevel(f"Submit: {a_name}", "1100x680")
        
        # Top: Assignment Details
        details_frame = tk.Frame(win, bg=style.AppConfig.CARD_BG, padx=15, pady=15)
        details_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(details_frame, text=f"Course: {c_name}", bg=style.AppConfig.CARD_BG, fg=style.AppConfig.TEXT_MUTED).pack(anchor="w")
        tk.Label(details_frame, text=f"Assignment: {a_name}", font=style.AppConfig.FONT_SUBHEADER, bg=style.AppConfig.CARD_BG).pack(anchor="w", pady=(5, 10))
        
        assign_data = self.controller.model.get_assignment_details(aid)
        if assign_data:
            desc_label = tk.Label(details_frame, text="Description:", bg=style.AppConfig.CARD_BG, font=style.AppConfig.FONT_BUTTON)
            desc_label.pack(anchor="w")
            
            # FIX: Reduced height to 3 to save space and keep button visible
            txt_description = tk.Text(details_frame, height=3, width=80, font=style.AppConfig.FONT_BODY, bg="#F3F4F6", wrap="word", relief="flat")
            txt_description.pack(fill="x", pady=5)
            txt_description.insert("1.0", assign_data['description'])
            txt_description.config(state="disabled")
            
            # FIX: Display Teacher Attachment if exists
            if assign_data.get('attachment_path'):
                lbl_att = tk.Label(details_frame, text=f"Attachment: {assign_data['attachment_path']}", bg=style.AppConfig.CARD_BG, fg=style.AppConfig.PRIMARY, cursor="hand2")
                lbl_att.pack(anchor="w", pady=(5, 0))
                lbl_att.bind("<Button-1>", lambda e: messagebox.showinfo("Attachment Info", f"File Path: {assign_data['attachment_path']}"))
        
        # Middle: Split Layout
        mid_pane = tk.PanedWindow(win, orient=tk.HORIZONTAL, bg=style.AppConfig.BG_COLOR)
        mid_pane.pack(fill="both", expand=True, padx=20, pady=(0, 10)) # Reduced bottom padding
        
        left_panel = tk.Frame(mid_pane, bg=style.AppConfig.BG_COLOR)
        mid_pane.add(left_panel, minsize=400)
        
        tk.Label(left_panel, text="Your Submission", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.BG_COLOR).pack(anchor="w", pady=(0, 5))
        # FIX: Reduced height to 9
        txt_sub = tk.Text(left_panel, height=9, font=style.AppConfig.FONT_BODY)
        txt_sub.pack(fill="both", expand=True)
        
        var_file = tk.StringVar()
        frm_file = tk.Frame(left_panel, bg=style.AppConfig.BG_COLOR)
        frm_file.pack(fill="x", pady=5)
        tk.Button(frm_file, text="Upload File", command=lambda: var_file.set(filedialog.askopenfilename())).pack(side="left")
        tk.Label(frm_file, textvariable=var_file, bg=style.AppConfig.BG_COLOR).pack(side="left", padx=10)
        
        right_panel = tk.Frame(mid_pane, bg=style.AppConfig.CARD_BG)
        mid_pane.add(right_panel, minsize=300)
        
        tk.Label(right_panel, text="Teacher Feedback", font=style.AppConfig.FONT_BUTTON, bg=style.AppConfig.CARD_BG).pack(anchor="w", pady=10, padx=10)
        
        existing_sub = self.controller.model.get_student_submission(self.controller.current_user['id'], aid)
        
        # FIX: Reduced height to 7
        feedback_text = tk.Text(right_panel, height=7, width=30, font=style.AppConfig.FONT_BODY, state="disabled", bg="#F9FAFB")
        feedback_text.pack(fill="both", expand=True, padx=10)
        
        lbl_score_display = tk.Label(right_panel, text="Score: --", font=("Segoe UI", 14, "bold"), fg=style.AppConfig.TEXT_MUTED, bg=style.AppConfig.CARD_BG)
        lbl_score_display.pack(pady=(10, 20))

        if existing_sub:
            txt_sub.insert("1.0", existing_sub['content_text'])
            var_file.set(existing_sub['file_path'])
            tk.Label(left_panel, text="Submitted at: " + str(existing_sub['submitted_at']), bg=style.AppConfig.BG_COLOR, fg="green").pack(anchor="w", pady=5)
            
            if existing_sub['score'] is not None:
                lbl_score_display.config(text=f"Score: {existing_sub['score']}", fg=style.AppConfig.SUCCESS)
            else:
                lbl_score_display.config(text="Score: Not Graded Yet", fg=style.AppConfig.TEXT_MUTED)
                
            fb = existing_sub.get('feedback')
            feedback_text.config(state="normal")
            feedback_text.delete("1.0", tk.END)
            if fb:
                feedback_text.insert(tk.END, fb)
            else:
                feedback_text.insert(tk.END, "No feedback available yet.")
            feedback_text.config(state="disabled")
        else:
            feedback_text.config(state="normal")
            feedback_text.insert(tk.END, "No feedback available yet.")
            feedback_text.config(state="disabled")

        def submit():
            txt = txt_sub.get("1.0", tk.END).strip()
            fpath = var_file.get()
            if isinstance(fpath, tuple): fpath = ""
            
            if not txt and not fpath:
                return messagebox.showwarning("Warning", "Please enter text or upload a file.")
            
            if self.controller.submit_assignment(aid, txt, fpath):
                messagebox.showinfo("Success", "Assignment Submitted!")
                win.destroy()
                self.refresh_student_grades()
            else:
                messagebox.showerror("Error", "Submission failed.")
                
        # FIX: Ensure button is always visible at bottom
        tk.Button(win, text="Submit Assignment", command=submit, bg=style.AppConfig.PRIMARY, fg="white", font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(side="bottom", pady=20)

    # --- ADMIN HELPERS ---
    def refresh_users(self, search=""):
        for item in self.tree_users.get_children(): self.tree_users.delete(item)
        for u in self.controller.get_all_users_data(search):
            self.tree_users.insert("", "end", values=(u['id'], u['username'], u['full_name'], u['role']))

    def refresh_courses(self, search=""):
        for item in self.tree_courses.get_children(): self.tree_courses.delete(item)
        for c in self.controller.get_all_courses_data(search):
            self.tree_courses.insert("", "end", values=(c['id'], c['title'], c.get('teacher_name')))

    def popup_add_user(self):
        win = self.create_toplevel("Add User", "400x500")
        
        entries = {}
        for f in ["Username", "Password", "Full Name"]:
            tk.Label(win, text=f, bg=style.AppConfig.BG_COLOR).pack(pady=5)
            e = ttk.Entry(win)
            if f == "Password": e.config(show="*")
            e.pack(pady=5)
            entries[f] = e
            
        tk.Label(win, text="Role:", bg=style.AppConfig.BG_COLOR).pack(pady=5)
        cb_role = ttk.Combobox(win, values=["admin", "teacher", "student"], state="readonly")
        cb_role.pack(pady=5)
        entries["Role"] = cb_role
        
        advisor_frame = tk.LabelFrame(win, text="Advisors (If Student)", bg=style.AppConfig.BG_COLOR)
        advisor_frame.pack(fill="x", padx=10, pady=10)
        
        teachers = [t for t in self.controller.get_all_users_data() if t['role'] == 'teacher']
        
        advisor_vars = {}
        for t in teachers:
            var = tk.IntVar(value=0)
            advisor_vars[t['id']] = var
            chk = tk.Checkbutton(advisor_frame, text=t['full_name'], variable=var, bg=style.AppConfig.BG_COLOR)
            chk.pack(anchor="w")
            
        def save():
            data = [entries["Username"].get(), entries["Password"].get(), entries["Full Name"].get(), entries["Role"].get()]
            if not all([d for d in data[:3]]) or not data[3]:
                 messagebox.showerror("Error", "All fields are required.")
                 return
            if self.controller.add_user(data):
                if data[3] == 'student':
                    all_users = self.controller.get_all_users_data()
                    new_user = next((u for u in all_users if u['username'] == data[0]), None)
                    if new_user:
                        selected_teachers = [tid for tid, var in advisor_vars.items() if var.get() == 1]
                        self.controller.update_advisors(new_user['id'], selected_teachers)
                
                messagebox.showinfo("Success", "Saved successfully")
                self.refresh_users()
                win.destroy()
            else:
                messagebox.showerror("Error", "Could not save. Username might exist.")
                
        tk.Button(win, text="Save", command=save, bg=style.AppConfig.PRIMARY, fg="white", 
                  font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(pady=20)

    def popup_edit_user(self):
        sel = self.tree_users.selection()
        if not sel: return messagebox.showwarning("Warning", "Select a user to edit.")
        item = self.tree_users.item(sel[0])
        vals = item['values']
        uid, current_username, current_name, current_role = vals
        
        self._edit_user_popup(uid, current_username, current_name, current_role)

    def _edit_user_popup(self, uid, current_username, current_name, current_role):
        win = self.create_toplevel("Edit User", "400x500")
        
        tk.Label(win, text="Username:", bg=style.AppConfig.BG_COLOR).pack(pady=5)
        e_user = ttk.Entry(win)
        e_user.insert(0, current_username)
        e_user.pack(pady=5)
        
        tk.Label(win, text="Full Name:", bg=style.AppConfig.BG_COLOR).pack(pady=5)
        e_name = ttk.Entry(win)
        e_name.insert(0, current_name)
        e_name.pack(pady=5)
        
        tk.Label(win, text="Role:", bg=style.AppConfig.BG_COLOR).pack(pady=5)
        cb_role = ttk.Combobox(win, values=["admin", "teacher", "student"], state="readonly")
        cb_role.set(current_role)
        cb_role.pack(pady=5)
        
        advisor_frame = tk.LabelFrame(win, text="Advisors (Subordination)", bg=style.AppConfig.BG_COLOR)
        advisor_frame.pack(fill="x", padx=10, pady=10)
        
        teachers = [t for t in self.controller.get_all_users_data() if t['role'] == 'teacher']
        current_advisors = self.controller.get_user_advisors(uid)
        
        advisor_vars = {}
        for t in teachers:
            var = tk.IntVar(value=1 if t['id'] in current_advisors else 0)
            advisor_vars[t['id']] = var
            chk = tk.Checkbutton(advisor_frame, text=t['full_name'], variable=var, bg=style.AppConfig.BG_COLOR)
            chk.pack(anchor="w")

        def save():
            new_user = e_user.get()
            new_name = e_name.get()
            new_role = cb_role.get()
            
            if not new_name or not new_user:
                messagebox.showerror("Error", "Fields cannot be empty.")
                return

            if self.controller.update_user(uid, new_name, new_role, new_user):
                if new_role == 'student':
                    selected_teachers = [tid for tid, var in advisor_vars.items() if var.get() == 1]
                    self.controller.update_advisors(uid, selected_teachers)
                
                messagebox.showinfo("Success", "User updated successfully")
                self.refresh_users()
                win.destroy()
            else:
                messagebox.showerror("Error", "Could not update user.")

        tk.Button(win, text="Save Changes", command=save, bg=style.AppConfig.PRIMARY, fg="white", 
                  font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(pady=20)

    def delete_user(self):
        sel = self.tree_users.selection()
        if not sel: return
        uid = self.tree_users.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this user?"):
            self.controller.delete_user(uid)
            self.refresh_users()

    def popup_add_course(self):
        win = self.create_toplevel("Add Course", "400x400")
        
        entries = []
        for f in ["Title", "Description", "Teacher ID"]:
            tk.Label(win, text=f, bg=style.AppConfig.BG_COLOR).pack(pady=5)
            e = ttk.Entry(win)
            e.pack(pady=5)
            entries.append(e)
            
        def save():
            data = [e.get() for e in entries]
            if self.controller.add_course(data):
                messagebox.showinfo("Success", "Saved successfully")
                self.refresh_courses()
                win.destroy()
            else:
                messagebox.showerror("Error", "Could not save. Check inputs.")
                
        tk.Button(win, text="Save", command=save, bg=style.AppConfig.PRIMARY, fg="white", 
                  font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(pady=20)
    
    def popup_enroll_students(self):
        sel = self.tree_courses.selection()
        if not sel: return messagebox.showwarning("Warning", "Select a course to enroll students.")
        course_item = self.tree_courses.item(sel[0])
        course_id = course_item['values'][0]
        course_name = course_item['values'][1]
        
        win = self.create_toplevel(f"Enroll Students: {course_name}", "400x500")
        
        # FIX: Search Bar
        search_frame = tk.Frame(win, bg=style.AppConfig.BG_COLOR)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(search_frame, text="Search:", bg=style.AppConfig.BG_COLOR).pack(side="left", padx=5)
        search_var = tk.StringVar()
        e_search = tk.Entry(search_frame, textvariable=search_var, width=20)
        e_search.pack(side="left", padx=5)
        btn_go = tk.Button(search_frame, text="Go", command=lambda: filter_students(), bg="#9CA3AF", fg="white", relief="flat", cursor="hand2")
        btn_go.pack(side="left")
        
        container_frame = tk.Frame(win, bg=style.AppConfig.BG_COLOR)
        container_frame.pack(fill="both", expand=True, padx=10)
        
        scrollbar = tk.Scrollbar(container_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        canvas = tk.Canvas(container_frame, yscrollcommand=scrollbar.set, bg=style.AppConfig.BG_COLOR, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        
        inner_frame = tk.Frame(canvas, bg=style.AppConfig.BG_COLOR)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        all_students = [u for u in self.controller.get_all_users_data() if u['role'] == 'student']
        enrolled_students = self.controller.model.get_course_students(course_id, teacher_id=None)
        enrolled_ids = {s['id'] for s in enrolled_students}
        
        # Store vars in a dictionary to persist state during filter
        enroll_vars = {}
        
        # Helper to populate list
        def populate_list(filter_text=""):
            for widget in inner_frame.winfo_children():
                widget.destroy()
                
            for s in all_students:
                if filter_text.lower() in s['full_name'].lower():
                    var = enroll_vars[s['id']] # Use existing var
                    chk = tk.Checkbutton(inner_frame, text=f"{s['full_name']} (ID: {s['id']})", variable=var, bg=style.AppConfig.BG_COLOR, anchor="w")
                    chk.pack(fill="x", padx=5, pady=2)
            
            inner_frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            
        def filter_students():
            populate_list(search_var.get())

        # Initialize vars and populate full list
        for s in all_students:
            enroll_vars[s['id']] = tk.IntVar(value=1 if s['id'] in enrolled_ids else 0)
            
        inner_frame.bind("<Configure>", on_frame_configure)
        populate_list()
        
        def save_enrollment():
            selected_ids = [sid for sid, var in enroll_vars.items() if var.get() == 1]
            
            for s in all_students:
                self.controller.unenroll_student(s['id'], course_id)
                
            count = 0
            for sid in selected_ids:
                if self.controller.enroll_student(sid, course_id):
                    count += 1
            
            messagebox.showinfo("Success", f"Enrolled {count} students.")
            win.destroy()
            
        tk.Button(win, text="Save Enrollments", command=save_enrollment, bg=style.AppConfig.PRIMARY, fg="white", font=style.AppConfig.FONT_BUTTON, relief="flat", cursor="hand2").pack(fill="x", padx=10, pady=10)
        
    def delete_course(self):
        sel = self.tree_courses.selection()
        if not sel: return
        cid = self.tree_courses.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this course?"):
            self.controller.delete_course(cid)
            self.refresh_courses()
