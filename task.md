# Project Tasks: Community Detection using Datalog

- [x] **Project Initialization**
    - [x] Define Project Architecture & Design (`technical_specification.md`) <!-- id: 0 -->
    - [x] Create Report Structure (`report_outline.md`) <!-- id: 1 -->
- [x] **Technical Specification Development**
    - [x] Design Datalog Graph Representation <!-- id: 2 -->
    - [x] Select and Justify Algorithm (LPA Focus) <!-- id: 3 -->
    - [x] Define Core Datalog Logic & Rules <!-- id: 4 -->
    - [x] Design Application Workflow (Input/Output/Engine) <!-- id: 5 -->
    - [x] Write Sample Datalog Code for Label Propagation (`lpa_example.dl`) <!-- id: 6 -->
- [x] **Application Implementation (CLI)**
    - [x] Create `parser.py` for CSV to Facts conversion <!-- id: 10 -->
    - [x] Create `visualizer.py` for plotting results <!-- id: 11 -->
    - [x] Update `main.py` to orchestrate the pipeline <!-- id: 7 -->
    - [x] Create Sample Dataset (`data/karate.csv`) <!-- id: 12 -->
    - [x] Create `README.md` with installation and usage guide <!-- id: 13 -->
    - [x] **Git Repository Setup**
    - [x] Initialize Git and Push to GitHub <!-- id: 14 -->
    - [x] Create `requirements.txt` <!-- id: 15 -->
- [x] **Reporting**
    - [x] Draft Full Academic Report (`report.md`) <!-- id: 16 -->
- [x] **Containerization**
    - [x] Create `Dockerfile` for easy execution <!-- id: 17 -->
    - [x] Fix Datalog compatibility issues <!-- id: 18 -->

- [x] **Web Migration (New Requirement)**
    - [x] **Infrastructure**
        - [x] Update `requirements.txt` with Flask <!-- id: 19 -->
        - [x] Update `Dockerfile` to expose port 5000 <!-- id: 20 -->
    - [x] **Backend Development**
        - [x] Create `app.py` (Flask Server) <!-- id: 21 -->
        - [x] Implement API `/run` to execute Datalog on request <!-- id: 22 -->
    - [x] **Frontend Development**
        - [x] Create `templates/index.html` with Vis.js <!-- id: 23 -->
        - [x] Add interactive physics/clustering controls <!-- id: 24 -->

## 📚 **Academic Requirements (Code/App)**
- [x] **Datalog Native Stats**
    - [x] Implement Degree Centrality `statistics.dl`
    - [x] Implement Triangle Counting `statistics.dl`
- [x] **Datalog Native Optimization**
    - [x] Implement Modularity Score `modularity.dl`
- [x] **Graph Traversal**
    - [x] Implement Transitive Closure `reachability.dl`
- [x] **Validation**
    - [x] Create Unit Tests `tests/test_datalog.py`

## 🎓 **Your Final Steps (Manual)**
- [x] **Execute Web App**
    - [x] Run `docker-compose up --build`
    - [x] Open `http://localhost:5000`
