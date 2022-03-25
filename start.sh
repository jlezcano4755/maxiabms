function is_in_remote() {
    local existed_in_remote=$(git ls-remote --heads https://unsecusr:unsecpwd1@github.com/jlezcano4755/maxiabms.git ${1})

    if [[ -z ${existed_in_remote} ]]; then
        echo false
    else
        echo true
    fi
}

function lanm() {
	local spin='-\|/'
	local i=0
	while kill -0 ${1} 2>/dev/null
	do
	  i=$(( (i+1) %4 ))
	  printf "\r{2} ${spin:$i:1}"
	  sleep .1
	done
}

branch=${1}
if $(is_in_remote ${branch}); then
	cd /tmp
	echo Cloning project...
	git clone https://unsecusr:unsecpwd1@github.com/jlezcano4755/maxiabms.git -b ${branch} >/dev/null 2>&1
	
	echo Configuring mosquitto...
	# Configuración de Mosquitto
	service mosquitto stop >/dev/null 2>&1
	mkdir -m 777 /run/mosquitto
	service mosquitto start >/dev/null 2>&1

	echo Configuring telegraf...
	# Configuración de Telegraf
	service telegraf stop >/dev/null 2>&1
	cp /tmp/maxiabms/config/telegraf/telegraf.conf /etc/telegraf/
	service telegraf start >/dev/null 2>&1

	echo Configuring influxdb...
	# Configuración de InfluxDB
	service influxdb stop >/dev/null 2>&1
	cp /tmp/maxiabms/config/influxdb/mosquitto.conf /etc/mosquitto/
	cp /tmp/maxiabms/config/influxdb/passwd /etc/mosquitto/
	service influxdb start >/dev/null 2>&1

	echo Configuring grafana...
	# Configuraciónde Grafana
	service grafana-server stop >/dev/null 2>&1
	cp /tmp/maxiabms/config/grafana/grafana_icon.svg /usr/share/grafana/public/img/
	cp /tmp/maxiabms/config/grafana/fav32.png /usr/share/grafana/public/img/
	#Plantillas de Correo Grafana a MaxiaBMS
	cp -r /tmp/maxiabms/config/grafana/emails/ /usr/share/grafana/public/
	service grafana-server start >/dev/null 2>&1

	echo Configuring python environment...
	pip3.8 install -r /tmp/maxiabms/src/requirements.txt >/dev/null 2>&1 &
	lanm $! "Configuring Python environment..."
	
	echo Running project...
	python3.8 /tmp/maxiabms/src/app.py
else
	echo Project $branch does not exist.
fi
