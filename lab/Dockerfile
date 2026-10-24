ARG PHP_IMAGE=php:8.5.11-apache
FROM ${PHP_IMAGE}

COPY apache/mpm_prefork.conf /etc/apache2/mods-available/mpm_prefork.conf
COPY apache/zzz-lab.conf /etc/apache2/conf-available/zzz-lab.conf
COPY php/lab.ini /usr/local/etc/php/conf.d/zz-lab.ini
COPY www/ /var/www/html/

RUN a2enconf zzz-lab \
    && chown -R www-data:www-data /var/www/html
