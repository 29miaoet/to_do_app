import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sqlite_handler

class AppMenu():
    def remove_frames(self):
        for widget in window.winfo_children():
            widget.grid_remove()
    def choose_file(self):
        global app
        app.close_db()
        file = filedialog.askopenfilename()
        app = sqlite_handler.Todo(file)
        app.create_db("tasks")
    def create_new(self):
        global app
        app.close_db()
        filename = filedialog.asksaveasfilename(
            title="Create New File",
            defaultextension=".bd",
            filetypes=[
                ("All files", "*.*"),
                ("Database file", "*.db"),
                ("SQLite Database file", "*.sqlite")
            ]
        )

        app = sqlite_handler.Todo(filename)
        app.create_db("tasks")
    def show_tasks(self):
        try:
            table = app.show_tasks().fetchall()
            self.remove_frames()
            tableframe = tk.Frame(window)
            tableframe.grid_columnconfigure([0,1,2], weight=1)
            tableframe.grid_rowconfigure([i for i in range(len(table)+1)], weight=1)
            i = 1
            labels = []
            for row in table:
                label1 = tk.Label(tableframe, text=row[0])
                label2 = tk.Label(tableframe, text=row[1])
                label3 = tk.Label(tableframe, text=row[2])
                label1.grid(row=i, column=0, sticky="nsew")
                label2.grid(row=i, column=1, sticky="nsew")
                label3.grid(row=i, column=2, sticky="nsew")

                labels.append((label1, label2, label3))
                i += 1
            id_label = tk.Label(tableframe, text="ID")
            taskname_label = tk.Label(tableframe, text="TASK NAME")
            priority_label = tk.Label(tableframe, text="PRIORITY")
            id_label.grid(row=0, column=0, sticky="nsew")
            taskname_label.grid(row=0, column=1, sticky="nsew")
            priority_label.grid(row=0, column=2, sticky="nsew")
            tableframe.grid(row=0, column=0, sticky="nsew")
        except sqlite3.Error:
            messagebox.showerror("Database Error","An error occurred in the database.")
        except tk.TclError:
            messagebox.showerror("GUI Error","An error occurred with GUI operations")
        except ValueError:
            messagebox.showerror("Input Error","Please do not enter gibberish.")

    def add_task(self):
        def process_info():
            try:
                name = entry_name.get()
                priority = entry_priority.get()
                identity = entry_id.get()
                if identity == "":
                    app.enter_task(name, int(priority))
                else:
                    app.enter_task(name, int(priority), identity)
                for entry_thing in (entry_name, entry_priority, entry_id):
                    entry_thing.delete(0, tk.END)
            except sqlite3.Error:
                messagebox.showerror("Database Error","An error occurred in the database.")
            except tk.TclError:
                messagebox.showerror("GUI Error","An error occurred with GUI operations")
            except ValueError:
                messagebox.showerror("Input Error","Please do not enter gibberish.")
        self.remove_frames()
        inputarea = tk.Frame(window)
        inputarea.grid_rowconfigure([0,1,2,3], weight=1)
        inputarea.grid_columnconfigure([0,1], weight=1)

        lbl_name = tk.Label(inputarea, text="Enter task name: ")
        lbl_priority = tk.Label(inputarea, text="Enter task priority: ")
        lbl_id = tk.Label(inputarea, text="Enter task id: ")

        entry_name = tk.Entry(inputarea)
        entry_priority = tk.Entry(inputarea)
        entry_id = tk.Entry(inputarea)

        i = 0
        for (lbl, entry) in zip((lbl_name, lbl_priority, lbl_id), (entry_name, entry_priority, entry_id)):
            lbl.grid(row=i, column=0, sticky="nsew")
            entry.grid(row=i, column=1, sticky="nsew")
            i += 1

        btn_submit = tk.Button(inputarea, text="Enter", command=process_info)
        btn_submit.grid(row=3, column=0, columnspan=2, sticky="nsew")

        inputarea.grid(row=0, column=0, sticky="nsew")
    def delete_task(self):
        try:
            def remove_selected():
                for i in range(len(checkvars)):
                    if checkvars[i].get() == 1:
                        app.remove_task(str(labels[i][0]["text"]))
                        labels[i][0].destroy()
                        labels[i][1].destroy()
                        labels[i][2].destroy()
                        checkbuttons[i].destroy()
                        
            table = app.show_tasks().fetchall()
            self.remove_frames()
            tableframe = tk.Frame(window)
            tableframe.grid_columnconfigure([0,1,2,3], weight=1)
            tableframe.grid_rowconfigure([i for i in range(len(table)+2)], weight=1)
            i = 1
            labels = []
            checkbuttons = []
            checkvars = []
            for row in table:
                label1 = tk.Label(tableframe, text=row[0])
                label2 = tk.Label(tableframe, text=row[1])
                label3 = tk.Label(tableframe, text=row[2])
                label1.grid(row=i, column=0, sticky="nsew")
                label2.grid(row=i, column=1, sticky="nsew")
                label3.grid(row=i, column=2, sticky="nsew")
                checkvar = tk.IntVar()
                checkbutton = tk.Checkbutton(tableframe, variable=checkvar, onvalue=1, offvalue=0)
                checkbutton.grid(row=i, column=3, sticky="nsew")
                labels.append((label1, label2, label3))
                checkbuttons.append(checkbutton)
                checkvars.append(checkvar)
                i += 1
            id_label = tk.Label(tableframe, text="ID")
            taskname_label = tk.Label(tableframe, text="TASK NAME")
            priority_label = tk.Label(tableframe, text="PRIORITY")
            id_label.grid(row=0, column=0, sticky="nsew")
            taskname_label.grid(row=0, column=1, sticky="nsew")
            priority_label.grid(row=0, column=2, sticky="nsew")
            submit = tk.Button(text="Delete", command=remove_selected)
            submit.grid(row=i+1, column=0, columnspan=4, sticky="nsew")
            tableframe.grid(row=0, column=0, sticky="nsew")
        except sqlite3.Error:
            messagebox.showerror("Database Error","An error occurred in the database.")
        except tk.TclError:
            messagebox.showerror("GUI Error","An error occurred with GUI operations")
        except ValueError:
            messagebox.showerror("Input Error","Please do not enter gibberish.")
    def change_priority(self):
            def change_selected():
                try:
                    new_pr = int(entry_newpriority.get())
                    label = labels[radiovar.get()-1]
                    lblid = int(label[0]["text"])
                    app.change_priority(lblid, new_pr)
                    label[2].config(text = str(new_pr))
                except sqlite3.Error:
                    messagebox.showerror("Database Error",f"An error occurred in the database.")
                except tk.TclError:
                    messagebox.showerror("GUI Error","An error occurred with GUI operations")
                except ValueError:
                    messagebox.showerror("Input Error","Please do not enter gibberish.")
                        
            self.remove_frames()
            table = app.show_tasks().fetchall()
            tableframe = tk.Frame(window)
            tableframe.grid_columnconfigure([0,1,2,3], weight=1)
            tableframe.grid_rowconfigure([i for i in range(len(table)+2)], weight=1)
            i = 1
            labels = []
            radiobuttons = []
            radiovar = tk.IntVar()
            for row in table:
                label1 = tk.Label(tableframe, text=row[0])
                label2 = tk.Label(tableframe, text=row[1])
                label3 = tk.Label(tableframe, text=row[2])
                label1.grid(row=i, column=0, sticky="nsew")
                label2.grid(row=i, column=1, sticky="nsew")
                label3.grid(row=i, column=2, sticky="nsew")
                radiobutton = tk.Radiobutton(tableframe, variable=radiovar, value=i)
                radiobutton.grid(row=i, column=3, sticky="nsew")
                labels.append((label1, label2, label3))
                radiobuttons.append(radiobutton)
                i += 1
            id_label = tk.Label(tableframe, text="ID")
            taskname_label = tk.Label(tableframe, text="TASK NAME")
            priority_label = tk.Label(tableframe, text="PRIORITY")

            id_label.grid(row=0, column=0, sticky="nsew")
            taskname_label.grid(row=0, column=1, sticky="nsew")
            priority_label.grid(row=0, column=2, sticky="nsew")
            submit = tk.Button(tableframe, text="Change", command=change_selected)

            lbl_prompt = tk.Label(tableframe, text="Enter new priority:")
            entry_newpriority = tk.Entry(tableframe)
            lbl_prompt.grid(row=i+1, column=0, sticky="nsew")
            entry_newpriority.grid(row=i+1, column=1, columnspan=2, sticky="nsew")
            submit.grid(row=i+1, column=3, sticky="nsew")
            tableframe.grid(row=0, column=0, sticky="nsew")
    def exit(self):
        window.destroy()

appmenu = AppMenu()
window = tk.Tk()
window.title("To do app")
window.minsize(500, 250)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

menubar = tk.Menu(window)
dropdown = tk.Menu(menubar, tearoff=0)

file = tk.Menu(dropdown, tearoff=0)
file.add_command(label="Open Database", command=appmenu.choose_file)
file.add_command(label="New Database", command=appmenu.create_new)
dropdown.add_cascade(label="File", menu=file)

dropdown.add_command(label="Show Tasks", command=appmenu.show_tasks)
dropdown.add_command(label="Add Task", command=appmenu.add_task)
dropdown.add_command(label="Change Priority", command=appmenu.change_priority)
dropdown.add_command(label="Delete Task", command=appmenu.delete_task)
dropdown.add_command(label="Exit", command=appmenu.exit)
menubar.add_cascade(label="Menu", menu=dropdown)
window.config(menu=menubar)

app = sqlite_handler.Todo("data.db")
app.create_db("tasks")
window.mainloop()
app.commit()   
        
