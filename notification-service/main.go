package main

import (
	"log"

	"github.com/streadway/amqp"
)

func main(){
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ : %v", err)
	}

	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel : %v", err)
	}
	defer ch.Close()

	queue, err := ch.QueueDeclare(
		"inventory_updates",
		false, 
		false, 
		false, 
		false,
		nil,
	)

	if err != nil {
		log.Fatalf("Failed to declare a queue : %v", err)
	}

	msgs, err := ch.Consume(
		queue.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)

	if err != nil {
		log.Fatalf("Failed to register a consumer : %v", err)
	}

	go func() {
		for d := range msgs {
			log.Printf("Notification sent for : %s", d.Body)
		}
	}()

	log.Printf("Waiting for inventory updates ...")
	select{}
}