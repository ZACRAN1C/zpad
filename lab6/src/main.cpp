#include <iostream>
#include <opencv2/opencv.hpp>

#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        return -1;
    }

    Display display("Лабораторна робота 6");
    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;

    display.createTrackbar("Яскравість", frameProcessor.getBrightnessSliderPtr(), 100);

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            break;
        }

        cv::Mat processedFrame = frameProcessor.process(frame, keyProcessor.getMode());
        display.show(processedFrame);

        int key = cv::waitKey(30);
        if (key == 27) {
            break;
        }
        
        keyProcessor.processKey(key);
    }

    return 0;
}