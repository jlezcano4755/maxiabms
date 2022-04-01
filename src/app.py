import json
import time
import paho.mqtt.client as mqtt
import sys
import multiprocessing

from datetime import date, datetime
from multiprocessing import cpu_count, shared_memory
from socket import create_connection
from umodbus.client import tcp
from numpy import array, ndarray, str_, float32

VERSION = "3.3"
NOMBRE = "Control_Prueba"
LOCAL_IP = "localhost"
broker_address = "localhost"
mbus_gwy1 = '172.20.10.68'  # Direccion de medidor

MINUTO = 60
HORA = 3600  # HORA = 60 * 60 segundos
DIA = 86400  # DIA = 60 * 60 * 24 segundos
SEMANA = 604800  # SEMANA = 60 * 60 * 24 * 7
MINUTOSDIA = 1440  # MINUTOSDIA = 24 * 60

#  Variables para BTD EDECHI
cargo_fijo = 5.06
cargo_dmaxima = 18.39
cargo10KKwh = 0.12286
cargo10_30KKwh = 0.13017
cargo30_50KKwh = 0.13528
cargom50KKwh = 0.15867

cargoEcomerKwh = 0.00887
cargoPEdistribKwh = 0.00725
cargoAPublicoSKwh = 0.00180
cargoAPublicoCKwh = 0.00382

mqtt_exec1 = 0


########################################


# Generates timestamp for general use
def time_stamp():
    obj_today = date.today()
    obj_now = datetime.now()

    curr_year = str(obj_today.year)
    curr_month = str(obj_today.month)
    curr_day = str(obj_today.day)
    curr_hour = str(obj_now.hour)
    curr_minute = str(obj_now.minute)
    curr_second = str(obj_now.second)

    if len(curr_month) < 2:
        curr_month = "0" + curr_month
    if len(curr_day) < 2:
        curr_day = "0" + curr_day
    if len(curr_hour) < 2:
        curr_hour = "0" + curr_hour
    if len(curr_minute) < 2:
        curr_minute = "0" + curr_minute
    if len(curr_second) < 2:
        curr_second = "0" + curr_second

    time_stamps = curr_year + curr_month + curr_day + curr_hour + curr_minute + curr_second

    return time_stamps


########################################


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("MQTT Connected with result code {0}".format(str(rc)))
    sys.stdout.flush()
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("control")


# The callback for when the client receives a CONNACK response from the server.
def on_connect1(client, userdata, flags, rc):
    print("MQTT Connected with result code {0}".format(str(rc)))
    sys.stdout.flush()
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("control")


########################################


# // {
# //   "Controller": "Control_Prueba",     .... ID del Controlador
# //   "Command": "CCON"                   .... CCON=Carga de nuevas constantes
# // }
# The callback for when a PUBLISH message is received from the server.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    sys.stdout.flush()
    doc = json.loads(msg.payload)
    if doc["Controller"] == NOMBRE:
        print("OK Nombre")
        sys.stdout.flush()
        doc = json.loads(msg.payload.decode())
        comando = doc["Command"]
        if comando == "CCON":
            try:
                f = open('/home/maxia/myapp/constants.json', "r")
                constantes = json.loads(f.read())
                cargo_fijo = constantes['cargo_fijo']
                cargo_dmaxima = constantes['cargo_dmaxima']
                cargo10KKwh = constantes['cargo10KKwh']
                cargo10_30KKwh = constantes['cargo10_30KKwh']
                cargo30_50KKwh = constantes['cargo30_50KKwh']
                cargom50KKwh = constantes['cargom50KKwh']
                cargoEcomerKwh = constantes['cargoEcomerKwh']
                cargoPEdistribKwh = constantes['cargoPEdistribKwh']
                cargoAPublicoSKwh = constantes['cargoAPublicoSKwh']
                cargoAPublicoCKwh = constantes['cargoAPublicoCKwh']
                print("cargo fichero constants.json")
            except:
                print("No existe fichero constants.json")
            return
    else:
        print("NO OK Nombre")
        sys.stdout.flush()


# ----------------------------------------------


def combine(a, b):
    if (a == 0 and b == 0):
        return 0
    else:
        variable = a * 65536 + b
        signo = variable >> 31
        exponente = (variable >> 23) & 255
        faccion = variable & 8388607
        resultado = ((-1) ** signo)
        resultado = resultado * (2 ** (exponente - 127) * (1 + (faccion / 8388608)))
        return resultado


# --------------------------------------------


# Client for MQTT connections
def mqtt_send():
    client = mqtt.Client(client_id="")  # create new instance
    client.username_pw_set(username='telegraf', password='telegraf')
    # client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker_address, 1883, 60)  # connect to broker
    client.loop_start()  # start the loop
    return client


