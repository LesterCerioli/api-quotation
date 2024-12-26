# Exchange Rate API

This API provides real-time USD to BRL (Brazilian Real) exchange rates. It fetches the latest exchange rate every 30 minutes and serves the data through a simple REST endpoint.

## How It Works

- The application fetches the latest USD to BRL exchange rate from the [Exchange Rate API](https://api.exchangerate-api.com/v4/latest/USD) every 30 minutes in the background.
- A Flask web server exposes an endpoint to retrieve the current exchange rate.

## API Endpoint

### **GET /api/exchange-rate**

Retrieve the latest USD to BRL exchange rate.
curl -X GET http://127.0.0.1:5000/api/exchange-rate 

### **POST /api/exchange-rate**
curl -X POST http://127.0.0.1:5000/api/exchange-rate

### **POST /api/logs**
curl -X POST http://127.0.0.1:5000/api/logs

### Addresses on Kubernetes:

- http://127.0.0.1:5000
- http://10.244.0.19:5000 

### DockerHub

ltservices/api-quotation:1.0.1











