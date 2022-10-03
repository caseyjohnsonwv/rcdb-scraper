import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', help="Directory containing CSVs to concatenate")
parser.add_argument('-f', '--filename', help="Destination filename (.csv extension required)")
ARGS = parser.parse_args()

target_path = pathlib.Path(ARGS.target)
csvs = []
for f in target_path.iterdir():
    if f.suffix == '.csv' and f.name != ARGS.filename:
        csvs.append(f.absolute())

print(f"Found {len(csvs)} CSVs in {target_path.absolute()}")
if len(csvs) == 0:
    exit()

with open(ARGS.filename, 'w') as out:
    for csv_file in csvs:
        with open(csv_file, 'r', encoding='ascii', errors='ignore') as f:
            for line in f.readlines():
                out.write(line)
