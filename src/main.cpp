/*The Parking management system is a software application designed to help manage parking spaces in a parking lot or garage. It allows users to track available parking spots, manage reservations, and monitor the status of parked vehicles. The system can be implemented using various programming languages, including C++, and can include features such as user authentication, payment processing, and reporting capabilities.*/
#include <iostream>

#include "../include/ParkingLot.h"
#include "../include/Vehicle.h"
using namespace std;

int main(){

    // System startup display
    cout<<"=========================================="<<endl;
    cout<<"|      Parking Management System         |"<<endl;
    cout<<"=========================================="<<endl;
    
    cout<<"System loading..."<<endl;
    cout<<endl;

    ParkingLot parkingLot(5); // Create a parking lot with 5 slots
    Vehicle vehicle1("KDA 443A", "Car");
    
    cout<<"\nVehicle Information:"<<endl;

    cout<<"Registration: "
    <<vehicle1.getRegistrationNumber()<<endl;

    cout<<"Type: "
        <<vehicle1.getRegistrationNumber()
        <<endl;
        
    

    parkingLot.displaySlots(); // Display the initial status of parking slots
    cout<<"\nFirst available slot: "
    <<parkingLot.findAvailableSlot()<<endl;

    parkingLot.occupySlot(2); // Occupy slot number 2
    cout<<"\nAfter vehicle parks in slot 2:"<<endl;
    parkingLot.displaySlots(); // Display the status of parking slots after occupying slot 2

    cout<<"\nFirst available slot: "
    <<parkingLot.findAvailableSlot()<<endl;

    parkingLot.releaseSlot(2); // Release slot number 2

    cout<<"\nAfter vehicle leaves slot 2:"<<endl;

    parkingLot.displaySlots(); //Display the status of parking slots after releasing slot 2
    return 0;
}




