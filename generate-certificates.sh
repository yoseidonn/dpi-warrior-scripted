#!/bin/sh
set -e

echo "Certificate generation requested..."

CERT_DIR=$(dirname "$CERT_FILE")
mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Generating new self-signed certificates for ${DOMAIN}..."

    openssl req -x509 -nodes -days 365 \
      -newkey rsa:4096 \
      -keyout "$KEY_FILE" \
      -out "$CERT_FILE" \
      -subj "/CN=${DOMAIN}" \
      -addext "subjectAltName = IP:${DOMAIN}"

    echo "Certificates generated successfully."
else
    echo "Certificates already exist. Skipping generation."
fi
