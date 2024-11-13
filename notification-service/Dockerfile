FROM golang:1.20

WORKDIR /app
COPY . .

RUN go mod init notification-service && go mod tidy
RUN go build -o notification-service .

CMD ["./notification-service"]