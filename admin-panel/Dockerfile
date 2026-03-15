# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Sao chép package.json và package-lock.json trước để tối ưu layer caching
COPY package*.json ./
RUN npm install

# Sao chép toàn bộ mã nguồn
COPY . .

# Argument build-time cho API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build ứng dụng
RUN npm run build

# Stage phục vụ bằng Nginx
FROM nginx:stable-alpine

# Sao chép file build từ stage trước
COPY --from=build /app/dist /usr/share/nginx/html

# (Tùy chọn) Sao chép file config Nginx nếu cần config custom
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
