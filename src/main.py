# initalize database
# OR open database

import time
import sqlite3
from db_manager import DBManager


print('yeet')
db = DBManager('yeet.sqlite3')

# DUMB ZONE BEGINS
db.drop_all()
db.setup_database()
# END DUMB ZONE

eq1 = db.insert_equipment('big ol tractor')
eq2 = db.insert_equipment('decent sized truck')

eqlist = db.get_all_equipment()
for eq in eqlist:
    print(eq.pk)
    print(eq.name)
    print('----')
print('')

op1 = db.insert_operation(eq1, None, 'sick operation', int(time.time()))
op2 = db.insert_operation(eq1, op1, 'sick operation', int(time.time()) + 20)
op3 = db.insert_operation(eq1, op2, 'sicker operation', int(time.time()))
print(op1)
print(op2)

ops = db.get_all_operations(eq1)
for op in ops:
    print(op.pk)
    print(op.name)
    print(op.date)
    print(op.prev_operation)
    print('----')