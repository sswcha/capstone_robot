// Stepper.cpp

#include <digitalWriteFast.h>
#include "Stepper.h"

// contructor
Stepper::Stepper(int step_pin, int dir_pin, int min_delay=600, int max_delay=5000, boolean forward_dir=1) : 
        _step_pin(step_pin), _dir_pin(dir_pin), _min_delay(min_delay), _max_delay(max_delay), _forward_dir(forward_dir) {
    pinModeFast(_step_pin, OUTPUT);
    pinModeFast(_dir_pin, OUTPUT);
    digitalWriteFast(_dir_pin, _forward_dir);

    _last_micros = 0;
    _is_stopped = true;
    _delay_micros = 5000;
    _delay_increment = 10;
    _cur_dir = _forward_dir;
}

void Stepper::oneStep() {
    digitalWriteFast(_step_pin, HIGH);
    digitalWriteFast(_step_pin, LOW);
}

void Stepper::goForward(unsigned long cur_micros) {
    if (_cur_dir != _forward_dir) {
        this->decelerate(cur_micros);
        if (_is_stopped == true) {
            this->switchDirection();
        }
    }
    _is_stopped = false;
    this->accelerate(cur_micros);
}

void Stepper::goBackward(unsigned long cur_micros) {
    if (_cur_dir == _forward_dir) {
        this->decelerate(cur_micros);
        if (_is_stopped == true) {
            this->switchDirection();
        }
    }
    _is_stopped = false;
    this->accelerate(cur_micros);
}

void Stepper::stopSpeed(unsigned long cur_micros) {
    
    _delay_micros = _max_delay;

    // _is_stopped = true;     only if delay reaches max delay
}

void Stepper::accelerate(unsigned long cur_micros) {
    if (cur_micros - _last_micros >= _delay_micros) {
        // check if max speed is met, if not, accelerate to max speed 
        if (_delay_micros > _min_delay) {
            _delay_micros -= _delay_increment;
        }
        this->oneStep();
        _last_micros = cur_micros;
    }
}

// decelerate while going in the current direction. Comes to a stop given enough time
void Stepper::decelerate(unsigned long cur_micros) {
    if (cur_micros - _last_micros >= _delay_micros) {
        // check if max speed is met, if not, accelerate to max speed 
        if (_delay_micros < _max_delay) {
            _delay_micros += _delay_increment;
            this->oneStep();
            _last_micros = cur_micros;
        } else { // minimum speed reached. come to stop.
            _is_stopped = true;
        }
    }
}

void Stepper::switchDirection() {
    _cur_dir = !_cur_dir;
    digitalWriteFast(_dir_pin, _cur_dir);
}

/*
// trigger if delay interval is met
    if (cur_micros - last_micros >= delay_micros) {
        // check if max speed is met, if not, accelerate to max speed 
        if (delay_micros > min_delay) {
            delay_micros -= delay_increment;
        }
        digitalWriteFast(STEP1, HIGH);
        digitalWriteFast(STEP1, LOW);
        last_micros = cur_micros;
    }
    */
