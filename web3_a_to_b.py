from confluent_kafka import Consumer, KafkaError
from web3 import Web3

# Kafka Configuration
kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'gasDataGroup',
    'auto.offset.reset': 'earliest'
}

# Ethereum Configuration (Infura)
infura_url = "https://sepolia.infura.io/v3/c8307f509144451ea0915ecc9b318cc0"
w3 = Web3(Web3.HTTPProvider(infura_url))

# Ethereum Account Configuration
YOUR_PRIVATE_KEY_A = 'd44b7492a778dc23c248a49dded1325ef7ad28304ab543c97a6242a246b154a4'
YOUR_ADDRESS_A = '0x788660fa8D25B4EA605F51d9bcf8E989C56b8bfF'  # Replace with Account A's address
YOUR_PRIVATE_KEY_B = 'd0c76db34cfb154537d1d12b8b2214c838b2ea5298b81bb8825ddc0919e1e25e'
YOUR_ADDRESS_B = '0xFDCF57A2Eef4d08bd8b617B43809bc8f124e728B'  # Replace with Account B's address
CONTRACT_ADDRESS = '0x37A6EC1d7E37f7a1c07E77a969d50E5935b48815'

# ABI (Application Binary Interface) of the Smart Contract
CONTRACT_ABI = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "gasValue",
                "type": "uint256"
            }
        ],
        "name": "applyPenalty",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    # ... (other ABI entries)
]

# Instantiate the Ethereum Contract
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Kafka Consumer Setup
consumer = Consumer(kafka_config)
consumer.subscribe(['gazData'])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Reached end of topic %s' % msg.topic())
            else:
                print('Error while consuming message: %s' % msg.error())
        else:
            gas_value = int(msg.value().decode('utf-8'))
            
            # Define a gas threshold (e.g., 50) for applying the penalty
            gas_threshold = 50

            if gas_value > gas_threshold:
                # Transfer funds from Account A to Account B
                txn = {
                    'from': YOUR_ADDRESS_A,
                    'to': YOUR_ADDRESS_B,
                    'value': w3.to_wei(0.01, 'ether'),  # Adjust the amount as needed
                    'gas': 200000,
                    'gasPrice': w3.to_wei('20', 'gwei'),
                    'nonce': w3.eth.get_transaction_count(YOUR_ADDRESS_A),
                }

                # Sign and send the transaction
                signed_txn = w3.eth.account.sign_transaction(txn, YOUR_PRIVATE_KEY_A)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print('Funds Transfer Transaction Hash:', tx_hash.hex())

except KeyboardInterrupt:
    print('Keyboard interrupt. Exiting...')
finally:
    consumer.close()