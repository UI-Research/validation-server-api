#!/bin/bash
# Deployment script for tax calculator
# Purpose: copies the correct docker-compose, requirements.txt, and .env file to
#          the correct locations and then runs the docker commands and initialization
#          scripts.
# Command: ./deploy.sh [environment]] -[destroy] -[restart]  > deployment.log
# Options: environment = development, staging, or production
#          -destroy = delete all containers and images before Building
#          -restart = restart docker-machine before building Containers
#          > deployment.log = write starttup messages to a file 'deployment.log'
#

echo "-----------------------------------------------------"
echo "Starting build:  $(date)"
echo "-----------------------------------------------------"
SECONDS=0

while getopts "e:m:r:d:i:c:" option; do
  case $option in
    e ) env=$OPTARG
    ;;
    m ) machine_name=$OPTARG
    ;;
    r ) restart=$OPTARG
    ;;
    d ) destroy=$OPTARG
    ;;
    i ) import=$OPTARG
    ;;
    c ) check=$OPTARG
    ;;
    o ) options=$OPTARG
    ;;
  esac
done


if [[ "$destroy" == "destroy" ]]
then
  destroy=1
else
  destroy=0
fi

if [[ "$restart" == "restart" ]]
then
  restart=1
else
  restart=0
fi

if [[ "$import" == "import" ]]
then
  import=1
else
  import=0
fi

if [[ "$check" == "check" ]]
then
  check=1
else
  check=0
fi

if [[ "$options" == "interactive" ]]
then
  interactive=1
else
  interactive=0
fi


if [[ "$env" == "prod" ]]
then
  environment="production"
elif [[ "$env" == "stg" ]]
then
  environment="staging"
elif [[ "$env" == "dev" ]]
then
  environment="development"
else
  environment=$env
fi


echo "-----------------------------------------------------"
echo "Inputs from command"
echo "-----------------------------------------------------"
echo "env: $env"
echo "environment: $environment"
echo "machine_name: $machine_name"
echo "restart: $restart"
echo "destroy: $destroy"
echo "import: $import"
echo "check: $check"


has_docker_machine=$(which docker-machine)

if [ -z "$has_docker_machine" ]
then
  docker_machine=0
else
  docker_machine=1
fi

echo "has docker machine: $has_docker_machine"
echo "docker machine flag: $docker_machine"
echo "docker machine condition: (($docker_machine != 0 ))"


# check arguments
if [ -z "$environment" ]
then
  echo "No environment was passed. Specify development, staging, or production."
  exit 1 # terminate and indicate error
fi

if [ -z "$machine_name" ]
then
  echo "No machine_name was passed, using default as docker-machine."
  machine_name=default
fi

# Is docker machine running
echo "Check if Docker-machine is running..."
if (($docker_machine == 1 ))
then
  docker_running=$(docker-machine status $machine_name)
  echo "-----------------------------------------------------"
  echo "Docker-machine status for $machine_name: $docker_running"
  echo "-----------------------------------------------------"


  if [[ "$docker_running" == *"Running"* ]]
  then
    echo "-----------------------------------------------------"
    echo "Docker-machine is running...set environment variables."
    echo "-----------------------------------------------------"
    eval "$(docker-machine env $machine_name)"
  fi

  if [[ "$docker_running" == *"Stopped"* ]]
  then
    echo "-----------------------------------------------------"
    echo "Docker-machine is stopped...start machine."
    echo "-----------------------------------------------------"
    $(docker-machine start $machine_name)
    echo "-----------------------------------------------------"
    echo "Set environment variables."
    echo "-----------------------------------------------------"
    eval "$(docker-machine env $machine_name)"
  fi
  if [[ "$docker_running" == *"Saved"* ]]
    then
      echo "-----------------------------------------------------"
      echo "Docker-machine is Saved...start machine."
      echo "-----------------------------------------------------"
      $(docker-machine start $machine_name)
      echo "-----------------------------------------------------"
      echo "Set environment variables."
      echo "-----------------------------------------------------"
      eval "$(docker-machine env $machine_name)"
  fi

  echo "-----------------------------------------------------"
  echo "Checking if destroy command was passed"
  echo "-----------------------------------------------------"
  if (($destroy != 0 ))
    then
      echo "-------------------------------------------------------------------"
      echo "Destroy was passed -- clearing out existing containers and images."
      echo "-------------------------------------------------------------------"
      eval $(docker stop $(docker ps -a -q)  && docker rm $(docker ps -a -q) --force && docker rmi $(docker images -a -q) --force)
  else
    echo "-----------------------------------------------------"
    echo "Destroy was not passed -- using containers."
    echo "-----------------------------------------------------"
  fi

  echo "-----------------------------------------------------"
  echo "Checking if restart command was passed"
  echo "-----------------------------------------------------"
  if (($restart != 0 ))
    then
      echo "-------------------------------------------------------------------"
      echo "Restart was passed -- restart docker machine."
      echo "-------------------------------------------------------------------"
      eval $(docker-machine restart $machine_name)
  else
    echo "-----------------------------------------------------"
    echo "Restart was not passed -- using existing docker machine."
    echo "-----------------------------------------------------"
  fi
