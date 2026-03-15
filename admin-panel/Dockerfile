# Stage 1: Build
FROM node:20-alpine AS build-stage
WORKDIR /app
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:stable-alpine AS production-stage
# Copy toàn bộ file đã build vào thư mục gốc của Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Tạo file cấu hình Nginx nội bộ để xử lý Routing của React
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]