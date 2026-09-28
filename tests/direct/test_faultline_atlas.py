def test_open_and_guard_duplicate(direct_vm, direct_deploy, direct_alice, contract_path):
    contract = direct_deploy(str(contract_path))
    direct_vm.sender = direct_alice
    contract.open_exercise("DRILL-1", "A heat wave disables the eastern power feeder while hospitals draw peak load.", ["No diesel reserve", "Keep water pressure above minimum"], ["Power", "Water", "Transit", "Medical"])
    assert contract.get_exercise("DRILL-1")["state"] == "ACTIVE"
    with direct_vm.expect_revert("unique exercise"):
        contract.open_exercise("DRILL-1", "A heat wave disables the eastern power feeder while hospitals draw peak load.", ["No diesel reserve", "Keep water pressure above minimum"], ["Power", "Water", "Transit", "Medical"])

def test_owner_cannot_seal_before_two_moves(direct_vm, direct_deploy, direct_alice, contract_path):
    contract = direct_deploy(str(contract_path))
    direct_vm.sender = direct_alice
    contract.open_exercise("DRILL-2", "A river surge isolates two neighborhoods and interrupts ambulance access routes.", ["One bridge remains open", "No helicopter capacity"], ["Bridge", "Shelter", "Medical", "Comms"])
    with direct_vm.expect_revert("after at least two moves"):
        contract.seal_exercise("DRILL-2")
