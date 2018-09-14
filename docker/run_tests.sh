#!/bin/bash -e
#Script to run django unit tests within a dockerized environment

usage() { echo "Usage: $0  [-w <seconds>] [-t <mysql|postgres|sqlite> -d <db_host>" 1>&2; exit 1; }

DELAY=1
TYPE="sqlite"


while getopts "w:d:t:" opt; do
  case $opt in
    d)
      DB_HOST=$OPTARG
      ;;
    t)
      TYPE=$OPTARG
      ;;
    w)
      DELAY=$OPTARG
      ;;
    
    *)
      usage
      ;;
  esac
done


if [ -z "$DB_HOST" ]; then
    usage
fi  

echo "db_type:" $TYPE
echo "db host:" $DB_HOST
echo "Delay in seconds:" $DELAY

sleep $DELAY

if [ "$TYPE" = "mysql" ]; then
	python scripts/mysql_init.py -d $DB_HOST
fi

python manage.py test --settings=django_core_models_settings.settings_test
