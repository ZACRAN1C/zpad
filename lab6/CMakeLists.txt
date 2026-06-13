cmake_minimum_required(VERSION 3.10)
project(OpenCV_Lab6 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(WIN32)
    set(OpenCV_DIR "C:/opencv/build")
endif()

find_package(OpenCV REQUIRED)

include_directories(include)

set(SOURCES
    src/main.cpp
    src/CameraProvider.cpp
    src/KeyProcessor.cpp
    src/FrameProcessor.cpp
    src/Display.cpp
)

add_executable(OpenCV_Lab6 ${SOURCES})
target_link_libraries(OpenCV_Lab6 ${OpenCV_LIBS})