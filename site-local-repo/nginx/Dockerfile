FROM nginx:1.27-alpine

COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/ssl

COPY ssl/ /etc/nginx/ssl/


EXPOSE 80 443
