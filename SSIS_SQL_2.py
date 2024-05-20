from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showwarning, showinfo, showerror
from tkinter.messagebox import askyesno


import mysql.connector
import re

db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="mydb")

mycursor = db.cursor(prepared=True)



"""Classes"""

class Error(Exception):
    pass

class IDInvalid(Error):
    pass

class DatabaseDisplay(ttk.Treeview):
    def __init__(self, master):
        super().__init__(master, columns=('id_no', 'name', 'course', 'year', 'gender'), show="headings", height = 16, style = "Treeview")

        dtbStyle = ttk.Style()
        dtbStyle.configure("Treeview", font=("Lucida Sans", "15"))
        dtbStyle.configure("Treeview.Heading", font=("Lucida Sans", "15"), background="black")


        self.heading('#0', text='', anchor=CENTER)
        self.heading('id_no', text='ID Number')
        self.heading('name', text='Name')
        self.heading('course', text='Course')
        self.heading('year', text='Year')
        self.heading('gender', text='Gender')

        self.column('#0', width=0, stretch=NO)
        self.column('id_no', width=120, minwidth= 100, anchor = CENTER)
        self.column('name', width=252, minwidth= 250, anchor = CENTER)
        self.column('course', width=125, minwidth= 100, anchor = CENTER)
        self.column('year', width=60, minwidth= 20, anchor = CENTER)
        self.column('gender', width=70, minwidth= 20, anchor = CENTER)

        self.grid(row=0, column=0, sticky = "nsew", ipadx = 105, ipady=10)

        scrollbar = ttk.Scrollbar(master, orient=VERTICAL, command=self.yview, cursor='sb_v_double_arrow')
        self.configure(yscroll=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky='ns',)


    def treeview_update(self, student_list):


        for i in self.get_children():
            self.delete(i)


        count = 1
        for element in student_list:
            rowid = 'I' + str('{:03}'.format(count))
            self.insert('', END, iid=rowid, values=element)
            count += 1


class UserDataDisplay(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="UserDataDisplay.TFrame", height = 315, width = 410)


        self.grid_propagate(0)

        self.Var_IDNo = StringVar()
        self.Var_FullName = StringVar()
        self.Var_Course = StringVar()
        self.Var_Year = StringVar()
        self.Var_Gender = StringVar()
        self._single_data_input = []

        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("UserDataDisplay.TFrame", background="#8E3E63")
        UserDataDisplay_style.configure("UserDataDisplay.TLabel", background="#8E3E63", foreground="white", font=("Lucida Sans", "16", "bold"), justify=CENTER)
        UserDataDisplay_style.configure("UserDataDisplay.TEntry", foreground="black")
        UserDataDisplay_style.configure("UserDataDisplay.TMenubutton", font=('Lucida Sans', "16", 'bold'))


        Label_IDNo = ttk.Label(self, text="ID No:", style = "UserDataDisplay.TLabel")
        Label_FullName = ttk.Label(self, text="Name:", style = "UserDataDisplay.TLabel")
        Label_Course = ttk.Label(self, text="Course:", style = "UserDataDisplay.TLabel")
        Label_Year = ttk.Label(self, text="Year:", style = "UserDataDisplay.TLabel")
        Label_Gender = ttk.Label(self, text="Gender:", style = "UserDataDisplay.TLabel")






        self.grid(row=0, column=3, rowspan = 5, padx=2, pady=2, ipadx=24, ipady=20, columnspan = 5)

        Label_IDNo.grid(row=1, column=3, pady = 20, sticky = "sw", padx=25)
        Label_FullName.grid(row=2, column=3, pady = 20, sticky = "w", padx=25)
        Label_Course.grid(row=3, column=3, pady = 20, sticky = "w", padx=15)
        Label_Year.grid(row=4, column=3, pady = 20, sticky = "w", padx=30)
        Label_Gender.grid(row=5, column=3, pady = 20, sticky = "w", padx=15)



    @property
    def single_data_input(self):

        self._single_data_input = [str(self.Var_IDNo.get()), str(self.Var_FullName.get()), str(self.Var_Course.get()), str(self.Var_Year.get()), str(self.Var_Gender.get())]
        return self._single_data_input

    @single_data_input.setter
    def single_data_input(self, value):
        self._single_data_input = value

class ButtonsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="BF.TFrame", height = 153, width = 171)

        searchvar = StringVar()

        self.grid_propagate(0)

        UserDataDisplay_style = ttk.Style()
        UserDataDisplay_style.configure("BF.TFrame", background="#8E3E63")
        UserDataDisplay_style.configure("BF.TLabel", background="#8E3E63", foreground="white", font=("Roboto Mono", "10", "bold"))

        self.grid(row=6, column=3, sticky = "nws", rowspan = 5, padx=2, pady=2, ipadx=143, ipady=20, columnspan = 5)

        Add_Button = Button(self, text="Add", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = master.master.master.add)
        Edit_Button = Button(self, text="Edit", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = master.master.master.edit_choice)
        Delete_Button = Button(self, text="Delete", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: master.master.master.delete_choice_popup())
        Search_Entry = ttk.Entry(self, textvariable=searchvar, style="UserDataDisplay.TEntry", width=25, font=('Lucida Sans', "16", 'bold'))

        def search_entry_type(event):
            try:
                master.master.master.search(searchvar.get())
            except FileNotFoundError:
                pass

        Search_Entry.bind("<KeyRelease>", search_entry_type)
        Search_Button = Button(self, text="Search", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: master.master.master.search(searchvar.get()))

        Display_Course_Button = Button(self, text= "Display Course", relief=RAISED, fg="white", bg="#8E3E63", height = 1, font=('Lucida Sans', "16", 'bold'), command = lambda: master.master.master.course_window_init())

        Add_Button.grid(row=0, column=0, padx=20, pady=20, sticky = "news")
        Edit_Button.grid(row=0, column=2, padx=48, pady=20, sticky = "news")
        Delete_Button.grid(row=0, column=4, padx=20, pady=20, sticky = "news")
        Search_Entry.grid(row=1, column=0, sticky = "ns", columnspan = 5, pady=10)
        Search_Button.grid(row=2, column=0, sticky = "ens", columnspan = 2, pady=5)
        Display_Course_Button.grid(row = 2, column = 2, pady = 5, columnspan = 3)




