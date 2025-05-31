FROM nginx:alpine

# Install additional packages
RUN apk add --no-cache \
    brotli \
    openssl

# Custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create SSL directory
RUN mkdir -p /etc/nginx/ssl

# Set up default configuration
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Make nginx run in foreground
CMD ["nginx", "-g", "daemon off;"]

