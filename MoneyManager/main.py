import sqlite3
from tkinter import *
from tkcalendar import DateEntry


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Správa židovství")
        self.minsize(640, 400)

        self.button = Button(self, text="Záznam činností", command=self.test).pack()
        self.button2 = Button(self, text="Dluhy", command=self.dlugy).pack()

    def test(self):
        JobRecord()

    def dlugy(self):
        debtWindow()


class JobRecord(Toplevel):
    def __init__(self):
        super(JobRecord, self).__init__()
        self.title("Zápis pracovní činnosti")
        self.company_button = Button(self, text="Zapsání firmy", command=self.company_record).grid(row=0, column=0)

        self.cal_label = Label(self, text="Datum").grid(row=1, column=0)
        self.cal = DateEntry(self, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        self.cal.grid(padx=10, pady=10, row=1, column=1, columnspan=3)

        self.name_label = Label(self, text="Název činnosti").grid(row=2, column=0)
        self.name_entry = Entry(self, width=20)
        self.name_entry.grid(row=2, column=1, columnspan=3)

        self.from_label = Label(self, text="Od").grid(row=3, column=0)
        self.from_hour_entry = Spinbox(self, from_=0, to=23, width=3)
        self.from_hour_entry.grid(row=3, column=1)
        self.from_dot = Label(self, text=":", width=1).grid(row=3, column=2)
        self.from_min_entry = Spinbox(self, from_=0, to=59, width=3)
        self.from_min_entry.grid(row=3, column=3)

        self.to_label = Label(self, text="Do").grid(row=4, column=0)
        self.to_hour_entry = Spinbox(self, from_=0, to=23, width=3)
        self.to_hour_entry.grid(row=4, column=1)
        self.to_dot = Label(self, text=":", width=1).grid(row=4, column=2)
        self.to_min_entry = Spinbox(self, from_=0, to=59, width=3)
        self.to_min_entry.grid(row=4, column=3)

        self.company_label = Label(self, text="Firma").grid(row=5, column=0)
        mb = Menubutton(self, text="Firma", relief=RAISED)
        mb.grid()
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        self.radio_menu = IntVar()
        dbCursor.execute('''SELECT company_id, company_name FROM COMPANY WHERE active==1''')
        data = dbCursor.fetchall()
        for record in data:
            mb.menu.add_radiobutton(label=record[1], variable=self.radio_menu, value=record[0])
        mb.grid(row=5, column=1, columnspan=3)
        self.submit = Button(self, text="Zapsat", command=self.submit).grid(row=6, column=1, columnspan=3)

    def company_record(self):
        CompanyRecord()

    def submit(self):
        job_date = self.cal.get()
        job_name = self.name_entry.get()
        job_from = int(self.from_hour_entry.get()) + int(self.from_min_entry.get()) / 60
        job_to = int(self.to_hour_entry.get()) + int(self.to_min_entry.get()) / 60
        job_company = self.radio_menu.get()
        print(job_company)
        dbCursor.execute('''INSERT INTO JOBS (work_date, work_name, work_start, work_end, company_name)
        VALUES (?, ?, ?, ?, ?)''', (job_date, job_name, job_from, job_to, job_company))
        dbConnect.commit()


class CompanyRecord(Toplevel):
    def __init__(self):
        super(CompanyRecord, self).__init__()
        self.title("Zápis firmy")

        self.comp_label = Label(self, text="Název firmy")
        self.comp_label.grid(row=0, column=0)
        self.comp_entry = Entry(self, width=20)
        self.comp_entry.grid(row=0, column=1)

        self.year_label = Label(self, text="Rok zápisu")
        self.year_label.grid(row=1, column=0)
        self.year_entry = Entry(self, width=20)
        self.year_entry.grid(row=1, column=1)

        self.money_label = Label(self, text="Hodinová mzda")
        self.money_label.grid(row=2, column=0)
        self.money_entry = Entry(self, width=20)
        self.money_entry.grid(row=2, column=1)

        self.break_label = Label(self, text="Pauza")
        self.break_label.grid(row=3, column=0)
        self.break_entry = Entry(self, width=20)
        self.break_entry.grid(row=3, column=1)

        self.submit_button = Button(self, text="Uložit", command=self.save_company)
        self.submit_button.grid(row=4, column=1)
        self.error_label = Label(self).grid(row=5)

    def save_company(self):
        company_name = self.comp_entry.get() + " " + self.year_entry.get()
        try:
            company_money = int(self.money_entry.get())
            company_break = int(self.break_entry.get())
            dbCursor.execute('''INSERT INTO COMPANY (company_name, money_per_hour, break) VALUES (?,?,?)''',
                             (company_name, company_money, company_break))
            dbConnect.commit()
            self.comp_entry.delete(0, 'end')
            self.year_entry.delete(0, 'end')
            self.money_entry.delete(0, 'end')
            self.break_entry.delete(0, 'end')
            self.error_label.configure(text="Úspěšně zapsáno")
            JobRecord().destroy()
        except ValueError:
            self.error_label.configure(text="Vstup je v nesprávném formátu")


class debtWindow(Toplevel):
    def __init__(self):
        super(debtWindow, self).__init__()
        self.title("Dluhy")

        self.record_button = Button(self, text="Zápis", command=self.record_debt_window).grid(row=0)
        self.refresh_button = Button(self, text="Refresh", command=self.reshresof).grid(row=0, column=1)
        self.les_button = Button(self, text="Zapsat", command=self.update_paid).grid(row=0, column=2)

        dbCursor.execute('''SELECT * FROM DEBT''')
        data = dbCursor.fetchall()
        self.array_id = []
        i = 1
        for person in data:
            j = 0
            self.array_id.append(IntVar())
            check = Checkbutton(self, variable=self.array_id[i - 1], offvalue=-1, onvalue=person[0]).grid(row=i,
                                                                                                          column=0)
            for record in person:
                cell = Label(self, text=record).grid(row=i, column=j + 1)
                j += 1
            i += 1
        print(self.array_id)

    def update_paid(self):
        select_array = []
        for pes in self.array_id:
            select_array.append(int(pes.get()))
            try:
                select_array.remove(0)
            except ValueError:
                pass

        for pes in select_array:
            print(pes)
        for element in select_array:
            dbCursor.execute(f'''SELECT debt_paid FROM DEBT WHERE debt_id == {element}''')
            test = dbCursor.fetchone()
            element2 = test[0]
            print(element2)
            if element2 == 1:
                dbCursor.execute('''UPDATE DEBT SET debt_paid = ? WHERE debt_id == ?''', (0, element))
                dbConnect.commit()
            elif element2 == 0:
                dbCursor.execute('''UPDATE DEBT SET debt_paid = ? WHERE debt_id == ?''', (1, element))
                dbConnect.commit()

    def record_debt_window(self):
        debtRecordWindow()

    def reshresof(self):
        self.destroy()
        debtWindow()


class debtRecordWindow(Toplevel):
    def __init__(self):
        super(debtRecordWindow, self).__init__()
        self.title("Zapsání dluhů")

        self.cal_label = Label(self, text="Datum").grid(row=0, column=0)
        self.cal = DateEntry(self, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        self.cal.grid(padx=10, pady=10, row=0, column=1, columnspan=3)

        self.name_label = Label(self, text="Název").grid(row=1, column=0)
        self.name_entry = Entry(self, width=20)
        self.name_entry.grid(row=1, column=1, columnspan=3)

        self.fname_label = Label(self, text="Jméno").grid(row=2, column=0)
        self.fname_entry = Entry(self, width=20)
        self.fname_entry.grid(row=2, column=1, columnspan=3)

        self.lname_label = Label(self, text="Přijmení").grid(row=3, column=0)
        self.lname_entry = Entry(self, width=20)
        self.lname_entry.grid(row=3, column=1, columnspan=3)

        self.money_label = Label(self, text="Peníze").grid(row=4, column=0)
        self.money_entry = Entry(self, width=20)
        self.money_entry.grid(row=4, column=1, columnspan=3)

        self.submit = Button(self, text="Uložit", command=self.submit_result).grid(row=5, column=1)

    def submit_result(self):
        debt_date = self.cal.get()
        debt_name = self.name_entry.get()
        debt_fname = self.fname_entry.get()
        debt_lname = self.lname_entry.get()
        debt_money = self.money_entry.get()
        self.delete_all()

        dbCursor.execute('''INSERT INTO DEBT (debt_date, debt_text, debt_name, debt_lname, debt_money)
        VALUES (?, ?, ?, ?, ?)''', (debt_date, debt_name, debt_fname, debt_lname, debt_money))
        dbConnect.commit()
        debtWindow.reshresof(debtWindow())

    def delete_all(self):
        self.cal.delete(0, END)
        self.name_entry.delete(0, END)
        self.fname_entry.delete(0, END)
        self.lname_entry.delete(0, END)
        self.money_entry.delete(0, END)


dbConnect = sqlite3.Connection('identifier.sqlite')
dbCursor = dbConnect.cursor()


def setup():
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS COMPANY
            ([company_id] INTEGER PRIMARY KEY,
            [company_name] text NOT NULL,
            [money_per_hour] integer NOT NULL ,
            [active] boolean DEFAULT 1 NOT NULL,
            [break] integer DEFAULT 0 NOT NULL)''')
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS JOBS
            ([jobs_id] INTEGER PRIMARY KEY,
            [work_date] date,
            [work_name] text,
            [work_start] float, 
            [work_end] float,
            [paid] boolean DEFAULT 0 NOT NULL,
            [company_name] INTEGER NOT NULL, 
            FOREIGN KEY (company_name) REFERENCES COMPANY (company_id))''')
    dbCursor.execute('''CREATE TABLE IF NOT EXISTS DEBT
                    ([debt_id] INTEGER PRIMARY KEY,
                    [debt_date] date,
                    [debt_text] text,
                    [debt_name] text,
                    [debt_lname] text,
                    [debt_money] integer NOT NULL,
                    [debt_paid] boolean DEFAULT 0 NOT NULL
                    )''')


setup()
root = Root()
root.mainloop()
