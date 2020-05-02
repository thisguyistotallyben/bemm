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
        self.cursor.execute('''
            SELECT
                pk,
                name,
                date,
                previousid,
                equipmentid
            FROM
                operation
            WHERE
                equipmentid=?''',
            (equipment.pk,))
        db_op = self.cursor.fetchall()

        '''
        So this bit is kind of sketchy and a little bit stupid.

        On the first go around, the prev_operation field is just the id
        On the second go around, it changes to the actual entity
        '''
        op_map = {}
        for op in db_op:
            if op[3] is None:
                key = -1
            else:
                key = op[3]
            op_map[key] = Operation(op[0], op[1], op[2], op[3], equipment)

        for op in op_map:
            prev_op_pk = op_map[op].prev_operation
            if prev_op_pk is None:
                continue
            op_map[op].prev_operation = op_map[prev_op_pk]

        return list(op_map.values())


    def insert_operation(self, equipment, previous_operation, operation_name, date):
        if previous_operation is None:
            prev_op_pk = None
        else:
            prev_op_pk = previous_operation.pk

        self.cursor.execute('''
            INSERT INTO
                operation(
                    name,
                    date,
                    previousid,
                    equipmentid)
            VALUES(?,?,?,?);''',
            (operation_name, date, prev_op_pk, equipment.pk,))
        self.conn.commit()

        pk = self.get_operation_pk(operation_name, date, equipment.pk)
        print(pk)
        if pk == None:
            return None
        return Operation(pk, operation_name, date, previous_operation, equipment)

    def get_operation_pk(self, name, date, equip_pk):
        self.cursor.execute( '''
            SELECT
                pk
            FROM
                operation
            WHERE
                name=?
            AND
                date=?
            AND
                equipmentid=?''',
            (name, date, equip_pk,))
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