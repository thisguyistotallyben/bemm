import os
import sqlite3


'''
THING I THINK I'M MISSING

The completed date shouldn't be a boolean because it can be overdue.
It was an integer before so it could be set to the date in which it was marked completed.
This should be changed back.
'''


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


class MaintenanceDate:
    def __init__(self, pk=-1, startdate=0, completed=False):
        self.pk = pk
        self.startdate = startdate
        self.completed = True if completed else False
        print('in entity')
        print(repr(completed))
        print(self.startdate)


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
        with open('src/db_setup.sql', 'r') as f:
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
                name DESC''') # this is not a mistake... blame treeview
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
            return None

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

        return mi_list

    def insert_maintenance_item(self, maintenance_name, numdays, equipment):
        self.cursor.execute('''
            INSERT INTO
                maintenanceitem(
                    name,
                    numdays,
                    equipmentid
                )
            VALUES(?,?,?);''',
            (maintenance_name, numdays, equipment.pk))
        self.conn.commit()

        pk = self.get_maintenance_item_pk(maintenance_name, numdays, equipment.pk)
        if pk == None:
            return None

        return MaintenanceItem(pk, maintenance_name, numdays, equipment)

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

    def get_all_maintenance_dates(self, m_item: MaintenanceItem):
        self.cursor.execute('''
            SELECT
                pk,
                startdate,
                completed
            FROM
                maintenancedate
            WHERE
                maintenanceid=?
            ORDER BY
                startdate DESC''',
            (m_item.pk,))
        db_md = self.cursor.fetchall()

        md_list = []
        for md in db_md:
            print('yee haw')
            print(md)
            print(md[1])
            md_list.append(MaintenanceDate(md[0], md[1], md[2]))

        return md_list

    def insert_maintenance_date(self, m_item: MaintenanceItem, startdate):
        self.cursor.execute('''
            INSERT INTO
                maintenancedate(
                    startdate,
                    completed,
                    maintenanceid
                )
            VALUES(?,?,?);''',
            (startdate, False, m_item.pk))
        self.conn.commit()
        pass

        # pk = self.get_maintenance_item_pk(maintenance_name, numdays, equipment.pk)
        # if pk == None:
        #     return None

        # return MaintenanceItem(pk, maintenance_name, numdays, equipment)

    def get_maintenance_date_pk(self, startdate, numdays):
        pass

    def set_completed(self, m_date: MaintenanceDate, completed: bool):
        self.cursor.execute('''
            UPDATE
                maintenancedate
            SET
                completed = ?
            WHERE
                pk = ?''',
            (completed, m_date.pk,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    # BE CAREFUL MY DUDE
    def drop_all(self):
        self.cursor.execute("DROP TABLE IF EXISTS equipment")
        self.cursor.execute("DROP TABLE IF EXISTS maintenanceitem")
        self.cursor.execute("DROP TABLE IF EXISTS maintenancedate")