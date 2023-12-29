package main

import (
	"cmd/cmd/keripto"
	"cmd/cmd/out"
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"os/signal"
	"strings"

	"github.com/logrusorgru/aurora/v4"
)

const (
	serverPort = "9090"
	serverType = "tcp"
	// User := keripto.EncodeBase64()
	User = "uZ6dlpDfspCNmouFjJCXkf"
	key  = "ab2d3417b6c04c07eec417d41a0fb5d4"
	res  = "a58b583b80e3c035e6972bb003dfe0e1"
)

var Args []string

func main() {
	gracefulExit()
	out.PrintInfo()
	fmt.Println("Service running...")
	service, err := net.Listen(serverType, ":"+serverPort)
	if err != nil {
		out.PrintFatal()
		fmt.Println("Error Listening : ", err)
		os.Exit(1)
	}
	defer service.Close()

	out.PrintInfo()
	fmt.Println("Waiting for client connection...")
	for {
		connection, err := service.Accept()
		if err != nil {
			out.PrintFatal()
			fmt.Println("Error Accepting connection : ", err)
			os.Exit(1)
		}
		out.PrintSucceed()
		fmt.Println("Client connected from channel : ", connection)
		go processClient(connection)
	}
}

func processClient(connection net.Conn) {
	fmt.Fprint(connection, "			     This is a secret vault!\n")
	fmt.Fprintf(connection, "	    	 	  Welcome %s\n", User+"!")
	cmd := exec.Command("binary/banner")
	outz, err := cmd.Output()
	if err != nil {
		out.PrintFatal()
		log.Fatalf("cmd.Output() failed with %s\n", err)
	}
	fmt.Fprintf(connection, "%s", outz)
	fmt.Fprint(connection, aurora.Blue("[INF] "))
	fmt.Fprint(connection, "Please enter your password sire : ")
	password := make([]byte, 1024)
	mLen, err := connection.Read(password)
	if err != nil {
		out.PrintFatal()
		fmt.Println("Error reading : ", err)
		connection.Close()
	}
	authPass := encrypt(string(password))
	if password != nil {
		if authPass == res {
			out.PrintSucceed()
			fmt.Println("The password is correct.")
			fmt.Fprint(connection, aurora.Green("[YAY] "))
			fmt.Fprint(connection, "The password is correct!\n")
			readBook(connection)
			connection.Close()
		} else {
			out.PrintError()
			fmt.Println("Incorrect password.")
			fmt.Fprint(connection, aurora.Red("[ERR] "))
			fmt.Fprint(connection, "Incorrect password!\n")
			connection.Close()
		}
	} else {
		out.PrintError()
		fmt.Println("Please provide password")
		fmt.Fprint(connection, aurora.Red("[ERR] "))
		fmt.Fprint(connection, "Please provide password\n")
		connection.Close()
	}
	out.PrintInfo()
	fmt.Printf("Received %s", string(password[:mLen]))
	out.PrintInfo()
	fmt.Printf("From channel %v\n", connection)
}

// fullName
func encrypt(readlyst_author string) string {
	encodedPass := keripto.EncodeBase64(readlyst_author)
	authPass := keripto.Md5hash(key, encodedPass)
	return authPass
}

func gracefulExit() {
	// setting up graceful exit
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	go func() {
		for range c {
			fmt.Println()
			out.PrintFatal()
			fmt.Println("CTRL+C pressed: Exiting")
			os.Exit(1)
		}
	}()
}

func readBook(connection net.Conn) {
	fmt.Fprint(connection, aurora.Cyan("[GRT] "))
	fmt.Fprint(connection, "Welcome Sir!\n")
	fmt.Fprint(connection, aurora.Yellow("[LST] "))
	fmt.Fprint(connection, "Caraval				The Book of Shells\n")
	fmt.Fprint(connection, aurora.Yellow("[LST] "))
	fmt.Fprint(connection, "Legendary				Beasts of Prey\n")
	fmt.Fprint(connection, aurora.Yellow("[LST] "))
	fmt.Fprint(connection, "Finale				The Queen of Nothing\n")
	fmt.Fprint(connection, aurora.Blue("[INF] "))
	fmt.Fprint(connection, "Please enter the book that you wish to read : ")
	book := make([]byte, 1024)
	cBook, err := connection.Read(book)
	if err != nil {
		out.PrintFatal()
		fmt.Println("Error reading : ", err)
		connection.Close()
	}
	os.Args[0] = string(book[:cBook])
	line := strings.TrimSuffix(os.Args[0], "\n")
	if line != "Beasts of Prey" || line != "Caraval" || line != "Finale" || line != "Legendary" || line != "The Book of Shells" || line != "The Queen of Nothing" {
		line = "Caraval"
	}
	line1 := "/usr/bin/cat " + "books/" + line
	cmd := exec.Command("/bin/bash", "-c", line1)
	output, errzz := cmd.CombinedOutput()
	if errzz != nil {
		fmt.Println(fmt.Sprint(errzz) + ": " + string(output))
		return
	}
	fmt.Fprint(connection, string(output))
}
