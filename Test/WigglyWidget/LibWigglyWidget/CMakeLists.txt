cmake_minimum_required(VERSION 3.14)

project(LibWigglyWidget LANGUAGES CXX)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 配置安装目录
set(CMAKE_INSTALL_DIR "${CMAKE_SOURCE_DIR}/dist")

# 静态库
set(BUILD_SHARED_LIBS OFF)

find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

add_library(LibWigglyWidget wigglywidget.cpp wigglywidget.h)

target_link_libraries(LibWigglyWidget PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

if(BUILD_SHARED_LIBS)
  target_compile_definitions(LibWigglyWidget PRIVATE LIBWIGGLYWIDGET_LIBRARY)
endif()

# 配置生成的文件安装目录
install(
  TARGETS ${PROJECT_NAME}
  RUNTIME DESTINATION "${CMAKE_INSTALL_DIR}/bin"
  LIBRARY DESTINATION "${CMAKE_INSTALL_DIR}/lib"
  ARCHIVE DESTINATION "${CMAKE_INSTALL_DIR}/lib")

install(FILES wigglywidget.h DESTINATION "${CMAKE_INSTALL_DIR}/include")