# --------------------------------------------
# Client for MQTT connections
def mqtt_send1():
    client = mqtt.Client(client_id="")  # create new instance
    client.username_pw_set(username='telegraf', password='telegraf')
    client.on_message = on_message
    client.on_connect = on_connect1
    client.connect(broker_address, 1883, 60)  # connect to broker
    client.loop_start()  # start the loop
    return client


# ------------------------------------------


def mqtt_MPE1(cola, shm_1):
    #curr_minute = cola.get(True)
    #print(curr_minute)
    #client_ = mqtt_send()
    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    time.sleep(5)
    while True:
        if mqtt_exec1 == 1:
            for i in range(len(slv1_array_)):
                client_.publish("sensores", (slv1_array_[i]['data']) + " valor=" + str(slv1_array_[i]['valor']), qos=0,
                                retain=False)
        for i in range(len(slv1_array_)):
            if i==12:
                print("Register 30073:", slv1_array_[i]['data'] + " value=" + str(slv1_array_[i]['valor']),"time:", datetime.now())
        time.sleep(0.3)


########################################


def lecturaregistrostr1(cola, shm_1):
    multiprocessing.current_process()
    slv1_read = 0
    slv1_fail = 0

    slv1_array = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)

    slv1_array[0]['data'] = 'tr1VoltajeAN'
    slv1_array[1]['data'] = 'tr1VoltajeBN'
    slv1_array[2]['data'] = 'tr1VoltajeCN'
    slv1_array[3]['data'] = 'tr1CurrentA'
    slv1_array[4]['data'] = 'tr1CurrentB'
    slv1_array[5]['data'] = 'tr1CurrentC'
    slv1_array[6]['data'] = 'tr1APowerA'
    slv1_array[7]['data'] = 'tr1APowerB'
    slv1_array[8]['data'] = 'tr1APowerC'
    slv1_array[9]['data'] = 'tr1APowerT'
    slv1_array[10]['data'] = 'tr1FPower'
    slv1_array[11]['data'] = 'tr1Frecuencia'
    slv1_array[12]['data'] = 'Total_Import_Active_Energy'
    slv1_array[13]['data'] = 'tr1EnergiaRAcumulada'
    slv1_array[14]['data'] = 'tr1DPPower'
    slv1_array[15]['data'] = 'tr1DUPower'
    slv1_array[16]['data'] = 'tr1DPRPower'
    slv1_array[17]['data'] = 'tr1VoltajeAB'
    slv1_array[18]['data'] = 'tr1VoltajeBC'
    slv1_array[19]['data'] = 'tr1VoltajeCA'
    slv1_array[20]['data'] = 'tr1THDVAN'
    slv1_array[21]['data'] = 'tr1THDVBN'
    slv1_array[22]['data'] = 'tr1THDVCN'
    slv1_array[23]['data'] = 'tr1THDCA'
    slv1_array[24]['data'] = 'tr1THDCB'
    slv1_array[25]['data'] = 'tr1THDCC'
    slv1_array[26]['data'] = 'tr1DUPowerMax'
    slv1_array[27]['data'] = 'tr1PowerAp'
    slv1_array[28]['data'] = 'tr1PowerQ'
    slv1_array[29]['data'] = 'tr1CurrentN'

    while True:
        # noinspection PyBroadException
        try:
            with create_connection((mbus_gwy1, 502), 1) as sock1:
                if slv1_read == 0:
                    message1 = tcp.read_input_registers(slave_id=1, starting_address=0, quantity=64)
                    message2 = tcp.read_input_registers(slave_id=1, starting_address=70, quantity=40)
                    message3 = tcp.read_input_registers(slave_id=1, starting_address=200, quantity=46)
                    # noinspection PyBroadException
                    try:
                        response1 = tcp.send_message(message1, sock1)
                        response2 = tcp.send_message(message2, sock1)
                        response3 = tcp.send_message(message3, sock1)
                        time.sleep(0.1)
                        slv1_read = 1
                    except Exception:
                        sock1.close()
                        print("sock1 reset")
                        sys.stdout.flush()
                        #mqtt_exec1 = 0
                        slv1_read = 0
                        slv1_fail = 1
                        time.sleep(0.5)

                if slv1_read == 1:
                    if response1 is not None:
                        slv1_array[0]['valor'] = round(combine(response1[0], response1[1]),
                                                       2)  # Phase 1 line to neutral volts
                        slv1_array[1]['valor'] = round(combine(response1[2], response1[3]),
                                                       2)  # Phase 2 line to neutral volts
                        slv1_array[2]['valor'] = round(combine(response1[4], response1[5]),
                                                       2)  # Phase 3 line to neutral volts
                        slv1_array[3]['valor'] = round(combine(response1[6], response1[7]), 2)  # Phase 1 current
                        slv1_array[4]['valor'] = round(combine(response1[8], response1[9]), 2)  # Phase 2 current
                        slv1_array[5]['valor'] = round(combine(response1[10], response1[11]), 2)  # Phase 3 current
                        slv1_array[6]['valor'] = round(combine(response1[12], response1[13]), 2)  # Act Pow Phase 1
                        slv1_array[7]['valor'] = round(combine(response1[14], response1[15]), 2)  # Act Pow Phase 2
                        slv1_array[8]['valor'] = round(combine(response1[16], response1[17]), 2)  # Act Pow Phase 3
                        slv1_array[9]['valor'] = round(combine(response1[52], response1[53]), 2)  # Total system power
                        slv1_array[28]['valor'] = round(combine(response1[60], response1[61]), 2)  # Total system power
                        slv1_array[10]['valor'] = abs(round(combine(response1[62], response1[63]),
                                                            2))  # Total system power factor
                        slv1_array[27]['valor'] = round(combine(response1[56], response1[57]),
                                                        2)  # Total system Aparent Power

                    if response2 is not None:
                        slv1_array[11]['valor'] = round(combine(response2[0], response2[1]), 2)  # Frequency 1
                        slv1_array[12]['valor'] = round(combine(response2[2], response2[3]),
                                                        8)  # Total import energy KWh
                        slv1_array[13]['valor'] = round(combine(response2[6], response2[7]),
                                                        8)  # Total import reactive energy
                        slv1_array[14]['valor'] = round(combine(response2[10], response2[11]),
                                                        2)  # total apparent energy
                        slv1_array[15]['valor'] = round(combine(response2[14], response2[15]),
                                                        2)  # total system power demand
                        slv1_array[26]['valor'] = round(combine(response2[16], response2[17]),
                                                        2)  # Max total system power demand
                        slv1_array[16]['valor'] = round(combine(response2[38], response2[39]),
                                                        2)  # Total system reactive power demand

                    if response3 is not None:
                        slv1_array[17]['valor'] = round(combine(response3[0], response3[1]),
                                                        2)  # Line 1 to Line 2 volts
                        slv1_array[18]['valor'] = round(combine(response3[2], response3[3]),
                                                        2)  # Line 2 to Line 3 volts
                        slv1_array[19]['valor'] = round(combine(response3[4], response3[5]),
                                                        2)  # Line 3 to Line 1 volts
                        slv1_array[20]['valor'] = round(combine(response3[34], response3[35]),
                                                        3)  # Phase 1 L/N volts THD
                        slv1_array[21]['valor'] = round(combine(response3[36], response3[37]),
                                                        3)  # Phase 2 L/N volts THD
                        slv1_array[22]['valor'] = round(combine(response3[38], response3[39]),
                                                        3)  # Phase 3 L/N volts THD
                        slv1_array[23]['valor'] = round(combine(response3[40], response3[41]), 3)  # Phase 1 Current THD
                        slv1_array[24]['valor'] = round(combine(response3[42], response3[43]), 3)  # Phase 2 Current THD
                        slv1_array[25]['valor'] = round(combine(response3[44], response3[45]), 3)  # Phase 3 Current THD
                        slv1_array[29]['valor'] = round(combine(response3[24], response3[25]), 3)  # Phase 3 Current THD
                        slv1_fail = 0

                    gwy_fail = 0

                    response1 = None
                    response2 = None
                    response3 = None
                    slv1_read = 0
                    #mqtt_exec1 = 1
                    time.sleep(0.01)
                    sock1.close()

        except Exception:
            print("Exception", datetime.now())
            sys.stdout.flush()
            gwy_fail = 1
            #mqtt_exec1 = 0
            time.sleep(5)
        time.sleep(0.3)


