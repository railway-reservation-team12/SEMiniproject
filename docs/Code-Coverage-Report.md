# Code Coverage Report

## Environment

- Operating systems: macOS / Linux / Windows
- Compiler: Apple Clang / LLVM 21.0.0 / GCC 13.x
- Standard: C++17
- Tests executed: 76 automated unit tests
- Execution dates: 2026-11-16 to 2026-11-17

## Application Source Coverage

| Metric | Coverage |
|---|---:|
| Region coverage | 77.85% |
| Function coverage | 92.86% |
| Line coverage | 73.30% |
| Branch coverage | 61.07% |

## Source Coverage Details

| Source file | Line coverage | Branch coverage | Functions Executed |
|---|---:|---:|---:|
| booking.cpp | 88.72% | 86.84% | 100.00% |
| cancellation.cpp | 56.44% | 52.50% | 100.00% |
| data_store.cpp | 70.59% | 44.59% | 88.89% |
| reservation.cpp | 50.00% | 30.77% | 75.00% |
| validation.cpp | 100.00% | 77.38% | 100.00% |

## Method

Coverage was generated with LLVM instrumentation using:

- `-fprofile-instr-generate`
- `-fcoverage-mapping`
- `llvm-profdata merge`
- `llvm-cov report`

Test files were excluded from application coverage statistics using:

```text
-ignore-filename-regex='tests/'
```

## Coverage Analysis & Insights

1. **Validation (`src/validation.cpp`):**
   - **100.00% line coverage** and **77.38% branch coverage**.
   - All input validation rules (names, dates, gender, age, stations, reservation IDs) and HTML display sanitization paths are thoroughly exercised.

2. **Booking Module (`src/booking.cpp`):**
   - **88.72% line coverage** and **86.84% branch coverage**.
   - Exercises route searching, train selection, seat availability validation, passenger record construction, and reservation reference generation.

3. **Data Persistence Layer (`src/data_store.cpp`):**
   - **70.59% line coverage** and **44.59% branch coverage**.
   - File loading and saving paths for trains and reservations are exercised; unhit branches correspond to filesystem access failures and file open error handlers.

4. **Cancellation & Reservation Modules (`src/cancellation.cpp`, `src/reservation.cpp`):**
   - Unhit lines in unit test coverage correspond to interactive stream prompts (`std::cin` prompts) which are exercised via interactive system CLI testing (TC-SYS-L01 through TC-SYS-C05).
