import json, re
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
KEY = re.search(r'^ACCOUNT_2_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
account = create_account(account_private_key=KEY)
client = create_client(chain=studionet, account=account)
tx = client.deploy_contract(code=(ROOT / "contracts" / "contract.py").read_text(encoding="utf-8"), args=[])
print("deploy_tx=" + str(tx), flush=True)
try:
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
except TypeError:
    receipt = client.wait_for_transaction_receipt(transaction_hash=tx, status="FINALIZED", retries=180, interval=5000, full_transaction=True)
leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
address = receipt.get("data", {}).get("contract_address") or receipt.get("to_address") or receipt.get("recipient")
assert str(receipt.get("result_name")).upper() == "MAJORITY_AGREE"
assert str(leader.get("execution_result")).upper() == "SUCCESS"
print(json.dumps({"wallet": account.address, "contract": address, "deploymentTx": str(tx), "status": receipt.get("status_name"), "consensus": receipt.get("result_name"), "execution": leader.get("execution_result")}, default=str), flush=True)
