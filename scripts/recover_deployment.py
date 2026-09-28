import json, re
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

TX = "0x899268a4f6e7fa66c525b7e60edca5b5fb96cc7c7a29c0e6b89f015eb49b7fc3"
ROOT = Path(__file__).parents[1]
env = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
private_key = re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', env, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=private_key))
receipt = client.wait_for_transaction_receipt(transaction_hash=TX, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
address = receipt.get("data", {}).get("contract_address") or receipt.get("to_address") or receipt.get("recipient")
print(json.dumps({"contract": address, "deploymentTx": TX, "status": receipt.get("status_name"), "consensus": receipt.get("result_name"), "execution": leader.get("execution_result"), "stderr": leader.get("stderr"), "data": receipt.get("data"), "to": receipt.get("to_address"), "recipient": receipt.get("recipient")}, default=str), flush=True)
