# Branch Coverage Report

## Environment

- Operating system: macOS
- Compiler: Apple Clang / LLVM 21.0.0
- Standard: C++17
- Execution date: 2026-11-16

## Result

| Metric | Value |
|---|---:|
| Total application branches | 262 |
| Covered branches | 160 |
| Missed branches | 102 |
| Branch coverage | 61.07% |

## Per-File Results

| Source file | Total branches | Missed branches | Coverage |
|---|---:|---:|---:|
| booking.cpp | 38 | 5 | 86.84% |
| cancellation.cpp | 40 | 19 | 52.50% |
| data_store.cpp | 74 | 41 | 44.59% |
| reservation.cpp | 26 | 18 | 30.77% |
| validation.cpp | 84 | 19 | 77.38% |

## Method

Branch coverage was obtained from the Branches, Missed Branches, and Cover columns produced by llvm-cov report.

The installed Apple LLVM version did not support the -show-branches=count option. The standard LLVM coverage report still provided branch totals and percentages.

## Coverage Gaps

- Persistence and file-error paths
- Missing reservation or train records
- Cancellation storage failures
- Reservation display fallback paths
- Less-common validation branches
