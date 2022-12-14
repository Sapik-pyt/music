FROM nginx:1.19.8-alpine
RUN rm /etc/nginx/conf.d/default.conf 
# выше удаляем конфиг с настройкми и вставляем свой
COPY default.conf /etc/nginx/conf.d