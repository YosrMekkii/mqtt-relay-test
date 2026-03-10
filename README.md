# MQTT Relay Test

Ce repository contient un projet de simulation et de test pour un **relay MQTT** reliant **Mosquitto** (broker MQTT local) à **RabbitMQ** (avec plugin MQTT). Il simule la partie IoT d'un système de gestion de clés RFID intelligentes, en relayant les messages de scans RFID de manière persistante et fiable. Cela résout les problèmes de connexions instables des bridges intégrés, comme mentionné par les encadrants.

## Architecture

Le système fonctionne comme suit :
- **IoT (Scanner RFID simulé)** → Publie sur Mosquitto (topic `rfid/scan`).
- **Mosquitto** (port 1884) → Broker MQTT local pour les publications IoT.
- **mqtt_relay.py** → Script Python qui écoute Mosquitto et republie vers RabbitMQ.
- **RabbitMQ** (port 1883 avec plugin MQTT) → Bus d'événements centralisé pour traiter/consommer les messages.

```
RFID Scanner simulé
    │  MQTT publish rfid/scan
    ▼
Mosquitto (port 1884)
    │  mqtt_relay.py s'abonne
    ▼
mqtt_relay.py  ──MQTT publish rfid.scan──▶  RabbitMQ MQTT plugin (port 1883)
    │
    ▼
RabbitMQ UI (localhost:15672) pour visualisation des messages
```

## Prérequis

- **Docker et Docker Compose** : Pour lancer RabbitMQ et Mosquitto.
- **Python 3.8+** : Pour les scripts.
- **Bibliothèques Python** : `paho-mqtt` (installé via `pip install -r requirements.txt`).

## Installation

1. Clonez le repository :
   ```bash
   git clone https://github.com/YosrMekkii/mqtt-relay-test.git
   cd mqtt-relay-test
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez les services Docker (RabbitMQ et Mosquitto) :
   ```bash
   docker compose up -d
   ```
   - RabbitMQ UI : http://localhost:15672 (login : guest/guest).
   - Mosquitto : Port 1884.
   - RabbitMQ MQTT : Port 1883.

## Usage

### 1. Lancer le relay
Le relay fonctionne en continu pour relayer les messages.
```bash
python mqtt_relay.py
```
- Il se connecte à Mosquitto (port 1884) et RabbitMQ (port 1883).
- Logs : "Connecté à Mosquitto", "Reçu de Mosquitto : {...}", "Relayé vers RabbitMQ".
- Arrêtez avec Ctrl+C.

### 2. Publier un message de test (simuler IoT)
Pour tester sans matériel réel :
```bash
python test_pub.py --tag TEST123
```
- Publie un payload JSON sur Mosquitto : `{"tag_id": "TEST123", "timestamp": 1234567890}`.
- Options : `--host`, `--port`, `--tag` (par défaut localhost:1884, TEST123).

### 3. Visualiser les résultats
- **RabbitMQ UI** : http://localhost:15672 > Queues > Créez une queue liée à `amq.topic` avec routing key `rfid.scan`. Les messages apparaissent.
- **Logs console** : Le relay affiche les messages relayés.
- Pour une GUI web (optionnel, voir section suivante).

## Configuration

Utilisez des variables d'environnement pour personnaliser :
- `MOSQUITTO_HOST` (défaut : localhost)
- `MOSQUITTO_PORT` (défaut : 1884)
- `RABBITMQ_HOST` (défaut : localhost)
- `RABBITMQ_PORT` (défaut : 1883)
- `RABBITMQ_USER` (défaut : guest)
- `RABBITMQ_PASS` (défaut : guest)
- `RFID_TOPIC` (défaut : rfid/scan)

## Explication des fichiers

### docker-compose.yml
- Définit les services Docker pour RabbitMQ et Mosquitto.
- RabbitMQ avec plugins activés via `enabled_plugins`.
- Mosquitto configuré via `mosquitto.conf`.

### enabled_plugins
- Liste des plugins RabbitMQ : `[rabbitmq_management,rabbitmq_mqtt]`.
- Active l'UI et le support MQTT.

### mosquitto.conf
- Configuration Mosquitto : port 1883, connexions anonymes autorisées.

### mqtt_relay.py
- Script principal : Souscrit à Mosquitto, republie vers RabbitMQ.
- Persistant (boucle infinie), résout les problèmes de stabilité.

### test_pub.py
- Publie un message de test sur Mosquitto pour simuler un scan RFID.

### requirements.txt
- Dépendances : `paho-mqtt`.

### .gitignore
- Ignore les fichiers temporaires Python.

## Tests

1. Lancez Docker : `docker compose up -d`.
2. Lancez le relay : `python mqtt_relay.py`.
3. Publiez : `python test_pub.py`.
4. Vérifiez RabbitMQ UI : Message dans la queue.
5. Arrêtez : `docker compose down`.
-----------------
