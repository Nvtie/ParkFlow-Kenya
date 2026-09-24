#include"../include/ParkingSlot.h"

ParkingSlot::ParkingSlot(int number){//:: operator means that this function belongs to Parking slot class.

    slotNumber = number;
    occupied =false;
}

void ParkingSlot::occupy(){
    occupied = true;

}

void ParkingSlot::release(){
    occupied = false;
}
bool ParkingSlot::isOccupied(){
    return occupied;
}

int ParkingSlot::getSlotNumber(){
    return slotNumber;
}