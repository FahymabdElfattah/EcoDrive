# Importation des bibliothèques nécessaires
import serial
import time  # Pour introduire des pauses entre les lectures du capteur
from confluent_kafka import Producer  # Pour envoyer des messages à Kafka

# Configuration de Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  # Adresse du serveur Kafka
    'client.id': 'raspberry-producer'  # Identifiant unique pour ce producteur
}
# Création d'une instance de producteur avec la configuration précédente
producer = Producer(conf)
# Fonction callback pour signaler le résultat de l'envoi d'un message à Kafka
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))  # Affichage de l'erreur en cas d'échec de l'envoi
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))  # Confirmation de la réussite de l'envoi

# Boucle principale pour lire en continu le capteur et envoyer les données à Kafka
ser = serial.Serial('/dev/ttyUSB0', 115200)
try:
    data = ser.readline().decode('utf-8').strip()
    gas_level = int(data)   # Lecture de la valeur du capteur de gaz
    print("Gas level:", gas_level)  # Affichage de la valeur lue
    # Envoi de la donnée lue à Kafka
    producer.produce('gazData', value=str(gas_level), callback=delivery_report)  # Envoi au topic "gazData"
    # Attendre que la donnée soit effectivement envoyée avant de continuer
    producer.flush()
    time.sleep(1)  # Pause d'une seconde avant la prochaine lecture
except KeyboardInterrupt:
    # Gérer l'arrêt de la boucle en cas d'interruption (par exemple, Ctrl+C)
    print("Arrêt de la lecture du capteur.")