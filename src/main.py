# initalize database
# OR open database

import time
import sqlite3
import tkinter as tk
from tkinter import ttk
from db_manager import DBManager


class Popup(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.widgets = {}


class Bemm(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # db things
        self.db = DBManager('yeet.sqlite3')

        # DUMB ZONE
        # self.db.drop_all()
        # self.db.setup_database()
        # eq1 = self.db.insert_equipment('big ol tractor')
        # eq2 = self.db.insert_equipment('decent sized truck')
        # END DUMB ZONE
        self.equipment = self.db.get_all_equipment()
        self.equipment_map = {}
        for eq in self.equipment:
            self.equipment_map[eq.name] = eq
        self.current_equipment = None

        self.create_widgets()

    def create_widgets(self):
        self.widgets = {}

        # labels
        self.widgets['equiptreelabel'] = ttk.Label(self, text="Equipment")
        self.widgets['optreelabel'] = ttk.Label(self, text="Maintenance Items")

        # equipment tree
        self.widgets['equiptree'] = ttk.Treeview(self, show='tree')
        equiptree = self.widgets['equiptree']
        equiptree.heading("#0",text="Equipment", anchor=tk.W)
        self.fill_equipment_tree(equiptree)
        equiptree.bind('<Double-1>', self.equip_click)

        # operations tree
        self.widgets['optree'] = ttk.Treeview(self)
        optree = self.widgets['optree']
        optree['columns'] = ('due', 'idk')
        optree.column("#0", width=270)
        optree.column("due", width=100)
        optree.heading('#0',text='Name',anchor=tk.W)
        optree.heading('due',text='Due Date',anchor=tk.W)

        self.widgets['addequipbutt'] = ttk.Button(self, text="Add New Equipment")
        self.widgets['addequipbutt']['command'] = self.add_equipment

        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=3)
        self.widgets['equiptreelabel'].grid(column=0, row=0, sticky='w')
        self.widgets['optreelabel'].grid(column=1, row=0, padx=(10, 0), sticky='w')
        equiptree.grid(column=0, row=1, sticky='nsew')
        optree.grid(column=1, row=1, padx=(10, 0), sticky='nsew')
        self.widgets['addequipbutt'].grid(column=0, row=2, sticky='nsew')

    def add_equipment(self):
        print('i did the thing')
        popupwin = tk.Tk()
        popupwin.wm_title('Add New Equipment')
        popupwin.geometry("400x100")
        popup = Popup(popupwin)
        popup.pack(fill="both", expand=True, padx=10, pady=10)

        widgets = {}
        widgets['addlabel'] = ttk.Label(popupwin, text='Equipment Name')
        widgets['addtext'] = ttk.Entry(popupwin)

        widgets['addlabel'].grid(column=0, row=0, sticky='w')

        popup.widgets = widgets
        popup.mainloop()

        # eq_name = self.widgets['eq input'].get()
        # print(eq_name)
        # if eq_name == '':
        #     return
        # self.db.insert_equipment(eq_name)
        # self.equipment = self.db.get_all_equipment()
        # self.fill_equipment_tree(self.widgets['tree'])

    def add_op(self):
        if self.current_equipment is None:
            print('nothing selected')
            return

        self.db.insert_operation(self.current_equipment, None, 'A thing', 100)

    def fill_equipment_tree(self, tree):
        self.clear_tree(tree)

        for i in list(self.equipment_map.keys()):
            tree.insert('', 0, '', text=i, tags=(i,))

    def clear_tree(self, tree):
        for i in tree.get_children():
            tree.delete(i)

    def equip_click(self, event):
        selected_equip = self.widgets['equiptree'].identify('item', event.x, event.y)
        equip_text = self.widgets['equiptree'].item(selected_equip, 'text')
        self.current_equipment = self.equipment_map[equip_text]
        print(equip_text)
        self.fill_op_tree(self.widgets['optree'], self.current_equipment)

    def fill_op_tree(self, tree, equipment):
        print(equipment)
        op_list = self.db.get_all_operations(equipment)

        self.clear_tree(tree)
        for i in op_list:
            tree.insert('', 0, '', text=i.name)


root = tk.Tk()
root.geometry("900x600")
root.wm_title('BEMM')
app = Bemm(master=root)
app.pack(fill="both", expand=True, padx=10, pady=10)
app.mainloop()









# eq1 = db.insert_equipment('big ol tractor')
# eq2 = db.insert_equipment('decent sized truck')

# eqlist = db.get_all_equipment()
# for eq in eqlist:
#     print(eq.pk)
#     print(eq.name)
#     print('----')
# print('')

# op1 = db.insert_operation(eq1, None, 'sick operation', int(time.time()))
# op2 = db.insert_operation(eq1, op1, 'sick operation', int(time.time()) + 20)
# op3 = db.insert_operation(eq1, op2, 'sicker operation', int(time.time()))
# print(op1)
# print(op2)

# ops = db.get_all_operations(eq1)
# for op in ops:
#     print(op.pk)
#     print(op.name)
#     print(op.date)
#     print(op.prev_operation)
#     print('----')