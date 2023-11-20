######################################
# ---------------------------------- #
# -------- COMPILER VERSION -------- #
# ---------------------------------- #
######################################

cmake_minimum_required(VERSION 3.22)
project(multi_demo VERSION 0.0.0)

message(STATUS "CMAKE_CXX_COMPILER_ID: ${CMAKE_CXX_COMPILER_ID}")
message(STATUS "CMAKE_CXX_COMPILER_VERSION: ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "CMAKE_SYSTEM: ${CMAKE_SYSTEM}")

# Compiler options.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# If using gperftools, run cmake with additional args:
# cmake -DCMAKE_CXX_FLAGS=-pg -DCMAKE_EXE_LINKER_FLAGS=-pg -DCMAKE_SHARED_LINKER_FLAGS=-pg ..

if (debug)
    message(STATUS "---- Building with debug options ----")

    if (NOT no_asan OR NOT DEFINED no_asan)
        # Memory debug
        set(CMAKE_CXX_FLAGS "-fexceptions -fsanitize=address")
        set(ASAN_OPTIONS=check_initialization_order=1)
        set(ASAN_OPTIONS=detect_leaks=1)
    else()
        set(CMAKE_CXX_FLAGS "-fexceptions")
    endif()

    add_definitions(-ggdb3 -Og -Wall)       # Debugging + minimal optimization

else()
    message(STATUS "---- Building with optimization ----")

    # Standard compilation
    add_definitions(-O3 -Wall)              # Much optimization
endif()


##############################################
# ------------------------------------------ #
# -------- LINKING EXTERNAL LIBRARY -------- #
# ---------------- ortools ----------------- #
# ------------------------------------------ #
##############################################

include(FetchContent)
FetchContent_Declare(
        ortools
        URL https://github.com/google/or-tools/archive/refs/tags/v9.7.tar.gz
)

set(BUILD_DEPS ON)
set(BUILD_DOC OFF)
set(BUILD_SAMPLES OFF)
set(BUILD_EXAMPLES OFF)

FetchContent_MakeAvailable(ortools)

include_directories(
        ${ortools_SOURCE_DIR}
        ${ortools_BINARY_DIR}
        ${absl_SOURCE_DIR}
        ${protobuf_SOURCE_DIR}/src
)

message(STATUS "ortools_SOURCE_DIR: " ${ortools_SOURCE_DIR})
message(STATUS "ortools_BINARY_DIR: " ${ortools_BINARY_DIR})
message(STATUS "absl_SOURCE_DIR: " ${absl_SOURCE_DIR})
message(STATUS "protobuf_SOURCE_DIR: /src: " ${protobuf_SOURCE_DIR}/src)


# ------- Misc -------

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

# -------- EXECUTABLES --------

set(EXECUTABLES
    demo
)

foreach(FILENAME_PREFIX ${EXECUTABLES})
    add_executable(${FILENAME_PREFIX} src/executable/${FILENAME_PREFIX}.cpp)

    target_link_libraries(${FILENAME_PREFIX}
        Threads::Threads
        ortools::ortools
    )

endforeach()


# -------- final steps --------

# Some potentially helpful messages
message(STATUS "CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")
message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message(STATUS "CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")
message(STATUS "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")