# ----------------------------------------------------------------------
def demanda_cada_15minutos(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)

    curr_minute = cola.get(True)
    print(curr_minute)
    sys.stdout.flush()
    #client_ = mqtt_send()
    # total system power demand
    tr1DUpoweracn = slv1_array_[15]['valor']

    time.sleep((15 * MINUTO - 0.1))

    tr1DUpoweracns = str(tr1DUpoweracn / 1000)
    if mqtt_exec1 == 1:
        client_.publish("sensores", "tr1DUpoweracn valor=" + tr1DUpoweracns, qos=0, retain=False)
    time.sleep(0.10)

    tr1DUpoweracns = str(0)
    if mqtt_exec1 == 1:
        client_.publish("sensores", "tr1DUpoweracn valor=" + tr1DUpoweracns, qos=0, retain=False)

    while True:
        tr1DUpoweracn = slv1_array_[15]['valor']

        time.sleep((15 * MINUTO - 0.1))

        tr1DUpoweracns = str(tr1DUpoweracn / 1000)
        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1DUpoweracn valor=" + tr1DUpoweracns, qos=0, retain=False)

        time.sleep(0.10)
        tr1DUpoweracns = str(0)
        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1DUpoweracn valor=" + tr1DUpoweracns, qos=0, retain=False)


