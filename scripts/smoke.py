import json, re, time
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).parents[1]
ENV = (ROOT.parents[3] / "accounts.env").read_text(encoding="utf-8")
DEPLOYMENT = json.loads((ROOT / "deployment.json").read_text(encoding="utf-8"))
ADDRESS = DEPLOYMENT["contractAddress"]

def account(slot):
    value = re.search(rf'^ACCOUNT_{slot}_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', ENV, re.M).group(1).strip()
    return create_account(account_private_key=value)

def send(client, name, args):
    tx = client.write_contract(address=ADDRESS, function_name=name, args=args, value=0)
    print(name + "=" + str(tx), flush=True)
    try:
        receipt = client.wait_for_transaction_receipt(transaction_hash=tx, wait_until="finalized", retries=180, interval=5000, full_transaction=True)
    except TypeError:
        receipt = client.wait_for_transaction_receipt(transaction_hash=tx, status="FINALIZED", retries=180, interval=5000, full_transaction=True)
    leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
    assert str(receipt.get("result_name")).upper() == "MAJORITY_AGREE"
    assert str(leader.get("execution_result")).upper() == "SUCCESS", (name, receipt)
    return str(tx)

owner = account(2)
responder = account(3)
owner_client = create_client(chain=studionet, account=owner)
responder_client = create_client(chain=studionet, account=responder)
exercise_id = "FA-LIVE-" + str(int(time.time()))
transactions = {}
transactions["open"] = send(owner_client, "open_exercise", [exercise_id, "A record heat wave disables the eastern power feeder while hospitals and water pumps reach peak demand.", ["No diesel reserve is available", "Water pressure must remain above the emergency minimum"], ["Power Grid", "Water Loop", "Transit Arc", "Medical Ridge"]])
transactions["dispatch"] = send(responder_client, "dispatch_move", [exercise_id, "Medical Ridge", "Move the mobile battery unit to Medical Ridge before peak load, then rotate non-critical equipment onto the remaining feeder."])
exercise = owner_client.read_contract(address=ADDRESS, function_name="get_exercise", args=[exercise_id])
moves = owner_client.read_contract(address=ADDRESS, function_name="get_moves_page", args=[exercise_id, 0, 20])
assert exercise["turn"] == 1 and moves["total"] == 1
print(json.dumps({"exerciseId": exercise_id, "state": exercise["state"], "health": exercise["health"], "move": moves["items"][0], "transactions": transactions}, default=str), flush=True)
