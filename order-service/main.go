package main

import (
	"log"
	"time"

	"github.com/streadway/amqp"
)

func main() {
	conn, err := amqp.Dial("amqp://guest:gues@rabbitmq:5672/")
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
		"order_queue",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Failed to declare a queue : %v", err)
	}

	for i := 1; i <= 10; i++ {
		body := "Order #" + string(i)
		err := ch.Publish(
			"",
			queue.Name,
			false,
			false,
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        []byte(body),
			},
		)
		if err != nil {
			log.Fatalf("Failed to publish a message : %v", err)
		}
		log.Printf("Sent : %s", body)
		time.Sleep(1 * time.Second)
	}
}