# ===========================================================================================================
def cada_minuto(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    var_combustible_btd = 0
    print("var_combustible_btd", var_combustible_btd)
    print(datetime.now())
    sys.stdout.flush()

    valor_actualtr1 = 0
    tr1EnergiaAAcumuladafn = 0
    tr1EnergiaAAcumuladamf = 0
    tr1FPtime = 0
    curr_second = datetime.now()

    while curr_second.second != 0:
        time.sleep(0.010)
        curr_second = datetime.now()

    #client_ = mqtt_send1()  # El que va a recibir los comandos

    for num in range(7):
        cola.put(curr_second, True)
    print("curr_minute", curr_second.minute)
    sys.stdout.flush()

    # Total import energy TR1
    if (slv1_array_[12]['valor']) < tr1EnergiaAAcumuladafn:
        tr1EnergiaAAcumuladafn = tr1EnergiaAAcumuladafn + (
                (2147483647 - tr1EnergiaAAcumuladafn) + slv1_array_[12]['valor'])
    else:
        tr1EnergiaAAcumuladafn = slv1_array_[12]['valor']

    valor_actualtr1 = tr1EnergiaAAcumuladafn

    time.sleep(MINUTO)

    while True:
        # Total import energy TR1

        if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladamf:
            tr1EnergiaAAcumuladamf = tr1EnergiaAAcumuladamf + (
                    (2147483647 - tr1EnergiaAAcumuladamf) + slv1_array_[12]['valor'])
        else:
            tr1EnergiaAAcumuladamf = slv1_array_[12]['valor']

        tr1EnergiaAAcumuladamfs = str(tr1EnergiaAAcumuladamf - valor_actualtr1)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladam valor=" + tr1EnergiaAAcumuladamfs, qos=0, retain=False)

        # Calculos temporales
        if curr_second.month == 12:
            diasm = (datetime(curr_second.year + 1, 1, 1) - datetime(curr_second.year, curr_second.month, 1)).days
        else:
            diasm = (datetime(curr_second.year, curr_second.month + 1, 1) - datetime(curr_second.year,
                                                                                     curr_second.month, 1)).days

        # Demanda de Potencia Activa Nueva TR1
        tr1DUpowerac = slv1_array_[15]['valor']

        # Factor de Potencia TR1
        tr1FPpower = slv1_array_[10]['valor']

        # Calculo de tarifa minuto

        tr1EnergiaBf = (tr1EnergiaAAcumuladamf - valor_actualtr1 - (
                    50000 * 5 / ((MINUTOSDIA) * diasm))) * cargom50KKwh + (
                               (cargo10KKwh * 10000) + (cargo10_30KKwh * 20000) + (cargo30_50KKwh * 20000)) * 5 / (
                                   MINUTOSDIA * diasm)

        if abs(tr1FPpower) < 0.9:
            tr1FPtime = tr1FPtime + 1
            if tr1FPtime >= 129600:
                tr1FPpowerBf = (((0.9 - abs(tr1FPpower)) * 100) * 0.02 * (
                        cargoEcomerKwh + cargoPEdistribKwh + cargoAPublicoSKwh + cargoAPublicoCKwh) * (
                                        tr1EnergiaAAcumuladamf - valor_actualtr1))
            else:
                tr1FPpowerBf = 0
        else:
            tr1FPtime = 0
            tr1FPpowerBf = 0

        tr1DUpoweracBf = tr1DUpowerac * cargo_dmaxima * 5 / (MINUTOSDIA * diasm * 1000)
        tr1EnergiaAAcumuladamBf = tr1EnergiaBf + tr1FPpowerBf + (
                tr1EnergiaAAcumuladamf - valor_actualtr1) * var_combustible_btd + \
                                  tr1DUpoweracBf + (cargo_fijo * 5 / (MINUTOSDIA * diasm))

        tr1EnergiaAAcumuladamBfs = str(tr1EnergiaAAcumuladamBf)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladamB valor=" + tr1EnergiaAAcumuladamBfs, qos=0,
                            retain=False)

        valor_actualtr1 = tr1EnergiaAAcumuladamf

        time.sleep(MINUTO)


########################################


