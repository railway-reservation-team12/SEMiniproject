#include "booking.h"
#include "models.h"
#include "data_store.h"
#include "validation.h"

#include <cstdio>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class CinRedirect {
private:
    std::istringstream input;
    std::streambuf* oldBuffer;

public:
    explicit CinRedirect(const std::string& text)
        : input(text),
          oldBuffer(std::cin.rdbuf(input.rdbuf())) {}

    ~CinRedirect() {
        std::cin.rdbuf(oldBuffer);
    }
};

int main() {
    int passed = 0;
    int failed = 0;

    auto check = [&](bool condition, const std::string& name) {
        if (condition) {
            std::cout << "[PASS] " << name << '\n';
            ++passed;
        } else {
            std::cout << "[FAIL] " << name << '\n';
            ++failed;
        }
    };

    const std::string trainFile = "build/test_trains.dat";
    const std::string reservationFile =
"build/test_reservations.dat";

    std::vector<Train> trains = {
        {
            "T001",
            "Bangalore Express",
            "Bengaluru",
            "Chennai",
            "06:00",
            "12:00",
            100,
            50
        }
    };

    std::vector<Reservation> reservations;

    std::cout << "\n--- Booking Tests ---\n";

    // ------------------------------------------------------------
    // BK-01 to BK-09: Valid booking
    // ------------------------------------------------------------
    {
        CinRedirect input(
            "T001\n"
            "Alice Johnson\n"
            "25\n"
            "F\n"
            "25-12-2026\n"
            "2\n"
        );

        bool result = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            result,
            "BK-01: Valid booking succeeds"
        );

        check(
            reservations.size() == 1,
            "BK-02: Reservation is added"
        );

        if (!reservations.empty()) {
            check(
                reservations[0].reservationId == "RES001",
                "BK-03: Reservation ID generated correctly"
            );

            check(
                reservations[0].trainId == "T001",
                "BK-04: Correct train ID stored"
            );

            check(
                reservations[0].passengerName == "Alice Johnson",
                "BK-05: Passenger name stored correctly"
            );

            check(
                reservations[0].passengerAge == 25,
                "BK-06: Passenger age stored correctly"
            );

            check(
                reservations[0].seatsBooked == 2,
                "BK-07: Seat count stored correctly"
            );

            check(
                reservations[0].status == STATUS_CONFIRMED,
                "BK-08: New reservation is confirmed"
            );
        } else {
            check(
                false,
                "BK-03: Reservation ID generated correctly"
            );

            check(
                false,
                "BK-04: Correct train ID stored"
            );

            check(
                false,
                "BK-05: Passenger name stored correctly"
            );

            check(
                false,
                "BK-06: Passenger age stored correctly"
            );

            check(
                false,
                "BK-07: Seat count stored correctly"
            );

            check(
                false,
                "BK-08: New reservation is confirmed"
            );
        }

        check(
            trains[0].availableSeats == 48,
            "BK-09: Available seats decrease correctly"
        );
    }

    // ------------------------------------------------------------
    // BK-10 to BK-12: Non-existent train
    // ------------------------------------------------------------
    {
        const size_t sizeBefore = reservations.size();
        const int seatsBefore = trains[0].availableSeats;

        CinRedirect input(
            "T999\n"
            "Bob Smith\n"
            "30\n"
            "M\n"
            "26-12-2026\n"
            "1\n"
        );

        bool result = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            !result,
            "BK-10: Non-existent train is rejected"
        );

        check(
            reservations.size() == sizeBefore,
            "BK-11: Reservation list unchanged after rejected booking"
        );

        check(
            trains[0].availableSeats == seatsBefore,
            "BK-12: Seat count unchanged after rejected booking"
        );
    }

    // ------------------------------------------------------------
    // BK-13 to BK-15: Invalid passenger name
    // ------------------------------------------------------------
    {
        const size_t sizeBefore = reservations.size();
        const int seatsBefore = trains[0].availableSeats;

        CinRedirect input(
            "T001\n"
            "Invalid@Name\n"
            "30\n"
            "M\n"
            "26-12-2026\n"
            "1\n"
        );

        bool result = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            !result,
            "BK-13: Invalid passenger name is rejected"
        );

        check(
            reservations.size() == sizeBefore,
            "BK-14: Reservation list unchanged after invalid name"
        );

        check(
            trains[0].availableSeats == seatsBefore,
            "BK-15: Seat count unchanged after invalid name"
        );
    }

    // ------------------------------------------------------------
    // BK-16 to BK-18: Too many seats
    // ------------------------------------------------------------
    {
        const size_t sizeBefore = reservations.size();
        const int seatsBefore = trains[0].availableSeats;

        CinRedirect input(
            "T001\n"
            "Charlie Brown\n"
            "25\n"
            "M\n"
            "26-12-2026\n"
            "100\n"
        );

        bool result = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            !result,
            "BK-16: Booking more seats than available is rejected"
        );

        check(
            reservations.size() == sizeBefore,
            "BK-17: Reservation list unchanged when seats unavailable"
        );

        check(
            trains[0].availableSeats == seatsBefore,
            "BK-18: Seat count unchanged when seats unavailable"
        );
    }

    // ------------------------------------------------------------
    // BK-19 to BK-21: Invalid journey date
    // ------------------------------------------------------------
    {
        const size_t sizeBefore = reservations.size();
        const int seatsBefore = trains[0].availableSeats;

        CinRedirect input(
            "T001\n"
            "David Kumar\n"
            "25\n"
            "M\n"
            "invalid-date\n"
            "1\n"
        );

        bool result = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            !result,
            "BK-19: Invalid journey date is rejected"
        );

        check(
            reservations.size() == sizeBefore,
            "BK-20: Reservation list unchanged after invalid date"
        );

        check(
            trains[0].availableSeats == seatsBefore,
            "BK-21: Seat count unchanged after invalid date"
        );
    }

    // ------------------------------------------------------------
    // TC-004 / TC-012: Unique reservation references and restart
    // ------------------------------------------------------------
    {
        CinRedirect input(
            "T001\n"
            "Second Passenger\n"
            "30\n"
            "M\n"
            "27-12-2026\n"
            "1\n"
        );

        bool secondBooking = bookReservation(
            trains,
            reservations,
            trainFile,
            reservationFile
        );

        check(
            secondBooking,
            "TC-004: Second booking succeeds"
        );

        check(
            reservations.size() == 2,
            "TC-004: Two successful bookings are stored"
        );

        if (reservations.size() >= 2) {
            const std::string& firstId = reservations[0].reservationId;
            const std::string& secondId = reservations[1].reservationId;

            check(
                firstId != secondId,
                "TC-004: Successful bookings receive unique reservation references"
            );

            check(
                isValidReservationId(firstId) &&
                isValidReservationId(secondId) &&
                firstId.length() <= 20 &&
                secondId.length() <= 20,
                "TC-004: Reservation references satisfy the 20-character format"
            );

            std::cout << "Evidence: Booking 1 reference = "
                      << firstId << '\n';

            std::cout << "Evidence: Booking 2 reference = "
                      << secondId << '\n';
        }

        // Simulate program restart by reloading persisted reservations.
        std::vector<Reservation> reloadedReservations =
            loadReservations(reservationFile);

        check(
            reloadedReservations.size() == 2,
            "TC-012: Reservations persist across program restart"
        );

        if (reloadedReservations.size() >= 2) {
            reservations = reloadedReservations;

            CinRedirect inputAfterRestart(
                "T001\n"
                "Third Passenger\n"
                "28\n"
                "F\n"
                "28-12-2026\n"
                "1\n"
            );

            bool thirdBooking = bookReservation(
                trains,
                reservations,
                trainFile,
                reservationFile
            );

            check(
                thirdBooking,
                "TC-012: Booking succeeds after program restart"
            );

            check(
                reservations.size() == 3,
                "TC-012: Third booking is stored after restart"
            );

            if (reservations.size() == 3) {
                const std::string& firstId =
                    reservations[0].reservationId;

                const std::string& secondId =
                    reservations[1].reservationId;

                const std::string& thirdId =
                    reservations[2].reservationId;

                check(
                    thirdId != firstId &&
                    thirdId != secondId,
                    "TC-012: Post-restart reservation reference remains unique"
                );

                check(
                    isValidReservationId(thirdId) &&
                    thirdId.length() <= 20,
                    "TC-012: Post-restart reference satisfies the 20-character format"
                );

                std::cout << "Evidence: Reloaded references = "
                          << firstId << ", "
                          << secondId << '\n';

                std::cout << "Evidence: Post-restart booking reference = "
                          << thirdId << '\n';
            }
        }
    }

    // Clean up temporary test files.
    std::remove(trainFile.c_str());
    std::remove(reservationFile.c_str());

    // ------------------------------------------------------------
    // Summary
    // ------------------------------------------------------------

    std::cout << "\n========================================\n";
    std::cout << "BOOKING TEST SUMMARY\n";
    std::cout << "========================================\n";
    std::cout << "Total:  " << passed + failed << '\n';
    std::cout << "Passed: " << passed << '\n';
    std::cout << "Failed: " << failed << '\n';

    if (failed == 0) {
        std::cout << "RESULT: ALL BOOKING TESTS PASSED\n";
        return 0;
    }

    std::cout << "RESULT: BOOKING TESTS FAILED\n";
    return 1;
}
