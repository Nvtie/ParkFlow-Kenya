#ifndef PARKING_LOT_H
#define PARKING_LOT_H

#include "ParkingSlot.h"
#include <vector> //this library is used to create a dynamic array of parking slots. it allows the parkind lot to manage multiple parking slots and perform operations on them.
using namespace std;

class ParkingLot{
    private:
    vector<ParkingSlot> slots; //vector of parking slots to store the parking slots in the parking lot. it allows the parking lot to manage multiple parking slots and perform operations on them.

    public:
    ParkingLot(int numberOfSlots); //constructor to initialize the parking Lot with a specifi number of parking slots. it creates the specified number of parking slots and adds them to the vector of parking slots,

    void displaySlots();
    int findAvailableSlot();

    void occupySlot(int slotNumber);
    void releaseSlot(int slotNumber);

    ParkingSlot* getSlot(int slotNumber); //this function returns a pointer to the parking slot with the specified slot number. it allows other classes or functions to access and manipulate specific parking slots in the parking lot.

        
};
#endif 
