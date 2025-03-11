# Kafka Streaming PoCs
This repository contains Proofs of Concept (PoCs) demonstrating Kafka-based data streaming pipelines for different data sources and sinks. Each PoC is self-contained within its own subdirectory, with automation provided by Taskfile and Dockerized environments for ease of setup and testing.

## Available PoCs
### 1. Elasticsearch to OpenSearch via Kafka and Logstash
- **Purpose**: Streams data from Elasticsearch to OpenSearch using Logstash and Kafka Connect.
- **Features**:
  - Seeds CSV data into Elasticsearch
  - Streams initial data and updates to Kafka
  - Sinks data into OpenSearch
  - Location: [elasticsearch/](elasticsearch)
  - Details: See [elasticsearch/README.md](elasticsearch/README.md)
 
### 2. MongoDB and Amazon DocumentDB with Kafka Connect
**Purpose**: Demonstrates bi-directional data streaming between MongoDB and Amazon DocumentDB using Kafka Connect.
**Features**:
- Seeds data into MongoDB and DocumentDB
- Supports local and cross-cloud replication
- Location: [mongo/](mongo/)
- Details: See [mongo/README.md](mongo/README.md)

### Prerequisites
- Docker (20.10+): Required for running services.
- Docker Compose (2.20+): Used for multi-container orchestration.
- Taskfile: Automation tool for managing tasks (installation guide).
- Optional: .env file for custom configurations (check each PoC’s README for details).


### Project Structure
```text
.
├── elasticsearch/           # Elasticsearch to OpenSearch PoC
│   ├── README.md            # Detailed instructions
│   ├── Taskfile.yaml        # Task automation
│   ├── docker-compose.yml   # Service definitions
│   └── ...                  # Additional configs and subdirs
├── lib/                    # Shared utilities and custom images
│   ├── kafka-connect/       # Custom Kafka Connect Dockerfile
│   ├── mongo/              # MongoDB initialization scripts
│   └── py-seed/            # Python-based data seeding tool
└── mongo/                  # MongoDB/DocumentDB PoC
    ├── README.md           # Detailed instructions
    ├── Taskfile.yaml       # Task automation
    ├── docker-compose.yml  # Service definitions
    └── ...                 # Additional configs and files
```

## Getting Started
### 1. Clone the Repository:
```bash
git clone git@github.com:hudl/cloud-alchemists-kafka-poc.git
cd kafka-streaming-pocs
```

### 2. Choose a PoC:
- For Elasticsearch to OpenSearch: Navigate to [elasticsearch/](elasticsearch/) and follow its README.
- For MongoDB/DocumentDB: Navigate to [mongo/](mongo/) and follow its README.
- 
### 3. Run the PoC:
Each subdirectory provides specific task commands to start services, seed data, and manage the pipeline.


## Shared Resources
The [lib/](lib/) directory contains reusable components:

- [kafka-connect/](lib/kafka-connect/): Custom Dockerfile for Kafka Connect with additional connectors.
- [mongo/](lib/mongo/): Initialization scripts for MongoDB replica sets.
- [py-seed/](lib/py-seed/): Python application for generating seed data (used in the MongoDB PoC).
