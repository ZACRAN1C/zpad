cmake_minimum_required(VERSION 3.10)
project(FaceDetectionLab)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(WIN32)
    set(OpenCV_DIR "C:/opencv/build")
endif()

find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED) 

include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(FaceDetectionLab main.cpp FaceDetector.hpp)

target_link_libraries(FaceDetectionLab ${OpenCV_LIBS} Threads::Threads)