#ifndef VEHICLE_H
#define VEHICLE_H
using namespace std;
#include <string>

class Vehicle {
    private:
    string registrationNumber;
    string vehicleType;

    public:
    Vehicle(string registration, string type);

    string getRegistrationNumber();
    string getVehicleType();

};


#endif 