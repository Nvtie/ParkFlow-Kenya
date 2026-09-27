#include "../include/ParkingSession.h"
#include <iostream>

using namespace std;

ParkingSession::ParkingSession(Vehicle vehicle, ParkingSlot* slot)
    : vehicle(vehicle), parkingSlot(slot) {
        
}

void ParkingSession::displaySession(){
    cout<<"\n===== PARKING SESSION ====="<<endl;

    cout<<"Vehicle:"
    <<vehicle.getRegistrationNumber()
    <<" - "
    <<endl;

    cout<<"Vehicle Type:"
    <<vehicle.getVehicleType()
    <<endl;

    cout<<"Parking Slot:"
    <<parkingSlot->getSlotNumber()
    <<endl;
}