// ============================================================================
// Cancellation Module Test Suite
// Tests for reservation lookup and ticket cancellation.
// Covers: TC-C01 through TC-C10 from the Test Plan
//
// Maps to: FR-019–FR-039, SEC-001–SEC-005, NFR-001, NFR-003, NFR-006, NFR-009
// ============================================================================

#include "../src/models.h"
#include "../src/data_store.h"
#include "../src/validation.h"
#include "../src/reservation.h"
#include "../src/cancellation.h"
#include <iostream>
#include <cassert>
#include <string>
#include <vector>
#include <chrono>
#include <sstream>

// Test counters
static int testsRun = 0;
static int testsPassed = 0;
static int testsFailed = 0;

// Helper: create test data in memory (no file dependency)
static void createTestData(std::vector<Train>& trains, std::vector<Reservation>& reservations) {
    trains.clear();
    reservations.clear();

    // Add sample trains
    Train t1 = {"T001", "Shatabdi Express", "Bangalore", "Chennai", "06:00", "11:00", 120, 115};
    Train t2 = {"T002", "Rajdhani Express", "Bangalore", "Delhi", "15:30", "07:00", 200, 198};
    trains.push_back(t1);
    trains.push_back(t2);

    // Add sample reservations
    Reservation r1 = {"RES001", "T001", "Rahul Sharma", 28, "M", "25-10-2026", 2, STATUS_CONFIRMED};
    Reservation r2 = {"RES002", "T002", "Priya Nair", 35, "F", "26-10-2026", 1, STATUS_CONFIRMED};
    Reservation r3 = {"RES003", "T001", "Vikram Singh", 30, "M", "25-10-2026", 3, STATUS_CANCELLED};
    reservations.push_back(r1);
    reservations.push_back(r2);
    reservations.push_back(r3);
}

class CinRedirect {
private:
    std::istringstream input;
    std::streambuf* oldBuffer;

public:
    explicit CinRedirect(const std::string& text)
        : input(text), oldBuffer(std::cin.rdbuf(input.rdbuf())) {}

    ~CinRedirect() {
        std::cin.rdbuf(oldBuffer);
    }
};

// Helper: report test result
static void reportTest(const std::string& testId, const std::string& description, bool passed) {
    testsRun++;
    if (passed) {
        testsPassed++;
        std::cout << "  [PASS] " << testId << ": " << description << std::endl;
    } else {
        testsFailed++;
        std::cout << "  [FAIL] " << testId << ": " << description << std::endl;
    }
}

// ============================================================================
// TC-C01: Successful cancellation
// FR-024–FR-030, FR-033
// ============================================================================
void testSuccessfulCancellation() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    int seatsBefore = trains[0].availableSeats; // T001: 115

    CancelResult result = processCancellation("RES001", reservations, trains);

    bool passed = (result == CANCEL_SUCCESS);
    reportTest("TC-C01a", "processCancellation returns CANCEL_SUCCESS", passed);

    // Verify status changed to CANCELLED (FR-029)
    Reservation* res = findReservationById(reservations, "RES001");
    passed = (res != nullptr && res->status == STATUS_CANCELLED);
    reportTest("TC-C01b", "Reservation status changed to CANCELLED", passed);

    // Verify seats were restored (FR-030)
    int seatsAfter = trains[0].availableSeats;
    passed = (seatsAfter == seatsBefore + 2); // RES001 had 2 seats
    reportTest("TC-C01c", "Available seats incremented by seats released", passed);
}

// ============================================================================
// TC-C02: Cancel already cancelled reservation
// FR-032, BR-005
// ============================================================================
void testAlreadyCancelled() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    // RES003 is already STATUS_CANCELLED
    CancelResult result = processCancellation("RES003", reservations, trains);

    bool passed = (result == CANCEL_ALREADY_CANCELLED);
    reportTest("TC-C02", "Already-cancelled reservation rejected", passed);
}

// ============================================================================
// TC-C03: Invalid (non-existent) reservation ID
// FR-031, FR-034, SEC-002
// ============================================================================
void testNonExistentId() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    CancelResult result = processCancellation("RES999", reservations, trains);

    bool passed = (result == CANCEL_NOT_FOUND);
    reportTest("TC-C03", "Non-existent reservation ID returns NOT_FOUND", passed);
}

