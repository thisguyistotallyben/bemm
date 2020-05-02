# initalize database
# OR open database

import sqlite3
from db_manager import DBManager


print('yeet')
db = DBManager('yeet.sqlite3')
eq1 = db.insert_equipment('big ol tractor')
eq2 = db.insert_equipment('decent sized truck')

eqlist = db.get_all_equipment()
for eq in eqlist:
    print(eq.pk)
    print(eq.name)
    print('----')

