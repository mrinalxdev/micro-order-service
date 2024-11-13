FROM golang:1.20

WORKDIR /app
COPY . .

RUN go mod init order-service && go mod tidy
RUN go build -o order-service .

CMD [ "./order-service" ]