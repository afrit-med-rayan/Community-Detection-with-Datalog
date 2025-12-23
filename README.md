# Community Detection with Datalog

A declarative approach to detecting communities in social networks using the Label Propagation Algorithm (LPA) and Soufflé.

## Project Structure
```
.
├── lpa_algorithm.dl       # Datalog implementation of LPA
├── main.py                # Main orchestrator script
├── parser.py              # CSV to Datalog facts converter
├── visualizer.py          # NetworkX-based visualization module
├── data/
│   └── karate.csv         # Sample dataset (generated on first run)
├── facts/                 # Generated Datalog facts directory
└── output/                # Analysis results and plots
```

## Prerequisites

1.  **Python 3.8+**
    *   Required packages: `networkx`, `matplotlib`
    *   `pip install networkx matplotlib`

2.  **Soufflé Datalog Engine**
    *   **Ubuntu/WSL**: `sudo apt install souffle`
    *   **Mac**: `brew install souffle`
    *   **Source**: [https://souffle-lang.github.io/](https://souffle-lang.github.io/)

## Usage

Run the main script. If no input is provided, it defaults to `data/karate.csv` (and creates it if missing):

```bash
python main.py
```

Or specify your own dataset:

```bash
python main.py data/your_network.csv
```

## How It Works

1.  **Parsing**: The Python script reads the Edge List CSV and generates fact files in `facts/` (`node.facts`, `edge.facts`).
2.  **Logic**: Soufflé executes `lpa_algorithm.dl`.
    *   Initializes every node with a unique label.
    *   Iteratively updates labels to the most frequent neighbor label.
    *   Calculates a Modularity score for the final partition.
3.  **Visualization**: Python reads the output communities and generates `output/communities.png`.

## Algorithm Details

*   **Label Propagation**: An efficient, near-linear time algorithm.
*   **Modularity Calculation**: Implemented purely in Datalog using aggregation functions.
