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

    # Question 4: Emit the request line
    print(f'Q4\t{request_line}')

    # Question 9: Emit the IP and size
    print(f'Q9\t{ip}\t{size}')

    # Question 10: Emit the size for requests on 16/Jan/2022 with status 200
    if date == '16/Jan/2022' and status == '200':
        print(f'Q10\t{size}')

for line in sys.stdin:
    mapper(line)
