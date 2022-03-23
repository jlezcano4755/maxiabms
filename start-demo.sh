#!/bin/bash

if !([ -x "$(command -v docker)" ]); then
	echo 'Installing Docker Engine...'
    apt-get -qq update
    apt-get -qq install ca-certificates curl gnupg lsb-release -y
    curl --silent -fsSL https://download.docker.com/linux/debian/gpg | gpg --batch --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
    	$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  	apt-get -qq install docker-ce docker-ce-cli containerd.io -y
fi
echo 'Running Demo...'
docker run -it alecjz4755/maxiabms:demo
