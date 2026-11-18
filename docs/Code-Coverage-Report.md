# Code Coverage Report

## 1. Environment

- Operating System: macOS
- Compiler: Apple Clang / LLVM 21.0.0
- Programming Language Standard: C++17
- Tests Executed: 76
- Execution Date: 2026-11-16

## 2. Overall Application Source Coverage

| Metric            | Covered | Total | Coverage |
| ----------------- | ------: | ----: | -------: |
| Region Coverage   |     253 |   325 |   77.85% |
| Function Coverage |      26 |    28 |   92.86% |
| Line Coverage     |     398 |   543 |   73.30% |
| Branch Coverage   |     160 |   262 |   61.07% |

## 3. Source Coverage Details

The following table presents the line coverage results for the five application source files.

| Source File      | Total Lines | Covered Lines | Missed Lines |   Coverage |
| ---------------- | ----------: | ------------: | -----------: | ---------: |
| booking.cpp      |         133 |           118 |           15 |     88.72% |
| cancellation.cpp |         101 |            57 |           44 |     56.44% |
| data_store.cpp   |         153 |           108 |           45 |     70.59% |
| reservation.cpp  |          82 |            41 |           41 |     50.00% |
| validation.cpp   |          74 |            74 |            0 |    100.00% |
| **TOTAL**        |     **543** |       **398** |      **145** | **73.30%** |

## 4. Function Coverage Details

Function coverage indicates how many application functions were executed during the test execution.

| Source File      | Total Functions | Executed Functions | Missed Functions |   Coverage |
| ---------------- | --------------: | -----------------: | ---------------: | ---------: |
| booking.cpp      |               5 |                  5 |                0 |    100.00% |
| cancellation.cpp |               3 |                  3 |                0 |    100.00% |
| data_store.cpp   |               9 |                  8 |                1 |     88.89% |
| reservation.cpp  |               4 |                  3 |                1 |     75.00% |
| validation.cpp   |               7 |                  7 |                0 |    100.00% |
| **TOTAL**        |          **28** |             **26** |            **2** | **92.86%** |

## 5. Coverage Analysis

- The application achieved an overall line coverage of 73.30%.
- Function coverage reached 92.86%, indicating that most application functions were executed.
- The validation module achieved 100.00% line coverage.
- The booking module achieved 88.72% line coverage.
- The cancellation module achieved 56.44% line coverage.
- The reservation module achieved 50.00% line coverage.
- The data storage module achieved 70.59% line coverage.

The cancellation and reservation modules have comparatively lower line coverage and should be considered for additional testing.

## 6. Coverage Generation Method

Coverage was generated using LLVM instrumentation.

The following compiler and coverage tools were used:

- `-fprofile-instr-generate`
- `-fcoverage-mapping`
- `llvm-profdata merge`
- `llvm-cov report`

Test files were excluded from the application source coverage report using:

`-ignore-filename-regex='tests/'`

The generated coverage report provided region, function, line, and branch coverage information.

## 7. Follow-up Actions

The following actions are recommended to improve code coverage:

1. Add additional test cases for uncovered cancellation functionality.
2. Improve test coverage for reservation lookup and display operations.
3. Investigate the two functions that were not executed during testing.
4. Add test cases for persistence and file-handling operations.
5. Review error-handling and fallback paths in the data storage module.
6. Re-run coverage after integrating additional test cases.

## 8. Conclusion

The Railway Reservation System achieved 73.30% line coverage and 92.86% function coverage across the five selected application source files.

The validation and booking modules demonstrated relatively strong coverage, while the cancellation and reservation modules have opportunities for improvement.

Additional testing of uncovered functionality can help improve the overall reliability and test coverage of the application.
