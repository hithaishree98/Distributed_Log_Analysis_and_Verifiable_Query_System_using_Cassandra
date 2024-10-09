###Part 1: Setting up Cassandra (50 points)

1. Install Java 8:
   - Follow the installation instructions for Java 8 suitable for your operating system.

     sudo apt-get update
     sudo apt-get install openjdk-8-jdk
     java -version

2. Install Python 3:
   - Skip this step if Python 3 is already installed on your system.
     
     sudo apt-get update
     sudo apt-get install python3
     python3 --version

3. Add Cassandra Repository:
   - Open a terminal and run the following command to add the Cassandra repository to your system:
     
     echo "deb https://debian.cassandra.apache.org 41x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list

4. Add Apache Cassandra Keys:
   - Download and add the Apache Cassandra keys to your system by running the following command:
     
     curl https://downloads.apache.org/cassandra/KEYS | sudo apt-key add -   

5.  Update Package Repository:
   - Update the package repository to include the newly added Cassandra repository:
     
     sudo apt-get update

6. Install Cassandra:
   - Install Cassandra on all nodes in your cluster using the following command:
     
     sudo apt-get install cassandra

7. Configure Cassandra:
   - Edit the Cassandra configuration file `cassandra.yaml` located at `/etc/cassandra/` using a text editor (e.g., `nano`):
     
     sudo nano /etc/cassandra/cassandra.yaml
     
   - Update the following lines in the `cassandra.yaml` file:
     
     seeds: "10.254.3.108,10.254.1.207,10.254.2.126"

     listen_address: 10.254.3.108 (on master node)
     listen_address: 10.254.1.207 (on slave node1)
     listen_address: 10.254.2.126 (on slave node2)

     rpc_address: 10.254.3.108 (on master node)
     rpc_address: 10.254.1.207 (on slave node1)
     rpc_address: 10.254.2.126 (on slave node2)
     
8. Start Cassandra Service:
   - Stop the Cassandra service on all nodes:
     
     sudo service cassandra stop
     
   - Start the Cassandra service manually to monitor the service status and logs:
     
     sudo service cassandra start

9. Check Cluster Status:
   - Open a new terminal and log into one of the VMs in the cluster.
   - Use `nodetool` to see the Cassandra cluster's status:
     
     nodetool status

10. Start CQL Client:
    - Start the CQL shell (CQLSH) on the master node to interact with the Cassandra cluster:
      
      cqlsh 10.254.3.108

Note:Ensure that all nodes in the cluster are properly configured and have access to each other over the network. Adjust the configuration settings and commands as necessary based on your specific setup and requirements.

##Test 

1. Setting Up Keyspace and Table
   - Created a keyspace named `patient` with replication settings:

     Cql
     CREATE KEYSPACE patient WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
     
   - Created a table named `exam` to store log details, including `patient_id`, `id`, `date`, and `details`:

     Cql
     CREATE TABLE patient.exam (patient_id int, id int, date timeuuid, details text, PRIMARY KEY (patient_id, id));
     
2. Importing Data
   - Inserted data for patient 1:

     Cql
     INSERT INTO exam (patient_id,id,date,details) values (1,1,now(),'first exam patient 1');
     INSERT INTO exam (patient_id,id,date,details) values (1,2,now(),'second exam patient 1');

   - Inserted data for patient 2 and patient 3:

     Cql
     INSERT INTO exam (patient_id,id,date,details) values (2,1,now(),'first exam patient 2');
     INSERT INTO exam (patient_id,id,date,details) values (3,1,now(),'first exam patient 3');
     
3. Verifying Data

   - To verify the data insertion, we used the following command to select all records for `patient_id=1`:

     cql
     SELECT * FROM exam WHERE patient_id=1;
     
------------------------------------------------------------------------------------------------------------------------------------------------------------


###Part 2: Import Data into Cassandra (25 points)

To import the access logs into Cassandra using the Python driver, follow these steps:

1. Download the log data set: 
   - Download the log data set from the provided link in Canvas.(We have used the new small log dataset)

2. Install Cassandra: 
   - If you haven't already, install Cassandra on your system following the installation instructions for your operating system.

3. Create a Keyspace: 
   - Open the CQL shell (`cqlsh`) and create a keyspace to store the log data. For example:

     Cql
     CREATE KEYSPACE log_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
     
4. Create a Table: 
   - Create a table to store the log data. Define the table schema based on your log data structure. For example:
    Cql:
    CREATE TABLE IF NOT EXISTS log_data_small_log (
    id UUID PRIMARY KEY,
    ip_address TEXT,
    datetime TIMESTAMP,
    method TEXT,
    url TEXT,
    protocol TEXT,
    status_code INT,
    response_size INT,
    user_agent TEXT
);


5. Import Data:
   -If you have a CSV file of the log data, you can use DataStax Bulk Loader (DSBulk) to efficiently import the data into the table.

   -The dsbulk.conf file is used to configure the import settings and is located in the virtual machine.

   -Place the CSV file in a location accessible to the machine where DSBulk is installed, and then use the following command  
  
    /home/ubuntu/Log_data/dsbulk-1.11.0/bin/dsbulk load -k log_keyspace -t log_data_small_log -url /home/ubuntu/Log_data/output_log_file_New.csv -header true -f dsbulk.conf -h 10.254.3.108 --port 9042 
 

       
------------------------------------------------------------------------------------------------------------------------------------------------------------

###Part 3: Operate Data in Cassandra (25 points)

In this part of the project, we utilized the Cassandra Query Language (CQL) and the Python driver for Cassandra to analyze access logs and answer specific questions about the dataset.

