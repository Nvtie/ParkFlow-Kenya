#ifndef PAYMENT_H
#define PAYMENT_H

#include <string>

class Payment {

private:
    double amount;
    std::string paymentMethod;
    bool paymentConfirmed;

public:
    Payment(double amount, std::string method);

    void confirmPayment();

    bool isPaymentConfirmed();

    double getAmount();

    std::string getPaymentMethod();

    void displayPayment();
};

#endif