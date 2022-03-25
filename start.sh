function is_in_remote() {
    local existed_in_remote=$(git ls-remote --heads https://unsecusr:unsecpwd1@github.com/jlezcano4755/maxiabms.git ${1})

    if [[ -z ${existed_in_remote} ]]; then
        echo false
    else
        echo true
    fi
}

apt-get install git -y
branch=${1}
if $(is_in_remote ${branch}); then
	cd /tmp
	git clone https://unsecusr:unsecpwd1@github.com/jlezcano4755/maxiabms.git -b ${branch}

	# Configuración de Mosquitto
	service mosquitto stop
	mkdir -m 777 /run/mosquitto
	service mosquitto start

	# Configuración de Telegraf
	service telegraf stop
	cp /tmp/maxiabms/config/telegraf/telegraf.conf /etc/telegraf/
	service telegraf start

	# Configuración de InfluxDB
	service influxdb stop
	cp /tmp/maxiabms/config/influxdb/mosquitto.conf /etc/mosquitto/
	cp /tmp/maxiabms/config/influxdb/passwd /etc/mosquitto/
	service influxdb start

	# Configuraciónde Grafana
	service grafana-server stop
	cp /tmp/maxiabms/config/grafana/grafana_icon.svg /usr/share/grafana/public/img/
	cp /tmp/maxiabms/config/grafana/fav32.png /usr/share/grafana/public/img/
	#Plantillas de Correo Grafana a MaxiaBMS
	cp -r /tmp/maxiabms/config/grafana/emails/ /usr/share/grafana/public/
	service grafana-server start

	pip3.8 install -r /tmp/maxiabms/src/requirements.txt
	python3.8 /tmp/maxiabms/src/app.py
else
	echo El proyecto $branch no existe en el sistema.
fi
