#include "reservation.h"
#include "validation.h"
#include "data_store.h"
#include <iostream>
#include <iomanip>
#include <string>

std::string getStatusString(ReservationStatus status) {
    switch (status) {
        case STATUS_CONFIRMED: return "Confirmed";
        case STATUS_CANCELLED: return "Cancelled";
        default: return "Unknown";
    }
}

LookupResult lookupReservation(const std::string& reservationId,
                                std::vector<Reservation>& reservations,
                                Reservation& outReservation) {
    if (!isValidReservationId(reservationId)) {
        return LOOKUP_INVALID_ID;
    }
    Reservation* found = findReservationById(reservations, reservationId);
    if (found == nullptr) {
        return LOOKUP_NOT_FOUND;
    }
    outReservation = *found;
    return LOOKUP_SUCCESS;
}

void displayReservation(const Reservation& reservation,
                        const std::vector<Train>& trains) {
    std::cout << std::endl;
    std::cout << "╔══════════════════════════════════════════════╗" << std::endl;
    std::cout << "║          RESERVATION DETAILS                 ║" << std::endl;
    std::cout << "╠══════════════════════════════════════════════╣" << std::endl;
    std::cout << "║  Reservation ID  : " << std::setw(25) << std::left << reservation.reservationId << "║" << std::endl;

    // Look up the matching train to display route and schedule info
    bool trainFound = false;
    for (const auto& train : trains) {
        if (train.trainId == reservation.trainId) {
            std::string trainDisplay = train.trainId + " - " + train.trainName;
            std::cout << "║  Train           : " << std::setw(25) << std::left << trainDisplay << "║" << std::endl;
            std::cout << "║  Route           : " << std::setw(25) << std::left
                      << (train.source + " → " + train.destination) << "║" << std::endl;
            std::cout << "║  Departure       : " << std::setw(25) << std::left << train.departureTime << "║" << std::endl;
            std::cout << "║  Arrival         : " << std::setw(25) << std::left << train.arrivalTime << "║" << std::endl;
            trainFound = true;
            break;
        }
    }
    // Fallback: show just the train ID if no matching train record exists
    if (!trainFound) {
        std::cout << "║  Train           : " << std::setw(25) << std::left << reservation.trainId << "║" << std::endl;
    }

    std::cout << "║  Passenger Name  : " << std::setw(25) << std::left << reservation.passengerName << "║" << std::endl;
    std::cout << "║  Age             : " << std::setw(25) << std::left << reservation.passengerAge << "║" << std::endl;
    std::cout << "║  Gender          : " << std::setw(25) << std::left << reservation.passengerGender << "║" << std::endl;
    std::cout << "║  Journey Date    : " << std::setw(25) << std::left << reservation.journeyDate << "║" << std::endl;
    std::cout << "║  Seats Booked    : " << std::setw(25) << std::left << reservation.seatsBooked << "║" << std::endl;
    std::string statusStr = getStatusString(reservation.status);
    std::cout << "║  Status          : " << std::setw(25) << std::left << statusStr << "║" << std::endl;
    std::cout << "╚══════════════════════════════════════════════╝" << std::endl;
}

bool viewReservationFlow(std::vector<Reservation>& reservations,
                         const std::vector<Train>& trains) {
    std::string reservationId;
    std::cout << std::endl;
    std::cout << "═══════ VIEW RESERVATION ═══════" << std::endl;
    std::cout << "Enter Reservation ID (e.g., RES001): ";
    std::getline(std::cin, reservationId);

    // Trim leading/trailing whitespace
    size_t start = reservationId.find_first_not_of(" \t\r\n");
    size_t end   = reservationId.find_last_not_of(" \t\r\n");
    reservationId = (start != std::string::npos)
                    ? reservationId.substr(start, end - start + 1)
                    : "";

    Reservation result;
    LookupResult lookupResult = lookupReservation(reservationId, reservations, result);
    switch (lookupResult) {
        case LOOKUP_SUCCESS:
            displayReservation(result, trains);
            return true;
        case LOOKUP_INVALID_ID:
            std::cout << std::endl;
            std::cout << "[Error] Invalid reservation ID format." << std::endl;
            std::cout << "        Reservation IDs follow the format: RESxxx (e.g., RES001)" << std::endl;
            return false;
        case LOOKUP_NOT_FOUND:
            std::cout << std::endl;
            std::cout << "[Error] Reservation not found." << std::endl;
            std::cout << "        Please verify your reservation ID and try again." << std::endl;
            return false;
        default:
            std::cout << std::endl;
            std::cout << "[Error] An unexpected error occurred. Please try again." << std::endl;
            return false;
    }
}