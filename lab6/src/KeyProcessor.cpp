#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(Mode::NORMAL) {}

void KeyProcessor::processKey(int key) {
    switch (key) {
        case '0': currentMode = Mode::NORMAL; break;
        case '1': currentMode = Mode::INVERSION; break;
        case '2': currentMode = Mode::GAUSSIAN_BLUR; break;
        case '3': currentMode = Mode::CANNY_FILTER; break;
        default: break;
    }
}

KeyProcessor::Mode KeyProcessor::getMode() const {
    return currentMode;
}   