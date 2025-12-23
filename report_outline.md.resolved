# Project Report Structure: Community Detection with Datalog

This outline is designed for a 20-30 page academic report.

## 1. Introduction
- **1.1 Background**: Rise of social networks and the need for analysis.
- **1.2 Problem Definition**: What is community detection? (Formal definition: partitioning graph $G(V,E)$).
- **1.3 Project Objective**: Exploring declarative logic programming (Datalog) as a paradigm for graph analysis.
- **1.4 Scope**: Focusing on Labal Propagation and Modularity on static, unweighted graphs.

## 2. Theoretical Framework
- **2.1 Social Network Analysis (SNA)**:
    - Key metrics: Degree, Betweenness, Clustering Coefficient.
    - Community definitions: Strong vs Weak communities.
- **2.2 Datalog & Logic Programming**:
    - Basics: Atoms, Literals, Horn Clauses.
    - Evaluation: Bottom-up (Forward Chaining) vs Top-down.
    - The `Semi-Naive Evaluation` strategy (how standard engines work).
    - Why it fits graphs: $G=(V,E)$ is exactly a binary relation $E \subseteq V \times V$.

## 3. Literature Review (Based on Survey)
- **3.1 Traditional Algorithms**:
    - Feature-based (Louvain, Girvan-Newman).
    - Dynamic approaches.
- **3.2 Declarative Graph Analysis**:
    - Existing work on using Datalog/Prolog for SNA.
    - Advantages cited in literature (conciseness, parallelism).

## 4. Methodology & Design
- **4.1 System Architecture**:
    - Conceptual diagram: `Raw Data -> Facts -> Inference Engine -> Relations`.
- **4.2 Algorithm: Label Propagation (LPA)**:
    - Mathematical formulation: $L_i(t) = f(\{L_j(t-1) : j \in P(i)\})$.
    - Adaptation to Datalog: Using iteration indices to simulate time steps.
- **4.3 Schema Design**:
    - Input Relations: `edge`, `node`.
    - Intermediate Relations: `neighbor_label_count`, `max_label_count`.
    - Output Relations: `final_community`.

## 5. Implementation
- **5.1 Environment**:
    - Engine: Soufflé 2.x.
    - OS: Linux/WSL (Standard for Soufflé).
    - Host Language: Python 3.9 (for glue code).
- **5.2 Core Datalog Code**:
    - Show the `initialization` rule.
    - Show the `propagation` rule.
    - Explain the `aggregation` (counting labels).
- **5.3 Optimization**:
    - Indexing strategies (Soufflé does this auto-magically, but mention it).
    - Limiting iterations to prevent infinite loops (oscillation).

## 6. Experiments & Results
- **6.1 Datasets**:
    - Karate Club (Zachary, 1977).
    - Dolphin Network.
    - Les Miserables.
- **6.2 Metrics Definitions**:
    - Modularity ($Q$).
    - NMI (Normalized Mutual Information) - if ground truth exists.
- **6.3 Results**:
    - **Quality**: Table showing detected communities vs Ground Truth.
    - **Performance**: Execution time vs Graph Size (Node count).
    - **Code Metrics**: Line count (Datalog vs equivalent Python).

## 7. Discussion
- **7.1 Declarative vs Imperative**:
    - "What" vs "How".
    - Case study: Implementing transitive closure is 1 line in Datalog, ~10+ in C++.
- **7.2 Limitations of Datalog**:
    - Difficulty with random tie-breaking (Datalog is deterministic).
    - Difficulty with non-monotonic updates (requiring iteration count).
- **7.3 Scalability**: 
    - Discussing how semi-naive evaluation handles large datasets.

## 8. Conclusion
- Summary of findings.
- Future work: Dynamic Graph Datalog (e.g., Differential Datalog).

## 9. References
- [Survey Paper Citation]
- [Soufflé Citation]
- [LPA Citation]

## Appendices
- **A. User Manual**: How to install and run the tool.
- **B. Full Source Code**: The `.dl` files.
