import sqlite3
from tkinter import *
from tkcalendar import DateEntry


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Správa židovství")
        self.minsize(640, 400)

        self.button = Button(self, text="Záznam činností", command=self.test).pack()

    def test(self):
        JobRecord()


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
        self.name_entry = Entry(self, width=20).grid(row=2, column=1, columnspan=3)

        self.from_label = Label(self, text="Od").grid(row=3, column=0)
        self.from_hour_entry = Spinbox(self, from_=0, to=23, width=3).grid(row=3, column=1)
        self.from_dot = Label(self, text=":", width=1).grid(row=3, column=2)
        self.from_min_entry = Spinbox(self, from_=0, to=59, width=3).grid(row=3, column=3)

        self.to_label = Label(self, text="Do").grid(row=4, column=0)
        self.to_hour_entry = Spinbox(self, from_=0, to=23, width=3).grid(row=4, column=1)
        self.to_dot = Label(self, text=":", width=1).grid(row=4, column=2)
        self.to_min_entry = Spinbox(self, from_=0, to=59, width=3).grid(row=4, column=3)

        self.company_label = Label(self, text="Firma").grid(row=5, column=0)
        mb = Menubutton(self, text="Firma", relief=RAISED)
        mb.grid()
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        radio_menu = 56454
        dbCursor.execute('''SELECT company_id, company_name FROM COMPANY WHERE active==1''')
        data = dbCursor.fetchall()
        for record in data:
            mb.menu.add_radiobutton(label=record[1], variable=radio_menu, value=record[0])
        mb.grid(row=5, column=1, columnspan=3)

    def company_record(self):
        CompanyRecord()


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
            self.error_label = Label(self, text="Úspěšně zapsáno").grid(row=5)
            JobRecord().destroy()
        except ValueError:
            self.error_label = Label(self, text="Vstup je v nesprávném formátu").grid()


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
            [work_start] time, 
            [work_end] time,
            [company_name] INTEGER NOT NULL, 
            FOREIGN KEY (company_name) REFERENCES COMPANY (company_id))''')


setup()
root = Root()
root.mainloop()
