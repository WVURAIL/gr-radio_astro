include(GrTest)
set(GR_TEST_TARGET_DEPS gnuradio-radio_astro)

foreach(name IN ITEMS
    dedispersion detect vmedian
    ra_ascii_sink ra_event_log ra_event_sink ra_integrate ra_vave ra_vmedian)
    GR_ADD_TEST(qa_${name} ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/qa_${name}.py)
endforeach()
