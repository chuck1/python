CMAKE_MINIMUM_REQUIRED(VERSION 2.8.8)

INCLUDE($ENV{HOME}/.config.cmake)


PROJECT(Fluids)

FIND_PACKAGE(CMakeHelper)
FIND_PACKAGE(Boost 1.55 COMPONENTS serialization)

SET(libs ${libs}
	${PROJECT_NAME}
	${Boost_LIBRARIES}
	png
	rt
	pthread
	X11
	Xrandr
	Xi
	Xcursor
	)




cmh_static_library()

add_subdirectory(test)




