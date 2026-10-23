#ifndef BOOKING_H
#define BOOKING_H

#include "models.h"
#include <vector>

bool searchTrains(const std::vector<Train>& trains);

bool bookReservation(
    std::vector<Train>& trains,
    std::vector<Reservation>& reservations,
    const std::string& trainFilepath = "data/trains.dat",
    const std::string& reservationFilepath = "data/reservations.dat"
);

#endif
