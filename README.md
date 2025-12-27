# Datalog Community Detection 🕸️

A robust Social Network Analysis (SNA) tool that uses Declarative Logic (**Datalog**) to identify communities in graphs. Now features a **Dynamic Web Interface**!

## 📂 Project Structure

- **`src/`**: Source code (`app.py`, Datalog rules, visualization logic).
- **`docs/`**: Academic report and technical specifications.
- **`data/`**: Input datasets (e.g., `karate.csv`).
- **`Dockerfile` / `docker-compose.yml`**: Container orchestration.

## 🚀 Quick Start (Docker Compose)

The easiest way to run the project.

1.  **Start the App**:
    ```bash
    docker-compose up --build
    ```

2.  **Access the Dashboard**:
    Open **[http://localhost:5000](http://localhost:5000)** in your browser.

## 🛠️ Manual Installation

If you prefer running locally without Docker:

**Prerequisites**:
*   Python 3.8+
*   [Soufflé Datalog Engine](https://souffle-lang.github.io/)

**Steps**:
1.  Install dependencies: `pip install -r requirements.txt`
2.  Run the server:
    ```bash
    python src/app.py
    ```

## 🧪 Algorithms

We support multiple community detection algorithms implemented in pure Datalog:

1. **Label Propagation (LPA)**: Iterative label assignment based on neighbor majority
2. **Connected Components**: Transitive closure-based component detection
3. **Degree Centrality**: Hub detection via node degree tiers

## 📊 Datasets

- **Karate Club** (34 nodes): Classic social network benchmark
- **Dolphin Network** (62 nodes): Marine mammal social interactions
- **Les Misérables** (77 nodes): Character co-appearance network
- **Football** (31 nodes): Team games network

Select algorithms and datasets dynamically through the web interface!

## 📄 License

Academic Project - Fall 2025.
