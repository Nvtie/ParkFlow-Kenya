#ifndef PARKING_SESSION_H
#define PARKING_SESSION_H

#include "Vehicle.h"
#include "ParkingSlot.h"

class ParkingSession {

    private:
    Vehicle vehicle;
    ParkingSlot* parkingSlot;

    public:
    ParkingSession(Vehicle vehicle, ParkingSlot* slot);

    void displaySession();

};
#endif

