#!/bin/sh
set -e

echo "Certificate generation requested..."

CERT_DIR=$(dirname "$CERT_FILE")
mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Generating new self-signed certificates for ${DOMAIN}..."

    if echo "$DOMAIN" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$'; then
        SAN="IP:${DOMAIN}"
    else
        SAN="DNS:${DOMAIN}"
    fi

    openssl req -x509 -nodes -days 365 \
      -newkey rsa:4096 \
      -keyout "$KEY_FILE" \
      -out "$CERT_FILE" \
      -subj "/CN=${DOMAIN}" \
      -addext "subjectAltName = $SAN"

    echo "Certificates generated successfully."
else
    echo "Certificates already exist. Skipping generation."
fi
