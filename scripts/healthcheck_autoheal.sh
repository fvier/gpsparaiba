#!/bin/bash
LOG_FILE="/var/log/gpsparaiba_autoheal.log"

HEALTH_STATUS=$(curl -s -k -m 5 https://gpsparaiba.com.br/health || echo "FAILED")

if ! echo "$HEALTH_STATUS" | grep -q '"database":"available"'; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [ALERT] Healthcheck failed: $HEALTH_STATUS. Initiating auto-recovery..." >> "$LOG_FILE"
    docker restart gpsparaiba-app >> "$LOG_FILE" 2>&1
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] Auto-recovery executed." >> "$LOG_FILE"
fi
