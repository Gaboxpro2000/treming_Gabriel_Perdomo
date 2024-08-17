# Utilizar la imagen oficial de Odoo 17
FROM odoo:17.0

# Instalar dependencias adicionales si es necesario
RUN apt-get update && apt-get install -y \
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

RUN mkdir -p /mnt/extra-addons/

# Copiar los addons personalizados dentro del contenedor
COPY ../addons_customs/package_calculation /mnt/extra-addons/package_calculation

# Exponer el puerto 8069
EXPOSE 8069

# Ejecutar Odoo
CMD ["odoo"]
