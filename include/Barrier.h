#ifndef BARRIER_H
#define BARRIER_H

class Barrier {

private:
    bool isOpen;

public:
    Barrier();

    void open();
    void close();

    bool getStatus();
};

#endif