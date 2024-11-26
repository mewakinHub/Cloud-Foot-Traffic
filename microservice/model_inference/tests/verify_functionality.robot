*** Settings ***
Library           Process
Library           Collections
Library           OperatingSystem
Library           BuiltIn

*** Variables ***
${SCRIPT_PATH}    /mnt/data/capture_and_detect.py
${PAYLOAD}        {"username": "testuser", "streaming_URL": "https://www.youtube.com/stream_url", "email": "test@example.com", "Monitoring_status": "active"}

*** Test Cases ***
Test Get Stream URL
    [Documentation]    Test the retrieval of stream URL using yt-dlp.
    Set Environment Variable    PAYLOAD    ${PAYLOAD}
    Run Process    python3    ${SCRIPT_PATH}
    Should Contain    ${OUTPUT}    Successfully retrieved stream URL

Test Frame Capture
    [Documentation]    Test capturing and processing frames.
    Set Environment Variable    PAYLOAD    ${PAYLOAD}
    Run Process    python3    ${SCRIPT_PATH}
    Should Contain    ${OUTPUT}    People Count:

Test Database Insertion
    [Documentation]    Ensure that results are inserted into the database correctly.
    Set Environment Variable    PAYLOAD    ${PAYLOAD}
    Run Process    python3    ${SCRIPT_PATH}
    Should Not Contain    ${OUTPUT}    [ERROR]
