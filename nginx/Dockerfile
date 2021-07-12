FROM nginx:1.15-alpine

# create sites-enabled -- not in alpine/nginx
ADD sites-enabled/ /etc/nginx/sites-enabled

# copy local version of nginx config
COPY nginx.conf  /etc/nginx/

# create SSL dir for certs
RUN mkdir /etc/nginx/ssl
RUN ls -lsat /etc/nginx/ssl

# add packages not available in Alpine
RUN apk update && apk add nano
RUN apk update && apk add bash

# Install Open SSL and create self-signed certs
RUN apk update && apk add -y openssl

# Generating signing SSL private key
RUN openssl genrsa -des3 -passout pass:urban1234 -out key.pem 2048

# Removing passphrase from private key
RUN cp key.pem key.pem.orig

RUN openssl rsa -passin pass:urban1234 -in key.pem.orig -out key.pem

# Generating certificate signing request
RUN openssl req -new -key key.pem -out cert.csr -subj "/C=US/ST=DC/L=Washington/O=Orgname/OU=Digital/CN=default"

# Generating self-signed certificate
RUN openssl x509 -req -days 3650 -in cert.csr -signkey key.pem -out cert.pem

# install certs
RUN mv cert.csr  /etc/nginx/ssl/cert.csr
RUN mv key.pem   /etc/nginx/ssl/key.pem
RUN mv cert.pem  /etc/nginx/ssl/cert.pem
