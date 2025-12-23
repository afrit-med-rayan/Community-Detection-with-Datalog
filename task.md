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

## 🌐 **Web Migration (New Requirement)**
- [ ] **Infrastructure**
    - [ ] Update `requirements.txt` with Flask <!-- id: 19 -->
    - [ ] Update `Dockerfile` to expose port 5000 <!-- id: 20 -->
- [ ] **Backend Development**
    - [ ] Create `app.py` (Flask Server) <!-- id: 21 -->
    - [ ] Implement API `/run` to execute Datalog on request <!-- id: 22 -->
- [ ] **Frontend Development**
    - [ ] Create `templates/index.html` with Vis.js <!-- id: 23 -->
    - [ ] Add interactive physics/clustering controls <!-- id: 24 -->

## 🎓 **Your Final Steps (Manual)**
- [ ] **Execute Web App**
    - Run `docker run -p 5000:5000 bda-datalog`
    - Open `http://localhost:5000`
