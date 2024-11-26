*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Verify Application Starts
    [Documentation]    Ensure the application starts successfully
    GET    http://localhost:8000/health
    Should Be Equal As Strings    ${response.status_code}    200
