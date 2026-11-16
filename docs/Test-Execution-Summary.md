# Test Execution Summary

## Environment

- Operating system: macOS
- Compiler: Apple Clang / C++17
- Execution date: 2026-11-16

## Automated Test Results

| Test suite | Total | Passed | Failed | Result |
|---|---:|---:|---:|---|
| Train search | 6 | 6 | 0 | Passed |
| Booking | 42 | 42 | 0 | Passed |
| Cancellation | 28 | 28 | 0 | Passed |
| **Total** | **76** | **76** | **0** | **Passed** |

## Test Plan Traceability

| Test Plan ID | Evidence | Status |
|---|---|---|
| TC-001 | TS-01; source/destination search | Partial |
| TC-002 | TS-03, TS-04; empty/invalid search input | Passed |
| TC-003 | Booking and seat checks | Passed |
| TC-004 | Booking and persistence tests | Passed |
| TC-005 | Unavailable-seat tests in `test_booking.cpp` | Passed |
| TC-006 | Lookup tests in `test_cancellation.cpp` | Passed |
| TC-007 | Successful cancellation tests | Passed |
| TC-008 | Invalid, repeated, and declined cancellation tests | Partial |
| TC-009 | Cancellation timing test | Partial |
| TC-010 | Validation and data-integrity tests | Passed |
| TC-011 | Manual usability review required | Pending |
| TC-012 | Unique-reference tests | Passed |
| TC-013 | Invalid-input tests | Partial |
| TC-014 | CI/platform evidence required | Pending |
| Inspection-001 | Manual modularity/testability inspection required | Pending |

## Deviations and Limitations

1. The current train-search test checks source and destination but does not validate journey-date filtering.
2. The cancellation confirmation decline path is automated. The confirmed `Y` path requires a safe system/manual test because it persists data.
3. Invalid passenger name, age, gender, date, and zero-seat inputs are covered by the booking tests.
4. Invalid input is rejected without terminating the application, but same-operation retry behavior is not fully validated.
5. Usability, portability, and modularity require manual or CI evidence.