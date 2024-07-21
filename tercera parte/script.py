#!/bin/bash

# Configuración de variables
GROUP_IP=34.175.51.116  # Reemplazar con la dirección IP del grupo de instancias
RETRY_COUNT=3             # Número de intentos para verificar el servidor
RETRY_DELAY=5             # Retardo en segundos entre intentos
TIMEOUT=10                # Tiempo máximo de espera para cada solicitud HTTP en segundos
LOGFILE="autoescalado_test.log"  # Archivo de log

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'  # Sin color

# Función para registrar mensajes en el log y en la consola
log() {
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOGFILE
}

# Función para verificar la disponibilidad del servidor web
check_server_availability() {
    local retry=0
    local status_code

    log "${YELLOW}Iniciando verificación de disponibilidad del servidor en $GROUP_IP.${NC}"

    while [ $retry -lt $RETRY_COUNT ]; do
        # Realizar solicitud HTTP GET y guardar el código de estado
        status_code=$(curl -sS -w "%{http_code}" -o /dev/null --max-time $TIMEOUT $GROUP_IP)

        # Verificar el código de estado de la solicitud HTTP
        if [ $status_code -eq 200 ]; then
            log "${GREEN}Autoescalado funciona correctamente. La solicitud HTTP fue exitosa (Código $status_code).${NC}"
            return 0  # Éxito
        else
            log "${RED}Intento #$((retry+1)) - Error: La solicitud HTTP devolvió el código de estado $status_code.${NC}"
        fi

        # Incrementar el contador de intentos y esperar antes de reintentar
        retry=$((retry + 1))
        sleep $RETRY_DELAY
    done

    log "${RED}Error: No se pudo verificar el autoescalado después de $RETRY_COUNT intentos.${NC}"
    return 1  # Error
}

# Ejecutar la función para verificar la disponibilidad del servidor web
check_server_availability
