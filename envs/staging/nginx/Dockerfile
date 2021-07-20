FROM nginx:1.15-alpine

# create sites-enabled -- not in alpine/nginx
ADD sites-enabled/ /etc/nginx/sites-enabled

# copy local version of nginx config
COPY nginx.conf  /etc/nginx/

# create SSL dir for certs
RUN mkdir /etc/nginx/ssl
COPY ssl/ /etc/nginx/ssl/

# add packages not available in Alpine
RUN apk update && apk add nano bash apache2-utils

# add user
RUN mkdir /etc/apache2/
RUN htpasswd -bcim /etc/apache2/.htpasswd ${NGINX_USER} ${NGINX_PASSWORD}