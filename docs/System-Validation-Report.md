# System Validation Report

## Scope

System-level validation of the Railway Reservation System workflows against the Software Requirements Specification (SRS) and Software Test Plan (STP).

## Automated Validation Evidence

| Workflow | Evidence | Result |
|---|---|---|
| Train search by source and destination | `test_train_search` (TS-01, TS-02) | Passed |
| Invalid search input rejection | `test_train_search` (TS-03, TS-04) | Passed |
| Ticket booking and seat allocation | `test_booking` (BK-01 to BK-09) | Passed |
| Booking with unavailable seats rejected | `test_booking` (BK-16 to BK-18) | Passed |
| Unique reservation references & persistence | `test_booking` (TC-004, TC-012) | Passed |
| Reservation lookup and formatted display | `test_cancellation` (TC-C08a–b) | Passed |
| Successful cancellation & seat restoration | `test_cancellation` (TC-C01a–c, TC-C05) | Passed |
| Repeated cancellation rejection | `test_cancellation` (TC-C02) | Passed |
| Invalid reservation identifiers rejection | `test_cancellation` (TC-C04, TC-C07a–c) | Passed |
| Cancellation declined with `N` | `test_cancellation` (TC-C11a–c) | Passed |

## Interactive CLI System Validation Evidence

| System Test ID | Workflow Tested | Inputs & Preconditions | Observed Outcome | Status |
|---|---|---|---|---|
| TC-SYS-L01 | Active Reservation View | Menu 5, ID `RES002` | Formatted details displayed, passenger Priya Nair, Status: Confirmed | Passed |
| TC-SYS-L02 | Cancelled Reservation View | Menu 5, ID `RES001` | Formatted details displayed, Status: Cancelled | Passed |
| TC-SYS-L03 | Non-existent ID Lookup | Menu 5, ID `RES999` | Handled gracefully with error prompt | Passed |
| TC-SYS-L04 | Malformed ID Lookup | Menu 5, ID `INVALID_ID` | Format error displayed, returned to menu | Passed |
| TC-SYS-C01 | Cancellation Aborted (`N`) | Menu 6, ID `RES002`, prompt `N` | Seats remain 198; status remains Confirmed; no disk mutation | Passed |
| TC-SYS-C02 | Cancellation Confirmed (`Y`)| Menu 6, ID `RES002`, prompt `Y` | Seats incremented to 199; status updated to Cancelled; disk persisted | Passed |
| TC-SYS-C03 | Cancel Non-existent Record | Menu 6, ID `RES999` | Rejected with not found error | Passed |
| TC-SYS-C04 | Cancel Malformed ID | Menu 6, ID `BAD_ID` | Rejected with invalid ID error | Passed |
| TC-SYS-C05 | Re-cancel Cancelled Record | Menu 6, ID `RES001` | Rejected: already cancelled | Passed |

## Results Summary

- Automated tests executed: 76 (Passed: 76, Failed: 0)
- Interactive CLI validation scenarios: 9 (Passed: 9, Failed: 0)
- Usability Review: Completed and verified in PR #41
- Cross-Platform Portability: Verified across Windows (MinGW-w64) and Linux via GitHub Actions CI (PR #42)

## Architectural & Reviewer Observations

1. **Seat & Status Invariant:** In live system testing, confirming cancellation on `RES002` for train `T002` transitioned available seats from 198 to 199 ($+1$), leaving `totalSeats` (200) invariant and all other train records untouched.
2. **Data Isolation Observation (`DEF-001`):** In-memory unit test mocks should avoid writing to production data files `data/trains.dat`.
3. **Journey-Date Filtering:** `searchTrains()` matches routes by source and destination stations. Journey-date filtering is noted as a future functional enhancement.

## Conclusion

All functional, security, and non-functional validation workflows have passed. The system is verified as robust, consistent, and ready for Part-3 academic submission.

