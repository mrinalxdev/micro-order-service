package main

import (
	"log"

	"github.com/streadway/amqp"
)

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@rabbitmq:5672/")
    if err != nil {
        log.Fatalf("Failed to connect to RabbitMQ : %v", err)
    }
    defer conn.Close()

    ch, err := conn.Channel()
    if err != nil {
        log.Fatalf("Failed to connect to RabbitMQ : %v", err)
    }
    defer ch.Close()

    orderQueue, err := ch.QueueDeclare(
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

    upadtesQueue, err := ch.QueueDeclare(
        "inventory_update",
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
        orderQueue.Name,
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

    go func(){
        for d := range msgs {
            log.Printf("Recieved an order : %s", d.Body)

            if string (d.Body) == "Order #5"{
                log.Printf("Out of stock for %s", d.Body)
                continue
            }

            err = ch.Publish(
                "",
                upadtesQueue.Name,
                false,
                false,
                amqp.Publishing{
                    ContentType: "text/plain",
                    Body : []byte("Order Processed : " + string(d.Body)),
                },
            )

            if err != nil {
                log.Fatalf("Failed to publish a message : %v", err)
            }
        }
    }()

    log.Printf("Waiting for orders ...")
    select{}
}