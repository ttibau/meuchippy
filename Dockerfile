FROM ubuntu
MAINTAINER ttibaudev@gmail.com

# Faz o donwload do zip -> instala o zip -> instala python e postgresql -> roda o pip pegando os requeriments

# Chaves PSQL
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Repo
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Python soft properties
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER twitter_user WITH SUPERUSER PASSWORD 'abc123';" &&\
    createdb -O twitter_user twitterdb &&\
    psql --command "ALTER ROLE twitter_user SET client_encoding TO 'utf8';" &&\
    psql --command "ALTER ROLE twitter_user SET default_transaction_isolation TO 'read committed';" &&\
    psql --command "ALTER ROLE twitter_user SET timezone TO 'UTC';" &&\
    psql --command "GRANT ALL PRIVILEGES ON DATABASE twitterdb TO twitter_user;"

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
