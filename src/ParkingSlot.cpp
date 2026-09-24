#include"../include/ParkingSlot.h"

ParkingSlot::ParkingSlot(int number){//:: operator means that this function belongs to Parking slot class.

    slotNumber = number;
    this->occupied = false;
}

void ParkingSlot::occupy(){
    this->occupied = true;

}

void ParkingSlot::release(){
    this->occupied = false;
}

bool ParkingSlot::isOccupied(){
    return this->occupied;
}

int ParkingSlot::getSlotNumber(){
    return slotNumber;
}