#include <opencv2/opencv.hpp>
#include <iostream>
#include "FaceDetector.hpp"
#include <windows.h>

int main() {
    SetConsoleOutputCP(CP_UTF8);
    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
        return -1;
    }
    std::cout << "Камера успішно ініціалізована." << std::endl;

    FaceDetector detector("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel");
    bool face_mode = true;

    std::cout << "Для увімкнення/вимкнення детекції НАТИСНІТЬ 'F' у вікні камери." << std::endl;

    while (true) {
        cv::Mat frame;
        cap >> frame;
        if (frame.empty()) {
            std::cerr << "Отримано порожній кадр з камери!" << std::endl;
            break;
        }

        detector.updateFrame(frame);

        int key = cv::waitKey(1);
        if (key == 27) { 
            break;
        }
        else if (key == 'f' || key == 'F') {
            face_mode = !face_mode;
            std::cout << "\n[MAIN] Перемикання режиму! face_mode тепер = " << (face_mode ? "УВІМКНЕНО" : "ВИМКНЕНО") << std::endl;
        }

        if (face_mode) {
            std::vector<cv::Rect> faces = detector.getFaces();

            if (!faces.empty()) {
                std::cout << "[MAIN] Знайдено облич на кадрі: " << faces.size() << std::endl;
            }

            for (const auto& box : faces) {
                cv::rectangle(frame, box, cv::Scalar(0, 255, 0), 2);
            }
        }

        cv::imshow("Camera", frame);
    }

    cap.release();
    cv::destroyAllWindows();
    return 0;
}