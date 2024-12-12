import os
import time
import customtkinter as ctk
from collections import defaultdict

class TheQuestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("TheQuest")
        self.geometry(f"1600x848+{(self.winfo_screenwidth()//2)-800}+{(self.winfo_screenheight()//2)-450}")
        self.configure(fg_color="#121212")
        self.language_projects = defaultdict(list)
        self.projects_base_path = os.path.join(os.path.expanduser("~"), "Projects")
        self._create_sidebar()
        self._create_main_content()
        self._load_recent_projects()

    def _create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color="#1E1E28", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1, minsize=300)
        ctk.CTkLabel(sidebar, text="TheQuest", font=("VT323", 64), text_color="#E0E0E0").pack(pady=(30, 220))
        nav_sections = [("Main", ["Projects", "Dashboard"]), ("Tools", ["Statistics", "Settings"])]
        for section_name, section_items in nav_sections:
            ctk.CTkLabel(sidebar, text=section_name.upper(), font=("VT323", 32), text_color="#A0A0A0").pack(anchor="w", padx=15)
            for item in section_items:
                ctk.CTkButton(sidebar, text=item, font=("VT323", 32), fg_color="transparent", hover_color="#3A3A3A", text_color="#E0E0E0", anchor="w").pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(sidebar, text="Exit", font=("VT323", 32), fg_color="#3A1A1A", hover_color="#5A2A2A", text_color="#E0E0E0", command=self.quit).pack(side="bottom", fill="x", padx=15, pady=15)

    def _create_main_content(self):
        main_frame = ctk.CTkFrame(self, fg_color="#121212")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        main_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(main_frame, text="Create New Project", font=("VT323", 36), text_color="#E0E0E0").grid(row=0, column=0, sticky="w", pady=(0, 20))
        project_header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        project_header_frame.grid(row=1, column=0, sticky="ew")
        add_project_btn = ctk.CTkButton(project_header_frame, text="+", font=("VT323", 115), width=400, fg_color="#3A3A3A", hover_color="#4A4A4A", command=self._add_project)
        add_project_btn.grid(row=0, column=0, padx=(0, 20), sticky="w")
        project_form_frame = ctk.CTkFrame(project_header_frame, fg_color="transparent")
        project_form_frame.grid(row=0, column=1, sticky="ew")
        self.project_name_entry = ctk.CTkEntry(project_form_frame, width=700, font=("VT323", 24), fg_color="#1E1E28", text_color="#FFFFFF")
        self.project_name_entry.pack(fill="x", pady=(0, 20))
        self.language_selector = ctk.CTkOptionMenu(project_form_frame, values=["Python", "C++", "C#", "PHP", "Node.js", "Frontend"], font=("VT323", 24), fg_color="#1E1E28", text_color="#FFFFFF", dropdown_font=("VT323", 20))
        self.language_selector.pack(fill="x")
        self._setup_recent_projects(main_frame)
        self._setup_language_stats(main_frame)

    def _setup_recent_projects(self, main_frame):
        ctk.CTkLabel(main_frame, text="Recent Projects", font=("VT323", 36), text_color="#E0E0E0").grid(row=2, column=0, sticky="w", pady=(30, 20))
        self.recent_projects_table = ctk.CTkScrollableFrame(main_frame, fg_color="#1E1E28")
        self.recent_projects_table.grid(row=3, column=0, sticky="nsew")

    def _setup_language_stats(self, main_frame):
        ctk.CTkLabel(main_frame, text="Language Project Statistics", font=("VT323", 36), text_color="#E0E0E0").grid(row=4, column=0, sticky="w", pady=(30, 20))
        self.language_stats_frame = ctk.CTkFrame(main_frame, fg_color="#1E1E28")
        self.language_stats_frame.grid(row=5, column=0, sticky="nsew")
        self._update_language_stats()

    def _format_time_ago(self, path):
        modified_time = os.path.getmtime(path)
        diff = time.time() - modified_time
        if diff < 60: return "Just now"
        if diff < 3600: return f"{int(diff // 60)}m ago"
        if diff < 86400: return f"{int(diff // 3600)}h ago"
        return f"{int(diff // 86400)}d ago"

    def _load_recent_projects(self):
        if not os.path.exists(self.projects_base_path): os.makedirs(self.projects_base_path)
        for language in os.listdir(self.projects_base_path):
            language_path = os.path.join(self.projects_base_path, language)
            if os.path.isdir(language_path):
                for project in os.listdir(language_path):
                    project_path = os.path.join(language_path, project)
                    if os.path.isdir(project_path):
                        self._add_recent_project(project, language, self._format_time_ago(project_path))

    def _add_recent_project(self, name, language, last_open):
        for child in self.recent_projects_table.winfo_children():
            if isinstance(child, ctk.CTkButton) and name in child.cget('text'):
                child.destroy()
        project_button = ctk.CTkButton(self.recent_projects_table, text=f"{name} | {language} | {last_open}", font=("VT323", 24), fg_color="transparent", hover_color="#3A3A3A", anchor="w", command=lambda: self._open_project(language, name))
        project_button.pack(fill="x", pady=5)
        self.language_projects[language].append(name)

    def _open_project(self, language, project_name):
        os.system(f"code \"{os.path.join(self.projects_base_path, language, project_name)}\"")

    def _count_language_folders(self):
        return {language: len([f for f in os.listdir(os.path.join(self.projects_base_path, language)) if os.path.isdir(os.path.join(self.projects_base_path, language, f))]) if os.path.exists(os.path.join(self.projects_base_path, language)) else 0 for language in ["Python", "C++", "C#", "PHP", "Node.js", "Frontend"]}

    def _add_project(self):
        project_name = self.project_name_entry.get()
        language = self.language_selector.get()
        if not project_name or not language:
            ctk.CTkMessagebox(title="Error", message="Please enter a project name and select a language.")
            return
        project_path = os.path.join(self.projects_base_path, language, project_name)
        template_files = {
            "PHP": [("index.php", "<?php\n\n"), ("db.php", "<?php\n\n")],
            "Node.js": [("server.js", "")],
            "Frontend": [("index.html", "<!DOCTYPE html>\n<html>\n</html>")],
            "Python": [("main.py", "")],
            "C++": [("main.cpp", "")],
            "C#": [("Program.cs", "")]
        }
        try:
            os.makedirs(project_path, exist_ok=True)
            for filename, content in template_files.get(language, []):
                with open(os.path.join(project_path, filename), 'w') as f:
                    f.write(content)
            os.system(f"code \"{project_path}\"")
            self._add_recent_project(project_name, language, self._format_time_ago(project_path))
            self.project_name_entry.delete(0, 'end')
            self._update_language_stats()
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"Error creating project: {e}")

    def _update_language_stats(self):
        for widget in self.language_stats_frame.winfo_children(): widget.destroy()
        for language, folder_count in self._count_language_folders().items():
            lang_frame = ctk.CTkFrame(self.language_stats_frame, fg_color="transparent")
            lang_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(lang_frame, text=language, font=("VT323", 24), width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(lang_frame, text=f"Folders: {folder_count}", font=("VT323", 24), width=200, anchor="w").pack(side="left", padx=10)

def main():
    TheQuestApp().mainloop()

if __name__ == "__main__":
    main()
