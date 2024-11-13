FROM golang:1.20

WORKDIR /app
COPY . .

RUN go mod init inventory-service && go mod tidy
RUN go build -o inventory-service .

CMD [ "./inventory-service" ]