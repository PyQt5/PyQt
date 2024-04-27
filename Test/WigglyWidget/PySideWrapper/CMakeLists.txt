cmake_minimum_required(VERSION 3.14)

project(PySideWrapper)

set(BINDINGS_HEADER_FILE "${CMAKE_CURRENT_SOURCE_DIR}/bindings.h")
set(BINDINGS_TYPESYSTEM_FILE "${CMAKE_CURRENT_SOURCE_DIR}/bindings.xml")
set(BINDINGS_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/dist")
set(BINDINGS_INCLUDE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../dist/include/")

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/bindings.txt.in"
               "${CMAKE_CURRENT_SOURCE_DIR}/bindings.txt")
