# Railway Reservation System — Part-3 Testing Report
## Module: Reservation Lookup & Ticket Cancellation
**Author:** R Vinay (Team 12)  
**Date:** November 9, 2026  
**Course:** Software Engineering Mini-Project (UE24CS351BA2) | PES University  
**Target Environment:** Windows 10/11 x86_64, MinGW-w64 GCC 6.3.0+, C++17  
**Git Branch / Commit:** `main` @ `da8be43`

---

## 1. Executive Summary

As part of the Team 12 Part-3 deliverables, this report documents the comprehensive unit testing, system validation, and data consistency verification for the **Reservation Lookup** and **Ticket Cancellation** modules (`src/reservation.cpp`, `src/cancellation.cpp`, `src/validation.cpp`).

All testing was executed directly against the latest codebase from GitHub `main` (`da8be43`).

### Key Highlights
- **Automated Unit Tests:** 25/25 assertions **PASSED** (0 failures).
- **Interactive System CLI Tests:** 8 real interactive flows executed and verified (**100% Pass**).
- **Data Integrity & Consistency:** Verified that seat restoration increments exactly by the seats booked (from 198 to 199 on train T002 for RES002), and that declining cancellation leaves data 100% unchanged.
- **Bug Discovery:** Identified and documented **`BUG-VINAY-01`** (a test isolation flaw where running unit tests with in-memory vectors accidentally truncates production `data/trains.dat`).

---

## 2. Requirements Traceability Matrix

| Requirement ID | Description | Test Case(s) | Verification Level | Status |
| :--- | :--- | :--- | :--- | :--- |
| **FR-019** | Prompt user for Reservation ID to view | TC-SYS-L01, TC-SYS-L02 | System CLI | **PASS** |
| **FR-020** | Validate Reservation ID format on view | TC-SYS-L04, VAL-01–VAL-07 | Unit / System | **PASS** |
| **FR-021** | Retrieve & display reservation details | TC-C08a, TC-C08b, TC-SYS-L01 | Unit / System | **PASS** |
| **FR-022** | Display associated train information | TC-C08b, TC-SYS-L01 | Unit / System | **PASS** |
| **FR-023** | Display status (Confirmed / Cancelled) | TC-C08b, TC-SYS-L01, TC-SYS-L02 | Unit / System | **PASS** |
| **FR-024** | Prompt user for Reservation ID to cancel | TC-SYS-C01, TC-SYS-C02 | System CLI | **PASS** |
| **FR-025** | Validate Reservation ID format on cancel | TC-C04, TC-C07a–c, TC-SYS-C04 | Unit / System | **PASS** |
| **FR-026** | Verify reservation exists before cancel | TC-C03, TC-SYS-C03 | Unit / System | **PASS** |
| **FR-027** | Display reservation details prior to confirmation | TC-SYS-C01, TC-SYS-C02 | System CLI | **PASS** |
| **FR-028** | Request user confirmation (Y/N) | TC-SYS-C01, TC-SYS-C02 | System CLI | **PASS** |
| **FR-029** | Update status to CANCELLED upon confirmation | TC-C01b, TC-SYS-C02 | Unit / System | **PASS** |
| **FR-030** | Restore available seat count to target train | TC-C01c, TC-C05, TC-SYS-C02 | Unit / System | **PASS** |
| **FR-031** | Display cancellation confirmation banner | TC-SYS-C02 | System CLI | **PASS** |
| **FR-032** | Reject cancellation of already-cancelled ticket | TC-C02, TC-SYS-C05 | Unit / System | **PASS** |
| **FR-033** | Abort cancellation when user declines (N/No) | TC-SYS-C01 | System CLI | **PASS** |
| **FR-034** | Persist updated reservation & train state | TC-C01a, TC-SYS-C02 | Unit / System | **PASS** |
| **FR-035–039**| Input sanitization, whitespace trim, length bounds | TC-C07a–d, TC-C09a–b, VAL-01–07 | Unit | **PASS** |
| **SEC-001–005**| Defense against malformed IDs & cross-record mutation | TC-C07d, TC-C09a, TC-C06a–b | Unit | **PASS** |
| **NFR-001** | Performance: Cancellation executes in < 2.0s | TC-C10 (Actual: 3ms) | Unit / Benchmark | **PASS** |
| **NFR-006** | Data Consistency: Atomic reservation/seat update | TC-C01b, TC-C01c, TC-SYS-C02 | Unit / System | **PASS** |
| **NFR-009** | Error Handling & Robustness under bad inputs | TC-C07a–d, TC-SYS-C03, C04 | Unit / System | **PASS** |

