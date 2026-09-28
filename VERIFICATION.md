# Verification

## Local gates

- GenVM AST lint: passed. SDK semantic validation could not refresh through the restricted local network path.
- Contract surface tests: 2 passed.
- Direct tests: collected, but the installed Windows loader fails before execution with `genlayer.py.calldata.DecodingError: unexpected end of memory`.
- TypeScript: passed.
- Static production build: passed.
- Emoji and em dash scans: passed.

## Live gates

Contract `0x95c8D011dE4C6ccB33fD7e575B0D5385AcB3eC14` deployed on StudioNet with `MAJORITY_AGREE` and leader execution `SUCCESS`. The current StudioNet simulation endpoint returned undefined-method execution errors for this contract and for a previously verified reference contract, so no live move is claimed. GitHub publication succeeded. The Cloudflare production URL returned HTTP 200 with the expected application title and shell.
