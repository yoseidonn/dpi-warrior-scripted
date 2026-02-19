#!/bin/sh
set -e

echo "Certificate generation requested..."

# Extract the directory path from the CERT_FILE variable so we can create it
CERT_DIR=$(dirname "$CERT_FILE")
mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Generating new self-signed certificates for ${DOMAIN}..."
    openssl req -x509 -newkey rsa:4096 -nodes -sha256 -days 365 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -subj "/CN=${DOMAIN}"
    echo "Certificates generated successfully at $CERT_DIR."
else
    echo "Certificates already exist. Skipping generation."
fi