else
  echo "-----------------------------------------------------"
  echo "Docker machine not installed - no restart is possible"
  echo "-----------------------------------------------------"
fi

# Set ENV variables
# Copy assets from deployment directories to execute directory
if [ ! -d "./envs/$environment" ]; then
  echo "./envs/$environment directory does not exist."
  exit 1 # terminate and indicate error
fi

if [ ! -f "./envs/$environment/docker-compose.yml" ]; then
  echo "$environment directory or docker-compose.yml do not exist."
  exit 1 # terminate and indicate error
fi

echo "-----------------------------------------------------"
echo "copying nginx files for $environment "
echo "-----------------------------------------------------"

echo "Loading $environment scripts"
cp -fr ./envs/$environment/nginx/sites-enabled ./nginx/
cp -fr ./envs/$environment/nginx/Dockerfile ./nginx/Dockerfile
cp -fr ./envs/$environment/docker-compose.yml ./docker-compose.yml
cp -fr ./envs/$environment/requirements.txt ./requirements.txt
cp -fr ./envs/$environment/nginx/ssl ./nginx/
echo "-----------------------------------------------------"

if [ ! -f "./docker-compose.yml" ]; then
  echo "docker-compose.yml does not exist. Was it copied?"
  exit 1 # terminate and indicate error
fi

# set .env vars
export $(grep -v '^#' .env | xargs)

if (($import != 0 ))
  then
  # Create DB Structure
  echo "-----------------------------------------------------"
  echo "Copy database dump to ./django-rest-app/scripts/mysql-dump"
  echo "Data will be imported when container is created"
  echo "-----------------------------------------------------"
  cp -fr ./$APP_DIR/scripts/$MYSQL_DATABASE_CREATE_SQL ./django-rest-app/scripts/mysql-dump/$MYSQL_DATABASE_CREATE_SQL
else
  echo "-----------------------------------------------------"
  echo "Database dump was removed from ./django-rest-app/scripts/mysql-dump"
  echo "No database created or updated because 'I' flag not passed"
  echo "-----------------------------------------------------"
  rm -rf ./$APP_DIR/scripts/mysql-dump/$MYSQL_DATABASE_CREATE_SQL

fi

echo "-----------------------------------------------------"
echo "Export mysql data"
echo "-----------------------------------------------------"
docker exec web python manage.py dumpdata --output mydata.json


#exit 1 # terminate and indicate error


