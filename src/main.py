'''
Ben's Equipment Maintenance Manager

Author:  Ben Johnson
Version: 0.3
'''

import time
import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from db_manager import DBManager


class Bemm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

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

        # labels
        self.labels['info'] = tk.StringVar()
        self.labels['info'].set("Info for: ")
        self.widgets['equiptreelabel'] = ttk.Label(self, text="Equipment")
        self.widgets['mitreelabel'] = ttk.Label(self, text="Maintenance Items")
        self.widgets['infolabel'] = ttk.Label(self, textvariable=self.labels['info'])

        # equipment tree
        equiptree = ttk.Treeview(self, show='tree')
        equiptree.heading("#0",text="Equipment", anchor=tk.W)
        equiptree.bind('<1>', self.equip_click)
        self.update_equipment_tree(equiptree)
        self.widgets['equiptree'] = equiptree

        # operations tree
        mitree = ttk.Treeview(self)
        mitree['columns'] = ('numdays', 'idk')
        mitree.column("#0", width=270)
        mitree.column("numdays", width=100)
        mitree.heading('#0',text='Name',anchor=tk.W)
        mitree.heading('numdays',text='# Days',anchor=tk.W)
        mitree.bind('<1>', self.item_click)
        self.widgets['mitree'] = mitree

        # buttons
        self.widgets['addequipbutt'] = ttk.Button(self, text="Add New Equipment")
        self.widgets['addequipbutt']['command'] = self.add_equipment

        self.widgets['addmibutt'] = ttk.Button(self, text="Add new Maintenance Item")
        self.widgets['addmibutt']['command'] = self.add_mi

        # Info Frame
        infoframe = ttk.Frame(self, borderwidth=2, relief="groove")
        self.widgets['infoframe'] = infoframe

        histtree = ttk.Treeview(infoframe)
        histtree['columns'] = ('start')
        histtree.column('#0', width=40)
        self.widgets['histtree'] = histtree

        self.widgets['setdate'] = ttk.Button(infoframe, text='Set Date')
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

        # row 0
        self.widgets['equiptreelabel'].grid(column=0, row=0, sticky='w')
        self.widgets['mitreelabel'].grid(column=1, row=0, padx=(10, 0), sticky='w')
        self.widgets['infolabel'].grid(column=2, row=0, sticky='w')

        # row 1
        equiptree.grid(column=0, row=1, pady=(0, 10), sticky='nsew')
        mitree.grid(column=1, row=1, padx=10, pady=(0, 10), sticky='nsew')

        # row 2
        self.widgets['addequipbutt'].grid(column=0, row=2, sticky='nsew')
        self.widgets['addmibutt'].grid(column=1, row=2, padx=10, sticky='nsew')

        # info area
        infoframe.grid(column=2, row=1, rowspan=2, ipadx=10, ipady=10, sticky='nsew')
        histtree.grid(column=0, row=1, padx=10, pady=(0, 10), sticky='nsew')
        self.widgets['calendar'].grid(column=0, row=0, padx=(10, 0), pady=10, sticky='w')


    def add_equipment(self):
        answer = simpledialog.askstring("New", "Enter Equipment Name", parent=self)

        if answer is None or answer == '':
            return

        self.db.insert_equipment(answer)
        self.get_equipment_values()
        self.update_equipment_tree(self.widgets['equiptree'])

    def add_mi(self):
        if self.current_equipment is None:
            messagebox.showerror('Failed', 'Double click an equipment entry to add an item')
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
        self.mi_map = {}

        mi_list = self.db.get_all_maintenance_items(equipment)

        for i in mi_list:
            self.mi_map[i.name] = i
            tree.insert('', 0, '', text=i.name, values=(i.numdays))

    def update_hist_tree(self, tree, m_item):
        # print('here then')
        # get all dates
        # iterate
        dates = self.db.get_all_maintenance_dates(m_item)
        # print(dates)


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

    def item_click(self, event):
        # print('here')
        selected_item = self.widgets['mitree'].identify('item', event.x, event.y)
        if selected_item == '':
            return

        item_text = self.widgets['mitree'].item(selected_item, 'text')
        self.labels['info'].set(f"Info for: {item_text}")
        m_item = self.mi_map[item_text]
        self.update_hist_tree(self.widgets['histtree'], m_item)

    # def new_date(self):
    #     cal =
    #     cal.grid(column=1, row=0)

    def clear_tree(self, tree):
        for i in tree.get_children():
            tree.delete(i)


root = tk.Tk()
root.geometry("900x600")
root.state('zoomed')
root.wm_title('Ben\'s Equipment Maintenance Manager')
root.style = ttk.Style()
app = Bemm(master=root)
app.pack(fill="both", expand=True, padx=10, pady=10)
app.mainloop()
