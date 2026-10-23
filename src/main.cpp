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

std::string lowerCase(std::string value) {
    std::transform(value.begin(), value.end(), value.begin(),
        [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    return value;
}


bool searchTrains(const std::vector<Train>& trains) {
    std::string source = readLine("Enter source station: ");
    std::string destination = readLine("Enter destination station: ");
    std::string date = readLine("Journey date (DD-MM-YYYY): ");

    if (!isValidStation(source) || !isValidStation(destination)) {
        std::cout << "Invalid station name.\n";
        return false;
    }

    if (!isValidDate(date)) {
        std::cout << "Invalid journey date. Use DD-MM-YYYY.\n";
        return false;
    }

    // Read the available train schedules.
    std::vector<std::pair<std::string, std::string>> schedules;
    std::ifstream scheduleFile("data/schedules.dat");
    if (!scheduleFile) {
        std::cout << "Could not open data/schedules.dat.\n";
        return false;
    }

    std::string line;
    while (std::getline(scheduleFile, line)) {
        if (line.empty() || line[0] == '#') {
            continue;
        }

        std::size_t separator = line.find('|');
        if (separator == std::string::npos) {
            continue;
        }

        std::string trainId = line.substr(0, separator);
        std::string journeyDate = line.substr(separator + 1);

        schedules.push_back({trainId, journeyDate});
    }

    source = lowerCase(source);
    destination = lowerCase(destination);
    bool found = false;

    std::cout << "\nMatching trains for " << date << ":\n";

    for (const auto& train : trains) {
        bool routeMatches =
            lowerCase(train.source) == source &&
            lowerCase(train.destination) == destination;

        bool dateMatches = false;
        for (const auto& schedule : schedules) {
            if (schedule.first == train.trainId &&
                schedule.second == date) {
                dateMatches = true;
                break;
            }
        }

        if (routeMatches && dateMatches) {
            std::cout << train.trainId << " | " << train.trainName
                      << " | " << train.source << " -> "
                      << train.destination
                      << " | Departure: " << train.departureTime
                      << " | Arrival: " << train.arrivalTime
                      << " | Available seats: " << train.availableSeats
                      << '\n';
            found = true;
        }
    }

    if (!found) {
        std::cout << "No trains found for that route and journey date.\n";
    }

    return found;
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


void bookReservation(std::vector<Train>& trains,
                     std::vector<Reservation>& reservations) {
    if (reservations.size() >= MAX_RESERVATIONS) {
        std::cout << "Reservation capacity reached.\n";
        return;
    }

    std::string trainId = readLine("Enter train ID: ");
    Train* train = findTrainById(trains, trainId);

    if (train == nullptr) {
        std::cout << "Train not found.\n";
        return;
    }

    std::string name = readLine("Passenger name: ");
    if (!isValidPassengerName(name)) {
        std::cout << "Invalid passenger name.\n";
        return;
    }

    std::string ageText = readLine("Passenger age: ");
    int age = 0;
    try {
        size_t used = 0;
        age = std::stoi(ageText, &used);
        if (used != ageText.size() || !isValidAge(age)) {
            std::cout << "Invalid age.\n";
            return;
        }
    } catch (...) {
        std::cout << "Invalid age.\n";
        return;
    }

    std::string gender = readLine("Passenger gender: ");
    if (!isValidGender(gender)) {
        std::cout << "Invalid gender value.\n";
        return;
    }

    std::string date = readLine("Journey date (DD-MM-YYYY): ");
    if (!isValidDate(date)) {
        std::cout << "Invalid journey date.\n";
        return;
    }

    std::string seatsText = readLine("Number of seats: ");
    int seats = 0;
    try {
        size_t used = 0;
        seats = std::stoi(seatsText, &used);
        if (used != seatsText.size() || seats <= 0) {
            std::cout << "Seat count must be a positive number.\n";
            return;
        }
    } catch (...) {
        std::cout << "Invalid seat count.\n";
        return;
    }

    if (seats > train->availableSeats) {
        std::cout << "Not enough seats available. Available: "
                  << train->availableSeats << '\n';
        return;
    }

    Reservation reservation;
    reservation.reservationId = generateReservationId(reservations);
    reservation.trainId = train->trainId;
    reservation.passengerName = name;
    reservation.passengerAge = age;
    reservation.passengerGender = gender;
    reservation.journeyDate = date;
    reservation.seatsBooked = seats;
    reservation.status = STATUS_CONFIRMED;

    const int previousSeats = train->availableSeats;
    train->availableSeats -= seats;
    reservations.push_back(reservation);

    if (!saveReservations(reservations) || !saveTrains(trains)) {
        reservations.pop_back();
        train->availableSeats = previousSeats;
        std::cout << "Could not save booking. Please check file permissions "
                     "and restore data from backup if necessary.\n";
        return;
    }

    std::cout << "\nBooking successful!\n";
    std::cout << "Reservation ID: " << reservation.reservationId << '\n';
    std::cout << "Train: " << train->trainName << '\n';
    std::cout << "Seats booked: " << seats << '\n';
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
          << "1. Search trains\n"
          << "2. Book reservation\n"
          << "3. View reservation\n"
          << "4. Cancel reservation\n"
          << "5. Display train details\n"
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

    case 5:
        displayTrainDetails(trains);
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
