CREATE TABLE equipment(
    pk INTEGER PRIMARY KEY,
    name TEXT,
    UNIQUE(name)
);

CREATE TABLE operation(
    pk INTEGER PRIMARY KEY,
    name TEXT,
    date INTEGER,
    previousid INTEGER,
    equipmentid INTEGER NOT NULL,
    UNIQUE(previousid),
    FOREIGN KEY(previousid) REFERENCES equipment(pk),
    FOREIGN KEY(equipmentid) REFERENCES operation(pk)
);