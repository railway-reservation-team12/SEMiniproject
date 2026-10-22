#ifndef RESERVATION_H
#define RESERVATION_H
#include "models.h"
#include <string>
#include <vector>

// Looks up a reservation by ID.  Returns LOOKUP_SUCCESS and populates
// outReservation if found, or an appropriate error code otherwise.
LookupResult lookupReservation(const std::string& reservationId,
                                std::vector<Reservation>& reservations,
                                Reservation& outReservation);

// Displays formatted reservation details to stdout, including
// associated train information when available.  Shows a fallback
// line with just the train ID if the train record is not found.
void displayReservation(const Reservation& reservation,
                        const std::vector<Train>& trains);

// Returns a human-readable string for the given reservation status.
std::string getStatusString(ReservationStatus status);

// Interactive flow: prompts the user for a reservation ID and
// displays the corresponding reservation details.
bool viewReservationFlow(std::vector<Reservation>& reservations,
                         const std::vector<Train>& trains);
#endif