import os
import sqlite3


class Equipment:
    def __init__(self, pk=-1, name=''):
        self.pk = pk
        self.name = name


class MaintenanceItem:
    def __init__(self, pk=-1, name='', numdays=-1, equipment=None):
        self.pk = pk
        self.name = name
        self.numdays = numdays
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
        self.cursor.execute('''
            SELECT
                pk,
                name
            FROM
                equipment
            ORDER BY
                name DESC''')
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

    # Maintenace Items

    def get_all_maintenance_items(self, equipment):
        self.cursor.execute('''
            SELECT
                pk,
                name,
                numdays,
                equipmentid
            FROM
                maintenanceitem
            WHERE
                equipmentid=?''',
            (equipment.pk,))
        db_mi = self.cursor.fetchall()

        mi_list = []
        for mi in db_mi:
            mi_list.append(MaintenanceItem(mi[0], mi[1], mi[2], equipment))

        print(mi_list)
        return mi_list

    def insert_maintenance_item(self, operation_name, numdays, equipment):
        self.cursor.execute('''
            INSERT INTO
                maintenanceitem(
                    name,
                    numdays,
                    equipmentid
                )
            VALUES(?,?,?);''',
            (operation_name, numdays, equipment.pk))
        self.conn.commit()

        pk = self.get_maintenance_item_pk(operation_name, numdays, equipment.pk)
        print(pk)
        if pk == None:
            return None

    def get_maintenance_item_pk(self, name, numdays, equip_pk):
        self.cursor.execute( '''
            SELECT
                pk
            FROM
                maintenanceitem
            WHERE
                name=?
            AND
                numdays=?
            AND
                equipmentid=?''',
            (name, numdays, equip_pk,))
        op = self.cursor.fetchone()

        if op == None:
            return None
        return op[0]

    def get_equipmentid(self, equipment_name):
        self.cursor.execute("SELECT id FROM equipment WHERE name=?", (equipment_name,))
        eq_id = self.cursor.fetchone()
        return eq_id[0]

    def close(self):
        self.conn.close()

    # BE CAREFUL MY DUDE
    def drop_all(self):
        self.cursor.execute("DROP TABLE IF EXISTS equipment")
        self.cursor.execute("DROP TABLE IF EXISTS operation")