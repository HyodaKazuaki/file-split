# split.py
#
# Copyright (C) 2021 HyodaKazuaki
# This script is released under the MIT license.
# For details, see: https://opensource.org/licenses/MIT

import argparse
import math
from pathlib import Path


def logger(message: str, flag: bool = False):
    """Very simple logger.

    Args:
        message (str): Message
        flag (bool, optional): Message shown flag. Defaults to False.
    """
    if flag:
        print(message)


def divide(
    input_path: Path,
    output_dir: Path,
    chunk_size: int,
    quiet: bool = False,
    verbose: bool = False,
):
    """Split files.

    Args:
        input_path (Path): Split target file path.
        output_dir (Path): Output directory path.
        chunk_size (int): Split chunk byte size.
        quiet (bool, optional): Silent mode flag. Defaults to False.
        verbose (bool, optional): Verbose flag. Defaults to False.
    """
    logger("Calcuate number of output file...", not quiet)
    num_outputfile = math.ceil(input_path.stat().st_size / chunk_size)
    logger("Calcuate number of output file finished.", verbose)
    logger(f"Number of output file: {num_outputfile}.", verbose)

    logger("Generate output file...", not quiet)
    with input_path.open("rb") as fr:
        for i in range(num_outputfile):
            logger("Seek position...", verbose)
            fr.seek(i * chunk_size)
            logger(f"Seeked position: {i * chunk_size} byte(s).", verbose)

            logger("Read data...", verbose)
            data = fr.read(chunk_size)
            logger(f"Read {len(data)} byte(s) data.", verbose)

            with (output_dir / f"{input_path.name}.{i}").open("wb+") as fw:
                logger(f"Opened file: {input_path.name}.{i}.", verbose)
                fw.write(data)
                logger("Wrote data.", verbose)
    logger("Generate output file finished.", verbose)


def main(
    input_path: Path,
    output_dir: Path,
    chunk: str,
    quiet: bool = False,
    verbose: bool = False,
):
    """Split script.

    Args:
        input_path (Path): Split target file path.
        output_dir (Path): Output directory path.
        chunk (str): Split chunk size. Supporting prefix is "k", "m" and "g".
        quiet (bool, optional): Silent mode flag. Defaults to False.
        verbose (bool, optional): Verbose flag. Defaults to False.
    """
    assert (
        output_dir.is_dir or not output_dir.exists
    ), "Output directory path must be directory."
    assert chunk[-1].isdigit() or chunk[-1].lower() in [
        "k",
        "m",
        "g",
    ], 'Supporting prefix is "k", "m", and "g".'
    assert "." not in chunk, "Floating value is not allowed."
    assert (
        not quiet or not verbose
    ), "It must be select an either quiet or verbose flag."

    logger("Create output directory...", not quiet)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger("Create output directory finished.", verbose)

    logger("Calcuate chunk size...", not quiet)
    chunk_size = 0
    if chunk[-1].isdigit():
        chunk_size = int(chunk)
    else:
        chunk_size = int(chunk[0:-1])
        prefix = chunk[-1]
        if prefix == "k":
            chunk_size *= 1024
        if prefix == "m":
            chunk_size *= 1024 ** 2
        if prefix == "g":
            chunk_size *= 1024 ** 3
    logger("Calcuate chunk size finished...", verbose)
    logger(f"Chunk size: {chunk_size} byte.", verbose)

    divide(
        input_path=input_path,
        output_dir=output_dir,
        chunk_size=chunk_size,
        quiet=quiet,
        verbose=verbose,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path, help="Split target file path")
    parser.add_argument("output_dir", type=Path, help="Output directory path")
    parser.add_argument(
        "-c",
        "--chunk",
        type=str,
        default="1g",
        help="Chunk size (byte including prefix such as k, m, g)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not show any message without error.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detail messages"
    )

    main(**vars(parser.parse_args()))
