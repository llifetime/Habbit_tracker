# nginx/Dockerfile
FROM nginx:alpine

# Удаление дефолтной конфигурации
RUN rm /etc/nginx/conf.d/default.conf

# Копирование нашей конфигурации
COPY nginx.conf /etc/nginx/conf.d/

# Создание директории для статики
RUN mkdir -p /static /media

EXPOSE 80