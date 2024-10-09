from collections import Counter
import sys
import heapq

def reducer():
    paths_count = Counter()
    ip_data = Counter()
    total_size_q10 = 0

    for line in sys.stdin:
        key, *values = line.strip().split('\t')

        if key == 'Q4':
            paths_count[values[0]] += 1
        elif key == 'Q9':
            ip, size = values
            ip_data[ip] += int(size)
        elif key == 'Q10':
            total_size_q10 += int(values[0])

    # Q4: Print the most requested path
    max_path, max_hits = paths_count.most_common(1)[0]
    print(f'Q4: {max_path} with {max_hits} hits')

    # Q9: Print the top 3 IPs by data transferred
    top_ips = heapq.nlargest(3, ip_data.items(), key=lambda x: x[1])
    print(f'Q9: {", ".join([f"{ip} ({size} bytes)" for ip, size in top_ips])}')

    # Q10: Print the total data transferred on 16/Jan/2022 with status 200
    print(f'Q10: {total_size_q10} bytes')

reducer()