def cada_hora(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    var_combustible_btd = 0

    curr_minute = cola.get(True)
    print("curr_hora:", curr_minute.hour)
    sys.stdout.flush()
    #client_ = mqtt_send()
    valor_actualtr1 = 0
    tr1EnergiaAAcumuladafn = 0
    tr1EnergiaAAcumuladahf = 0
    tr1FPtime = 0

    # Total import energy TR1
    if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladafn:
        tr1EnergiaAAcumuladafn = tr1EnergiaAAcumuladafn + (
                (2147483647 - tr1EnergiaAAcumuladafn) + slv1_array_[12]['valor'])
    else:
        tr1EnergiaAAcumuladafn = slv1_array_[12]['valor']

    valor_actualtr1 = tr1EnergiaAAcumuladafn

    # total system power demand cada 15 minutos
    tr1DUpowerac = slv1_array_[15]['valor']

    time.sleep(HORA)

    while True:
        # Total import energy TR1
        if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladahf:
            tr1EnergiaAAcumuladahf = tr1EnergiaAAcumuladahf + (
                    (2147483647 - tr1EnergiaAAcumuladahf) + slv1_array_[12]['valor'])
        else:
            tr1EnergiaAAcumuladahf = slv1_array_[12]['valor']

        tr1EnergiaAAcumuladahfs = str(tr1EnergiaAAcumuladahf - valor_actualtr1)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladah valor=" + tr1EnergiaAAcumuladahfs, qos=0,
                            retain=False)

        # Calculos temporales
        if curr_minute.month == 12:
            diasm = (datetime(curr_minute.year + 1, 1, 1) - datetime(curr_minute.year, curr_minute.month, 1)).days
        else:
            diasm = (datetime(curr_minute.year, curr_minute.month + 1, 1) - datetime(curr_minute.year,
                                                                                     curr_minute.month, 1)).days

        # Factor de Potencia TR1
        tr1FPpower = slv1_array_[10]['valor']

        # Calculo de tarifa hora

        tr1EnergiaBf = (tr1EnergiaAAcumuladahf - valor_actualtr1 - (50000 / ((24) * diasm))) * cargom50KKwh + (
                (cargo10KKwh * 10000) + (cargo10_30KKwh * 20000) + (cargo30_50KKwh * 20000)) / (24 * diasm)

        if (abs(tr1FPpower) < 0.9):
            tr1FPtime = tr1FPtime + 1
            if tr1FPtime >= 129600:
                tr1FPpowerBf = (((0.9 - abs(tr1FPpower)) * 100) * 0.02 * (
                        cargoEcomerKwh + cargoPEdistribKwh + cargoAPublicoSKwh + cargoAPublicoCKwh) * (
                                        tr1EnergiaAAcumuladahf - valor_actualtr1))
            else:
                tr1FPpowerBf = 0
        else:
            tr1FPtime = 0
            tr1FPpowerBf = 0

        tr1DUpoweracBf = tr1DUpowerac * cargo_dmaxima / (24 * diasm * 1000)
        tr1EnergiaAAcumuladahBf = tr1EnergiaBf + tr1FPpowerBf + (
                tr1EnergiaAAcumuladahf - valor_actualtr1) * var_combustible_btd + \
                                  tr1DUpoweracBf + (cargo_fijo / (24 * diasm))

        tr1EnergiaAAcumuladahBfs = str(tr1EnergiaAAcumuladahBf)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladahB valor=" + tr1EnergiaAAcumuladahBfs, qos=0, retain=False)

        client_.publish("prueba", "valor_actualtr1=" + str(valor_actualtr1), qos=0, retain=False)
        valor_actualtr1 = tr1EnergiaAAcumuladahf
        tr1DUpowerac = slv1_array_[15]['valor']

        time.sleep(HORA)