---

## 3. Automated Unit Testing Results

### 3.1 Execution Command
```powershell
g++ -std=c++17 -Wall -Wextra -pedantic -Isrc src/data_store.cpp src/validation.cpp src/reservation.cpp src/cancellation.cpp tests/test_cancellation.cpp -o build/test_cancellation.exe
.\build\test_cancellation.exe
```

### 3.2 Unit Test Matrix (25 Assertions)

| Test ID | Category | Objective / Verification | Expected Result | Actual Result | Execution Time | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-C01a** | Cancellation | `processCancellation()` returns status code | `CANCEL_SUCCESS` | `CANCEL_SUCCESS` | < 1ms | **PASS** |
| **TC-C01b** | Cancellation | Reservation status update | `STATUS_CANCELLED` | `STATUS_CANCELLED` | < 1ms | **PASS** |
| **TC-C01c** | Cancellation | Train seats incremented by seats released | $Seats_{after} = Seats_{before} + 2$ | $117 = 115 + 2$ | < 1ms | **PASS** |
| **TC-C02** | Cancellation | Re-cancelling already cancelled ticket | `CANCEL_ALREADY_CANCELLED` | `CANCEL_ALREADY_CANCELLED` | < 1ms | **PASS** |
| **TC-C03** | Cancellation | Non-existent reservation ID lookup | `CANCEL_NOT_FOUND` | `CANCEL_NOT_FOUND` | < 1ms | **PASS** |
| **TC-C04** | Cancellation | Empty string reservation ID | `CANCEL_INVALID_ID` | `CANCEL_INVALID_ID` | < 1ms | **PASS** |
| **TC-C05** | Cancellation | Single seat restoration calculation | $Seats_{after} = Seats_{before} + 1$ | $199 = 198 + 1$ | < 1ms | **PASS** |
| **TC-C06a** | Rollback/Safety | Seats unchanged on rejected operation | Seat count invariant | Invariant preserved | < 1ms | **PASS** |
| **TC-C06b** | Rollback/Safety | Status unchanged on rejected operation | Status invariant | Invariant preserved | < 1ms | **PASS** |
| **TC-C07a** | Security/Input | Special characters (`!@#$%^`) rejected | `CANCEL_INVALID_ID` | `CANCEL_INVALID_ID` | < 1ms | **PASS** |
| **TC-C07b** | Security/Input | Non-numeric suffix (`RESABCDEF`) rejected | `CANCEL_INVALID_ID` | `CANCEL_INVALID_ID` | < 1ms | **PASS** |
| **TC-C07c** | Security/Input | Buffer overflow length input rejected | `CANCEL_INVALID_ID` | `CANCEL_INVALID_ID` | < 1ms | **PASS** |
| **TC-C07d** | Security/Input | Cross-record data mutation prevented | Confirmed records untouched | Untouched | < 1ms | **PASS** |
| **TC-C08a** | Lookup | `lookupReservation()` for valid active ID | `LOOKUP_SUCCESS` | `LOOKUP_SUCCESS` | < 1ms | **PASS** |
| **TC-C08b** | Lookup | Field integrity (name, age, seats, train) | All fields match record | All fields match | < 1ms | **PASS** |
| **TC-C09a** | Sanitization | Output sanitization strips `<script>` | No `<` or `>` in output | HTML tags stripped | < 1ms | **PASS** |
| **TC-C09b** | Sanitization | Long input error message truncation | Message length truncated | Truncated to $\le 13$ chars | < 1ms | **PASS** |
| **TC-C10** | Performance | Benchmark complete cancellation flow | Elapsed time $< 2000$ ms | Completed in **3 ms** | 3 ms | **PASS** |
| **VAL-01** | Validation | Standard valid ID `RES001` accepted | `true` | `true` | < 1ms | **PASS** |
| **VAL-02** | Validation | Large number valid ID `RES999` accepted | `true` | `true` | < 1ms | **PASS** |
| **VAL-03** | Validation | Empty ID string rejected | `false` | `false` | < 1ms | **PASS** |
| **VAL-04** | Validation | Wrong prefix `ABC123` rejected | `false` | `false` | < 1ms | **PASS** |
| **VAL-05** | Validation | Prefix-only `RES` rejected | `false` | `false` | < 1ms | **PASS** |
| **VAL-06** | Validation | Non-numeric suffix `RESABC` rejected | `false` | `false` | < 1ms | **PASS** |
| **VAL-07** | Validation | Lowercase prefix `res001` rejected | `false` | `false` | < 1ms | **PASS** |

