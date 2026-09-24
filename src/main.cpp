/*The Parking management system is a software application designed to help manage parking spaces in a parking lot or garage. It allows users to track available parking spots, manage reservations, and monitor the status of parked vehicles. The system can be implemented using various programming languages, including C++, and can include features such as user authentication, payment processing, and reporting capabilities.*/
#include <iostream>
#include "../include/ParkingSlot.h"
using namespace std;

int main(){

    // System startup display
    cout<<"=========================================="<<endl;
    cout<<"|      Parking Management System         |"<<endl;
    cout<<"=========================================="<<endl;
    
    cout<<"System loading..."<<endl;
    cout<<endl;

    //Creat parking slot
    ParkingSlot slot1(1);
    cout<< "Parking Slot:"
    <<slot1.getSlotNumber()<<endl;

    cout<<"Occupied: "
    <<slot1.isOccupied()<<endl;

    //Occupy the parking slot
    slot1.occupy();

    cout<<endl;
    cout<<"After vehicle parks:"<<endl;

    cout<<"Occupied: "
    <<slot1.isOccupied()<<endl;

    //release the parking slot
    slot1.release();
    cout<<"After vehicle leaves:"<<endl;
    cout<<"Occupied: "
    <<slot1.isOccupied()<<endl;

    return 0;
}