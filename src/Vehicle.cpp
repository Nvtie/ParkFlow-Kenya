#include "../include/Vehicle.h"
using namespace std;


Vehicle::Vehicle(string registration,string type){

    registrationNumber = registration;
    vehicleType =type;
}

string Vehicle::getRegistrationNumber(){

    return registrationNumber;

}

string Vehicle::getVehicleType(){
    return vehicleType;
}


