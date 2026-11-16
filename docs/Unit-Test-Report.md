# Unit Test Report

## Environment

- Operating system: macOS
- Compiler: Apple Clang via g++
- Standard: C++17
- Execution date: 2026-11-16

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
- Cancellation performance
- Invalid passenger age, gender, and zero-seat inputs are covered.

## Limitations

- Journey-date filtering is not tested because the current search function does not accept a journey date.
- Cancellation confirmation with `Y` requires manual/system validation because it writes persistent data.
- Same-operation retry behavior is not fully validated.
