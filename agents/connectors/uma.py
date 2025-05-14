from web3 import Web3
import json
import time


provider_url = "https://mainnet.infura.io/v3/3e3e139cbb9b448ab07bb48fb383c6f4"
web3 = Web3(Web3.HTTPProvider(provider_url))

# Check if connected
if web3.provider.is_connected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect to Ethereum network")

# UMA Optimistic Oracle contract address
optimistic_oracle_address = "0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74" # v2; see https://docs.polymarket.com/#resolution-process

# Optimistic Oracle ABI (simplified version, you'll need the correct ABI)

def abi_to_str() -> str:
    with open("abi.json", "r") as abi:
        abi_read = abi.read()
        return abi_read.strip()

optimistic_oracle_abi = json.loads(abi_to_str())

# Connect to the contract
optimistic_oracle = web3.eth.contract(address=optimistic_oracle_address, abi=optimistic_oracle_abi)

# Get data function (retrieve the vote result)
def get_data(vote_id):
    requester = "0x91430CaD2d3975766499717fA0D66A78D814E5c5"
    identifier = web3.keccak(text=vote_id)  # Generate the unique data ID
    # data = optimistic_oracle.events.QuestionInitialized.createFilter(fromBlock=1000000, toBlock='latest')
    data = optimistic_oracle.caller.questions

    # .yesOrNoIdentifier.create_filter(fromBlock="0x0", argument_filters={'from': '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf'})
    
    print(data.functions)

# Example usage
# request_data("vote12345")  # Request data for a vote with ID 'vote12345'
get_data("1746388283631")      # Retrieve data for vote ID 'vote12345'