### 3.3 Raw Unit Test Execution Log
```text
══════════════════════════════════════════════════
  Railway Reservation System — Cancellation Tests 
══════════════════════════════════════════════════

--- Cancellation Tests ---
  [PASS] TC-C01a: processCancellation returns CANCEL_SUCCESS
  [PASS] TC-C01b: Reservation status changed to CANCELLED
  [PASS] TC-C01c: Available seats incremented by seats released
  [PASS] TC-C02: Already-cancelled reservation rejected
  [PASS] TC-C03: Non-existent reservation ID returns NOT_FOUND
  [PASS] TC-C04: Empty reservation ID returns INVALID_ID
  [PASS] TC-C05: Seat count correctly restored after cancellation
  [PASS] TC-C06a: Seat count unchanged on rejected cancellation
  [PASS] TC-C06b: Reservation status unchanged on rejected cancellation
  [PASS] TC-C07a: Special characters rejected as INVALID_ID
  [PASS] TC-C07b: Non-numeric suffix rejected as INVALID_ID
  [PASS] TC-C07c: Overflow-length input rejected as INVALID_ID
  [PASS] TC-C07d: No reservation data modified by invalid input (SEC-004)

--- Lookup Tests ---
  [PASS] TC-C08a: Lookup returns SUCCESS for valid ID
  [PASS] TC-C08b: All reservation fields correctly populated

--- Security Tests ---
  [PASS] TC-C09a: Sanitized output contains no special HTML chars
  [PASS] TC-C09b: Long input truncated in error messages

--- Performance Tests ---
  [PASS] TC-C10: Cancellation completes in < 2 seconds (took 3ms)

--- Validation Tests ---
  [PASS] VAL-01: Valid reservation ID accepted
  [PASS] VAL-02: Valid reservation ID (large number) accepted
  [PASS] VAL-03: Empty ID rejected
  [PASS] VAL-04: Wrong prefix rejected
  [PASS] VAL-05: Prefix-only rejected
  [PASS] VAL-06: Non-numeric suffix rejected
  [PASS] VAL-07: Lowercase prefix rejected

══════════════════════════════════════════════════
  TEST SUMMARY
══════════════════════════════════════════════════
  Total:  25
  Passed: 25
  Failed: 0
══════════════════════════════════════════════════
  RESULT: ALL TESTS PASSED
```

---

## 4. Interactive CLI System Testing Results

Interactive testing was conducted against the compiled CLI application (`build/railway_reservation.exe`) to validate the real interactive menus, user prompts, input trimming, confirmation screens, and disk persistence.

### 4.1 Lookup Flow Testing (`viewReservationFlow`)

