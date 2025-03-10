FROM docker:latest

RUN apk add --no-cache docker-compose bash

WORKDIR /app
COPY . .

EXPOSE 8000 3000

CMD ["sh", "-c", "docker-compose up -d"]
