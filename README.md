# FAULTLINE ATLAS / DISPATCH SHEET

Status: deployed on StudioNet  
Network: StudioNet  
Repository: assigned to `warnedwarn`

Contract: `0x95c8D011dE4C6ccB33fD7e575B0D5385AcB3eC14`  
Explorer: `https://explorer-studio.genlayer.com/address/0x95c8D011dE4C6ccB33fD7e575B0D5385AcB3eC14`

Live map: `https://faultline-atlas.pages.dev/`  
Source: `https://github.com/warnedwarn/faultline-atlas`

## Map legend

Faultline Atlas is a shared emergency rehearsal map. Four named sectors begin with equal resilience. Distinct participants dispatch one response each. GenLayer validators determine whether the move stabilizes, redirects, or amplifies risk in the selected sector, then deterministic contract code applies a bounded health change.

`ACTIVE` accepts moves. `BREACHED` means a sector reached zero. `SEALED` means the turn limit was reached or the exercise owner closed the drill after meaningful participation.

## Exercise doctrine

The contract owns the scenario, constraints, sector health, unique participant list, move ledger, and final state. Before AI judgment it rejects unknown sectors, short actions, duplicate actors, and closed drills. After consensus it converts each verdict into a fixed impact band, clamps sector health to 0 through 8, advances exactly one turn, and derives terminal state in code.

The consensus question is narrow: does this concrete response plausibly stabilize, redirect, or amplify risk in the named sector under the frozen scenario and operating constraints? Validators verify the proposed causal direction against the same stored facts. A plausible JSON shape alone is not enough.

## Chain record

Writes: `open_exercise`, `dispatch_move`, `seal_exercise`.

Reads: `get_summary`, `get_exercise`, `get_exercises_page`, `get_moves_page`.

The frontend is a static map-first Next.js application. It reads the current map without a wallet, requests a browser wallet only for writes, and represents transaction consensus as a moving dispatch strip rather than a generic spinner.

## Drill procedure

```text
cd frontend
npm install
npm run typecheck
npm run build
```

From the project root:

```text
genvm-lint check contracts/contract.py
python -m pytest tests/test_surface.py -q
python -m pytest tests/direct -q
node scripts/no-emoji.js
node scripts/no-emdash.js
```

## After-action limits

Direct mode does not execute the validator function. StudioNet is required to verify the complete leader and validator path. The simulation is a coordination exercise, not professional emergency advice, and it deliberately stores compact causal outcomes rather than attempting a real-world disaster forecast.
