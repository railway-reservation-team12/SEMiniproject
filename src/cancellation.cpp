#include "cancellation.h"
#include "reservation.h"
#include "validation.h"
#include "data_store.h"
#include <iostream>
#include <iomanip>
#include <string>

bool updateSeatAvailability(std::vector<Train>& trains,
                             const std::string& trainId,
                             int seatsToRelease) {
    Train* train = findTrainById(trains, trainId);
    if (train == nullptr) {
        std::cerr << "[Warning] Train not found for seat update: cannot restore seats." << std::endl;
        return false;
    }

    train->availableSeats += seatsToRelease;

    // Clamp to total capacity so seats never exceed the train's limit
    if (train->availableSeats > train->totalSeats) {
        train->availableSeats = train->totalSeats;
    }
    return true;
}

CancelResult processCancellation(const std::string& reservationId,
                                  std::vector<Reservation>& reservations,
                                  std::vector<Train>& trains) {
    // Validate format before any lookup
    if (!isValidReservationId(reservationId)) {
        return CANCEL_INVALID_ID;
    }

    Reservation* reservation = findReservationById(reservations, reservationId);
    if (reservation == nullptr) {
        return CANCEL_NOT_FOUND;
    }

    if (reservation->status == STATUS_CANCELLED) {
        return CANCEL_ALREADY_CANCELLED;
    }

    // Mark cancelled and restore seats
    reservation->status = STATUS_CANCELLED;
    bool seatsUpdated = updateSeatAvailability(trains, reservation->trainId, reservation->seatsBooked);
    if (!seatsUpdated) {
        std::cerr << "[Warning] Seats could not be restored for train "
                  << reservation->trainId << std::endl;
    }

    // Persist both collections atomically
    bool resSaved = saveReservations(reservations);
    bool trainsSaved = saveTrains(trains);
    if (!resSaved || !trainsSaved) {
        std::cerr << "[Error] Failed to persist cancellation data." << std::endl;
        return CANCEL_STORAGE_ERROR;
    }

    return CANCEL_SUCCESS;
}

CancelResult cancelReservationFlow(std::vector<Reservation>& reservations,
                                    std::vector<Train>& trains) {
    std::string reservationId;

    std::cout << std::endl;
    std::cout << "═══════ CANCEL RESERVATION ═══════" << std::endl;
    std::cout << "Enter Reservation ID to cancel (e.g., RES001): ";
    std::getline(std::cin, reservationId);

    // Trim leading/trailing whitespace
    size_t start = reservationId.find_first_not_of(" \t\r\n");
    size_t end   = reservationId.find_last_not_of(" \t\r\n");
    reservationId = (start != std::string::npos)
                    ? reservationId.substr(start, end - start + 1)
                    : "";

    // ── Early validation ────────────────────────────────────────────
    if (!isValidReservationId(reservationId)) {
        std::cout << std::endl;
        std::cout << "[Error] Invalid reservation ID format." << std::endl;
        std::cout << "        Reservation IDs follow the format: RESxxx (e.g., RES001)" << std::endl;
        return CANCEL_INVALID_ID;
    }

    Reservation* reservation = findReservationById(reservations, reservationId);
    if (reservation == nullptr) {
        std::cout << std::endl;
        std::cout << "[Error] Reservation not found." << std::endl;
        std::cout << "        Please verify your reservation ID and try again." << std::endl;
        return CANCEL_NOT_FOUND;
    }

    if (reservation->status == STATUS_CANCELLED) {
        std::cout << std::endl;
        std::cout << "[Error] This reservation has already been cancelled." << std::endl;
        return CANCEL_ALREADY_CANCELLED;
    }

    // ── Show details and request confirmation ───────────────────────
    displayReservation(*reservation, trains);
    std::cout << std::endl;

    std::string confirm;
    std::cout << "Are you sure you want to cancel this reservation? (Y/N): ";
    std::getline(std::cin, confirm);

    // Trim confirmation input
    start = confirm.find_first_not_of(" \t\r\n");
    end   = confirm.find_last_not_of(" \t\r\n");
    confirm = (start != std::string::npos)
              ? confirm.substr(start, end - start + 1)
              : "";

    if (confirm != "Y" && confirm != "y" && confirm != "yes" && confirm != "Yes" && confirm != "YES") {
        std::cout << std::endl;
        std::cout << "Cancellation aborted. Your reservation remains active." << std::endl;
        return CANCEL_USER_DECLINED;
    }

    // ── Delegate the actual cancellation to processCancellation ─────
    // Capture display info before the reservation is modified.
    int    seatsBooked = reservation->seatsBooked;
    std::string trainId = reservation->trainId;

    CancelResult result = processCancellation(reservationId, reservations, trains);

    if (result == CANCEL_SUCCESS) {
        // Build dynamic-width success banner
        std::string cancelMsg = "Reservation " + reservationId + " has been cancelled.";
        std::string seatMsg   = std::to_string(seatsBooked)
                              + " seat(s) restored to train " + trainId + ".";

        std::cout << std::endl;
        std::cout << "╔══════════════════════════════════════════════╗" << std::endl;
        std::cout << "║        CANCELLATION SUCCESSFUL               ║" << std::endl;
        std::cout << "╠══════════════════════════════════════════════╣" << std::endl;
        std::cout << "║  " << std::setw(44) << std::left << cancelMsg << "║" << std::endl;
        std::cout << "║  " << std::setw(44) << std::left << seatMsg   << "║" << std::endl;
        std::cout << "╚══════════════════════════════════════════════╝" << std::endl;
    } else if (result == CANCEL_STORAGE_ERROR) {
        std::cout << std::endl;
        std::cout << "[Error] Cancellation could not be saved. Please contact support." << std::endl;
    }

    return result;
}