// ============================================================================
// TC-C04: Empty reservation ID
// FR-036, FR-038
// ============================================================================
void testEmptyId() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    CancelResult result = processCancellation("", reservations, trains);

    bool passed = (result == CANCEL_INVALID_ID);
    reportTest("TC-C04", "Empty reservation ID returns INVALID_ID", passed);
}

// ============================================================================
// TC-C05: Seat restoration verified
// FR-030, BR-006, NFR-006
// ============================================================================
void testSeatRestoration() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    // Before cancellation: T002 has 198 available, RES002 has 1 seat on T002
    int seatsBefore = trains[1].availableSeats; // 198

    processCancellation("RES002", reservations, trains);

    int seatsAfter = trains[1].availableSeats;
    bool passed = (seatsAfter == seatsBefore + 1);
    reportTest("TC-C05", "Seat count correctly restored after cancellation", passed);
}

// ============================================================================
// TC-C06: User declines cancellation (tested via processCancellation logic)
// FR-028 — Note: interactive confirmation tested via cancelReservationFlow
// ============================================================================
void testNoDataChangeOnError() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    int seatsBefore = trains[0].availableSeats;
    ReservationStatus statusBefore = reservations[2].status; // RES003 already cancelled

    // Try to cancel already-cancelled reservation
    processCancellation("RES003", reservations, trains);

    bool passed = (trains[0].availableSeats == seatsBefore);
    reportTest("TC-C06a", "Seat count unchanged on rejected cancellation", passed);

    passed = (reservations[2].status == statusBefore);
    reportTest("TC-C06b", "Reservation status unchanged on rejected cancellation", passed);
}

// ============================================================================
// TC-C07: Malformed input
// FR-039, NFR-009, SEC-004
// ============================================================================
void testMalformedInput() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    // Test various malformed inputs
    CancelResult r1 = processCancellation("!@#$%^", reservations, trains);
    bool passed = (r1 == CANCEL_INVALID_ID);
    reportTest("TC-C07a", "Special characters rejected as INVALID_ID", passed);

    CancelResult r2 = processCancellation("RESABCDEF", reservations, trains);
    passed = (r2 == CANCEL_INVALID_ID);
    reportTest("TC-C07b", "Non-numeric suffix rejected as INVALID_ID", passed);

    // Very long input
    std::string longId = "RES" + std::string(100, '1');
    CancelResult r3 = processCancellation(longId, reservations, trains);
    passed = (r3 == CANCEL_INVALID_ID);
    reportTest("TC-C07c", "Overflow-length input rejected as INVALID_ID", passed);

    // Verify no data was modified (SEC-004)
    passed = (reservations[0].status == STATUS_CONFIRMED);
    reportTest("TC-C07d", "No reservation data modified by invalid input (SEC-004)", passed);
}

// ============================================================================
// TC-C08: Lookup displays correct info
// FR-021, FR-023
// ============================================================================
void testLookupCorrectInfo() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    Reservation result;
    LookupResult lookupResult = lookupReservation("RES001", reservations, result);

    bool passed = (lookupResult == LOOKUP_SUCCESS);
    reportTest("TC-C08a", "Lookup returns SUCCESS for valid ID", passed);

    passed = (result.reservationId == "RES001" &&
              result.trainId == "T001" &&
              result.passengerName == "Rahul Sharma" &&
              result.passengerAge == 28 &&
              result.seatsBooked == 2 &&
              result.status == STATUS_CONFIRMED);
    reportTest("TC-C08b", "All reservation fields correctly populated", passed);
}

// ============================================================================
// TC-C09: Error message safety
// SEC-003 — validated via sanitizeForDisplay function
// ============================================================================
void testErrorMessageSafety() {
    std::string sensitive = "Password<script>123";
    std::string sanitized = sanitizeForDisplay(sensitive, 20);

    // Should not contain angle brackets or script tags
    bool passed = (sanitized.find('<') == std::string::npos &&
                   sanitized.find('>') == std::string::npos);
    reportTest("TC-C09a", "Sanitized output contains no special HTML chars", passed);

    // Test truncation for long inputs
    std::string longInput(50, 'A');
    std::string truncated = sanitizeForDisplay(longInput, 10);
    passed = (truncated.length() <= 13); // 10 chars + "..."
    reportTest("TC-C09b", "Long input truncated in error messages", passed);
}

