#ifndef FACEDETECTOR_HPP
#define FACEDETECTOR_HPP

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <chrono>
#include <condition_variable>
#include <iostream>

class FaceDetector {
private:
    cv::dnn::Net net;
    std::thread worker;
    std::mutex mtx;
    std::condition_variable cv;
    std::atomic<bool> running;
    cv::Mat current_frame;
    std::vector<cv::Rect> faces;
    bool frame_ready;

    void workerLoop() {
        std::cout << "[WORKER] Фоновий потік запущено успішно." << std::endl;
        while (running) {
            cv::Mat frame_to_process;
            {
                std::unique_lock<std::mutex> lock(mtx);
                cv.wait(lock, [this] { return frame_ready || !running; });
                if (!running) break;
                frame_to_process = current_frame.clone();
                frame_ready = false;
            }

            if (frame_to_process.empty()) continue;

            cv::Mat blob = cv::dnn::blobFromImage(frame_to_process, 1.0, cv::Size(300, 300), cv::Scalar(104.0, 177.0, 123.0));
            net.setInput(blob);
            cv::Mat detections = net.forward();

            std::vector<cv::Rect> local_faces;
            cv::Mat detectionMat(detections.size[2], detections.size[3], CV_32F, detections.ptr<float>());

            for (int i = 0; i < detectionMat.rows; i++) {
                float confidence = detectionMat.at<float>(i, 2);
                if (confidence > 0.5) { 
                    int x1 = static_cast<int>(detectionMat.at<float>(i, 3) * frame_to_process.cols);
                    int y1 = static_cast<int>(detectionMat.at<float>(i, 4) * frame_to_process.rows);
                    int x2 = static_cast<int>(detectionMat.at<float>(i, 5) * frame_to_process.cols);
                    int y2 = static_cast<int>(detectionMat.at<float>(i, 6) * frame_to_process.rows);
                    local_faces.push_back(cv::Rect(cv::Point(x1, y1), cv::Point(x2, y2)));
                }
            }

            if (!local_faces.empty()) {
                std::cout << "[WORKER] Облич виявлено: " << local_faces.size() << std::endl;
            }


            {
                std::lock_guard<std::mutex> lock(mtx);
                faces = local_faces;
            }
        }
        std::cout << "[WORKER] Фоновий потік завершив роботу." << std::endl;
    }

public:
    FaceDetector(const std::string& proto, const std::string& model) {
        net = cv::dnn::readNetFromCaffe(proto, model);
        running = true;
        frame_ready = false;
        worker = std::thread(&FaceDetector::workerLoop, this);
    }

    ~FaceDetector() {
        running = false;
        cv.notify_one();
        if (worker.joinable()) {
            worker.join();
        }
    }

    void updateFrame(const cv::Mat& frame) {
        std::lock_guard<std::mutex> lock(mtx);
        current_frame = frame.clone();
        frame_ready = true;
        cv.notify_one();
    }

    std::vector<cv::Rect> getFaces() {
        std::lock_guard<std::mutex> lock(mtx);
        return faces;
    }
};

#endif