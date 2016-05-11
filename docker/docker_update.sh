#/bin/sh -ev
# script to update docker environment within travis
sudo apt-get update;
sudo apt-get -o Dpkg::Options::="--force-confnew" --yes --force-yes install docker-engine;
curl -L https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` > docker-compose;
chmod +x docker-compose;
sudo mv docker-compose /usr/local/bin;