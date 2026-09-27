/*The Parking management system is a software application designed to help manage parking spaces in a parking lot or garage. It allows users to track available parking spots, manage reservations, and monitor the status of parked vehicles. The system can be implemented using various programming languages, including C++, and can include features such as user authentication, payment processing, and reporting capabilities.*/
#include <iostream>

#include "../include/ParkingLot.h"
#include "../include/Vehicle.h"
#include "../include/ParkingSession.h"
#include "../include/FeeCalculator.h"
#include "../include/Payment.h"
#include "../include/Barrier.h"

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
        <<vehicle1.getVehicleType()
        <<endl;

    

    parkingLot.displaySlots(); // Display the initial status of parking slots
    
    int availableSlot = parkingLot.findAvailableSlot();
    cout<<"\nFirst available slot: "
    <<availableSlot<<endl;

    parkingLot.occupySlot(availableSlot); // Occupy slot number 2
    cout<<"\nAfter vehicle parks in slot :"
    <<":"<<endl;

    parkingLot.displaySlots(); // Display the status of parking slots after occupying slot 2

    ParkingSlot* assignedSlot = parkingLot.getSlot(availableSlot); // Get the pointer to the occupied slot
    ParkingSession session(vehicle1, assignedSlot); // Create a parking session for the vehicle and the assigned slot
    session.displaySession(); // Display the parking session details

      //Test fee calculation
    cout <<"\n===== FEE CALCULATION ===="<<endl;
    int duration = 150; // Example duration in minutes

    double amount = FeeCalculator::calculateFee(duration);

    cout << "Parking Duration: " << duration << " minutes" << endl;

    cout<< "Amount Payable: Ksh"
    << amount << endl;

   

    // Create payment
Payment payment(amount, "M-Pesa");

// Display payment before confirmation
payment.displayPayment();

// Confirm payment
payment.confirmPayment();

// Display payment after confirmation
payment.displayPayment();


// Create barrier
Barrier barrier;

// Check payment before opening barrier
if (payment.isPaymentConfirmed()) {

    cout << "\nPayment confirmed." << endl;

    barrier.open();

}
else {

    cout << "\nPayment not confirmed. Barrier remains closed." << endl;

}

// Vehicle exits after successful payment
if (payment.isPaymentConfirmed()) {

    cout << "\nVehicle is exiting the parking lot..." << endl;

    // Release the parking slot
    parkingLot.releaseSlot(availableSlot);

    cout << "Parking slot "
         << availableSlot
         << " is now available."
         << endl;

    // Close the barrier after vehicle exits
    barrier.close();

}

    
    //release the occupied slot
    parkingLot.releaseSlot(availableSlot); // Release available slot number 2

    cout<<"\nAfter vehicle leaves slot :"
    <<availableSlot
    <<":"<<endl;

    parkingLot.displaySlots(); //Display the status of parking slots after releasing slot 2
    
  
    return 0;
}