def cada_dia(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    var_combustible_btd = 0

    curr_day = cola.get(True)
    print("curr_day:", curr_day.day)
    sys.stdout.flush()
    #client_ = mqtt_send()
    valor_actualtr1 = 0
    tr1EnergiaAAcumuladafn = 0
    tr1EnergiaAAcumuladadf = 0
    tr1FPtime = 0

    # Total import energy TR1
    if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladafn:
        tr1EnergiaAAcumuladafn = tr1EnergiaAAcumuladafn + (
                (2147483647 - tr1EnergiaAAcumuladafn) + slv1_array_[12]['valor'])
    else:
        tr1EnergiaAAcumuladafn = slv1_array_[12]['valor']

    valor_actualtr1 = tr1EnergiaAAcumuladafn

    # total system power demand cada 15 minutos
    tr1DUpowerac = slv1_array_[15]['valor']
    time.sleep(DIA)

    while True:
        # Total import energy TR1
        if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladadf:
            tr1EnergiaAAcumuladadf = tr1EnergiaAAcumuladadf + (
                    (2147483647 - tr1EnergiaAAcumuladadf) + slv1_array_[12]['valor'])
        else:
            tr1EnergiaAAcumuladadf = slv1_array_[12]['valor']

        tr1EnergiaAAcumuladadfs = str(tr1EnergiaAAcumuladadf - valor_actualtr1)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladad valor=" + tr1EnergiaAAcumuladadfs, qos=0,
                            retain=False)

        # Calculos temporales
        if curr_day.month == 12:
            diasm = (datetime(curr_day.year + 1, 1, 1) - datetime(curr_day.year, curr_day.month, 1)).days
        else:
            diasm = (datetime(curr_day.year, curr_day.month + 1, 1) - datetime(curr_day.year, curr_day.month, 1)).days

        # Factor de Potencia TR1
        tr1FPpower = slv1_array_[10]['valor']

        # Calculo de tarifa dia
        tr1EnergiaBf = (tr1EnergiaAAcumuladadf - valor_actualtr1 - (50000 / diasm)) * cargom50KKwh + (
                (cargo10KKwh * 10000) + (cargo10_30KKwh * 20000) + (cargo30_50KKwh * 20000)) / diasm

        if abs(tr1FPpower) < 0.9:
            tr1FPtime = tr1FPtime + 1
            if tr1FPtime >= 90:
                tr1FPpowerBf = (((0.9 - abs(tr1FPpower)) * 100) * 0.02 * (
                        cargoEcomerKwh + cargoPEdistribKwh + cargoAPublicoSKwh + cargoAPublicoCKwh) * (
                                        tr1EnergiaAAcumuladadf - valor_actualtr1))
            else:
                tr1FPpowerBf = 0
        else:
            tr1FPtime = 0
            tr1FPpowerBf = 0

        tr1DUpoweracBf = tr1DUpowerac * cargo_dmaxima / (diasm * 1000)
        tr1EnergiaAAcumuladadBf = tr1EnergiaBf + tr1FPpowerBf + (
                tr1EnergiaAAcumuladadf - valor_actualtr1) * var_combustible_btd + \
                                  tr1DUpoweracBf + (cargo_fijo / diasm)
        tr1EnergiaAAcumuladadBfs = str(tr1EnergiaAAcumuladadBf)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladadB valor=" + tr1EnergiaAAcumuladadBfs, qos=0, retain=False)

        valor_actualtr1 = tr1EnergiaAAcumuladadf
        tr1DUpowerac = slv1_array_[15]['valor']
        time.sleep(DIA)


def cada_semana(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    var_combustible_btd = 0

    curr_day = cola.get(True)
    dia_semana = curr_day.weekday()
    print("curr_day_week:", dia_semana)
    sys.stdout.flush()
    #client_ = mqtt_send()
    valor_actualtr1 = 0
    tr1EnergiaAAcumuladafn = 0
    tr1EnergiaAAcumuladawf = 0
    tr1FPtime = 0

    # Total import energy TR1
    if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladafn:
        tr1EnergiaAAcumuladafn = tr1EnergiaAAcumuladafn + (
                (2147483647 - tr1EnergiaAAcumuladafn) + slv1_array_[12]['valor'])
    else:
        tr1EnergiaAAcumuladafn = slv1_array_[12]['valor']

    valor_actualtr1 = tr1EnergiaAAcumuladafn

    # total system power demand cada 15 minutos
    tr1DUpowerac = slv1_array_[15]['valor']

    time.sleep(SEMANA)

    while True:
        # Total import energy TR1
        if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladawf:
            tr1EnergiaAAcumuladawf = tr1EnergiaAAcumuladawf + (
                    (2147483647 - tr1EnergiaAAcumuladawf) + slv1_array_[12]['valor'])
        else:
            tr1EnergiaAAcumuladawf = slv1_array_[12]['valor']

        tr1EnergiaAAcumuladawfs = str(tr1EnergiaAAcumuladawf - valor_actualtr1)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladaw valor=" + tr1EnergiaAAcumuladawfs, qos=0,
                            retain=False)

        # Calculos temporales
        if curr_day.month == 12:
            diasm = (datetime(curr_day.year + 1, 1, 1) - datetime(curr_day.year, curr_day.month, 1)).days
        else:
            diasm = (datetime(curr_day.year, curr_day.month + 1, 1) - datetime(curr_day.year, curr_day.month, 1)).days

        # Factor de Potencia TR1
        tr1FPpower = slv1_array_[10]['valor']

        # Calculo de tarifa dia
        tr1EnergiaBf = (tr1EnergiaAAcumuladawf - valor_actualtr1 - (50000 / (diasm / 7))) * cargom50KKwh + (
                (cargo10KKwh * 10000) + (cargo10_30KKwh * 20000) + (cargo30_50KKwh * 20000)) / (diasm / 7)

        if abs(tr1FPpower) < 0.9:
            tr1FPtime = tr1FPtime + 1
            if tr1FPtime >= 13:
                tr1FPpowerBf = (((0.9 - abs(tr1FPpower)) * 100) * 0.02 * (
                        cargoEcomerKwh + cargoPEdistribKwh + cargoAPublicoSKwh + cargoAPublicoCKwh) * (
                                        tr1EnergiaAAcumuladawf - valor_actualtr1))
            else:
                tr1FPpowerBf = 0
        else:
            tr1FPtime = 0
            tr1FPpowerBf = 0

        tr1DUpoweracBf = tr1DUpowerac * cargo_dmaxima / (diasm * 1000 / 7)
        tr1EnergiaAAcumuladawBf = tr1EnergiaBf + tr1FPpowerBf + (
                tr1EnergiaAAcumuladawf - valor_actualtr1) * var_combustible_btd + \
                                  tr1DUpoweracBf + (cargo_fijo / (diasm / 7))
        tr1EnergiaAAcumuladawBfs = str(tr1EnergiaAAcumuladawBf)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladawB valor=" + tr1EnergiaAAcumuladawBfs, qos=0, retain=False)

        valor_actualtr1 = tr1EnergiaAAcumuladawf
        tr1DUpowerac = slv1_array_[15]['valor']

        time.sleep(SEMANA)


