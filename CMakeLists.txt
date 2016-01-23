cmake_minimum_required(VERSION 2.8.11)
project(zested C CXX)

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake")
if(${CMAKE_VERSION} VERSION_GREATER 3.0.0)
    cmake_policy(SET CMP0042 NEW)
endif()

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'release' as none was specified.")
  set(CMAKE_BUILD_TYPE "release" CACHE STRING "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel." FORCE)
endif()

set(CMAKE_CXX_STANDARD 11)
set(CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTORCC ON)

add_subdirectory(external)
include_directories(BEFORE SYSTEM ${PROJECT_BINARY_DIR}/include)
include_directories(BEFORE SYSTEM ${PROJECT_BINARY_DIR}/include/python2.7)

find_package(Qt5 REQUIRED COMPONENTS Core Widgets Gui UiTools)

file(GLOB SRC src/*.cpp assets/zested.qrc)
file(GLOB HEADERS include/*.hpp)
file(GLOB PYTHON python/*.py)

include_directories(include)
include_directories(SYSTEM external/boost/)

add_executable(Zested ${SRC} ${HEADERS} ${PYTHON})
target_link_libraries(Zested Qt5::Widgets Qt5::UiTools python hunspell boost_python)
add_dependencies(Zested boost_python hunspell-1.3.2)

if(APPLE)
    set_target_properties(Zested PROPERTIES MACOSX_BUNDLE TRUE)
    # Copy Qt libraries inside the .app bundle
    add_custom_command(TARGET Zested POST_BUILD COMMAND macdeployqt Zested.app -no-strip)

    add_custom_command(TARGET Zested POST_BUILD
        COMMAND cmake -E make_directory ${PROJECT_BINARY_DIR}/Zested.app/Contents/Resources/lib/python2.7/
        COMMAND rsync -r "${PROJECT_BINARY_DIR}/lib/python2.7/"
                         "${PROJECT_BINARY_DIR}/Zested.app/Contents/Resources/lib/python2.7/"
        COMMENT "Copying Python standard library inside the application bundle.")

    add_custom_command(TARGET Zested POST_BUILD
        COMMAND rsync -r "${PROJECT_SOURCE_DIR}/python/"
                         "${PROJECT_BINARY_DIR}/Zested.app/Contents/Resources/lib/python2.7/"
        COMMENT "Copying Python scripts inside the application bundle.")

    add_custom_command(TARGET Zested POST_BUILD
        COMMAND rsync -r "${PROJECT_SOURCE_DIR}/assets/dicts/" "${PROJECT_BINARY_DIR}/Zested.app/Contents/Resources/dicts"
        COMMENT "Copying Hunspell dictionaries inside the application bundle.")

    set(RESOURCES_PATH "../Resources/")
endif()

add_definitions("-DRESOURCES_PATH=\"${RESOURCES_PATH}\"")

set(CPACK_GENERATOR "TGZ")
include(Cpack)
