# Directory Tree

Print a pretty tree view of a directory.

## Requirements

- Python 3.8+
- No third-party packages (standard library only)

## Usage

```bash
python3 main.py [folder] [--max-depth N] [--dirs-only] [--show-size] [--show-hidden]
```

Defaults to the current directory when no folder is given.

## Example

```bash
$ python3 main.py ./project
./project/
├── src/
│   ├── main.py
│   └── utils.py
├── README.md
└── LICENSE

5 entries listed.
```

## License

MIT — see [LICENSE](LICENSE).
