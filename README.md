# file-split
File split script in Python

## How to Use
If you want to split the file `something.bin` 1GB and save them `./out`:
```console
python split.py -c 1g something.bin ./out
```

## Command-line options
Below options are available.
| Option | short | Description |
| ------ | ----- | ----------- |
| `chunk` | `c`  | Split chunk size, prefix: "k"(kilo), "m"(mega) and "g"(giga) are available. |
| `quiet` | `q`  | Do not show any message without error (Silent mode). It must be select an either quiet or verbose flag. |
| `verbose` | `v` | Show detail messages. It must be select an either quiet or verbose flag. |

## License
This script is released under the MIT License.
For details, See [LICENSE](LICENSE).