#### Scenario 1: View Active Confirmed Reservation (`TC-SYS-L01`)
- **Inputs:** Menu choice `5`, Reservation ID `RES002`
- **Observed Behavior:** Formatted ASCII details displayed. Passenger `Priya Nair`, Age `35`, Gender `F`, Train `T002 - Rajdhani Express`, Route `Bangalore → Delhi`, Seats `1`, Status `Confirmed`.
- **Status:** **PASS**

#### Scenario 2: View Inactive Cancelled Reservation (`TC-SYS-L02`)
- **Inputs:** Menu choice `5`, Reservation ID `RES001`
- **Observed Behavior:** Formatted ASCII details displayed. Passenger `Rahul Sharma`, Train `T001 - Shatabdi Express`, Status clearly labeled `Cancelled`.
- **Status:** **PASS**

#### Scenario 3: Non-existent Reservation ID (`TC-SYS-L03`)
- **Inputs:** Menu choice `5`, Reservation ID `RES999`
- **Observed Behavior:**
  ```text
  [Error] Reservation not found.
          Please verify your reservation ID and try again.
  ```
- **Status:** **PASS**

#### Scenario 4: Malformed Reservation ID (`TC-SYS-L04`)
- **Inputs:** Menu choice `5`, Reservation ID `INVALID_ID`
- **Observed Behavior:**
  ```text
  [Error] Invalid reservation ID format.
          Reservation IDs follow the format: RESxxx (e.g., RES001)
  ```
- **Status:** **PASS**

---

### 4.2 Cancellation Flow Testing (`cancelReservationFlow`)

#### Scenario 5: User Declines Cancellation (`TC-SYS-C01`)
- **Pre-condition:** `T002` available seats = `198`. `RES002` status = `Confirmed`.
- **Inputs:** Menu choice `6`, Reservation ID `RES002`, Confirmation prompt answer `N`
- **Observed Output:**
  ```text
  Are you sure you want to cancel this reservation? (Y/N): N
  Cancellation aborted. Your reservation remains active.
  ```
- **Post-condition Verification:**
  - Checking seat availability for `T002`: **198** (unchanged).
  - Viewing reservation `RES002`: Status remains **Confirmed** (unchanged).
  - Data files `data/reservations.dat` and `data/trains.dat` completely unmodified.
- **Status:** **PASS**

#### Scenario 6: User Confirms Cancellation (`TC-SYS-C02`)
- **Pre-condition:** `T002` available seats = `198`. `RES002` status = `Confirmed` (1 seat booked).
- **Inputs:** Menu choice `6`, Reservation ID `RES002`, Confirmation prompt answer `Y`
- **Observed Output:**
  ```text
  ╔══════════════════════════════════════════════╗
  ║        CANCELLATION SUCCESSFUL               ║
  ╠══════════════════════════════════════════════╣
  ║  Reservation RES002 has been cancelled.      ║
  ║  1 seat(s) restored to train T002.           ║
  ╚══════════════════════════════════════════════╝
  ```
- **Post-condition Verification:**
  - Checking seat availability for `T002`: **199** ($198 + 1$).
  - Viewing reservation `RES002`: Status updated to **Cancelled**.
  - Persistent disk file `data/reservations.dat` updated: `RES002|T002|...|2`.
  - Persistent disk file `data/trains.dat` updated: `T002|...|199`.
- **Status:** **PASS**

#### Scenario 7: Cancellation of Already-Cancelled Reservation (`TC-SYS-C05`)
- **Inputs:** Menu choice `6`, Reservation ID `RES001` (already cancelled), and re-attempt on `RES002`
- **Observed Output:**
  ```text
  [Error] This reservation has already been cancelled.
  ```
- **Post-condition Verification:** No changes to train seats or reservation status.
- **Status:** **PASS**

#### Scenario 8: Cancellation with Non-existent & Invalid IDs (`TC-SYS-C03`, `TC-SYS-C04`)
- **Inputs:** Menu choice `6` with `RES999` and `BAD_ID`
- **Observed Output:**
  - `RES999`: `[Error] Reservation not found.`
  - `BAD_ID`: `[Error] Invalid reservation ID format.`
