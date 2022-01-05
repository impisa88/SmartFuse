#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>
 
DHT dht(16, DHT22);

const char* SSID = "CLARO_2GBBF150";
const char* password =  "7DBBF150";
WiFiClient espClient;

const char* mqttServer = "192.168.0.7"; 
const int mqttPort = 1883;
const char* mqttUser = "mosquitto";
const char* mqttPassword = "12345";
const char* mqttTopicSubTemp = "Temperatura"; 
const char* mqttTopicSubUmi = "Umidade"; 
PubSubClient MQTT(espClient);
 
float t; //Temperatura
float h; // Umidade
char mensagem[30];

void reconectabroker();
void leitura();



void setup() {
  WiFi.begin(SSID, password);
  dht.begin();
  Serial.begin(115200);

//********************** Inicia WIFI

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Iniciando conexao com a rede WiFi..");
  }
  Serial.println("Conectado na rede WiFi!");

//********************** Inicia MQTT

  MQTT.setServer(mqttServer, mqttPort);

}

void loop() {
  reconectabroker();
  leitura();
  MQTT.loop();
}

void leitura(){
  h = dht.readHumidity();
  t = dht.readTemperature();
  
  Serial.println(t);
  Serial.println(h);
  sprintf (mensagem,"%f",t);
  MQTT.publish("Temperatura", mensagem);

   sprintf (mensagem,"%f",h);
  MQTT.publish("Umidade", mensagem);
  delay(2000);
}

void reconectabroker()
{
  //Conexao ao broker MQTT
  while (!MQTT.connected())
  {
    Serial.println("Conectando ao broker MQTT...");   
    Serial.println(mqttServer);
    if (MQTT.connect("ESP32"))
    {
      Serial.println("Conectado ao broker!");
    }
    else
    {
      Serial.print("Falha na conexao ao broker - Estado: ");
      Serial.println(MQTT.state());
      delay(1000);
    }
  }
}
