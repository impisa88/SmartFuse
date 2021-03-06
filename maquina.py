import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from E000F import *
import sys

class MqttClient(QtCore.QObject):
    Disconnected = 0
    Connecting = 1
    Connected = 2

    MQTT_3_1 = mqtt.MQTTv31
    MQTT_3_1_1 = mqtt.MQTTv311

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    stateChanged = QtCore.pyqtSignal(int)
    hostnameChanged = QtCore.pyqtSignal(str)
    portChanged = QtCore.pyqtSignal(int)
    keepAliveChanged = QtCore.pyqtSignal(int)
    cleanSessionChanged = QtCore.pyqtSignal(bool)
    protocolVersionChanged = QtCore.pyqtSignal(int)

    messageSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MqttClient, self).__init__(parent)

        self.m_hostname = "192.168.0.7"
        self.m_port = 1883
        self.m_keepAlive = 60
        self.m_cleanSession = True
        self.m_protocolVersion = MqttClient.MQTT_3_1

        self.m_state = MqttClient.Disconnected

        self.m_client =  mqtt.Client(clean_session=self.m_cleanSession,
            protocol=self.protocolVersion)

        self.m_client.on_connect = self.on_connect
        self.m_client.on_message = self.on_message
        self.m_client.on_disconnect = self.on_disconnect


    @QtCore.pyqtProperty(int, notify=stateChanged)
    def state(self):
        return self.m_state

    @state.setter
    def state(self, state):
        if self.m_state == state: return
        self.m_state = state
        self.stateChanged.emit(state)

    @QtCore.pyqtProperty(str, notify=hostnameChanged)
    def hostname(self):
        return self.m_hostname

    @hostname.setter
    def hostname(self, hostname):
        if self.m_hostname == hostname: return
        self.m_hostname = hostname
        self.hostnameChanged.emit(hostname)

    @QtCore.pyqtProperty(int, notify=portChanged)
    def port(self):
        return self.m_port

    @port.setter
    def port(self, port):
        if self.m_port == port: return
        self.m_port = port
        self.portChanged.emit(port)

    @QtCore.pyqtProperty(int, notify=keepAliveChanged)
    def keepAlive(self):
        return self.m_keepAlive

    @keepAlive.setter
    def keepAlive(self, keepAlive):
        if self.m_keepAlive == keepAlive: return
        self.m_keepAlive = keepAlive
        self.keepAliveChanged.emit(keepAlive)

    @QtCore.pyqtProperty(bool, notify=cleanSessionChanged)
    def cleanSession(self):
        return self.m_cleanSession

    @cleanSession.setter
    def cleanSession(self, cleanSession):
        if self.m_cleanSession == cleanSession: return
        self.m_cleanSession = cleanSession
        self.cleanSessionChanged.emit(cleanSession)

    @QtCore.pyqtProperty(int, notify=protocolVersionChanged)
    def protocolVersion(self):
        return self.m_protocolVersion

    @protocolVersion.setter
    def protocolVersion(self, protocolVersion):
        if self.m_protocolVersion == protocolVersion: return
        if protocolVersion in (MqttClient.MQTT_3_1, MQTT_3_1_1):
            self.m_protocolVersion = protocolVersion
            self.protocolVersionChanged.emit(protocolVersion)

    #################################################################
    @QtCore.pyqtSlot()
    def connectToHost(self):
        if self.m_hostname:
            self.m_client.connect(self.m_hostname,
                port=self.port,
                keepalive=self.keepAlive)

            self.state = MqttClient.Connecting
            self.m_client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        self.m_client.disconnect()

    def subscribe(self, path):
        if self.state == MqttClient.Connected:
            self.m_client.subscribe(path)

    #################################################################
    # callbacks
    def on_message(self, mqttc, obj, msg):
        mstr = msg.payload.decode()
        # print("on_message", mstr, obj, mqttc)
        self.messageSignal.emit(mstr)

    def on_connect(self, *args):
        # print("on_connect", args)
        self.state = MqttClient.Connected
        self.connected.emit()

    def on_disconnect(self, *args):
        # print("on_disconnect", args)
        self.state = MqttClient.Disconnected
        self.disconnected.emit()

class Machine(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, brokerTemperature = "", brokerHumidity = ""):
        super().__init__(parent)
        super().setupUi(self)

        self.brokerTemperature = brokerTemperature
        self.brokerHumidity = brokerHumidity
        self.host = "192.168.0.7"

        self.client_temperature = MqttClient(self)
        self.client_temperature.stateChanged.connect(self.on_stateChanged_Temperature)
        self.client_temperature.messageSignal.connect(self.on_messageSignal_Temperature)
        self.client_temperature.hostname = self.host
        self.client_temperature.connectToHost()

        self.client_Humidity= MqttClient(self)
        self.client_Humidity.stateChanged.connect(self.on_stateChanged_Humidity)
        self.client_Humidity.messageSignal.connect(self.on_messageSignal_Humidity)
        self.client_Humidity.hostname = self.host
        self.client_Humidity.connectToHost()

    @QtCore.pyqtSlot(int)
    def on_stateChanged_Temperature(self, state):
        if state == MqttClient.Connected:
            print(state)
            self.client_temperature.subscribe(self.brokerTemperature)

    @QtCore.pyqtSlot(str)
    def on_messageSignal_Temperature(self, msg):
        try:
            val = float(msg)
            self.lcdTemperatura.display(val)
        except ValueError:
            print("error: Not is number")

    @QtCore.pyqtSlot(int)
    def on_stateChanged_Humidity(self, state):
        if state == MqttClient.Connected:
            print(state)
            self.client_Humidity.subscribe(self.brokerHumidity)

    @QtCore.pyqtSlot(str)
    def on_messageSignal_Humidity(self, msg):
        try:
            val = float(msg)
            self.lcdUmidade.display(val)
        except ValueError:
            print("error: Not is number")

if __name__ == '__main__':
    qt = QApplication(sys.argv)
    E002F = Machine(brokerTemperature="Temperatura", brokerHumidity="Umidade")
    E002F.show()
    qt.exec_()
