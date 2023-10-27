# Usamos una imagen base de Ubuntu
FROM ubuntu:latest

# Instalamos python3 y pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copiamos nuestro código al contenedor
COPY clientHTTP.py /opt/clientHTTP.py

# Establecemos el directorio de trabajo en /opt
WORKDIR /opt

# Indicamos el comando por defecto para ejecutar el script cuando se inicie el contenedor
CMD ["python3", "clientHTTP.py"]
