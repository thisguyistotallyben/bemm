package db

import "gorm.io/gorm"

// Entity is the interface that entities inherit
type Entity interface {
	CreateTable(d *Database)
	Insert(d *Database)
}

// Equipment data structure
type Equipment struct {
	gorm.Model
	Name string
}

// CreateTable creates the Equipment table
func (entity Equipment) CreateTable(d *Database) {
	d.db.AutoMigrate(&Equipment{})
}

// Insert inserts a Equipment into the
func (entity Equipment) Insert(d *Database) {
	d.db.Create(&entity)
}

// Item data structure
type Item struct {
	gorm.Model
	Name        string
	NumDays     int
	EquipmentID int
	Equipment   Equipment
}

// CreateTable creates the Item table
func (entity Item) CreateTable(d *Database) {
	d.db.AutoMigrate(&Item{})
}

// Insert inserts a User into the
func (entity Item) Insert(d *Database) {
	d.db.Create(&entity)
}

// Date data structure
type Date struct {
	gorm.Model
	Start    int64
	Complete int64
	ItemID   int
	Item     Item
}

// CreateTable creates the Date table
func (entity Date) CreateTable(d *Database) {
	d.db.AutoMigrate(&Date{})
}

// Insert inserts a Date into the
func (entity Date) Insert(d *Database) {
	d.db.Create(&entity)
}
