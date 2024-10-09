import sys

def mapper(line):
    parts = line.split()
    if len(parts) < 10:
        return  # Skip lines that do not have enough parts

    ip = parts[0]
    request_line = parts[6]
    method = parts[5].strip('"').split()[0] if parts[5].strip('"').split() else '-'
    status = parts[8]
    size = parts[9] if parts[9] != '-' else '0'
    date = parts[3][1:].split(':')[0]

   # Question 1: Count hits to "/images/smilies/" directory
    if '/images/smilies/' in request_line:
        print('Q1\t1')

    # Question 2: Count hits from IP 96.32.128.5
    if ip == '96.32.128.5':
        print('Q2\t1')

    # Question 3
    print(f'Q3\t{method}')

    # Question 4
    print(f'Q4\t{request_line}')

    # Question 5
    print(f'Q5\t{ip}')

    # Question 6
    if method == 'POST':
        print('Q6\t1')

    # Question 7
    if status == '404':
        print('Q7\t1')

    # Question 8
    if date == '19/Dec/2020':
        print(f'Q8\t{size}')

    # Question 9
    print(f'Q9\t{ip}\t{size}')

    # Question 10
    if date == '16/Jan/2022' and status == '200':
        print(f'Q10\t{size}')

for line in sys.stdin:
    mapper(line)
