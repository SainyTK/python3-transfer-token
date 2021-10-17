from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

account = '0x52Ab9c52054B6df51E00ffdDFd8B1Ad31493E621'
private_key = os.getenv('PRIVATE_KEY')
node_endpoint = os.getenv('NODE_ENDPOINT')

with open('abi.json') as json_file:
    abi = json.load(json_file)

w3 = Web3(Web3.HTTPProvider(node_endpoint))
contract_address = '0x8D1372dA80F876f148066E29C667702EEbE8E0bC'
token = w3.eth.contract(address=contract_address, abi=abi)

# Check user's balance
balance = token.functions.balanceOf(account).call()
symbol = token.functions.symbol().call()
print('Balance of ' + account + ' is ' + str(w3.fromWei(balance, 'ether')) + ' ' + symbol)

# Transfer tokens
recipient = '0x52Ab9c52054B6df51E00ffdDFd8B1Ad31493E621'
amount = w3.toWei('1', 'ether')

nonce = w3.eth.getTransactionCount(account)
tx = {
    'nonce': nonce,
    'to': contract_address,
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
    'data': token.encodeABI(fn_name="transfer", args=[recipient, amount])
}

signed_tx = w3.eth.account.sign_transaction(tx, private_key)

tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

print('https://rinkeby.etherscan.io/tx/' + w3.toHex(tx_hash))