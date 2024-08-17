# Utilizar una imagen base de Ubuntu
FROM ubuntu:22.04

# Configurar el entorno
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    libjpeg-dev \
    libpq-dev \
    liblcms2-dev \
    libblas-dev \
    libatlas-base-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    xz-utils \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    nodejs \
    npm \
    git \
    curl \
    wget \
    supervisor \
    libpng-dev \
    libjpeg-dev \
    python3-venv \
    gdebi-core \
    && apt-get clean

# Instalar PostgreSQL
RUN apt-get install -y postgresql postgresql-contrib

# Configurar PostgreSQL
USER postgres
RUN service postgresql start && \
    psql --command "CREATE USER odoo WITH SUPERUSER PASSWORD 'odoo';" && \
    createdb -O odoo odoo && \
    service postgresql stop
USER root

# Crear directorio para Odoo y clonar el repositorio de Odoo
RUN mkdir /odoo
WORKDIR /odoo
RUN git clone https://www.github.com/odoo/odoo --branch 17.0 --depth 1 .

# Copiar los addons personalizados dentro del contenedor
COPY ./addons_custom /mnt/extra-addons

# Instalar dependencias de Python
RUN pip3 install -r requirements.txt

# Exponer el puerto 8069
EXPOSE 8069

# Ejecutar Odoo
CMD ["./odoo-bin", "-c", "/odoo/odoo.conf"]
