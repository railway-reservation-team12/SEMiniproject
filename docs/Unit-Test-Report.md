# Unit Test Report

## Environment

- Operating systems: Windows 11 / macOS / Ubuntu Linux (CI)
- Compiler: MinGW-w64 GCC 13.x / Apple Clang / GCC 11+
- Standard: C++17
- Execution dates: 2026-11-16 to 2026-11-17

## Results

| Module | Tests | Passed | Failed |
|---|---:|---:|---:|
| Train search | 6 | 6 | 0 |
| Booking | 42 | 42 | 0 |
| Cancellation and reservation | 28 | 28 | 0 |
| **Total** | **76** | **76** | **0** |

## Covered Areas

- Train route search
- Invalid and empty search input
- Passenger-name validation
- Journey-date validation
- Seat availability
- Booking persistence
- Unique reservation references
- Reservation lookup
- Cancellation
- Repeated cancellation rejection
- Seat restoration
- Reservation-ID validation
- Invalid-input protection
- Cancellation-decline confirmation
- Cancellation performance (TC-C10 benchmark: 3ms–11ms)
- Invalid passenger age, gender, and zero-seat inputs are covered.

## Verification & Limitations Notes

- Journey-date filtering is not tested in route search because the current search function matches routes by source and destination; journey date is validated during booking.
- Cancellation confirmation with `Y` writes persistent data and was verified via interactive system CLI testing (TC-SYS-C02 in `docs/System-Validation-Report.md` and `docs/Vinay_Reservation_Cancellation_Report.md`).
- Same-operation retry behavior is handled at the interactive menu loop level.

