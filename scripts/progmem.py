import sys
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("output_name")
argparser.add_argument("--addr", "-a", default=8)
argparser.add_argument("--data", "-d", default=8)
args = argparser.parse_args()

output_name = sys.argv[1]

with open(args.output_name, "wb") as f:
    for val in range(2**args.addr):
        f.write(val.to_bytes(length=args.data // 8, byteorder="little", signed=False))
