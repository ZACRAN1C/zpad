#include "Display.hpp"

Display::Display(const std::string& name) : windowName(name) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
}

Display::~Display() {
    cv::destroyWindow(windowName);
}

void Display::show(const cv::Mat& frame) const {
    if (!frame.empty()) {
        cv::imshow(windowName, frame);
    }
}

void Display::createTrackbar(const std::string& barName, int* value, int maxValue) {
    cv::createTrackbar(barName, windowName, value, maxValue, nullptr);
}