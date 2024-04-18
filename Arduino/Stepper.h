// Stepper.h

#ifndef STEPPER_H
#define STEPPER_H

#include <Arduino.h>

class Stepper
{
public:
//private:
    const int _step_pin;
    const int _dir_pin;
    const int _min_delay;
    const int _max_delay;

    unsigned long _last_micros;
    unsigned long _delay_micros;
    unsigned long _delay_increment;

    boolean _is_stopped;
    boolean _forward_dir;
    boolean _cur_dir;

//public:
    Stepper() {}
    Stepper(int step_pin, int dir_pin, int min_delay=600, int max_delay=6000, boolean forward_dir=1);

    void oneStep();
    void goForward(unsigned long cur_micros);
    void goBackward(unsigned long cur_micros);
    void stopSpeed(unsigned long cur_micros);
    void accelerate(unsigned long cur_micros);
    void decelerate(unsigned long cur_micros);
    void switchDirection();
    
};

#endif
