# Fetch the requested Xray image
FROM ghcr.io/xtls/xray-core:25.6.8 AS xray-base

# Build the runtime image
FROM alpine:latest

# Install gettext for envsubst and ca-certificates for TLS support, tzdata for timezone data, and openssl for any cryptographic needs
RUN apk add --no-cache gettext ca-certificates tzdata openssl

# Copy Xray binary and dat files
COPY --from=xray-base /usr/local/bin/xray /usr/local/bin/xray
COPY --from=xray-base /usr/local/share/xray/ /usr/local/share/xray/

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
COPY generate-certificates.sh /generate-certificates.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /generate-certificates.sh

ENTRYPOINT ["/entrypoint.sh"]