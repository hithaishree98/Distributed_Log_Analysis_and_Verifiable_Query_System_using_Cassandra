#!/usr/bin/env python
import sys

current_ngram = None
current_count = 0
ngram = None

# Input comes from standard input (which is sorted by the Hadoop framework)
for line in sys.stdin:
    line = line.strip()

    # Parse the input from mapper
    ngram, count = line.split('\t', 1)

    # Convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        continue

    if current_ngram == ngram:
        current_count += count
    else:
        if current_ngram:
            # Write result to standard output
            print(f"{current_ngram}\t{current_count}")
        current_ngram = ngram
        current_count = count

# Output the last n-gram if needed
if current_ngram == ngram:
    print(f"{current_ngram}\t{current_count}")


