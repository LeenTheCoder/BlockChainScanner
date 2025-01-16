# BlockChainScanner

[Русский](Rus-README.md) | **English**

---

**BlockChainScanner** is a Python utility for analyzing the Bitcoin blockchain. It allows scanning block ranges, identifying addresses with a minimum balance, and recording those that meet specified conditions.

## Features

- Scanning blocks within a specified range.
- Identifying addresses with a minimum balance (e.g., more than 1 BTC).
- Considering the time of the last transaction (e.g., before 2013).
- Writing suitable addresses to a `result.txt` file.

### Example

To scan blocks from 250000 to 300000, looking for addresses with a balance of more than 1 BTC and the last transaction before 2013:

```bash
python blockchain_scanner.py -s 250000 -e 300000 -b 1 -y 2013
```

## Parameters
- `-s`, --start-block — starting block for analysis.
- `-e`, --end-block — ending block for analysis.
- `-b`, --min-balance — minimum balance in BTC for addresses.
- `-y`, --min-year — minimum year of the last transaction. 

## Dependencies

- Python 3.7+
- requests

Install dependencies with the command:

```bash
pip install -r requirements.txt
```

## Build and Run

To build or run the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/LeenTheCoder/BlockChainScanner.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the utility:
  ```bash
  python blockchain_scanner.py -s <start block number> -e <end block number> -b <minimum balance> -y <minimum year>
   ```


## Frequently Asked Questions

### What if scanning blocks takes a long time?

You can use a narrower range of blocks or increase the minimum balance to reduce the amount of data processed.

### Does the application require API keys?

No, the utility uses the public Blockstream API to obtain data.

### What data is saved?

Only addresses that meet the specified conditions are written to `result.txt`.

## License

This project is distributed under the MIT license. See [LICENSE](LICENSE) for more details.

