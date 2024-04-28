cmake_minimum_required(VERSION 3.14)
cmake_policy(VERSION 3.14)

# Enable policy to not use RPATH settings for install_name on macOS.
if(POLICY CMP0068)
  cmake_policy(SET CMP0068 NEW)
endif()

# Enable policy to run automoc on generated files.
if(POLICY CMP0071)
  cmake_policy(SET CMP0071 NEW)
endif()

project(PySideWrapper)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(BINDINGS_HEADER_FILE "${CMAKE_CURRENT_SOURCE_DIR}/bindings.h")
set(BINDINGS_TYPESYSTEM_FILE "${CMAKE_CURRENT_SOURCE_DIR}/bindings.xml")
set(BINDINGS_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/dist")
set(BINDINGS_INCLUDE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../dist/include/")

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/bindings.txt.in"
               "${CMAKE_CURRENT_SOURCE_DIR}/bindings.txt")
