#!/bin/bash

while true
do
    echo "Enviando POST para /api/exchange-rate..."
    curl -X POST http://127.0.0.1:5000/api/exchange-rate
    echo ""
    echo "Aguardando 120 segundos..."
    sleep 120
done
