package main

import (
	"fmt"
	"net"
	"os"
)

type Position struct {
	x   float32
	y   float32
	z   float32
	dir float32
}

func main() {
	// Get ip address and port from cli args
	var ip string = "0.0.0.0"
	if len(os.Args) > 1 {
		ip = os.Args[1]
	}

	addr, err := net.ResolveUDPAddr("udp4", ip+":55555")
	if err != nil {
		fmt.Println("Error resolving address:", err)
		os.Exit(1)
	}

	conn, err := net.ListenUDP("udp4", addr)
	if err != nil {
		fmt.Println("Error listening:", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Println("UDP Server listening on ", ip+":55555...")

	buffer := make([]byte, 1024)

	var clientList []*net.UDPAddr

	for {
		n, clientAddr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error reading packet:", err)
			continue
		}

		known := false
		for _, client := range clientList {
			if client.String() == clientAddr.String() {
				known = true
				break
			}
		}

		if !known {
			clientList = append(clientList, clientAddr)
			fmt.Printf("Added client: %s (total: %d)\n", clientAddr.String(), len(clientList))
		}

		for _, client := range clientList {
			if client.String() != clientAddr.String() {
				_, err := conn.WriteToUDP(buffer[:n], client)
				if err != nil {
					fmt.Println("Error sending packet to", client.String(), ":", err)
				}
			}
		}
	}
}