if [ -f "./docker-compose.yml" ]; then

  docker_ip=$(docker-machine ip $machine_name)

  echo "-----------------------------------------------------"
  echo "Starting containers on $docker_ip"
  echo "-----------------------------------------------------"

  # Build Containers
  echo "-----------------------------------------------------"
  echo "Building containers"
  echo "-----------------------------------------------------"
  docker-compose build

  # Start Containers
  echo "-----------------------------------------------------"
  echo "Starting containers"
  echo "-----------------------------------------------------"
  if (($interactive != 0 ))
    then
      echo "-----------------------------------------------------"
      echo "Running as interactive so create superuser and checks will not run"
      echo "-----------------------------------------------------"
      docker-compose up --remove-orphans
      echo "-----------------------------------------------------"
      echo "Running as interactive allows changes in code to compile on server"
      echo "-----------------------------------------------------"

  else
      echo "-----------------------------------------------------"
      echo "Running as detached so create superuser and checks will run"
      echo "-----------------------------------------------------"

      docker-compose up -d --remove-orphans
      echo "-----------------------------------------------------"
      echo "Running as detached means rebuilding containers to recompile code"
      echo "-----------------------------------------------------"

      echo "-----------------------------------------------------"
      echo "Pause to allow things to come up"
      echo "-----------------------------------------------------"
      sleep 15

      # Initialize Application
      echo "-----------------------------------------------------"
      echo "Create superuser"
      echo "-----------------------------------------------------"
      docker exec -tt web python manage.py createsuperuser --noinput

      echo "-----------------------------------------------------"
      echo "Create static files"
      echo "-----------------------------------------------------"
      docker exec web python manage.py collectstatic --noinput

      echo "-----------------------------------------------------"
      echo "Import mysql data"
      echo "-----------------------------------------------------"
      docker exec web python manage.py loaddata mydata.json


      docker_ip=$(docker-machine ip $machine_name)
      echo "-----------------------------------------------------"
      echo "Containers are running on $docker_ip"
      echo "-----------------------------------------------------"

      # Run tests
      echo "-----------------------------------------------------"
      echo "Run tests"
      echo "-----------------------------------------------------"
    fi

    minutes=$((SECONDS/60))
    seconds=$((SECONDS%60))

    echo "-----------------------------------------------------"
    echo "Ending build:  $(date)"
    echo "Build took $minutes minutes and $seconds seconds."
    echo "-----------------------------------------------------"

    # These are dependency and security checks that should be run on each build.
    # Any security issues should be mitagated or a description of why they are
    #     not relevant should be included below.

    if (($check != 0 ))
      then
      echo "-----------------------------------------------------"
      echo "PEP8 checks"
      echo "-----------------------------------------------------"
      exec -it web pep8 --show-source --show-pep8 testsuite/E40.py
      exec -it web pep8 --statistics -qq Python-3.6/Lib

      echo "-----------------------------------------------------"
      echo "Dependency checks"
      echo "Only works with versioned packages check"
      echo "-----------------------------------------------------"
      echo "Dependency Security check"
      echo "-----------------------------------------------------"
      docker exec -it web safety check --json -r requirements.txt
      echo "-----------------------------------------------------"
      echo "Version check"
      echo "-----------------------------------------------------"
      docker exec -it web pip-check -a -H

      # Any security issues should be mitagated or a description of why they are
      #     not relevant should be inccluded below.
      echo "-----------------------------------------------------"
      echo "Django Security check"
      echo "-----------------------------------------------------"
      docker exec -it web python manage.py check --deploy

      echo "-----------------------------------------------------"
      echo "Bandit Security check"
      echo "-----------------------------------------------------"
      docker exec -it web bandit -r $APP_DIR/

      echo "-----------------------------------------------------"
      echo "License check"
      echo "-----------------------------------------------------"
      docker exec -it web  pip-licenses --with-system --with-urls --order=license
    else
      echo "-----------------------------------------------------"
      echo "No security or version checks were donw"
      echo "-----------------------------------------------------"
    fi

    minutes=$((SECONDS/60))
    seconds=$((SECONDS%60))

    echo "-----------------------------------------------------"
    echo "Ending build:  $(date)"
    echo "Build took $minutes minutes and $seconds seconds."
    echo "-----------------------------------------------------"

fi # end running detached

# unset .env vars
unset $(grep -v '^#' .env | sed -E 's/(.*)=.*/\1/' | xargs)
