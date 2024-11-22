container_name=anuff-postgres
password=""
if [ -z "$1" ]; then
    while [ -z "$password" ]; do
        read -p "Enter new admin password: " password
    done
else
    password="$1"
fi
echo "Using passrword '$password' to create $container_name"

if [ ! -z "$(docker ps -a | grep $container_name)" ]; then
    docker rm -f anuff-postgres
fi

docker run \
    --name $container_name \
    -e POSTGRES_PASSWORD=password \
    -d \
    -p 5432:5432 \
    postgres

docker cp ./init.sql $container_name:/var/lib/postgresql/init.sql

timeout 90s bash -c "until docker exec -u postgres $container_name pg_isready ; do sleep 5 ; done"

docker exec -u postgres $container_name psql -c "create user admin with superuser password '$password';"
docker exec -u postgres $container_name psql -c "create database anuff;"
docker exec -u postgres $container_name psql -f /var/lib/postgresql/init.sql anuff