def cada_mes(cola, shm_1):
    p = multiprocessing.current_process()

    slv1_array_ = ndarray(core_array_1.shape, dtype=core_array_1.dtype, buffer=shm_1.buf)
    subsidio_ley15 = 0.6
    var_combustible_btd = 0

    #client_ = mqtt_send()
    valor_actualtr1 = 0
    tr1EnergiaAAcumuladafn = 0
    tr1EnergiaAAcumuladamof = 0
    tr1FPtime = 0

    if curr_dia_mes.month == 12:
        diasm = (datetime(curr_dia_mes.year + 1, 1, 1) - datetime(curr_dia_mes.year, curr_dia_mes.month, 1)).days
    else:
        diasm = (datetime(curr_dia_mes.year, curr_dia_mes.month + 1, 1) - datetime(curr_dia_mes.year,
                                                                                   curr_dia_mes.month, 1)).days

    # Total import energy TR1
    if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladafn:
        tr1EnergiaAAcumuladafn = tr1EnergiaAAcumuladafn + (
                (2147483647 - tr1EnergiaAAcumuladafn) + slv1_array_[12]['valor'])
    else:
        tr1EnergiaAAcumuladafn = slv1_array_[12]['valor']

    valor_actualtr1 = tr1EnergiaAAcumuladafn

    # total system power demand cada 15 minutos

    tr1DUpowerac = slv1_array_[15]['valor']
    time.sleep(diasm * 60 * 24 * 60)
    while True:

        # Total import energy TR1
        if slv1_array_[12]['valor'] < tr1EnergiaAAcumuladamof:
            tr1EnergiaAAcumuladamof = tr1EnergiaAAcumuladamof + (
                    (2147483647 - tr1EnergiaAAcumuladamof) + slv1_array_[12]['valor'])
        else:
            tr1EnergiaAAcumuladamof = slv1_array_[12]['valor']

        tr1EnergiaAAcumuladamofs = str(tr1EnergiaAAcumuladamof - valor_actualtr1)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladamo valor=" + tr1EnergiaAAcumuladamofs, qos=0,
                            retain=False)

        # Calculos temporales
        if curr_dia_mes.month == 12:
            diasm = (datetime(curr_dia_mes.year + 1, 1, 1) - datetime(curr_dia_mes.year, curr_dia_mes.month, 1)).days
        else:
            diasm = (datetime(curr_dia_mes.year, curr_dia_mes.month + 1, 1) - datetime(curr_dia_mes.year,
                                                                                       curr_dia_mes.month, 1)).days

        # Factor de Potencia TR1
        tr1FPpower = slv1_array_[10]['valor']

        # Calculo de tarifa dia
        tr1EnergiaBf = (tr1EnergiaAAcumuladamof - valor_actualtr1 - (10000)) * cargo10_30KKwh + (cargo10KKwh * 10000)

        # Calculo de tarifa dia
        tr1EnergiaBf = (tr1EnergiaAAcumuladamof - valor_actualtr1 - (50000)) * cargom50KKwh + (
                (cargo10KKwh * 10000) + (cargo10_30KKwh * 20000) + (cargo30_50KKwh * 20000))

        tr1DUpoweracBf = tr1DUpowerac * cargo_dmaxima / 1000

        if (abs(tr1FPpower) < 0.9):
            tr1FPtime = tr1FPtime + 1
            if tr1FPtime >= 3:
                tr1FPpowerBf = (((0.9 - abs(tr1FPpower)) * 100) * 0.02 * (
                        cargoEcomerKwh + cargoPEdistribKwh + cargoAPublicoSKwh + cargoAPublicoCKwh) * (
                                        tr1EnergiaAAcumuladamof - valor_actualtr1))
            else:
                tr1FPpowerBf = 0
        else:
            tr1FPtime = 0
            tr1FPpowerBf = 0

        if (tr1EnergiaAAcumuladamof - valor_actualtr1 - 10000) > 500000:  # Se aplica el subsidio ley 15
            tr1EnergiaAAcumuladamoBf = tr1FPpowerBf + (tr1EnergiaBf + (
                    tr1EnergiaAAcumuladamof - valor_actualtr1) * var_combustible_btd + tr1DUpoweracBf +
                                                       (cargo_fijo / (7 / diasm))) * (1 + subsidio_ley15 / 100)
        else:
            tr1EnergiaAAcumuladamoBf = tr1FPpowerBf + (tr1EnergiaBf + (
                    tr1EnergiaAAcumuladamof - valor_actualtr1) * var_combustible_btd + tr1DUpoweracBf +
                                                       (cargo_fijo / (7 / diasm)))

        tr1EnergiaAAcumuladamoBfs = str(tr1EnergiaAAcumuladamoBf)

        if mqtt_exec1 == 1:
            client_.publish("sensores", "tr1EnergiaAAcumuladamoB valor=" + tr1EnergiaAAcumuladamoBfs, qos=0,
                            retain=False)

        valor_actualtr1 = tr1EnergiaAAcumuladamof
        tr1DUpowerac = slv1_array_[15]['valor']

        time.sleep(diasm * 60 * 60 * 24)


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    print("Start running @", datetime.now())
    sys.stdout.flush()
    cpus = cpu_count()
    print("Número de cpus:", cpus)
    print("Prueba:", VERSION)
    sys.stdout.flush()
    try:
        f = open('/home/maxia/myapp/constants.json', "r")
        constantes = json.loads(f.read())
        cargo_fijo = constantes['cargo_fijo']
        cargo_dmaxima = constantes['cargo_dmaxima']
        cargo10KKwh = constantes['cargo10KKwh']
        cargo10_30KKwh = constantes['cargo10_30KKwh']
        cargo30_50KKwh = constantes['cargo30_50KKwh']
        cargom50KKwh = constantes['cargom50KKwh']
        cargoEcomerKwh = constantes['cargoEcomerKwh']
        cargoPEdistribKwh = constantes['cargoPEdistribKwh']
        cargoAPublicoSKwh = constantes['cargoAPublicoSKwh']
        cargoAPublicoCKwh = constantes['cargoAPublicoCKwh']
        print("Cargo fichero constants.json")
    except:
        print("No existe fichero constants.json")

    cola = multiprocessing.Queue()

    core_array_1 = array([('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0),
                          ('', 0.0)
                          ], dtype=[('data', (str_, 30)), ('valor', float32)])

    shm_1 = shared_memory.SharedMemory(create=True, size=core_array_1.nbytes)

    time.sleep(5)

    task0 = multiprocessing.Process(target=lecturaregistrostr1, args=(cola, shm_1,))
    task0.daemon = True

    task2 = multiprocessing.Process(target=cada_minuto, args=(cola, shm_1,))
    task2.daemon = True

    task3 = multiprocessing.Process(target=cada_hora, args=(cola, shm_1,))
    task3.daemon = True

    task4 = multiprocessing.Process(target=cada_dia, args=(cola, shm_1,))
    task4.daemon = True

    task5 = multiprocessing.Process(target=cada_semana, args=(cola, shm_1,))
    task5.daemon = True

    task6 = multiprocessing.Process(target=cada_mes, args=(cola, shm_1,))
    task6.daemon = True

    task7 = multiprocessing.Process(target=demanda_cada_15minutos, args=(cola, shm_1))
    task7.daemon = True

    mqtt_MPE1_task = multiprocessing.Process(target=mqtt_MPE1, args=(cola, shm_1,))
    mqtt_MPE1_task.daemon = True

    task0.start()

    time.sleep(2)

    #task2.start()
    #task3.start()
    #task4.start()
    #task5.start()
    #task6.start()
    #task7.start()

    mqtt_MPE1_task.start()

while True:
    time.sleep(5)
