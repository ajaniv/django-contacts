#!/bin/bash -exv
#Script to run django within a dockerized environment

PYTHON=python
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=${DIR}/..
DJANGO_SETTINGS_MODULE=django_core_models_settings.settings

source ${DIR}/docker_cmd.sh

if [ "$TYPE" = "mysql" ]; then
	$PYTHON scripts/mysql_init.py -d $DB_HOST
fi

$PYTHON manage.py migrate --setting=$DJANGO_SETTINGS_MODULE
$PYTHON scripts/create_super_user.py --setting=$DJANGO_SETTINGS_MODULE
$PYTHON manage.py runserver 0.0.0.0:8000 --setting=$DJANGO_SETTINGS_MODULE
