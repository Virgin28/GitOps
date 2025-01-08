# Use official NGINX image as a base image
FROM nginx:latest

# Copy the custom NGINX configuration file into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static frontend files (HTML, CSS, JS) to the appropriate directory in the NGINX container
COPY ./templates /usr/share/nginx/html

# Expose port 80 (NGINX default)
EXPOSE 80

# Run NGINX in the foreground
CMD ["nginx", "-g", "daemon off;"]
