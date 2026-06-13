#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() : brightnessSlider(50) {}

int* FrameProcessor::getBrightnessSliderPtr() {
    return &brightnessSlider;
}

cv::Mat FrameProcessor::process(const cv::Mat& inputFrame, KeyProcessor::Mode mode) {
    if (inputFrame.empty()) return inputFrame;

    cv::Mat result;

    switch (mode) {
        case KeyProcessor::Mode::INVERSION:
            cv::bitwise_not(inputFrame, result);
            break;
        case KeyProcessor::Mode::GAUSSIAN_BLUR:
            cv::GaussianBlur(inputFrame, result, cv::Size(15, 15), 0);
            break;
        case KeyProcessor::Mode::CANNY_FILTER:
            cv::Canny(inputFrame, result, 50, 150);
            cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
            break;
        case KeyProcessor::Mode::NORMAL:
        default:
            result = inputFrame.clone();
            break;
    }

    int offset = brightnessSlider - 50;
    result.convertTo(result, -1, 1, offset);

    cv::putText(result, "0:Orig | 1:Invert | 2:Blur | 3:Canny | ESC:Exit", 
                cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);

    return result;
}