class App(Tk):
    def __init__(self):
        super().__init__()

        self.rex = re.compile("^[0-9]{4}[-][0-9]{4}$")

        self.IDNo = ''
        self.FullName = ''
        self.Course = ''
        self.Year = ''
        self.Gender = ''

        self.dataread_list = []
        self.index = 0

        self.filepath = ''

        self.addCheck = False
        self.editCheck = False
        self.ID_removedisplay_check = False

        self.title("Student Information System")
        self.geometry("1365x670+0+0")



        self.wm_minsize(1365, 670)
        self.wm_maxsize(1365, 670)

        self.state('zoomed')


        style = ttk.Style()
        style.configure("Treeview.Heading", rowheight = 40)
        style.configure("Treeview", rowheight = 40)

        menubar = Menu(self)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File",menu=file_menu)

        file_menu.add_command(label="Close          'Closes the program'", command = self.close_file)

        framestyle = ttk.Style()
        framestyle.configure("mainframe.TFrame", background="#D2649A")
        framestyle.configure("secondframe.TFrame", background='#D2649A')
        framestyle.configure("dataFrame.TFrame", background='white')


        mainframe = ttk.Frame(self, style="mainframe.TFrame")
        mainframe.grid(row=0, column=0, sticky = "news", rowspan = 40, columnspan = 3, ipadx=2)
        self.treeview = DatabaseDisplay(mainframe)


        secondframe = ttk.Frame(self, style="secondframe.TFrame")
        secondframe.grid(row=0, column=3, sticky = "news", rowspan = 40, ipadx=8)



        frame1 = ttk.Frame(secondframe, style="dataFrame.TFrame")
        frame1.grid(row=0, column=3, sticky = "news", rowspan=5, ipadx=0, padx = 20, ipady = 0, columnspan = 5, pady = 30)

        frame2 = ttk.Frame(secondframe, style="dataFrame.TFrame", height = 197, width = 461)
        frame2.grid(row=6, column=3, sticky = "nws", ipadx=0, padx = 20, columnspan = 5, pady = 40)

        frame2.grid_propagate(0)

        self.UserDataFrame = UserDataDisplay(frame1)
        UserButtonsFrame = ButtonsFrame(frame2) #needed to make the buttons appear on screen

        self.update_list()


        self.Entry_IDNo = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_IDNo, style="UserDataDisplay.TEntry", width=9, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))
        self.Option_Course = ttk.Entry(self.UserDataFrame, textvariable=self.UserDataFrame.Var_Course, style="UserDataDisplay.TEntry", width=8, font=('Lucida Sans', "16", 'bold'))


        self.year_tuple = ("1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year", "Irregular")
        self.Option_Year = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Year, self.year_tuple[0], *self.year_tuple)


        self.gender_tuple = ("-----", "Male", "Female", "Other")
        self.Option_Gender = ttk.OptionMenu(self.UserDataFrame, self.UserDataFrame.Var_Gender, self.gender_tuple[0], *self.gender_tuple)

        self.Button_Done = Button(self.UserDataFrame, text="Done", relief=RAISED, fg="white", bg="#141d26", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = self.doneFunc)

        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)
        self.Option_Course.grid(row=3, column=4, pady = 20, sticky = "w")

        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")

        self.Button_Done.grid(row=5, column=5, sticky="nw")

        self.before_edit_button(self.UserDataFrame)
        self.treeview.bind('<<TreeviewSelect>>', self.item_selected)

    def close_file(self):
        close_window = askyesno("Close Student Information System?", "Are you sure you want to exit?")
        if close_window:
            self.destroy()

    def item_selected(self, event):
        try:
            for student_selected in self.treeview.selection():
                item = self.treeview.item(student_selected)
                student_data = item['values']

                self.IDNo, self.FullName, self.Course, self.Year, self.Gender = student_data
                self.IDNo = str(self.IDNo)
                self.FullName = str(self.FullName)

                course_list = []
                mycursor.execute("SELECT coursecode, course_name FROM Course")
                for x in mycursor:
                    course_list.append(x)
                course_dict = dict(course_list)
                if str(self.Course) in course_dict:
                    self.Course = course_dict[str(self.Course)]

                self.Course = str(self.Course)
                self.Year = str(self.Year)
                self.Gender = str(self.Gender)
                student_data = [self.IDNo, self.FullName, self.Course, self.Year, self.Gender]

                self.IDNo_DataDisplay.config(text=self.IDNo)
                self.FullName_DataDisplay.config(text=self.FullName)
                self.Course_DataDisplay.config(text=self.Course)
                self.Year_DataDisplay.config(text=self.Year)
                self.Gender_DataDisplay.config(text=self.Gender)

                return student_data

        except TclError:
            pass


    def course_window_init(self):
        course_window = Toplevel(self, bg="#243447")
        course_window.geometry("500x500")
        course_window.grid_propagate(0)

        course_window.grid_columnconfigure(0, weight=1)
        course_window.grid_rowconfigure(0, weight=1)

        self.cinput = StringVar()

        self.course_treeview = ttk.Treeview(course_window, columns=('course_code', 'course_name'), show="headings", height = 5, style = "Treeview")


        self.course_treeview.heading('#0', text='', anchor=CENTER)
        self.course_treeview.heading('course_code', text='Code')
        self.course_treeview.heading('course_name', text='Name')


        self.course_treeview.column('#0', width=0, stretch=NO)
        self.course_treeview.column('course_code', width=5, minwidth= 1)
        self.course_treeview.column('course_name', width=250, minwidth= 1)


        self.course_treeview.grid(row=0, column=0, sticky = "nsew")

        scrollbars = ttk.Scrollbar(course_window, orient=VERTICAL, command=self.course_treeview.yview, cursor='sb_v_double_arrow')
        self.course_treeview.configure(yscroll=scrollbars.set)

        scrollbars.grid(row=0, column=1, sticky='ns',)

        course_buttons_frame = Frame(course_window, width = 100, height = 500, bg = "#243447")
        course_buttons_frame.grid(row = 0, column = 2)
        course_buttons_frame.pack_propagate(False)

        Label(course_buttons_frame, bg = "#243447", text = '').pack(pady=20)
        Button(course_buttons_frame, text = "Add", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.addcourse(course_window)).pack(padx = 10, pady = 20)
        Button(course_buttons_frame, text = "Edit", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.editcourse(course_window)).pack(padx = 10, pady = 20)
        Button(course_buttons_frame, text = "Delete", relief=RAISED, fg="white", bg="#8E3E63", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.delcourse(course_window)).pack(padx = 10, pady = 20)
        

        self.course_treeview.bind('<<TreeviewSelect>>', self.course_selected)

        self.courseDisplay()


    def courseDisplay(self):

        global db, mycursor
        course_list = []

        for i in self.course_treeview.get_children():
            self.course_treeview.delete(i)

        mycursor.execute("SELECT * FROM Course")
        for x in mycursor:
            course_list.append(x)




        count = 1
        for element in course_list:
            rowid = 'I' + str('{:03}'.format(count))
            self.course_treeview.insert('', END, iid=rowid, values=element)
            count += 1


    def course_selected(self, event):
        course_row = ''
        for items in self.course_treeview.selection():
            course_row = self.course_treeview.item(items)
            course_row = course_row['values']

        return course_row

    def editcourse(self, course_window):

        coursename_entry = StringVar()
        coursecode_entry = StringVar()

        editcourse_selected = self.course_selected("<<TreeviewSelect>>")
        initial_ccode = editcourse_selected[0]

        editcourse_Toplevel = Toplevel(self, bg="#243447")
        editcourse_Toplevel.geometry("400x200")
        editcourse_Toplevel.pack_propagate(False)

        rowa = Frame(editcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowa.pack(anchor = "w")
        rowa.pack_propagate(False)
        rowb = Frame(editcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowb.pack(anchor = "w")
        rowb.pack_propagate(False)
        rowc = Frame(editcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowc.pack(anchor = "w")
        rowc.pack_propagate(False)
        rowd = Frame(editcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowd.pack(anchor = "w")
        rowd.pack_propagate(False)


        Label(rowa, fg = "white", bg = "#243447", text = 'Edit Course', font=('Lucida Sans', "16", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowb, fg = "white", bg = "#243447", text = 'Course Code: ', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowc, fg = "white", bg = "#243447", text = 'Course Name:', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)

        Entry(rowb, width = 5, font=('Lucida Sans', "16", 'bold'), textvariable = coursecode_entry).pack(side = LEFT, padx = 10, anchor = "w")
        Entry(rowc, width = 15, font=('Lucida Sans', "16", 'bold'), textvariable = coursename_entry).pack(side = LEFT, padx = 10, anchor = "w")

        coursecode_entry.set(editcourse_selected[0])
        coursename_entry.set(editcourse_selected[1])

        Button(rowd, text = "Edit", relief=RAISED, fg="white", bg="#141d26", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.editcourse_confirm(editcourse_Toplevel, coursecode_entry, coursename_entry, course_window, initial_ccode)).pack(side = LEFT, padx = 10)

    def editcourse_confirm(self, courseedit, ccode, cname, course_window, initial_ccode):
        try:
            # Retrieve the new course code and course name from the entry fields
            new_ccode = ccode.get()
            new_cname = cname.get()

            # Check if the new course code already exists in the database, but is not the current course being edited
            check_query = "SELECT COUNT(*) FROM Course WHERE coursecode = ? AND coursecode != ?"
            mycursor.execute(check_query, (new_ccode, initial_ccode))
            result = mycursor.fetchone()

            if result[0] > 0:
                # If the course code already exists, show a warning and do not proceed with the update
                showwarning("Duplicate Course Code", "The course code that you entered already exists.")
            else:
                # Check if there are any students enrolled in the course being edited
                student_check_query = "SELECT COUNT(*) FROM Student WHERE coursecode = ?"
                mycursor.execute(student_check_query, (initial_ccode,))
                student_result = mycursor.fetchone()

                if student_result[0] > 0:
                    # If there are students enrolled, show a warning and do not proceed with the update
                    showwarning("Enrolled Students", "There are students enrolled in this course. Please unenroll them before editing the course.")
                else:
                    # Begin a transaction if no transaction is already in progress
                    if not db.in_transaction:
                        db.start_transaction()

                    try:
                        # Update the Course table
                        update_course_query = "UPDATE Course SET coursecode = ?, course_name = ? WHERE coursecode = ?"
                        mycursor.execute(update_course_query, (new_ccode, new_cname, initial_ccode))

                        # Commit the transaction
                        db.commit()

                        showinfo("Success", f"'{initial_ccode}' has been successfully edited to '{new_ccode}'.")
                        self.courseDisplay()  # Update the course display after successful edit

                    except mysql.connector.Error as err:
                        # Roll back the transaction if an error occurs
                        db.rollback()
                        showwarning("Error", f"Failed to update course. {err}")

            # Focus back on the course window and destroy the edit course window
            course_window.focus()
            courseedit.destroy()

        except mysql.connector.errors.InterfaceError as e:
            showwarning("Database Error", str(e))
            course_window.focus()
        except Exception as e:
            showwarning("Error", str(e))
            course_window.focus()





    def delcourse(self, course_window):
        course_delete_warn = askyesno(title = "Delete?", message = "Are you sure you want to delete the selected row?")

        if course_delete_warn:
            self.delcourse_confirm(course_window)

    def delcourse_confirm(self, course_window):
        ccode = self.course_selected("<<TreeviewSelect>>")
        ccode = ccode[0]

        # Update coursecode to NULL for students enrolled in the course being deleted
        update_student_query = "UPDATE Student SET coursecode = NULL WHERE coursecode = ?"
        mycursor.execute(update_student_query, (ccode,))

        # Delete the course from the Course table
        sql_query = "DELETE FROM Course WHERE coursecode = ?"
        try:
            mycursor.execute(sql_query, (ccode,))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            showwarning("Error", f"Failed to delete course. {err}")

        # Update any NULL coursecode values in the Student table to 'N/A'
        update_null_coursecode_query = "UPDATE Student SET coursecode = 'N/A' WHERE coursecode IS NULL"
        mycursor.execute(update_null_coursecode_query)
        db.commit()

        showinfo("Success", f"'{ccode}' has been successfully removed from the courses.")
        course_window.focus()
        self.courseDisplay()
        self.update_list()



    def addcourse(self, course_window):


        coursename_entry = StringVar()
        coursecode_entry = StringVar()

        addcourse_Toplevel = Toplevel(self, bg="#243447")
        addcourse_Toplevel.geometry("400x200")
        addcourse_Toplevel.pack_propagate(False)

        rowa = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowa.pack(anchor = "w")
        rowa.pack_propagate(False)
        rowb = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowb.pack(anchor = "w")
        rowb.pack_propagate(False)
        rowc = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowc.pack(anchor = "w")
        rowc.pack_propagate(False)
        rowd = Frame(addcourse_Toplevel, bg = "#243447", width = 400, height = 50)
        rowd.pack(anchor = "w")
        rowd.pack_propagate(False)


        Label(rowa, fg = "white", bg = "#243447", text = 'Add Course', font=('Lucida Sans', "16", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowb, fg = "white", bg = "#243447", text = 'Course Code: ', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)
        Label(rowc, fg = "white", bg = "#243447", text = 'Course Name:', font=('Lucida Sans', "14", 'bold')).pack(side = LEFT, padx = 10)

        Entry(rowb, width = 5, font=('Lucida Sans', "16", 'bold'), textvariable = coursecode_entry).pack(side = LEFT, padx = 10, anchor = "w")
        Entry(rowc, width = 15, font=('Lucida Sans', "16", 'bold'), textvariable = coursename_entry).pack(side = LEFT, padx = 10, anchor = "w")

        Button(rowd, text = "Add", relief=RAISED, fg="white", bg="#141d26", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.addcourse_confirm(addcourse_Toplevel, coursecode_entry, coursename_entry, course_window)).pack(side = LEFT, padx = 10)

    def addcourse_confirm(self, coursetop, ccode, cname, course_window):
        try:
            coursetop.destroy()


            ccode = ccode.get()
            cname = cname.get()



            sql_query = "INSERT INTO Course (coursecode, course_name) VALUES (?, ?)"
            courseholder = (ccode, cname)
            mycursor.execute(sql_query, courseholder)
            db.commit()

            showinfo("Success", f"'{ccode}' has been successfully added from the courses.")
            course_window.focus()
            self.courseDisplay()
        except mysql.connector.errors.InterfaceError:
            showwarning("Invalid Input", "The course code that you entered already exists.")
            course_window.focus()

    def add(self):
        if not self.addCheck:
            if not self.editCheck:
                self.UserDataFrame.Var_IDNo.set('')
                self.UserDataFrame.Var_FullName.set('')
                self.UserDataFrame.Var_Course.set('')
                self.UserDataFrame.Var_Year.set('')
                self.UserDataFrame.Var_Gender.set('')


                self.after_edit_button(self.UserDataFrame, "add")
                self.addCheck = True



    def get_input(self):
        global db, mycursor


        x = self.UserDataFrame.single_data_input

        sql_query = "INSERT INTO Student (studentID, studentName, coursecode, year, gender) VALUES (?, ?, ?, ?, ?)"
        mycursor.execute(sql_query, (x))
        db.commit()
        self.update_list()
        self.before_edit_button(self.UserDataFrame)
        self.IDNo_DataDisplay.config(text=self.UserDataFrame.Var_IDNo.get())
        self.FullName_DataDisplay.config(text=self.UserDataFrame.Var_FullName.get())
        self.Course_DataDisplay.config(text=self.UserDataFrame.Var_Course.get())
        self.Year_DataDisplay.config(text=self.UserDataFrame.Var_Year.get())
        self.Gender_DataDisplay.config(text=self.UserDataFrame.Var_Gender.get())

    def update_list(self):
        global db, mycursor
        student_list = []

        mycursor.execute("SELECT * FROM Student")
        for x in mycursor:
            student_list.append(x)
        self.treeview.treeview_update(student_list)

    def doneFunc(self, check, edit_IDNo):
        global db, mycursor

        try:
            if not self.rex.match(self.UserDataFrame.Var_IDNo.get()):
                raise IDInvalid
        except IDInvalid:
                showerror("Invalid Input for ID", "Invalid Input. \nID must be in \nYYYY-NNNN format.")
                return
        except mysql.connector.errors.InterfaceError:
                showerror("Invalid Input", "The course code that you entered already exists.")
                return
            

        if check == "add":
            self.addCheck = False
            self.editCheck = False
            self.ID_removedisplay_check = False
            self.get_input()

        elif check == "edit":
            self.addCheck = False
            self.editCheck = False
            self.ID_removedisplay_check = False
            x = self.UserDataFrame.single_data_input
            sql_query = "UPDATE Student SET studentID = ?, studentName = ?, coursecode = ?, year = ?, gender = ? WHERE studentID = ?"
            try:
                mycursor.execute(sql_query, tuple(x + [edit_IDNo]))
                db.commit()
            except:
                showwarning("Invalid ID", f"{x[0]} already exists. Please add a new student ID.")



            self.before_edit_button(self.UserDataFrame)

            self.update_list()
            self.IDNo_DataDisplay.config(text=self.UserDataFrame.Var_IDNo.get())
            self.FullName_DataDisplay.config(text=self.UserDataFrame.Var_FullName.get())
            self.Course_DataDisplay.config(text=self.UserDataFrame.Var_Course.get())
            self.Year_DataDisplay.config(text=self.UserDataFrame.Var_Year.get())
            self.Gender_DataDisplay.config(text=self.UserDataFrame.Var_Gender.get())
            edit_IDNo = ""

    def after_edit_button(self, classObj, type="", edit_IDNo=""):
        global db, mycursor

        sql_query = "SELECT coursecode from Course"
        mycursor.execute(sql_query)
        course_tuple = ()

        for x in mycursor:
            course_tuple += x


        self.IDNo_DataDisplay.destroy()
        self.FullName_DataDisplay.destroy()
        self.Course_DataDisplay.destroy()
        self.Year_DataDisplay.destroy()
        self.Gender_DataDisplay.destroy()


        self.Entry_IDNo = ttk.Entry(classObj, textvariable=classObj.Var_IDNo, style="UserDataDisplay.TEntry", width=10, font=('Lucida Sans', "16", 'bold'))
        self.Entry_FullName = ttk.Entry(classObj, textvariable=classObj.Var_FullName, style="UserDataDisplay.TEntry", width=20, font=('Lucida Sans', "16", 'bold'))

        self.Option_Course = ttk.OptionMenu(classObj, classObj.Var_Course, None, *course_tuple, style = "UserDataDisplay.TMenubutton")
        self.Option_Year = ttk.OptionMenu(classObj, classObj.Var_Year, self.year_tuple[0], *self.year_tuple, style = "UserDataDisplay.TMenubutton")
        self.Option_Gender = ttk.OptionMenu(classObj, classObj.Var_Gender, self.gender_tuple[0], *self.gender_tuple, style = "UserDataDisplay.TMenubutton")


        self.Button_Done = Button(classObj, text="Done", relief=RAISED, fg="white", bg="#141d26", height = 1, width = 6, font=('Lucida Sans', "16", 'bold'), command = lambda: self.doneFunc(type, edit_IDNo))

        self.Entry_IDNo.grid(row=1, column=4, pady = 20, sticky = "w")
        self.Entry_FullName.grid(row=2, column=4, pady = 20, sticky = "w", columnspan = 2)


        self.Option_Course.grid(row=3, column=4, pady = 20, sticky = "w")
        self.Option_Year.grid(row=4, column=4, pady = 20, sticky = "w")
        self.Option_Gender.grid(row=5, column=4, pady = 20, sticky = "w")


        #code for preinserting of YYYY-NNNN format when clicking add button
        if type == "add":
            classObj.Var_IDNo.set("YYYY-NNNN")
            def ID_removedisplay(event):
                if not self.ID_removedisplay_check:
                    if classObj.Var_IDNo.get() == "YYYY-NNNN":
                        event.widget.delete(0, END)
                    self.ID_removedisplay_check = True
            self.Entry_IDNo.bind("<Button-1>", ID_removedisplay)

        self.Button_Done.grid(row=5, column=5, sticky="e")



    def before_edit_button(self, classObj):

        self.Entry_IDNo.destroy()
        self.Entry_FullName.destroy()
        self.Option_Course.destroy()
        self.Option_Year.destroy()
        self.Option_Gender.destroy()
        self.Button_Done.destroy()

        self.IDNo_DataDisplay = ttk.Label(classObj, text=self.IDNo, style = "UserDataDisplay.TLabel")
        self.FullName_DataDisplay = ttk.Label(classObj, text=self.FullName, style = "UserDataDisplay.TLabel")
        self.Course_DataDisplay = ttk.Label(classObj, text=self.Course, style = "UserDataDisplay.TLabel")
        self.Year_DataDisplay = ttk.Label(classObj, text=self.Year, style = "UserDataDisplay.TLabel")
        self.Gender_DataDisplay = ttk.Label(classObj, text=self.Gender, style = "UserDataDisplay.TLabel")

        self.IDNo_DataDisplay.grid(row=1, column=4, pady = 20, sticky = "ew", padx=5)
        self.FullName_DataDisplay.grid(row=2, column=4, pady = 20, sticky = "ew", padx=5)
        self.Course_DataDisplay.grid(row=3, column=4, pady = 20, sticky = "ew", padx=5)
        self.Year_DataDisplay.grid(row=4, column=4, pady = 20, sticky = "ew", padx=5)
        self.Gender_DataDisplay.grid(row=5, column=4, pady = 20, sticky = "ew", padx=5)


    def edit_choice(self):
        global mycursor, db
        if not self.editCheck:
            if not self.addCheck:
                edit_list = self.item_selected('<<TreeviewSelect>>')



                sql_query = "SELECT * FROM Student WHERE studentID = ?"
                mycursor.execute(sql_query, (edit_list[0], ))

                for x in mycursor:
                    edit_list[2] = x[2]

                edit_IDNo = edit_list[0]

                self.UserDataFrame.Var_IDNo.set(edit_list[0])
                self.UserDataFrame.Var_FullName.set(edit_list[1])
                self.UserDataFrame.Var_Course.set(edit_list[2])

                self.after_edit_button(self.UserDataFrame, "edit", edit_IDNo)

                self.UserDataFrame.Var_Year.set(edit_list[3])
                self.UserDataFrame.Var_Gender.set(edit_list[4])
                self.editCheck = True


    def delete_choice_popup(self):
        if not self.editCheck and not self.addCheck:
            try:
                delete_list = self.item_selected('<<TreeviewSelect>>')
                self.UserDataFrame.Var_IDNo.set(delete_list[0])

                delete_warn_widget = askyesno(title = "Delete?", message = "Are you sure you want to delete the selected row?")

                if delete_warn_widget:
                    self.delete_choice()


            except FileNotFoundError:
                showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")
            except TypeError:
                showwarning("Error", "Choose a row first before clicking 'Delete'.")
            except TclError:
                pass



    def delete_choice(self):
        global db, mycursor
        delete_list = self.item_selected('<<TreeviewSelect>>')

        sql_query = "DELETE FROM Student WHERE studentID = ?"
        mycursor.execute(sql_query, (delete_list[0],))
        db.commit()

        self.IDNo_DataDisplay.config(text='')
        self.FullName_DataDisplay.config(text='')
        self.Course_DataDisplay.config(text='')
        self.Year_DataDisplay.config(text='')
        self.Gender_DataDisplay.config(text='')
        self.update_list()


    def search(self, search_input):
        if search_input == '':
            self.update_list()
        try:
            search_display = []
            self.treeview.selection_set()
            search_input = "^" + search_input

            sql_query = "SELECT * FROM Student WHERE studentID REGEXP ? OR studentName REGEXP ?"
            searchinput = [search_input]
            searchinput.append(search_input)



            mycursor.execute(sql_query, searchinput)
            for x in mycursor:
                search_display.append(x)


            self.treeview.treeview_update(search_display)
            try:
                self.treeview.selection_set('I001')
            except TclError:
                pass

        except FileNotFoundError:
            showwarning("No files opened", "Create/Open a file first.\nClick 'File' on the top-left corner.")

if __name__ == '__main__':
    app = App()
    app.mainloop()
