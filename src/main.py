'''
Ben's Equipment Maintenance Manager

Author:  Ben Johnson
Version: 0.3
'''

import time
from datetime import datetime, timedelta, timezone
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from db_manager import DBManager, Equipment, MaintenanceItem, MaintenanceDate


complete_emoji = '✅'
incomplete_emoji = '❌'


class Bemm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # dope variables
        self.equipment_map = {}
        self.mi_map = {}
        self.md_map = {}

        # db things
        self.db = DBManager('db.sqlite3')

        self.current_equipment = None
        self.get_equipment_values()

        self.create_widgets()

    def get_equipment_values(self):
        self.equipment = self.db.get_all_equipment()
        self.equipment_map = {}
        for eq in self.equipment:
            self.equipment_map[eq.name] = eq

    def create_widgets(self):
        self.widgets = {}
        self.labels = {}

        '''
        Frames
        '''
        equipframe = ttk.Frame(self, borderwidth=2, relief="groove")
        miframe = ttk.Frame(self, borderwidth=2, relief="groove")
        infoframe = ttk.Frame(self, borderwidth=2, relief="groove")
        self.widgets['equipframe'] = equipframe
        self.widgets['miframe'] = miframe
        self.widgets['infoframe'] = infoframe


        '''
        Labels
        '''
        self.labels['info'] = tk.StringVar()
        self.labels['info'].set("Info for: ")

        self.widgets['equiptreelabel'] = ttk.Label(self, text="Equipment")
        self.widgets['mitreelabel'] = ttk.Label(self, text="Maintenance Items")
        self.widgets['infolabel'] = ttk.Label(self, textvariable=self.labels['info'])

        '''
        Trees
        '''
        equiptree = ttk.Treeview(equipframe, show='tree')
        equiptree.heading("#0",text="Equipment", anchor=tk.W)
        equiptree.bind('<1>', self.equip_click)
        self.update_equipment_tree(equiptree)
        self.widgets['equiptree'] = equiptree

        mitree = ttk.Treeview(miframe)
        mitree['columns'] = ('numdays', 'idk')
        mitree.column("#0", width=270)
        mitree.column("numdays", width=100)
        mitree.heading('#0',text='Name',anchor=tk.W)
        mitree.heading('numdays',text='# Days',anchor=tk.W)
        mitree.bind('<1>', self.item_click)
        self.widgets['mitree'] = mitree

        histtree = ttk.Treeview(infoframe)
        histtree['columns'] = ('due')
        histtree.column('#0', width=20)
        histtree.column('due', width=100)
        histtree.heading('#0',text='Completed',anchor=tk.W)
        histtree.heading('due',text='Due Date',anchor=tk.W)
        histtree.bind('<Double-1>', self.date_click)
        self.widgets['histtree'] = histtree

        '''
        Buttons
        '''
        self.widgets['addequipbutt'] = ttk.Button(equipframe, text="Add New Equipment")
        self.widgets['addequipbutt']['command'] = self.add_equipment

        self.widgets['addmibutt'] = ttk.Button(miframe, text="Add new Maintenance Item")
        self.widgets['addmibutt']['command'] = self.add_mi

        self.widgets['setdate'] = ttk.Button(infoframe, text='Set Date')
        self.widgets['setdate']['command'] = self.add_date
        self.widgets['calendar'] = DateEntry(infoframe, width=12, background='gray',
                                             foreground='white', borderwidth=2)

        '''
        DISPLAY
        '''

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=3)
        tk.Grid.columnconfigure(self, 2, weight=2)

        tk.Grid.rowconfigure(infoframe, 1, weight=1)
        tk.Grid.columnconfigure(infoframe, 0, weight=1)

        # equip frame
        self.widgets['equiptreelabel'].grid(column=0, row=0, sticky='w')
        equipframe.grid(column=0, row=1, sticky='nsew')
        tk.Grid.rowconfigure(equipframe, 1, weight=1)
        tk.Grid.columnconfigure(equipframe, 1, weight=1)
        self.widgets['addequipbutt'].grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        equiptree.grid(column=0, columnspan=2, row=1, padx=10, pady=(0, 10), sticky='nsew')

        # maintenance item frame
        miframe.grid(column=1, row=1, padx=10, sticky='nsew')
        tk.Grid.rowconfigure(miframe, 1, weight=1)
        tk.Grid.columnconfigure(miframe, 1, weight=1)
        self.widgets['addmibutt'].grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        mitree.grid(column=0, columnspan=2, row=1, padx=10, pady=(0, 10), sticky='nsew')

        # row 0
        self.widgets['mitreelabel'].grid(column=1, row=0, padx=(10, 0), sticky='w')
        self.widgets['infolabel'].grid(column=2, row=0, sticky='w')

        # row 1

        # row 2

        # info area
        infoframe.grid(column=2, row=1, rowspan=2, ipadx=10, ipady=10, sticky='nsew')
        histtree.grid(column=0, row=1, columnspan=2, padx=10, pady=(0, 10), sticky='nsew')
        self.widgets['calendar'].grid(column=0, row=0, padx=(10, 0), pady=10, sticky='w')
        self.widgets['setdate'].grid(column=1, row=0, padx=(10, 0), pady=10)


    def add_equipment(self):
        answer = simpledialog.askstring("New", "Enter Equipment Name", parent=self)

        if not answer:
            return

        self.db.insert_equipment(answer)
        self.get_equipment_values()
        self.update_equipment_tree(self.widgets['equiptree'])

    def add_mi(self):
        if self.current_equipment is None:
            messagebox.showerror('Failed', 'Select an equipment entry to add an item')
            return

        op_name = simpledialog.askstring('New', 'Enter New Maintenance Item')
        if op_name is None:
            return

        num_days = simpledialog.askinteger('New', 'Enter number of days between servicing')
        if num_days is None:
            return

        self.db.insert_maintenance_item(op_name, num_days, self.current_equipment)
        self.update_mi_tree(self.widgets['mitree'], self.current_equipment)

    '''
    Update trees
    '''
    def update_equipment_tree(self, tree):
        self.clear_tree(tree)

        for i in list(self.equipment_map.keys()):
            tree.insert('', 0, '', text=i, tags=(i,))

    def update_mi_tree(self, tree, equipment):
        self.clear_tree(tree)
        self.clear_tree(self.widgets['histtree'])
        self.mi_map = {}

        mi_list = self.db.get_all_maintenance_items(equipment)

        for i in mi_list:
            self.mi_map[i.name] = i
            tree.insert('', 0, '', text=i.name, values=(i.numdays))

    def update_hist_tree(self):
        tree = self.widgets['histtree']
        dates = self.db.get_all_maintenance_dates(self.current_item)
        print('here then')
        print(tree)
        # get all dates
        # iterate
        self.clear_tree(tree)

        if dates is not None:
            self.md_map = {}
            for date in dates:
                print('DATE INFO -----------------')
                print(date.pk)
                print(date.iscomplete)
                print(date.startdate)
                self.md_map[date.pk] = date
                tree.insert('', 0, '',
                    text=complete_emoji if date.iscomplete else '',
                    values=(self.get_due_date(date.startdate, self.current_item.numdays)),
                    tags=(date.pk,))
            # update md_map

        # print(dates)
        pass

    def set_history_section(self):
        print(self.current_item)

        self.update_hist_tree()
        # update info section


        self.labels['info'].set(f"Info for: {self.current_item.name}")


    '''
    Event Callbacks
    '''
    def equip_click(self, event):
        selected_equip = self.widgets['equiptree'].identify('item', event.x, event.y)
        if selected_equip == '':
            return

        equip_text = self.widgets['equiptree'].item(selected_equip, 'text')
        self.current_equipment = self.equipment_map[equip_text]
        self.update_mi_tree(self.widgets['mitree'], self.current_equipment)

        print('BIIIIIIIG')
        self.labels['info'].set(f"Info for:")

    def item_click(self, event):
        selected_item = self.widgets['mitree'].identify('item', event.x, event.y)
        if selected_item == '':
            return

        m_item = self.mi_map[
            self.widgets['mitree'].item(selected_item, 'text')
        ]

        self.current_item = m_item
        self.set_history_section()

    def date_click(self, event):
        print('time to complete')
        selected_item = self.widgets['histtree'].identify('item', event.x, event.y)

        print(self.md_map)
        m_date = self.md_map[
            int(self.widgets['histtree'].item(selected_item, 'tags')[0])
        ]
        print(m_date)

        if m_date.completed:
            return

        self.set_completed(m_date, True)
        pass

    def add_date(self):
        print('adding a date', time.time())
        cal_date = self.widgets['calendar'].get_date()
        # print(datetime.fromtimestamp(cal_date, timezone.utc))
        self.db.insert_maintenance_date(self.current_item, cal_date)
        # self.update_hist_tree()

    def clear_tree(self, tree):
        print('clearing')
        print(tree)
        for i in tree.get_children():
            tree.delete(i)

    def get_due_date(self, date, numdays):
        date = datetime.fromtimestamp(date) + timedelta(days=numdays)
        print(date.strftime("%d/%m/%Y"))
        return date

    def set_completed(self, m_date: MaintenanceDate, completed: bool):
        print('yeeeeeeeeeet')
        self.db.set_completed(m_date, completed)
        self.update_hist_tree()



root = tk.Tk()
root.geometry("900x600")
root.state('zoomed')
root.wm_title('Ben\'s Equipment Maintenance Manager')
root.style = ttk.Style()
# root.style.theme_use('classic')
app = Bemm(master=root)
app.pack(fill="both", expand=True, padx=10, pady=10)
app.mainloop()
