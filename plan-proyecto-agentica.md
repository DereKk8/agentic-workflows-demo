# Project Plan: Architectures for Agentic AI (Agentic Workflows)

## 1. Project Objective

Develop a comprehensive research project and an educational functional prototype that illustrates the implementation of **Agentic AI (Agentic Workflows)**, focused on architectures for autonomous agents through the use of tools and APIs from the current ecosystem, such as LangChain and CrewAI.

## 2. Scope and Minimum Requirements

* **Practical Case:** Free topic, designed to demonstrate the interaction of autonomous agents.
* **Base Functional Requirement:** Implementation of at least two (2) domain entities with their respective CRUD flows (Create, Read, Update, Delete), over which agents can operate or interact.

## 3. Final Deliverables

All project artifacts will be centralized in a single **public GitHub repository**, which will contain a final version *Release*.

* **Source Code:** Complete functional prototype.
* **Infrastructure and Tests:** Docker configuration files and Postman collections.
* **Academic Documentation:** Final research document in LaTeX format, ready to compile in Overleaf.
* **Audiovisual Material:**
* Supporting visual presentation with architecture and concept diagrams.

* **Operations (README):** Detailed step-by-step instructions for local project deployment.

**Note:** The structured script for a 10 to 15 minute explanatory video will remain local and will not be part of the public GitHub repository.

---

## 4. Academic Research Structure (LaTeX Document)

### 4.1. Theoretical and Conceptual Framework

For Agentic AI, LangChain, CrewAI, and related APIs:

* Theoretical definition.
* Main characteristics.
* History and evolution of the paradigm.
* Architectural advantages and disadvantages.
* **Use Cases:** Specific problems and ideal situations for applying the approach.
* **Application Cases:** Real examples and proven success cases in industry.

### 4.2. Architectural and Relational Analysis

Evaluation of the agentic ecosystem against software engineering standards:

* **Adoption:** How common the designated technology stack is today.
* **Analysis Matrices (Cross-Evaluation):**
* *SOLID Principles* vs. Agentic Architecture.
* *Quality Attributes* (Scalability, Performance, Maintainability, etc.) vs. Agentic AI.
* *Architectural Tactics* vs. Agent Implementation.
* *Design Patterns* vs. Ecosystem (LangChain/CrewAI).
* *Labor Market* (Demand, roles, salaries) vs. Agentic Technologies.

---

## 5. Design and Architecture of the Illustrative Prototype

The functional prototype must ground the theoretical research in a practical deployment. The visual documentation of the system will follow industry standards:

### 5.1. Visual Modeling (C4 Model & UML)

* **Level 1:** Context Diagram (High level - User interaction with the agent system).
* **Level 2:** Container Diagram (APIs, Databases, Agent Orchestrator).
* **Level 3:** Component / UML Package Diagram (Internal structure of each container).
* **Dynamic Diagram:** Execution flow and communication between agents and CRUD entities.
* **Deployment Diagram:** Infrastructure topology (Docker container mapping).

### 5.2. Technical Specifications of the Prototype

* **Containerized Deployment:** Mandatory use of Docker (Dockerfile and docker-compose) to guarantee portability.
* **API Testing:** Mandatory use of Postman, exporting the collection to the repository, to document and test the CRUD and agent endpoints.
