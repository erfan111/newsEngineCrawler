#!/bin/bash
if [[ ! -f .env ]]; then
	sudo apt-get update
	sudo apt-get install git mongodb htop build-essential libxml2 libxml2-dev libssl-dev libffi-dev libxslt1-dev zlib1g-dev
	sudo apt-get install python-dev python3-dev python3-virtualenv python-virtualenv python-pip python3-pip
	sudo locale-gen "en_US.UTF-8"
	export LC_ALL="en_US.UTF-8"		 
	mkdir -p .venv/
	virtualenv -p python3 .venv
	source .venv/bin/activate
	pip3 install -r requirements.txt
	echo "run again"
	touch .env
	exit 0
fi 
source .venv/bin/activate
var=1
while [ 1 ];
do
	((var++))
	echo "Crawl started"
	scrapy crawl Tabnak >> scrapy.log
	scrapy crawl Aftabnews >> scrapy.log
	scrapy crawl KhabarOnline >> scrapy.log
	scrapy crawl Farsnews >> scrapy.log
	scrapy crawl Javan >> scrapy.log
	echo "Crawl finished"
	if [[ $(( var % 20 )) == 0 ]];then
		echo "n-gram started"
		python3 nearDetection.py
		curl -u erfan:123 -X POST http://78.47.195.58:8080/index >> scrapy.log
		echo "n-gram finished"
	fi
	sleep 20
done
