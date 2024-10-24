# Infra-Config


## Nginx

1. **OpenSSL로 자체 서명**
   ```shell
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout certs/server.key -out certs/server.crt
   ```

2. **Compose로 구성**

