#include "../include/FeeCalculator.h"

double FeeCalculator::calculateFee(int durationMinutes) {
    if(durationMinutes <=30){
        return 0;
    }
    else if(durationMinutes <=120){
        return 50;
    }
    else if (durationMinutes <= 240){
        return 100;
    }
    else if(durationMinutes <=360){
        return 300;
    }
    else{
        return 500;
    }
}