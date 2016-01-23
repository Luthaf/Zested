include(ExternalProject)

ExternalProject_add(python-2.7.10
    PREFIX python
    URL file://${CMAKE_CURRENT_SOURCE_DIR}/python.tar.gz
    URL_MD5 "b58f5eb44aba2e3ed9bcdb4b2226dc70"
    CMAKE_ARGS  -DBUILD_SHARED_LIBS=OFF
                -DUSE_SYSTEM_LIBRARIES=OFF
                -DPY_VERSION_PATCH=10
                -DDOWNLOAD_SOURCES=ON
                # Setting compilers
                -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
                -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
                # Setting installation directory
                -DCMAKE_INSTALL_PREFIX=${PROJECT_BINARY_DIR}
                # Support cross-compilation
                # -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
                # -DCMAKE_FIND_ROOT_PATH=${CMAKE_FIND_ROOT_PATH}
                # -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=${CMAKE_FIND_ROOT_PATH_MODE_LIBRARY}
                # -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=${CMAKE_FIND_ROOT_PATH_MODE_INCLUDE}
                # -DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=${CMAKE_FIND_ROOT_PATH_MODE_PROGRAM}
)
add_library(python STATIC IMPORTED GLOBAL)
set_property(
    TARGET python
    PROPERTY IMPORTED_LOCATION ${PROJECT_BINARY_DIR}/lib/libpython2.7${CMAKE_STATIC_LIBRARY_SUFFIX}
)

###=============================================================================###

ExternalProject_add(hunspell-1.3.2
    PREFIX hunspell
    URL file://${CMAKE_CURRENT_SOURCE_DIR}/hunspell.tar.gz
    URL_MD5 "c4335df0987bbfc5093206b336acfed1"
    CMAKE_ARGS  # Setting compilers
                -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
                -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
                # Setting installation directory
                -DCMAKE_INSTALL_PREFIX=${PROJECT_BINARY_DIR}
                # Support cross-compilation
                -DCMAKE_SYSTEM_NAME=${CMAKE_SYSTEM_NAME}
                -DCMAKE_FIND_ROOT_PATH=${CMAKE_FIND_ROOT_PATH}
                -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=${CMAKE_FIND_ROOT_PATH_MODE_LIBRARY}
                -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=${CMAKE_FIND_ROOT_PATH_MODE_INCLUDE}
                -DCMAKE_FIND_ROOT_PATH_MODE_PROGRAM=${CMAKE_FIND_ROOT_PATH_MODE_PROGRAM}
)

add_library(hunspell STATIC IMPORTED GLOBAL)
set_property(
    TARGET hunspell
    PROPERTY IMPORTED_LOCATION ${PROJECT_BINARY_DIR}/lib/libhunspell${CMAKE_STATIC_LIBRARY_SUFFIX}
)

###=============================================================================###

if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/boost/LICENSE_1_0.txt")
    message(STATUS "Unpacking Boost sources")
    execute_process(
        COMMAND ${CMAKE_COMMAND} -E tar xf ${CMAKE_CURRENT_SOURCE_DIR}/boost.tar.gz
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
endif()

include_directories(SYSTEM boost)
include_directories(SYSTEM ${CMAKE_BINARY_DIR}/include/python2.7)
file(GLOB_RECURSE BOOST_PYTHON_SRC boost/src/*.cpp)
add_library(boost_python STATIC ${BOOST_PYTHON_SRC})

add_dependencies(boost_python python-2.7.10)
