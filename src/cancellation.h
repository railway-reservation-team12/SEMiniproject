#ifndef CANCELLATION_H
#define CANCELLATION_H
#include "models.h"
#include <string>
#include <vector>

// Processes a cancellation: validates the ID, marks the reservation
// as cancelled, restores seat availability, and persists changes.
// Returns the appropriate CancelResult status code.
CancelResult processCancellation(const std::string& reservationId,
                                  std::vector<Reservation>& reservations,
                                  std::vector<Train>& trains);

// Restores the given number of seats to the specified train,
// capping at the train's total seat capacity.  Returns false
// if the train ID was not found.
bool updateSeatAvailability(std::vector<Train>& trains,
                             const std::string& trainId,
                             int seatsToRelease);

// Interactive cancellation flow: prompts for a reservation ID,
// displays details, asks for confirmation, and delegates the
// actual cancellation to processCancellation.
CancelResult cancelReservationFlow(std::vector<Reservation>& reservations,
                                    std::vector<Train>& trains);
#endif