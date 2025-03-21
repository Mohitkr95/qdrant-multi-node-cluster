# Qdrant Multi-Node Cluster

<p align="center">
  <img src="https://dbdb.io/media/logos/qdrant.svg" alt="Qdrant Logo" width="300">
</p>

<p align="center">
  <a href="https://github.com/Mohitkr95/qdrant-multi-node-cluster/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/Mohitkr95/qdrant-multi-node-cluster/build.yml?branch=main&label=build%20%26%20docs" alt="Build & Docs Status"></a>
  <a href="https://github.com/Mohitkr95/qdrant-multi-node-cluster/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Mohitkr95/qdrant-multi-node-cluster" alt="License"></a>
  <a href="https://github.com/Mohitkr95/qdrant-multi-node-cluster/releases"><img src="https://img.shields.io/github/v/release/Mohitkr95/qdrant-multi-node-cluster" alt="Version"></a>
  <a href="https://github.com/Mohitkr95/qdrant-multi-node-cluster/issues"><img src="https://img.shields.io/github/issues/Mohitkr95/qdrant-multi-node-cluster" alt="Issues"></a>
  <a href="https://github.com/Mohitkr95/qdrant-multi-node-cluster/stargazers"><img src="https://img.shields.io/github/stars/Mohitkr95/qdrant-multi-node-cluster" alt="Stars"></a>
</p>

## Overview

The Qdrant Multi-Node Cluster project demonstrates a scalable deployment architecture for the Qdrant vector database. It showcases how to set up and configure multiple Qdrant nodes to work in harmony, providing enhanced vector search capabilities with high availability and performance.

This implementation allows you to experiment with and understand:

- Advanced vector search mechanisms in a distributed environment
- Sharding and replication strategies for vector databases
- Performance monitoring and optimization for vector search operations
- Reliable clustering techniques for production-level deployments

## Why Qdrant?

[Qdrant](https://qdrant.tech/) is a high-performance vector similarity search engine with extended filtering capabilities. Its key advantages include:

- **Million-scale search**: Efficiently manage and search through millions of high-dimensional vectors
- **Filtering**: Combine vector search with metadata filtering for precise results
- **Clustering**: Support for distributed deployments with built-in sharding
- **Performance**: Optimized algorithms for fast and accurate search results

## Key Features

This project implements:

- **Scalable Multi-Node Setup:** Deploying multiple Qdrant instances in a clustered configuration
- **Load Distribution:** Techniques for evenly distributing search queries across nodes
- **Data Redundancy:** Implementation of data replication for fault tolerance
- **Monitoring Stack:** Integration with Prometheus and Grafana for real-time performance monitoring
- **Python Client Integration:** Demonstration of client operations against a clustered database

## Documentation

- [Getting Started](guides/getting-started.md) - Quick setup instructions
- [Architecture Overview](guides/architecture.md) - System architecture and components
- [Configuration Guide](guides/configuration.md) - Detailed configuration options
- [API Reference](api/reference.md) - API documentation
- [Performance Tuning](guides/performance.md) - Optimization strategies
- [Troubleshooting](guides/troubleshooting.md) - Solutions to common issues

## Visualizations and Monitoring

This project includes a comprehensive monitoring solution utilizing Prometheus and Grafana:

<p align="center">
  <img src="images/grafana-dashboard.png" alt="Grafana Dashboard" width="800">
</p>

## Contributing

We welcome contributions! See the [Contributing Guide](guides/contributing.md) for more information on how to get involved.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Mohitkr95/qdrant-multi-node-cluster/blob/main/LICENSE) file for details. 