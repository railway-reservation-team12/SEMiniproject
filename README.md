# Team 12 – Railway Reservation System

[![C++ Tests CI](https://github.com/railway-reservation-team12/SEMiniproject/actions/workflows/cpp-tests.yml/badge.svg)](https://github.com/railway-reservation-team12/SEMiniproject/actions)
![C++ Standard](https://img.shields.io/badge/standard-C%2B%2B17-blue.svg)
![Tests](https://img.shields.io/badge/unit%20tests-76%20passed%20%7C%200%20failed-brightgreen.svg)
![Audit Status](https://img.shields.io/badge/reviewer%20audit-approved-success.svg)
![Institution](https://img.shields.io/badge/PES%20University-Section%20F-orange.svg)

> **Course:** Software Engineering Mini-Project (UE24CS351BA2)  
> **Department:** Department of Computer Science and Engineering, PES University, Bangalore  
> **Academic Year:** 2026–2027 | **Section:** F | **Team:** 12  
> **Baseline Commit:** `main` @ `08207b7` (synchronized with `railway-reservation-team12/SEMiniproject.git`)  
> **Final Reviewer Verdict:** **APPROVED FOR FINAL SUBMISSION**

---

## 1. Project Overview & Scope

The **Railway Reservation System** is a modular, high-reliability academic software system engineered in modern **C++17** and adhering strictly to international software engineering standards (**IEEE 830/29148** for SRS, **IEEE 1016** for SAD, **IEEE 829** for Software Test Documentation, and **IEEE 1028** for Independent Quality Audits).

### Core Capabilities:
- **Train Route Search:** Search scheduled trains by source and destination stations (case-insensitive, whitespace-trimmed).
- **Seat Availability Checking:** Dynamic, real-time seat inventory retrieval.
- **Ticket Booking:** Passenger detail validation (Name, Age 1–120, Gender `M`/`F`, Date `DD-MM-YYYY`), atomic seat count reduction, and sequential unique reference generation (`RES001`, `RES002`...).
- **Reservation Lookup:** Search and display formatted reservation details including passenger information, journey schedule, and status (`Confirmed` or `Cancelled`).
- **Ticket Cancellation:** Atomic cancellation workflow requiring explicit `(Y/N)` confirmation, seat restoration ($Seats_{after} = Seats_{before} + Seats_{booked}$), duplicate cancellation prevention, and data persistence.
- **Security & Input Sanitization:** Regex-based boundary enforcement and HTML character stripping (`<` and `>` sanitized) to prevent injection and memory corruption.
- **Bonus Web UI:** Local web-based interactive client and lightweight HTTP server.

---

## 2. Team Members & Designated Roles

| Name | Role | Core Contributions |
|:---|:---|:---|
| **Parinitha Ramesh** | Development Lead | Booking module architecture, passenger flow, web interface |
| **Pranav S S** | QA & Test Lead | Software Test Plan (STP), test harness development, CI workflows |
| **R Vinay** | Independent Reviewer / Quality Lead | Independent quality audit, SRS/SAD/STP compliance, cancellation testing, reviewer report |
| **Dhriti Rajesh** | Analysis & Testing Lead | Code & branch coverage analysis, modularity inspection, traceability verification |

---

## 3. Project Deliverables & Documentation Index

### Part-1: Specification & Design Documents (Audited v1.2)
* [Railway_Reservation_System_SRS_Team12_Audited.docx](Railway_Reservation_System_SRS_Team12_Audited.docx): Software Requirements Specification (v1.2) compliant with IEEE 830/29148. Features 39 Functional Requirements (FR-001–039), 5 Security Requirements (SEC-001–005), 10 Non-Functional Requirements (NFR-001–010), a fully linked Requirements Traceability Matrix (**0 TBDs**), and Appendix D Reviewer Approval.
* [SAD_Railway_Reservation_System_Team12_Audited.docx](SAD_Railway_Reservation_System_Team12_Audited.docx): Software Architecture and Design Specification (v1.2) compliant with IEEE 1016. Details the 4-layer architecture, component diagrams, sequence diagrams with validation, API signatures, resolved open issues, and signed reviewer approval.
* [Test_Plan_Railway_Reservation_System.docx](Test_Plan_Railway_Reservation_System.docx): Software Test Plan (v1.2) compliant with IEEE 829. Security validation located in Section 5.1 per faculty brief, 15 formal test items (TC-001 through TC-014, Inspection-001) updated to **Passed**, and Reviewer sign-off in Table 11.
* [Team12_Strict_Part1_Audit_Report.docx](Team12_Strict_Part1_Audit_Report.docx): Formal audit report evaluating Part-1 deliverables.

### Part-2: Implementation & Source Architecture
* Modular C++17 layered application in `src/`:
  - `src/main.cpp`: CLI presentation layer and interactive menu loop.
  - `src/booking.cpp` & `src/booking.h`: Train search and passenger ticket booking.
  - `src/cancellation.cpp` & `src/cancellation.h`: Ticket cancellation, seat restoration, and confirmation handling.
  - `src/reservation.cpp` & `src/reservation.h`: Reservation lookup and ASCII record rendering.
  - `src/validation.cpp` & `src/validation.h`: Input validation, regex bounds, and display sanitization.
  - `src/data_store.cpp` & `src/data_store.h`: Delimited file-based persistence for `data/trains.dat` and `data/reservations.dat`.
  - `src/models.h`: Core data domain structures (`Train`, `Reservation`, `Passenger`, `ReservationStatus`).
* Web UI client and servers in `web/` and `ui/`.

### Part-3: Testing, Quality Assurance & Reviewer Evidence
* [Reviewer_Audit_and_Compliance_Report_Team12.docx](Reviewer_Audit_and_Compliance_Report_Team12.docx) & [docs/Reviewer-Audit-and-Compliance-Report.md](docs/Reviewer-Audit-and-Compliance-Report.md): **Master Independent Reviewer Report** containing all 5 mandatory reviewer evidence deliverables:
  1. Detailed Document Review Comments (SRS, SAD, STP, Code)
  2. Complete Requirement-to-Code/Test Consistency Check (Exhaustive RTM)
  3. Defect & Issue List (`DEF-001` through `DEF-005` with root causes and remediation)
  4. Formal Approval & Sign-Off Record
  5. 25-Point Final Submission Readiness Checklist
* [docs/Test-Execution-Summary.md](docs/Test-Execution-Summary.md): Consolidated execution summary covering all 15 Test Plan cases.
* [docs/Unit-Test-Report.md](docs/Unit-Test-Report.md): Automated unit test execution log (**76 passed, 0 failed**).
* [docs/System-Validation-Report.md](docs/System-Validation-Report.md): End-to-end interactive CLI system validation scenarios (TC-SYS-L01–04, TC-SYS-C01–05).
* [docs/Code-Coverage-Report.md](docs/Code-Coverage-Report.md): LLVM instrumentation coverage analysis (**73.30% line coverage, 92.86% function coverage, 100% validation coverage**).
* [docs/Branch-Coverage-Report.md](docs/Branch-Coverage-Report.md): LLVM branch coverage report (**61.07% application branch coverage**).
* [docs/Inspection-001-Modularity-Testability.md](docs/Inspection-001-Modularity-Testability.md): Architectural inspection verifying component modularity.
* [docs/Vinay_Reservation_Cancellation_Report.md](docs/Vinay_Reservation_Cancellation_Report.md): Lookup & cancellation module testing report.

---

## 4. Architectural Pattern: 4-Layer Architecture

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│         CLI (src/main.cpp)  /  Web UI (web/)           │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    Application Layer                   │
│   src/booking.cpp  |  src/cancellation.cpp  |  ...     │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
┌─────────────▼──────────────┐ ┌───────────▼─────────────┐
│  Domain Validation Layer   │ │    Data Persistence     │
│     src/validation.cpp     │ │   src/data_store.cpp    │
│  (Sanitization & Bounds)   │ │  (data/trains, res.dat) │
└────────────────────────────┘ └─────────────────────────┘
```

---

## 5. Build, Test & Execution Guide

### 5.1 Prerequisites
- **Compiler:** C++17 compatible compiler (MinGW-w64 GCC 10+ on Windows, GCC 10+ on Linux, Apple Clang on macOS)
- **Build Tool:** GNU Make or manual shell invocations
- **Runtime:** Standard C++ standard library (zero external binary dependencies)
- **Optional Web UI:** Python 3.8+ (for local web server)

### 5.2 Building the Application
To compile the complete CLI system:
```bash
# Using Makefile
make

# Or using GCC directly on Windows/Linux:
g++ -std=c++17 -Wall -Wextra -Isrc src/main.cpp src/booking.cpp src/cancellation.cpp src/reservation.cpp src/validation.cpp src/data_store.cpp -o build/railway_reservation.exe
```

### 5.3 Running the Application
```bash
# Windows
.\build\railway_reservation.exe

# Linux / macOS
./build/railway_reservation
```

### 5.4 Running the Automated Test Suites
The project includes 3 standalone automated unit test suites exercising 76 test assertions:

```bash
# 1. Train Search Suite (6 assertions)
g++ -std=c++17 -Wall -Wextra -Isrc src/data_store.cpp src/validation.cpp src/booking.cpp tests/test_train_search.cpp -o build/test_train_search.exe
.\build\test_train_search.exe

# 2. Booking Suite (42 assertions)
g++ -std=c++17 -Wall -Wextra -Isrc src/data_store.cpp src/validation.cpp src/booking.cpp tests/test_booking.cpp -o build/test_booking.exe
.\build\test_booking.exe

# 3. Cancellation & Reservation Suite (28 assertions)
g++ -std=c++17 -Wall -Wextra -Isrc src/data_store.cpp src/validation.cpp src/reservation.cpp src/cancellation.cpp tests/test_cancellation.cpp -o build/test_cancellation.exe
.\build\test_cancellation.exe
```

**Test Results Summary:**
- Total Tests Executed: **76**
- Passed: **76 (100% Pass Rate)**
- Failed: **0**

### 5.5 Running the Web UI (Bonus Feature)
- **Windows:** Double-click or run `run_website.bat`
- **Manual (Python):**
  ```bash
  python web/server.py
  ```
  Open `http://localhost:8000` in any modern web browser.

---

## 6. Continuous Integration & Cross-Platform Support

All pull requests and pushes to `main` are automatically built and tested across multiple operating systems via GitHub Actions (`.github/workflows/cpp-tests.yml`):
- **Ubuntu Linux (GCC):** Compiles cleanly with `-Wall -Wextra -Werror` and executes all 76 unit tests.
- **Windows (MinGW-w64):** Validates Windows executable generation, path handling, and test execution.

---

## 7. Quality & Compliance Audit Verdict

The project has undergone an end-to-end audit by the **Independent Quality Reviewer (R Vinay)**:
- **Traceability:** 100% of functional, security, and non-functional requirements are linked to source code and tests. Zero `TBD` entries remain.
- **Consistency:** Confirmed seat restoration ($198 \rightarrow 199$) and non-mutation of inactive records verified on disk.
- **Performance:** Cancellation completes in **3 ms** (far exceeding the $\le 2.0\text{ s}$ requirement).
- **Final Verdict:** **APPROVED FOR FINAL SUBMISSION**
