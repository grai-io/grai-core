FROM node:18-slim AS builder

LABEL org.opencontainers.image.source="https://github.com/grai-io/grai-core"

ENV NODE_ENV production

# Install python
RUN apt-get update || : && apt-get install python3 pkg-config libpixman-1-dev libcairo2-dev libpango1.0-dev libgif-dev make g++ -y

# Add a work directory
WORKDIR /app

# Cache and Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && cache clean --force

# Copy app files
COPY . .

# Build the app
RUN npm run build

# Bundle static assets with nginx
FROM nginx:1.23.2-alpine as production

ENV NODE_ENV production

# Add bash
RUN apk add --no-cache bash

# Copy .env file and shell script to container
WORKDIR /usr/share/nginx/html
COPY ./env.sh .
COPY .env.example .

# Make our shell script executable
RUN chmod +x env.sh

# Add your nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]
