#include "data_store.h"
#include "reservation.h"
#include "cancellation.h"
#include "validation.h"
#include "booking.h"

#include <iostream>
#include <limits>

int main() {
    std::vector<Train> trains = loadTrains();
    std::vector<Reservation> reservations = loadReservations();

    if (trains.empty()) {
        std::cerr << "No train data loaded. Check data/trains.dat.\n";
        return 1;
    }

    int choice = -1;

    do {
        std::cout << "\n=== Railway Reservation System ===\n"
                  << "1. Search trains\n"
                  << "2. Book reservation\n"
                  << "3. View reservation\n"
                  << "4. Cancel reservation\n"
                  << "0. Exit\n"
                  << "Enter choice: ";

        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(
                std::numeric_limits<std::streamsize>::max(), '\n'
            );
            std::cout << "Enter a valid menu number.\n";
            continue;
        }

        std::cin.ignore(
            std::numeric_limits<std::streamsize>::max(), '\n'
        );

        switch (choice) {
            case 1:
                searchTrains(trains);
                break;

            case 2:
                bookReservation(trains, reservations);
                break;

            case 3:
                viewReservationFlow(reservations, trains);
                break;

            case 4:
                cancelReservationFlow(reservations, trains);
                break;

            case 0:
                std::cout << "Exiting Railway Reservation System.\n";
                break;

            default:
                std::cout << "Invalid choice. Try again.\n";
        }

    } while (choice != 0);

    return 0;
}
