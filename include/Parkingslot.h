#ifndef PARKINGSLOT_H
#define PARKINGSLOT_H

class ParkingSlot{

    private: //Private means that these variable cannot be affected or accessed by any other class or function outside of this class. They can only be accessed and modified by the member functions of this class.(encapsulation).

        int slotNumber;//stores the slot number of the parking slot
        bool occupied;//boolean variable to indicate whether the parking slot is occupied or not.occupied=true means the slot is occupied, while occupied=false means the slot is available.
    
    public: //Public means that these functions can be accessed and called by any other class or function outside of this class.
        ParkingSlot(int number);// this is a constructor. Its job is to initialize a new parking-slot object with a specific slot number.

        void occupy();
        void vacate();

        bool isOccupied();
        int getSlotNumber();
};
#endif