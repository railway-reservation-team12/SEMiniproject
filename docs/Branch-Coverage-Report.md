
# Branch Coverage Report

## 1. Environment

- Operating System: macOS
- Compiler: Apple Clang / LLVM 21.0.0
- Programming Language Standard: C++17
- Execution Date: 2026-11-16

## 2. Overall Branch Coverage Results

Branch coverage measures how many decision outcomes in the application were executed during testing.

| Metric                     | Value |
| -------------------------- | ----: |
| Total Application Branches |   262 |
| Covered Branches           |   160 |
| Missed Branches            |   102 |
| Branch Coverage            | 61.07% |

## 3. Per-File Branch Coverage Results

The following table presents the branch coverage results for the five application source files.

| Source File      | Total Branches | Covered Branches | Missed Branches | Coverage |
| ---------------- | -------------: | ---------------: | --------------: | -------: |
| booking.cpp      |             38 |               33 |               5 | 86.84% |
| cancellation.cpp |             40 |               21 |              19 | 52.50% |
| data_store.cpp   |             74 |               33 |              41 | 44.59% |
| reservation.cpp  |             26 |                8 |              18 | 30.77% |
| validation.cpp   |             84 |               65 |              19 | 77.38% |
| **TOTAL**        |        **262** |          **160** |         **102** | **61.07%** |

## 4. Branch Coverage Analysis

The overall branch coverage achieved by the Railway Reservation System is 61.07%.

The following observations can be made from the results:

- The booking module achieved 86.84% branch coverage, demonstrating relatively strong execution of its decision paths.
- The validation module achieved 77.38% branch coverage.
- The cancellation module achieved 52.50% branch coverage.
- The data storage module achieved 44.59% branch coverage.
- The reservation module achieved 30.77% branch coverage.

The reservation and data storage modules have the highest number of missed branches and should be prioritised for additional testing.

## 5. Coverage Generation Method

Branch coverage was obtained using the Branches, Missed Branches, and Cover columns produced by `llvm-cov report`.

The following LLVM tools and instrumentation options were used:

- `-fprofile-instr-generate`
- `-fcoverage-mapping`
- `llvm-profdata merge`
- `llvm-cov report`

The installed Apple LLVM version did not support the `-show-branches=count` option. The standard LLVM coverage report provided the branch totals and percentages used in this report.

## 6. Identified Coverage Gaps and Areas for Further Testing

The following areas should be considered for additional test coverage:

1. **Persistence and File-Error Paths**
   - File access and persistence-related error handling.
   - Failure scenarios during storage operations.

2. **Missing Reservation or Train Records**
   - Handling of train IDs that do not exist.
   - Handling of reservation IDs that cannot be found.

3. **Cancellation Storage Failures**
   - Error handling when reservation updates cannot be persisted.
   - Failure scenarios during cancellation operations.

4. **Reservation Display Fallback Paths**
   - Alternative execution paths when reservation details are unavailable.
   - Handling of missing or incomplete reservation information.

5. **Validation Branches**
   - Less-common invalid input conditions.
   - Boundary and exceptional validation scenarios.

These are areas for further investigation; the exact uncovered branch conditions require detailed branch-level coverage output.

## 7. Recommended Follow-up Actions

1. Add test cases for missing train and reservation records.
2. Test invalid reservation IDs and invalid user inputs.
3. Test already-cancelled reservation scenarios.
4. Add tests for storage and file-operation failures.
5. Test user-declined cancellation scenarios.
6. Verify successful booking and cancellation execution paths.
7. Coordinate with the test-case owner when additional test cases are required.
8. Re-run branch coverage after integrating additional tests and compare the results.

## 8. Conclusion

The Railway Reservation System achieved an overall branch coverage of 61.07%, with 160 out of 262 application branches covered.

The booking module achieved the highest branch coverage at 86.84%, while the reservation module had the lowest branch coverage at 30.77%.

Additional test cases should focus on reservation handling, data storage, cancellation error handling, and less-common validation conditions to improve branch coverage and strengthen the reliability of the application.
