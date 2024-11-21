#!/bin/bash

set -eu

pushd "$(dirname "$0")" > /dev/null

# set env variables from .env file
set -a && source .env && set +a

golang_migrate_dir="./golang-migrate/"

if [ ! -d "$golang_migrate_dir" ]; then
	echo "golang-migrate not found. downloading..."

	mkdir -p $golang_migrate_dir
	pushd ./golang-migrate > /dev/null
	curl -L https://github.com/golang-migrate/migrate/releases/download/v${GOLANG_MIGRATE_VERSION}/migrate.linux-amd64.tar.gz | tar xvz
	popd > /dev/null

	echo "golang-migrate installed at $golang_migrate_dir"
fi

pm_tools=(
	"tenable"
	"pmp"
)

for i in "${pm_tools[@]}"; do
	echo "Setting up test database for $i..."

	sql=$(cat <<-END
CREATE DATABASE IF NOT EXISTS ${i}_test;
GRANT ALL PRIVILEGES ON ${i}_test.* TO '$MARIADB_USER'@'$MARIADB_HOST' IDENTIFIED BY '$MARIADB_PWD';
FLUSH PRIVILEGES;
END
)


	echo "Migrating database for $i..."

	echo -e "[client]\nuser=root\npassword=$MARIADB_ROOT_PWD" | sudo mariadb --defaults-extra-file=/dev/stdin -e "$sql"
	./golang-migrate/migrate -path "src/$i/migrations" -database "mysql://$MARIADB_USER:$MARIADB_PWD@tcp($MARIADB_HOST:$MARIADB_PORT)/${i}_test" up


	echo "Test database created and migrated for $i!"
done

popd >> /dev/null;

