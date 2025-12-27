# 🌐 Community Detection with Datalog

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Datalog](https://img.shields.io/badge/Datalog-Souffl%C3%A9-orange?style=for-the-badge)](https://souffle-lang.github.io/)

A state-of-the-art community detection platform that combines the declarative power of **Datalog** with a modern **Flask** backend and **Vis.js** frontend. This project demonstrates high-performance graph analysis using logic programming.

---

## 📽️ Preview

![UI Preview](https://via.placeholder.com/1200x600/764ba2/ffffff?text=Community+Detection+Dashboard+Preview)
*Modern, responsive dashboard with real-time graph visualization and physics controls.*

---

## 🚀 Key Features

### 🧠 Advanced Algorithms
- **Label Propagation (LPA)**: An iterative algorithm where nodes adopt the most frequent label of their neighbors. Perfect for social network clustering.
- **Connected Components**: Uses transitive closure to identify disconnected subgraphs with high efficiency.
- **Degree Centrality Tiers**: Identifies "Hubs" and "Peripheral" nodes based on relative degree centrality rankings.

### 📊 Included Datasets
- **Karate Club**: The classic 34-node benchmark for community detection.
- **Dolphin Network**: Social interactions among 62 dolphins in New Zealand.
- **Les Misérables**: Character co-appearance network from Victor Hugo's masterpiece (77 nodes).
- **Football**: NCAA football games network showcasing team clusters (31 nodes).

### 📈 Native Datalog Metrics
Calculated directly within the Soufflé engine for maximum performance:
- **Modularity Score (Q)**: Quantitative measure of clustering quality.
- **Triangle Counting**: Efficient subgraph motif detection.
- **Degree Centrality**: Per-node connectivity metrics.

---

## 🛠️ Architecture

The application is built with a modular "Logic + Glue" architecture:

1.  **Logic Layer (Soufflé Datalog)**: Handles all graph processing, reachability, and statistical calculations.
2.  **Orchestration Layer (Python/Flask)**: Manages the execution lifecycle, data parsing, and API endpoints.
3.  **Visualization Layer (Vis.js)**: Provides an interactive, physics-enabled canvas for exploring graph structures.
4.  **Environment (Docker)**: Ensures consistent execution across all platforms.

---

## 🚦 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Installation & Execution

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/afrit-med-rayan/Community-Detection-with-Datalog.git
    cd Community-Detection-with-Datalog
    ```

2.  **Launch via Docker Compose**:
    ```bash
    docker-compose up --build
    ```

3.  **Access the Dashboard**:
    Open your browser and navigate to:
    [**http://localhost:5000**](http://localhost:5000)

---

## 🧪 Development & Testing

Run the automated test suite to verify Datalog logic and system integration:

```bash
python -m pytest tests/test_datalog.py
```

---

## 📄 Documentation

- [**Academic Report**](report.md): Full theoretical background and methodology.
- [**Technical Specification**](technical_specification.md): Deep dive into the Datalog implementation details.
- [**Report Outline**](report_outline.md): Structure for the project documentation.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
**Author:** [Your Name] | **Course:** Big Data Analytics Project 2025
