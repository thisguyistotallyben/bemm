package main

import (
	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	"github.com/thisguyistotallyben/bemm/db"
)

func main() {
	var database db.Database
	database.Connect()
	database.CreateTables()
	// eq := db.Equipment{
	// 	Name: "BIG STONKS",
	// }
	// eq.Insert(&database)

	equipmentList := database.GetAllEquipment()

	myApp := app.New()
	myWindow := myApp.NewWindow("Widget")

	someList := createEquipmentListWidget(equipmentList)
	someList2 := createEquipmentListWidget(equipmentList)

	button := widget.NewButton("YEET HAW", func() {
		butt := db.Equipment{
			Name: "Big Stonkaroonis",
		}
		butt.Insert(&database)
		equipmentList = database.GetAllEquipment()
		someList.Refresh()
	})

	content := container.New(layout.NewGridLayout(2), button, someList, someList2)

	myWindow.SetContent(content)
	myWindow.ShowAndRun()
}

func createEquipmentListWidget(data []db.Equipment) *widget.List {
	someList := widget.NewList(
		func() int {
			return len(data)
		},
		func() fyne.CanvasObject {
			label := widget.NewLabel("")
			return container.NewBorder(nil, nil, nil, nil,
				label)
		},
		func(id widget.ListItemID, obj fyne.CanvasObject) {
			text := obj.(*fyne.Container).Objects[0].(*widget.Label)
			text.SetText(data[id].Name)
		})

	return someList
}

/* END USEFUL CODE */

// package main

// import (
// 	"github.com/thisguyistotallyben/bemm/db"
// )

// func main() {
// 	var database db.Database
// 	database.Connect()

// 	database.CreateTables()

// 	eq := db.Equipment{
// 		Name: "HECK",
// 	}
// 	eq.Insert(&database)

// 	item := db.Item{
// 		Name:      "AN ITEM",
// 		NumDays:   42,
// 		Equipment: eq,
// 	}
// 	item.Insert(&database)
// }
