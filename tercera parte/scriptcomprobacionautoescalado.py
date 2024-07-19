#!/bin/bash

# Configuración de variables
GROUP_IP=34.175.150.167  # Reemplazar con la dirección IP del grupo de instancias
REQUESTS_PER_SECOND=10           # Número de solicitudes por segundo
DURATION=$((5 * 24 * 60 * 60))   # Duración de la simulación en segundos (5 días)
LOGFILE="autoscaling_apache.log" # Archivo de log para registros

# Función para enviar una solicitud HTTP con curl
send_requests() {
    local start_time=$(date +%s)
    local end_time=$((start_time + 1))
    local requests=0

    while [ $end_time -lt $((start_time + $REQUESTS_PER_SECOND)) ]; do
        curl -sS -o /dev/null $GROUP_IP &
        end_time=$(date +%s)
        requests=$((requests + 1))
    done

    echo "$(date) - Enviadas $requests solicitudes a $GROUP_IP"
}

# Bucle infinito para generar carga continua
echo "Iniciando simulación de autoescalado en servidor Apache..."
echo "Generando carga continua a $GROUP_IP con $REQUESTS_PER_SECOND solicitudes por segundo durante 5 días..."

while true; do
    send_requests
    sleep 1
    # Salir del bucle después de la duración especificada
    if [ $SECONDS -ge $DURATION ]; then
        break
    fi
done

echo "Simulación de autoescalado en servidor Apache completada."
