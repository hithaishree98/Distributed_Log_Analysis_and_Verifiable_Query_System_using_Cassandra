from collections import defaultdict, Counter
import sys
import heapq

def reducer():
    data = defaultdict(list)
    for line in sys.stdin:
        key, *values = line.strip().split('\t')
        data[key].append(values)

    # Process each question
    for key in sorted(data.keys()):
        if key in {'Q1', 'Q6', 'Q7', 'Q8', 'Q10'}:
            print(f'{key}: {sum(int(x[0]) for x in data[key])} bytes' if key in {'Q8', 'Q10'} else f'{key}: {sum(int(x[0]) for x in data[key])}')
        elif key == 'Q2':
            print(f'{key}: {len(data[key])}')
        elif key == 'Q3':
            methods = {x[0] for x in data[key]}
            print(f'{key}: {len(methods)} methods used: {", ".join(methods)}')
        elif key == 'Q4':
            paths = Counter(x[0] for x in data[key])
            max_path, max_hits = paths.most_common(1)[0]
            print(f'{key}: {max_path} with {max_hits} hits')
        elif key == 'Q5':
            ips = Counter(x[0] for x in data[key])
            max_ip, max_accesses = ips.most_common(1)[0]
            print(f'{key}: {max_ip} with {max_accesses} accesses')
        elif key == 'Q9':
            ip_data = defaultdict(int)
            for ip, size in data[key]:
                ip_data[ip] += int(size)
            top_ips = heapq.nlargest(3, ip_data.items(), key=lambda x: x[1])
            print(f'{key}: {", ".join([f"{ip} ({size} bytes)" for ip, size in top_ips])}')

reducer()
