#!/usr/bin/env python3
"""
Relay MQTT : consomme depuis Mosquitto et publie vers RabbitMQ (plugin MQTT).
Évite l'incompatibilité bridge.
"""

import paho.mqtt.client as mqtt
import time

# Configuration
MOSQUITTO_HOST = "localhost"  # ou "mosquitto" si dans Docker
MOSQUITTO_PORT = 1884         # port exposé de Mosquitto
RABBITMQ_HOST = "localhost"   # ou "rabbitmq" si dans Docker
RABBITMQ_PORT = 1883          # port MQTT de RabbitMQ

TOPICS = [("rfid/scan", 0), ("key/event", 0), ("ai/anomaly", 0)]

# Client pour s'abonner à Mosquitto
mqtt_sub = mqtt.Client(client_id="relay-sub", protocol=mqtt.MQTTv311)
mqtt_sub.on_connect = lambda client, userdata, flags, rc: print("Connecté à Mosquitto")
mqtt_sub.on_message = lambda client, userdata, msg: publish_to_rabbitmq(msg.topic, msg.payload.decode('utf-8'))

# Client pour publier vers RabbitMQ
mqtt_pub = mqtt.Client(client_id="relay-pub", protocol=mqtt.MQTTv311)
mqtt_pub.on_connect = lambda client, userdata, flags, rc: print("Connecté à RabbitMQ")

def publish_to_rabbitmq(topic, payload):
    """Republie le message vers RabbitMQ."""
    mqtt_pub.publish(topic, payload, qos=0)
    print(f"Relayé : {topic} -> {payload}")

# Connexion et abonnement
mqtt_sub.connect(MOSQUITTO_HOST, MOSQUITTO_PORT, 60)
mqtt_pub.connect(RABBITMQ_HOST, RABBITMQ_PORT, 60)

for topic, qos in TOPICS:
    mqtt_sub.subscribe(topic, qos)

# Boucle principale
mqtt_sub.loop_start()
mqtt_pub.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Arrêt du relay")
    mqtt_sub.loop_stop()
    mqtt_pub.loop_stop()
    mqtt_sub.disconnect()
    mqtt_pub.disconnect()