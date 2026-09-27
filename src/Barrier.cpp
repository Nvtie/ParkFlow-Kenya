#include "../include/Barrier.h"
#include <iostream>

Barrier::Barrier() {

    isOpen = false;
}

void Barrier::open() {

    isOpen = true;

    std::cout << "\nBarrier: OPEN" << std::endl;
}

void Barrier::close() {

    isOpen = false;

    std::cout << "\nBarrier: CLOSED" << std::endl;
}

bool Barrier::getStatus() {

    return isOpen;
}