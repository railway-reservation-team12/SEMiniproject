# Code Coverage Report

## 1. Environment

- Operating Systems: Windows 11 / macOS / Ubuntu Linux (CI)
- Compiler: Apple Clang / LLVM 21.0.0 / GCC 13.x
- Programming Language Standard: C++17
- Tests Executed: 76 automated unit tests
- Execution Dates: 2026-11-16 to 2026-11-19

## 2. Overall Application Source Coverage

| Metric            | Covered | Total | Coverage |
| ----------------- | ------: | ----: | -------: |
| Region Coverage   |     253 |   325 |   77.85% |
| Function Coverage |      26 |    28 |   92.86% |
| Line Coverage     |     398 |   543 |   73.30% |
| Branch Coverage   |     160 |   262 |   61.07% |

## 3. Line & Branch Coverage Details

The following table presents the line and branch coverage results for the five application source files:

| Source File      | Total Lines | Covered Lines | Missed Lines | Line Coverage | Branch Coverage | Functions Executed |
| ---------------- | ----------: | ------------: | -----------: | ------------: | --------------: | -----------------: |
| booking.cpp      |         133 |           118 |           15 |        88.72% |          86.84% |            100.00% |
| cancellation.cpp |         101 |            57 |           44 |        56.44% |          52.50% |            100.00% |
| data_store.cpp   |         153 |           108 |           45 |        70.59% |          44.59% |             88.89% |
| reservation.cpp  |          82 |            41 |           41 |        50.00% |          30.77% |             75.00% |
| validation.cpp   |          74 |            74 |            0 |       100.00% |          77.38% |            100.00% |
| **TOTAL**        |     **543** |       **398** |      **145** |    **73.30%** |      **61.07%** |         **92.86%** |

## 4. Function Coverage Details

Function coverage indicates how many application functions were executed during the test execution:

| Source File      | Total Functions | Executed Functions | Missed Functions |   Coverage |
| ---------------- | --------------: | -----------------: | ---------------: | ---------: |
| booking.cpp      |               5 |                  5 |                0 |    100.00% |
| cancellation.cpp |               3 |                  3 |                0 |    100.00% |
| data_store.cpp   |               9 |                  8 |                1 |     88.89% |
| reservation.cpp  |               4 |                  3 |                1 |     75.00% |
| validation.cpp   |               7 |                  7 |                0 |    100.00% |
| **TOTAL**        |          **28** |             **26** |            **2** | **92.86%** |

## 5. Coverage Analysis & Insights

1. **Validation Engine (`src/validation.cpp`):**
   - Achieved **100.00% line coverage** and **77.38% branch coverage**.
   - All input validation rules (passenger names, journey dates, gender, age, station routes, reservation IDs) and HTML display sanitization paths are thoroughly exercised.

2. **Booking Module (`src/booking.cpp`):**
   - Achieved **88.72% line coverage** and **86.84% branch coverage**.
   - Fully covers route search, train selection, seat availability verification, passenger record construction, and reservation reference generation.

3. **Data Persistence Layer (`src/data_store.cpp`):**
   - Achieved **70.59% line coverage** and **44.59% branch coverage**.
   - File loading and saving paths for trains and reservations are exercised; unhit branches correspond to filesystem access failures and file open error handlers.

4. **Cancellation & Reservation Modules (`src/cancellation.cpp`, `src/reservation.cpp`):**
   - Achieved **56.44%** and **50.00%** line coverage in automated unit testing.
   - Unhit lines in unit test coverage primarily correspond to interactive stream prompts (`std::cin` prompts) and defensive fallback paths. These interactive flows were fully exercised and verified via interactive system CLI testing (TC-SYS-L01 through TC-SYS-C05 in `docs/System-Validation-Report.md`).

## 6. Coverage Generation Method

Coverage was generated using LLVM instrumentation with the following options:

- `-fprofile-instr-generate`
- `-fcoverage-mapping`
- `llvm-profdata merge`
- `llvm-cov report`

Test files were excluded from the application source coverage report using:

```text
-ignore-filename-regex='tests/'
```

The generated coverage report provided region, function, line, and branch coverage information.

## 7. Quality Findings & Next Steps

1. Add mock-safe parameterized test cases for uncovered cancellation error paths (`DEF-001`).
2. Improve unit test coverage for reservation lookup and display operations without interactive stream dependence.
3. Review error-handling and filesystem fallback paths in the data storage module.
4. Continue leveraging interactive system testing for interactive menu prompts.

## 8. Conclusion

The Railway Reservation System achieved **73.30% line coverage** and **92.86% function coverage** across all application source files, with **100% line coverage** on core validation logic.

All 76 automated test assertions pass without failure, and the remaining interactive paths are validated through interactive CLI system execution.
