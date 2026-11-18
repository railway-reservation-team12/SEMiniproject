#include "data_store.h"
#include "reservation.h"
#include "cancellation.h"
#include "validation.h"
#include "booking.h"

#include <iostream>
#include <limits>
#include <string>
#include <vector>
#include <fstream>
#include <utility>

std::string readLine(const std::string& prompt) {
    std::string value;
    std::cout << prompt;
    std::getline(std::cin, value);
    return value;
}

void displayTrainDetails(std::vector<Train>& trains)  {
    std::string trainId = readLine("Enter train ID: ");

    Train* train = findTrainById(trains, trainId);

    if (train == nullptr) {
        std::cout << "Train not found. Please enter a valid train ID.\n";
        return;
    }

    std::cout << "\n=== Train Details ===\n"
              << "Train ID: " << train->trainId << '\n'
              << "Train Name: " << train->trainName << '\n'
              << "Source: " << train->source << '\n'
              << "Destination: " << train->destination << '\n'
              << "Departure: " << train->departureTime << '\n'
              << "Arrival: " << train->arrivalTime << '\n'
              << "Total Seats: " << train->totalSeats << '\n'
              << "Available Seats: " << train->availableSeats << '\n';
}


void checkSeatAvailability(std::vector<Train>& trains) {
    std::string trainId = readLine("Enter train ID to check seat availability: ");
    Train* train = findTrainById(trains, trainId);

    if (train == nullptr) {
        std::cout << "Train not found. Please enter a valid train ID.\n";
        return;
    }

    std::cout << "\n=== Seat Availability ===\n"
              << "Train ID: " << train->trainId << '\n'
              << "Train Name: " << train->trainName << '\n'
              << "Total Seats: " << train->totalSeats << '\n'
              << "Available Seats: " << train->availableSeats << '\n';
}

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
          << "1. Search Train\n"
          << "2. View Train Details\n"
          << "3. Check Seat Availability\n"
          << "4. Book Ticket\n"
          << "5. View Reservation\n"
          << "6. Cancel Ticket\n"
          << "7. Exit\n"
          << "Enter menu choice (1-7): ";

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
        displayTrainDetails(trains);
        break;
    case 3:
        checkSeatAvailability(trains);
        break;
    case 4:
        bookReservation(trains, reservations);
        break;
    case 5:
        viewReservationFlow(reservations, trains);
        break;
    case 6:
        cancelReservationFlow(reservations, trains);
        break;
    case 7:
        std::cout << "Exiting Railway Reservation System.\n";
        break;
    default:
        std::cout << "Invalid choice. Try again.\n";
}
    } while (choice != 7);

    return 0;
}
