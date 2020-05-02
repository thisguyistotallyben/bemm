import os
import sqlite3


class Equipment:
    def __init__(self, pk=-1, name=''):
        self.pk = pk
        self.name = name


class Operation:
    def __init__(self, pk=-1, name='', date=-1, prev_operation=None, equipment=None):
        self.pk = pk
        self.name = name
        self.date = date
        self.prev_operation = prev_operation
        self.equipment = equipment


class DBManager:
    def __init__(self, name):
        exists = False
        if os.path.isfile(name):
            exists = True

        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

        if not exists:
            self.setup_database()

    def setup_database(self):
        with open('db_setup.sql', 'r') as f:
            db_instructions = f.read()

        self.conn.executescript(db_instructions)

    # Equipment

    def get_all_equipment(self):
        self.cursor.execute("SELECT pk, name FROM equipment")
        db_eq = self.cursor.fetchall()

        equipment_list = []
        for eq in db_eq:
            equipment_list.append(Equipment(eq[0], eq[1]))

        return equipment_list

    def get_equipment(self, name):
        self.cursor.execute("SELECT pk, name FROM equipment WHERE name=?", (name,))
        db_eq = self.cursor.fetchone()

        if db_eq == None:
            return None

        return Equipment(db_eq[0], db_eq[1])

    def insert_equipment(self, name):
        try:
            self.cursor.execute("INSERT INTO equipment(name) VALUES(?);", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('That equipment already exists')

        return self.get_equipment(name)

    # Operation

    def get_all_operations(self, equipment):
        self.cursor.execute("SELECT * FROM operation WHERE equipmentid=?", (equipment.pk,))
        db_op = self.cursor.fetchall()

        operation_list = []
        for op in db_op:
            operation_list.append(Operation(op[0], op[1], op[2], op[3]))

        return operation_list

    def insert_operation(self, equipment, operation_name, date):
        eq_id = self.get_equipmentid(equipment_name)
        print(eq_id)
        if eq_id is None:
            print('oof that does not exist')
            return

        self.cursor.execute(
            "INSERT INTO operation(name, previousid, equipmentid) VALUES(?,?,?);",
            (operation_name, None, eq_id,))
        self.conn.commit()

    def get_equipmentid(self, equipment_name):
        self.cursor.execute("SELECT id FROM equipment WHERE name=?", (equipment_name,))
        eq_id = self.cursor.fetchone()
        return eq_id[0]

    def close(self):
        self.conn.close()