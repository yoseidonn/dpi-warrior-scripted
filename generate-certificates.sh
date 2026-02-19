#!/bin/sh
set -e

echo "Certificate generation requested..."

CERT_DIR=$(dirname "$CERT_FILE")
mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "Generating new self-signed certificates for ${DOMAIN}..."

    cat > /tmp/openssl.cnf <<EOF
[req]
default_bits       = 4096
prompt             = no
default_md         = sha256
distinguished_name = dn
x509_extensions    = v3_req

[dn]
CN = ${DOMAIN}

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
IP.1 = ${DOMAIN}
EOF

    openssl req -x509 -nodes -days 365 \
        -newkey rsa:4096 \
        -keyout "$KEY_FILE" \
        -out "$CERT_FILE" \
        -config /tmp/openssl.cnf

    rm /tmp/openssl.cnf

    echo "Certificates generated successfully at $CERT_DIR."
else
    echo "Certificates already exist. Skipping generation."
fi