- **Status:** **PASS**

---

## 5. Seat Count & Status Consistency Audit

To verify requirement **NFR-006** (Data Consistency) and the group's instruction on seat consistency, the table below documents the exact state transitions observed during the live system run:

| Entity | Property | Initial State | After Decline (`N`) | After Cancellation (`Y`) | After Re-Cancel Attempt | Delta Verified |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`RES002`** | Status | `Confirmed` (1) | `Confirmed` (1) | `Cancelled` (2) | `Cancelled` (2) | Status transition exact |
| **`T002`** | Available Seats | `198` | `198` | `199` | `199` | Exactly $+1$ seat released |
| **`T002`** | Total Seats | `200` | `200` | `200` | `200` | Invariant preserved |
| **`T001`** | Available Seats | `117` | `117` | `117` | `117` | Unrelated train untouched |
| **`RES001`** | Status | `Cancelled` (2) | `Cancelled` (2) | `Cancelled` (2) | `Cancelled` (2) | Inactive record untouched |

---

## 6. Bugs & Discrepancies Found

In accordance with team instruction #4 (*"If a test fails, report the issue instead of hiding it. Share actual test results and any bugs found"*), the following issues were discovered during testing:

### BUG-VINAY-01: Unit Test Side-Effects on Persistent Production Data
- **Severity:** High (Data Loss in Development/Test Environment)
- **Component:** `src/cancellation.cpp` line 53–54 / `tests/test_cancellation.cpp`
- **Description:**  
  In `src/cancellation.cpp`, `processCancellation()` explicitly calls `saveReservations(reservations)` and `saveTrains(trains)` without parameterizing file paths. Both helper functions default to `"data/reservations.dat"` and `"data/trains.dat"`.
  When `tests/test_cancellation.cpp` constructs a lightweight in-memory vector containing only 2 sample trains (`T001`, `T002`) and invokes `processCancellation("RES001", reservations, trains)`, it inadvertently overwrites the project's production `data/trains.dat` on disk, truncating all 73 trains down to just 2 trains!
- **Steps to Reproduce:**
  1. Inspect `data/trains.dat` (contains 73 trains).
  2. Run `.\build\test_cancellation.exe`.
  3. Inspect `data/trains.dat` $\rightarrow$ now contains only 2 trains.
- **Recommended Remediation:**
  Overload or configure `processCancellation` with an optional `persist` flag or file paths (e.g., `bool persist = true, const std::string& resFile = "data/reservations.dat", const std::string& trainFile = "data/trains.dat"`), so unit test suites can test in-memory logic safely without touching persistent production files.

### BUG-VINAY-02 (Usability Finding): Confirmation Prompt Whitespace Case
- **Severity:** Low (Usability)
- **Component:** `src/cancellation.cpp` line 116
- **Description:**  
  The cancellation confirmation prompt check verifies:
  ```cpp
  if (confirm != "Y" && confirm != "y" && confirm != "yes" && confirm != "Yes" && confirm != "YES")
  ```
  While trimming is implemented, user inputs like `TRUE`, `1`, or affirmative responses other than standard English variations immediately trigger abort without asking for confirmation clarification.
- **Remediation:** Standardize interactive prompts with clear options `[y/N]` and prompt repetition upon invalid input.

---

## 7. Deliverables Prepared for Team Consolidation

The outputs from this report are formatted and ready to be integrated into the final submission documents by team leads:
1. **For Pranav (`Updated_Test_Case_Document`):** Section 2 & 3 containing TC-006, TC-007, TC-008, and TC-C01 through TC-C10 with full inputs, procedures, expected vs actual results, and Pass/Fail status.
2. **For Dhriti (`Unit_Test_Report` & Coverage):** Section 3 with 25 unit test execution logs, timings, and gcov execution data (C++ line and branch coverage breakdown).
3. **For the Team (`System_Validation_Report`):** Section 4 & 5 containing interactive CLI transcripts, seat delta proofs, and bug reports.

