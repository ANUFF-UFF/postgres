#!/bin/bash
container_name=anuff-postgres
password=""
venv_name=.venv

# if [ -z "$1" ]; then
#     while [ -z "$password" ]; do
#         read -p "Enter new admin password: " password
#     done
# else
#     password="$1"
# fi
# echo "Using passrword '$password' to create $container_name"
#
# if [ ! -z "$(sudo docker ps -a | grep $container_name)" ]; then
#     sudo docker rm -f anuff-postgres
# fi
#
# sudo docker run \
#     --name $container_name \
#     -e POSTGRES_PASSWORD=password \
#     -d \
#     -p 5432:5432 \
#     postgres
#
# sudo docker cp ./init.sql $container_name:/var/lib/postgresql/init.sql
#
# timeout 90s bash -c "until sudo docker exec -u postgres $container_name pg_isready ; do sleep 5 ; done"
#
# sudo docker exec -u postgres $container_name psql -c "create user admin with superuser password '$password';"
# sudo docker exec -u postgres $container_name psql -c "create database anuff;"
# sudo docker exec -u postgres $container_name psql -f /var/lib/postgresql/init.sql anuff

cd ./api_anuff/api_anuff/
if [ ! -d $venv_name ]; then
    python -m venv $venv_name
    $venv_name/bin/python -m pip install -r requirements.txt
fi
$venv_name/bin/python -m fastapi dev
