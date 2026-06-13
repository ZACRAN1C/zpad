#!/bin/bash
echo "=== Збірка проєкту за допомогою CMake ==="
mkdir -p build
cd build || exit
cmake ..
make