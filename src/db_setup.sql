CREATE TABLE equipment(
    pk INTEGER PRIMARY KEY,
    name TEXT,
    UNIQUE(name)
);

CREATE TABLE maintenanceitem(
    pk INTEGER PRIMARY KEY,
    name TEXT,
    numdays INTEGER,
    equipmentid INTEGER NOT NULL,
    FOREIGN KEY(equipmentid) REFERENCES operation(pk)
);

CREATE TABLE maintenancedate(
    pk INTEGER PRIMARY KEY,
    startdate INTEGER,
    maintenanceid INTEGER NOT NULL,
    FOREIGN KEY(maintenanceid) REFERENCES maintenance(pk)
)