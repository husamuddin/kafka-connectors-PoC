# Kafka Connector PoC for MongoDB and Amazon DocumentDB

This repository demonstrates a Proof of Concept (PoC) for streaming data between MongoDB and Amazon DocumentDB using Kafka Connect. It includes both source and sink connectors with automated setup via Taskfile.

## Features

- 🚀 Seed data generation for MongoDB & DocumentDB
- 🔄 Bi-directional data streaming between:
  - Local MongoDB instances
  - Local MongoDB and AWS DocDB
- 📦 Dockerized environment with:
  - Kafka ecosystem (Broker, Connect, Schema Registry)
  - MongoDB containers
  - Data seeding service
- ⚡ Taskfile automation for:
  - Connector setup
  - Data seeding
  - Database connections

## Architecture Overview
```mermaid
graph TB
    subgraph Data Sources
        A[(MongoDB 1)]
        D[(Amazon DocumentDB)]
    end

    subgraph Kafka Ecosystem
        C1[Source Connector]
        C2[Source Connector]
        E{Kafka Cluster}
        S1[Sink Connector]
        S3[Sink Connector]
    end

    subgraph Data Destinations
        B[(MongoDB 2)]
        D2[(Amazon DocumentDB)]
    end

    A -->|Change Streams| C1 --> E
    D -->|Change Streams| C2 --> E
    E -->|Replicate| S1 --> B
    E -->|Cross-cloud Sync| S3 --> D2
```


## Prerequisites

- Docker 20.10+
- Docker Compose 2.20+
- Taskfile ([installation guide](https://taskfile.dev/installation/))
- AWS DocumentDB:
  - Connection string
  - CA certificate (`global-bundle.pem`)
- `.env` file with required credentials—copy `.env.example` to `.env` and set the right values

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone git@github.com:hudl/cloud-alchemists-kafka-poc.git
cd kafka-mongodb-poc
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your credentials
```

Example `.env`:
```
DOCDB_HOST=t-some-host.us-east-1.docdb.amazonaws.com
DOCDB_PASSWORD=<docdb_password>
DOCDB_CONNECTION_STRING=mongodb://<docdb_username>:<docdb_password>@some-host.us-east-1.docdb.amazonaws.com:27018/?tls=true&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false
```

### 3. Start Services
```bash
docker-compose up -d --build
```

Wait 2-3 minutes for services to initialize.

### 📋 Taskfile Commands
```bash
task mongo_1:seed -- 400    # Seed MongoDB with 400 documents
task docdb:seed -- 400    # Seed DocumentDB with 400 documents
```
You can change the number of records if you want.

### Connector Management
```
# Source Connectors
task kafka:mongo_1:source  # Create MongoDB source connector
task kafka:docdb:source    # Create DocumentDB source connector

# Sink Connectors
task kafka:mongo-2:sink-mongo   # MongoDB->MongoDB replication
task kafka:mongo-2:sink-docdb   # DocDB->MongoDB replication
```

### Database Access
```bash
task docdb:connect  # Connect to DocumentDB via mongosh
```

### 🐳 Docker Services Overview
| Service	| Ports	| Description |
| --- | --- | --- | 
Kafka Broker |	9092 |	Apache Kafka message broker
Schema Registry |	8081 |	Avro schema management
Kafka Connect |	8083 |	Connector management API
Control Center |	9021 |	Web UI for monitoring
MongoDB (mongo_1) |	27017 |	Primary MongoDB instance
MongoDB (mongo_2) |	- |	Secondary MongoDB for replication
KSQLDB Server |	8088 |	Stream processing engine

### 🔍 Testing the Pipeline

#### 1. Verify Connectors
```bash
# list the kafka connectors
curl -sS http://localhost:8083/connectors | jq

# check the connector status
curl -sS localhost:8083/connectors/<connector name>/status
```

#### 2. Monitor Data Flow
Access Control Center:
http://localhost:9021
Check:

- Connector statuses
- Topic messages (mongo_1.demo.users, docdb.demo.users)
- Consumer lag metrics

#### 3. Inspect Databases
##### MongoDB
```bash
docker exec -it mongo_1 mongosh demo --eval "db.getCollectionNames()"
```

##### DocumentDB:
```bash
task docdb:connect
> use demo
> db.imported_users.countDocuments()
```

### 📁 Project Structure
```
.
├── lib/
│   ├── kafka-connect/    # Custom Kafka Connect image
│   ├── mongo/            # Replica set initialization
│   └── py-seed/          # Data generation application
├── docker-compose.yml    # Service definitions
├── Taskfile.yaml         # Automation commands
└── global-bundle.pem     # DocumentDB CA cert
```

### 🚨 Troubleshooting
#### Common Issues:
##### 1. Connectors failing to start
 - Check Connect logs:
```bash
docker logs connect -f
```
- Verify network connectivity between containers

##### 2. DocumentDB connection issues
- Make sure that the VPN is connected
- Ensure global-bundle.pem exists in root
- Verify connection string format:
```ini
mongodb://<user>:<password>@<endpoint>:27017/?tls=true&replicaSet=rs0
```

##### 3. Data not appearing in sinks
- Check topic subscriptions:
```
docker exec -it kcat kafkacat -b broker:9092 -L
```

## FAQ
- ### How many databases and collections can Kafka handle?
For mongodb kafka connector, there's no explicit limit on the number of databases or collections it can handle. the practical limitations depend more on:
- infrastructure resources (cpu, memory, network bandwidth)
- kafka cluster configuration (partitions, brokers, topic settings)
- mongodb deployment architecture

**key considerations**:
- each collection typically maps to a kafka topic
- resource usage scales with the number of connector tasks running
- proper sizing of kafka partitions is critical for performance
- connection pooling settings should be optimized for the scale

- ### Can Kafka MongoDB Connector work with sharded databases as sources?
Yes! The connector fully supports reading from sharded MongoDB, it captures changes (via Change Streams) across all shards in the cluster

**key considerations**:
Change Streams support: The Kafka MongoDB connector relies heavily on MongoDB's Change Streams feature, which was introduced in MongoDB 3.6 (for replica sets) and fully supported for sharded clusters in MongoDB 4.0+.


- ### With DMS/CDC, we need to create indexes first before transferring any data. Can Kafka connector handle this?
No, Kafka Connector can't automatically create indexes on the target MongoDB collections. We'll need to manually set up any necessary indexes before starting data transfer, similar to the process with DMS/CDC.

- ### We know that DMS has little impact on the source database (and that’s something we need to not affect production applications). Do we know Kafka impact in the source in terms of resources usage?
The connector utilizes MongoDB's change streams to monitor real-time data changes, which is efficient but also introduce some overhead, high data volumes and numerous monitoring collections can increase CPU and memory usage. The Connector configuration need to be tuned for that, like the connector batch.size and poll.await.time to balance throughput and resource consumption.

