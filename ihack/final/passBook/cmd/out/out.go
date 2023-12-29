package out

import (
	"fmt"

	"github.com/logrusorgru/aurora/v4"
)

func PrintError() {
	fmt.Print("[")
	fmt.Print(aurora.Red("ERR"))
	fmt.Print("] ")
}

func PrintInfo() {
	fmt.Print("[")
	fmt.Print(aurora.Blue("INF"))
	fmt.Print("] ")
}

func PrintSucceed() {
	fmt.Print("[")
	fmt.Print(aurora.Green("YAY"))
	fmt.Print("] ")
}

func PrintFatal() {
	fmt.Print("[")
	fmt.Print(aurora.Red("FTL"))
	fmt.Print("] ")
}
