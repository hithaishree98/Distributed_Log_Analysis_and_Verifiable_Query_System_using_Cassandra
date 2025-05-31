*** Distributed Log Analysis and Verifiable Query System using Cassandra

📆 Project Structure

📁 Part 1: Distributed Log Analysis with Cassandra

Objective:

Set up a Cassandra cluster across multiple nodes.

Import and analyze real web server logs using CQL and Python.

Highlights:

Cassandra 3-node cluster setup with cassandra.yaml configuration.

Log data imported using DSBulk.

Log analysis performed using Python + Cassandra Driver (CQL).

Key Files:

dsbulk.conf – Config for DataStax Bulk Loader

log_data_small_log.csv – Sample log dataset

log_queries.py – Python scripts for analytical queries

📁 Part 2: Blockchain-Assisted Verifiable Cassandra

Objective:

Enable verifiable data queries in an outsourced database environment using Merkle Trees and Ethereum smart contracts.

Highlights:

Implements four roles: Data Owner, Service Provider, Query Client, Malicious Client

Uses merkletools to construct Merkle Trees

Smart contract interaction handled using Web3.py and Ganache

Key Files:

driver.py – Runs the complete verification workflow

contract.sol – Ethereum smart contract

merkle_utils.py – Utility functions to generate Merkle Tree and proofs

📊 Queries Answered (Part 1)

Hits to specific path

Most active IP

Browser-based access counts (Firefox, Mozilla)

Ratio of GET requests

Size-based filtering

IPs with more than ten 404s

🔐 Verifiable Queries (Part 2)

Data verification using Merkle Root comparison

Attack detection via tampered data scenarios

