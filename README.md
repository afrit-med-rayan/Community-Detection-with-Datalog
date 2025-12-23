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

## 🧪 Algorithm

We use a **Connected Components** algorithm implemented in pure Stratified Datalog (`src/cc_algorithm.dl`). This declarative approach ensures correctness and parallel scalability without complex imperative state management.

## 📄 License

Academic Project - Fall 2025.
