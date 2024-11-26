# *** Settings ***
# Library           Process
# Library           Collections
# Library           OperatingSystem
# Library           BuiltIn

# *** Variables ***
# ${SCRIPT_PATH}    /mnt/data/capture_and_detect.py
# ${PAYLOAD}        {"username": "user1", "streaming_URL": "https://www.youtube.com/live/o4F9RFUzpas?si=Sx8gHWnZ_akIOTw6", "email": "user1@example.com", "Monitoring_status": 1}

# *** Test Cases ***
# Test Get Stream URL
#     [Documentation]    Test the retrieval of stream URL using yt-dlp.
#     Set Environment Variable    PAYLOAD    ${PAYLOAD}
#     Run Process    python3    ${SCRIPT_PATH}
#     Should Contain    ${OUTPUT}    Successfully retrieved stream URL

# Test Frame Capture
#     [Documentation]    Test capturing and processing frames.
#     Set Environment Variable    PAYLOAD    ${PAYLOAD}
#     Run Process    python3    ${SCRIPT_PATH}
#     Should Contain    ${OUTPUT}    People Count:

# Test Database Insertion
#     [Documentation]    Ensure that results are inserted into the database correctly.
#     Set Environment Variable    PAYLOAD    ${PAYLOAD}
#     Run Process    python3    ${SCRIPT_PATH}
#     Should Not Contain    ${OUTPUT}    [ERROR]


# *** Settings ***
# Library           Process
# Library           Collections
# Library           OperatingSystem
# Library           json

# *** Variables ***
# ${SCRIPT_PATH}    capture_and_detect.py
# ${PAYLOAD}        {"username": "user1", "streaming_URL": "https://www.youtube.com/live/o4F9RFUzpas?si=Sx8gHWnZ_akIOTw6", "email": "user1@example.com", "Monitoring_status": 1}

# *** Test Cases ***
# Test Get Stream URL
#     [Documentation]    Test the retrieval of stream URL using yt-dlp.
#     ${result}=    Run Process    python3    ${SCRIPT_PATH}    env:PAYLOAD=${PAYLOAD}    stderr=STDOUT
#     Log    ${result.stdout}
#     Should Contain    ${result.stdout}    Successfully retrieved stream URL

# Test Frame Capture
#     [Documentation]    Test capturing and processing frames.
#     ${result}=    Run Process    python3    ${SCRIPT_PATH}    env:PAYLOAD=${PAYLOAD}    stderr=STDOUT
#     Log    ${result.stdout}
#     Log    ${result.stderr}
#     Should Contain    ${result.stdout}    People Count:

# Test Database Insertion
#     [Documentation]    Ensure that results are inserted into the database correctly.
#     ${result}=    Run Process    python3    ${SCRIPT_PATH}    env:PAYLOAD=${PAYLOAD}    stderr=STDOUT
#     Log    ${result.stdout}
#     Log    ${result.stderr}
#     Should Not Contain    ${result.stdout}    [ERROR]
#     Should Contain    ${result.stdout}    Successfully inserted data into Result table

# *** Keywords ***
# Parse JSON Result
#     [Arguments]    ${json_string}
#     ${result}=    Evaluate    json.loads('''${json_string}''')    json
#     [Return]    ${result}