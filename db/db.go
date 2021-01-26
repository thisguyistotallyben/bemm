package db

import (
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// Database is the database struct lol
type Database struct {
	db *gorm.DB
}

// Connect starts the connection to the database
func (d *Database) Connect() {
	var err error

	dsn := "database.db"
	d.db, err = gorm.Open(sqlite.Open(dsn), &gorm.Config{})

	if err != nil {
		panic("failed to connect to database :(")
	}
}

// CreateTables creates the tables
func (d *Database) CreateTables() {
	Equipment{}.CreateTable(d)
	Item{}.CreateTable(d)
	Date{}.CreateTable(d)
}

// GetAllEquipment does things
func (d *Database) GetAllEquipment() []Equipment {
	var list []Equipment
	d.db.Find(&list)

	return list

}