Installation of DataStax Python Driver for Apache Cassandra

To interact with Apache Cassandra from Python, you need to install the DataStax Python driver. Follow these steps to install the driver:
- pip install cassandra-driver

## Running the Python Script

After installing the DataStax Python driver, you can create and run a Python script to interact with your Cassandra cluster. Follow these steps:

In VM, navigate to the directory where your CSV file is located. Then, create a new Python script file named `python_code_x.py` and run the following command:

- python3 python_code_x.py

1. How many hits were made to the website item "/administrator/index.php"?
   - CQL Query: Please refer screenshot in report for query

2. How many hits were made from the IP: 96.32.128.5?
   - CQL Query: Please refer screenshot in report for query

3. Which path in the website has been hit most? How many hits were made to the path?
   python code:
from cassandra.cluster import Cluster
from collections import Counter

def find_most_hit_path():
    # Connect to the Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all URLs
    query = "SELECT url FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of each URL
    url_counts = Counter(row.url for row in rows)

    # Find the most hit URL
    if url_counts:
        most_hit_url, hit_count = url_counts.most_common(1)[0]
        print(f"Most hit path: {most_hit_url} with {hit_count} hits")
    else:
        print("No data found.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    find_most_hit_path()

4. Which IP accesses the website most? How many accesses were made by it?
   python code:
   from cassandra.cluster import Cluster
from collections import Counter

def find_most_active_ip():
    # Connect to the Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all IP addresses
    query = "SELECT ip_address FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of each IP address
    ip_counts = Counter(row.ip_address for row in rows)

    # Find the IP address with the most accesses
    if ip_counts:
        most_active_ip, access_count = ip_counts.most_common(1)[0]
        print(f"Most active IP: {most_active_ip} with {access_count} accesses")
    else:
        print("No data found.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    find_most_active_ip()


5. How many accesses were made by Firefox (Mozilla)?
Python code for firefox:
from cassandra.cluster import Cluster

def count_firefox_accesses():
    # Connect to your Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all user agents
    query = "SELECT user_agent FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of Firefox
    firefox_count = sum(1 for row in rows if 'Firefox' in row.user_agent)

    # Print the result
    print(f"Number of accesses made by Firefox: {firefox_count}")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    count_firefox_accesses()

Python code for Mozilla:

from cassandra.cluster import Cluster

def count_mozilla_accesses():
    # Connect to your Cassandra cluster
    cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
    session = cluster.connect('log_keyspace')

    # Query to get all user agents
    query = "SELECT user_agent FROM log_data_small_log;"
    rows = session.execute(query)

    # Count the occurrences of Mozilla
    mozilla_count = sum(1 for row in rows if 'Mozilla' in row.user_agent)

    # Print the result
    print(f"Number of accesses made by Mozilla: {mozilla_count}")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    count_mozilla_accesses()



6. For all requests on 02/Apr/2022, what is the ratio of GET request?
   Python code:
from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['10.254.3.108', '10.254.1.207', '10.254.2.126'])
session = cluster.connect('log_keyspace')

# Query to get the total number of requests on April 2, 2022
total_requests_query = "SELECT COUNT(*) AS total_requests FROM log_data_small_log WHERE datetime >= '2022-04-02' AND datetime < '2022-04-03'"

# Query to get the number of GET requests on April 2, 2022
get_requests_query = "SELECT COUNT(*) AS get_requests FROM log_data_small_log WHERE datetime >= '2022-04-02' AND datetime < '2022-04-03' AND method = 'GET'"

# Execute the queries
total_requests_result = session.execute(total_requests_query).one()
get_requests_result = session.execute(get_requests_query).one()

# Calculate the ratio of GET requests to total requests
total_requests = total_requests_result['total_requests']
get_requests = get_requests_result['get_requests']
ratio = get_requests / total_requests if total_requests != 0 else 0.0

# Print the ratio
print(f"Ratio of GET requests to total requests on 2022-04-02: {ratio}")

# Close the session and cluster
session.shutdown()
cluster.shutdown()
   

7. How many requests are lower than or equal to 404 bytes?
   - CQL Query: Please refer screenshot in report for query
  

8. List the IPs that have more than ten 404 requests. If no IP fulfills, print the IP that has most 404 requests and the number of requests.

   python code: 
from cassandra.cluster import Cluster
from collections import Counter

def list_ips_with_404_requests():
    # Connect to your Cassandra cluster
    cluster = Cluster([''10.254.3.108', '10.254.1.207', '10.254.2.126''])
    session = cluster.connect('log_keyspace')

    # Query to get all 404 requests
    query = "SELECT ip_address FROM log_data_small_log WHERE status_code = 404;"
    rows = session.execute(query)

    # Count the occurrences of each IP address
    ip_counts = Counter(row.ip_address for row in rows)

    # Find IPs with more than ten 404 requests
    ips_with_more_than_ten_404 = [ip for ip, count in ip_counts.items() if count > 10]

    # Print the result
    if ips_with_more_than_ten_404:
        print("IPs with more than ten 404 requests:")
        for ip in ips_with_more_than_ten_404:
            print(f"{ip}: {ip_counts[ip]} requests")
    else:
        most_404_ip = ip_counts.most_common(1)[0]
        print(f"No IP has more than ten 404 requests. The IP with the most 404 requests is {most_404_ip[0]} with {most_404_ip[1]} requests.")

    # Close the connection
    cluster.shutdown()

if __name__ == '__main__':
    list_ips_with_404_requests()