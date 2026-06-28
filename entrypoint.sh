#!/bin/sh
set -e

# Auto-generate self-signed certificates if requested
if [ "$GENERATE_CERTS" = "true" ]; then
    $(dirname "$0")/generate-certificates.sh
fi

# Replace environment variables in the template and write to the final destination
envsubst < /etc/xray/config.template.json > /etc/xray/config.json

# Execute Xray
echo "Starting Xray..."
exec xray run -config /etc/xray/config.json