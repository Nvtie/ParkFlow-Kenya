#include "../include/ParkingLot.h"
#include <iostream>
using namespace std;

ParkingLot::ParkingLot(int numberOfSlots){

    for(int i=1; i<=numberOfSlots; i++){
        slots.push_back(ParkingSlot(i));
    }
}
void ParkingLot::displaySlots(){
    cout<<"\nParking Slots:\n";

    for (ParkingSlot &slot : slots){
        cout<<"Slot"
        <<slot.getSlotNumber()
        <<"-";
    

        if(slot.isOccupied()){
            cout<<"Occupied"<<endl;
        }
        else{
                cout<<"Available"<<endl;
            }
        
    }
}
int ParkingLot::findAvailableSlot(){

    for (ParkingSlot &slot : slots){
        if (!slot.isOccupied()){
            return slot.getSlotNumber();
        }
    }
    return -1; // No available slot found

}
void ParkingLot::occupySlot(int slotNumber){
    for (ParkingSlot &slot : slots){
        if (slot.getSlotNumber() == slotNumber){
            slot.occupy();
            return;
        }
    }
    
}
void ParkingLot::releaseSlot(int slotNumber){
    for (ParkingSlot &slot : slots){

        if (slot.getSlotNumber() == slotNumber){
            slot.release();
            return;
        }
    }
}