#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
private:
    int brightnessSlider;

public:
    FrameProcessor();
    cv::Mat process(const cv::Mat& inputFrame, KeyProcessor::Mode mode);
    int* getBrightnessSliderPtr();
};

#endif