#include "../include/Payment.h"
#include <iostream>

Payment::Payment(double amount, std::string method) {

    this->amount = amount;
    paymentMethod = method;
    paymentConfirmed = false;
}

void Payment::confirmPayment() {

    paymentConfirmed = true;
}

bool Payment::isPaymentConfirmed() {

    return paymentConfirmed;
}

double Payment::getAmount() {

    return amount;
}

std::string Payment::getPaymentMethod() {

    return paymentMethod;
}

void Payment::displayPayment() {

    std::cout << "\n===== PAYMENT =====" << std::endl;

    std::cout << "Amount: KSh "
              << amount
              << std::endl;

    std::cout << "Payment Method: "
              << paymentMethod
              << std::endl;

    if (paymentConfirmed) {
        std::cout << "Payment Status: CONFIRMED"
                  << std::endl;
    }
    else {
        std::cout << "Payment Status: PENDING"
                  << std::endl;
    }
}