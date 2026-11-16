# System Validation Report

## Scope

Validation of the Railway Reservation System workflows against the SRS and Test Plan.

## Automated Validation Evidence

| Workflow | Evidence | Result |
|---|---|---|
| Train search by source and destination | `test_train_search` | Passed |
| Invalid search input | `test_train_search` | Passed |
| Ticket booking | `test_booking` | Passed |
| Booking with unavailable seats | `test_booking` | Passed |
| Unique reservation references | `test_booking` | Passed |
| Reservation lookup | `test_cancellation` | Passed |
| Successful cancellation | `test_cancellation` | Passed |
| Repeated cancellation rejection | `test_cancellation` | Passed |
| Invalid reservation identifiers | `test_cancellation` | Passed |
| Cancellation declined with `N` | `test_cancellation` | Passed |

## Results

- Automated tests executed: 76
- Passed: 76
- Failed: 0

## Manual or Pending Validation

1. Confirmed cancellation using `Y` should be validated manually using safe test data.
2. Journey-date filtering is not validated because the current search function does not accept a date.
3. Same-operation retry behavior is not fully validated.
4. Usability review remains pending.
5. Full portability validation requires CI results on both supported platforms.

## Conclusion

The tested workflows passed. The limitations above must be recorded as partial, pending, or blocked rather than reported as fully validated.