// ============================================================================
// TC-C10: Performance — cancellation under 2 seconds
// NFR-001, NFR-002
// ============================================================================
void testPerformance() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    auto start = std::chrono::high_resolution_clock::now();

    processCancellation("RES001", reservations, trains);

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    bool passed = (duration.count() < 2000); // Must be under 2 seconds
    reportTest("TC-C10", "Cancellation completes in < 2 seconds (took "
               + std::to_string(duration.count()) + "ms)", passed);
}

// ============================================================================
// Validation function tests
// FR-035, FR-036, SEC-001
// ============================================================================

void testInteractiveCancellationDeclined() {
    std::vector<Train> trains;
    std::vector<Reservation> reservations;
    createTestData(trains, reservations);

    const int seatsBefore = trains[0].availableSeats;

    CinRedirect input("RES001\nN\n");

    CancelResult result =
        cancelReservationFlow(reservations, trains);

    Reservation* reservation =
        findReservationById(reservations, "RES001");

    reportTest(
        "TC-C11a",
        "User-declined cancellation is rejected",
        result == CANCEL_USER_DECLINED
    );

    reportTest(
        "TC-C11b",
        "Declined cancellation leaves reservation active",
        reservation != nullptr &&
        reservation->status == STATUS_CONFIRMED
    );

    reportTest(
        "TC-C11c",
        "Declined cancellation does not change seats",
        trains[0].availableSeats == seatsBefore
    );
}


void testValidation() {
    // Valid IDs
    bool passed = isValidReservationId("RES001");
    reportTest("VAL-01", "Valid reservation ID accepted", passed);

    passed = isValidReservationId("RES999");
    reportTest("VAL-02", "Valid reservation ID (large number) accepted", passed);

    // Invalid IDs
    passed = !isValidReservationId("");
    reportTest("VAL-03", "Empty ID rejected", passed);

    passed = !isValidReservationId("ABC123");
    reportTest("VAL-04", "Wrong prefix rejected", passed);

    passed = !isValidReservationId("RES");
    reportTest("VAL-05", "Prefix-only rejected", passed);

    passed = !isValidReservationId("RESABC");
    reportTest("VAL-06", "Non-numeric suffix rejected", passed);

    passed = !isValidReservationId("res001");
    reportTest("VAL-07", "Lowercase prefix rejected", passed);
}

// ============================================================================
// Main test runner
// ============================================================================
int main() {
    std::cout << std::endl;
    std::cout << "══════════════════════════════════════════════════" << std::endl;
    std::cout << "  Railway Reservation System — Cancellation Tests " << std::endl;
    std::cout << "══════════════════════════════════════════════════" << std::endl;
    std::cout << std::endl;

    std::cout << "--- Cancellation Tests ---" << std::endl;
    testSuccessfulCancellation();
    testAlreadyCancelled();
    testNonExistentId();
    testEmptyId();
    testSeatRestoration();
    testNoDataChangeOnError();
    testMalformedInput();

    std::cout << std::endl;
    std::cout << "--- Lookup Tests ---" << std::endl;
    testLookupCorrectInfo();

    std::cout << std::endl;
    std::cout << "--- Security Tests ---" << std::endl;
    testErrorMessageSafety();

    std::cout << std::endl;
    std::cout << "--- Performance Tests ---" << std::endl;
    testPerformance();

    std::cout << std::endl;
    std::cout << "--- Validation Tests ---" << std::endl;
    testInteractiveCancellationDeclined();
    testValidation();

    // Summary
    std::cout << std::endl;
    std::cout << "══════════════════════════════════════════════════" << std::endl;
    std::cout << "  TEST SUMMARY" << std::endl;
    std::cout << "══════════════════════════════════════════════════" << std::endl;
    std::cout << "  Total:  " << testsRun << std::endl;
    std::cout << "  Passed: " << testsPassed << std::endl;
    std::cout << "  Failed: " << testsFailed << std::endl;
    std::cout << "══════════════════════════════════════════════════" << std::endl;

    if (testsFailed > 0) {
        std::cout << "  RESULT: SOME TESTS FAILED" << std::endl;
        return 1;
    } else {
        std::cout << "  RESULT: ALL TESTS PASSED" << std::endl;
        return 0;
    }
}
