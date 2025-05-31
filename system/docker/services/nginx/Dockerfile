FROM nginx:alpine

# Install additional packages
RUN apk add --no-cache \
    curl \
    openssl \
    brotli \
    # Add any other required packages here
    && rm -rf /var/cache/apk/*

# Create nginx user/group first, to be consistent throughout docker variants
RUN set -x \
    && addgroup -g 101 -S nginx \
    && adduser -S -D -H -u 101 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Create required directories
RUN mkdir -p /etc/nginx/conf.d \
    && mkdir -p /var/cache/nginx \
    && mkdir -p /var/log/nginx \
    && mkdir -p /etc/nginx/ssl \
    && chown -R nginx:nginx /etc/nginx /var/cache/nginx /var/log/nginx /etc/nginx/ssl

# Custom nginx configuration
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Security headers
RUN echo "add_header X-Frame-Options 'SAMEORIGIN';" > /etc/nginx/conf.d/security-headers.conf \
    && echo "add_header X-Content-Type-Options 'nosniff';" >> /etc/nginx/conf.d/security-headers.conf \
    && echo "add_header X-XSS-Protection '1; mode=block';" >> /etc/nginx/conf.d/security-headers.conf \
    && echo "add_header Strict-Transport-Security 'max-age=31536000; includeSubDomains' always;" >> /etc/nginx/conf.d/security-headers.conf

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# Set proper permissions
RUN chmod 755 /var/cache/nginx \
    && chmod -R 755 /var/log/nginx \
    && chmod -R 755 /etc/nginx

EXPOSE 80 443

# Switch to non-root user
USER nginx

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]

