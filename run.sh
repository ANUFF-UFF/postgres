#!/bin/bash
container_name=anuff-postgres
venv_name=.venv

# arquivo de variaveis de ambiente com a seguinte cara:
if [ -f ./set_env ]; then
    . set_env
else
    echo criando arquivo set_env
    read -p "USERNAME: " user
    read -p "PASSWORD: " password
    read -p "HOSTNAME: " name
    read -p "DATABASE: " database
    echo export USERNAME="$user" >> set_env
    echo export PASSWORD="$password" >> set_env
    echo export HOSTNAME="$name" >> set_env
    echo export DATABASE="$database" >> set_env
fi

echo "Using password '$PASSWORD' to create $container_name"

if [ ! -z "$(sudo docker ps -a | grep $container_name)" ]; then
    sudo docker rm -f anuff-postgres
fi

sudo docker run \
    --name $container_name \
    -e POSTGRES_PASSWORD=$PASSWORD \
    -d \
    -p 5432:5432 \
    postgres

# sudo docker cp ./init.sql $container_name:/var/lib/postgresql/init.sql

timeout 90s bash -c "until sudo docker exec -u postgres $container_name pg_isready ; do sleep 5 ; done"

sudo docker exec -u postgres $container_name psql -c "create user $USERNAME with superuser password '$PASSWORD';"
sudo docker exec -u postgres $container_name psql -c "create database $DATABASE;"
# sudo docker exec -u postgres $container_name psql -f /var/lib/postgresql/init.sql anuff

cd ./api_anuff/api_anuff/
if [ ! -d $venv_name ]; then
    python -m venv $venv_name
    $venv_name/bin/python -m pip install -r requirements.txt
fi
$venv_name/bin/python -m fastapi dev

cd ../..
