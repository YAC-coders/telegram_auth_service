FROM nginx:1.29.0-alpine

WORKDIR /etc/nginx

COPY . .

RUN rm -f /etc/nginx/conf.d/default.conf

EXPOSE 80 443
