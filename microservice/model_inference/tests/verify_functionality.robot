*** Settings ***
Library           RequestsLibrary
Library           SeleniumLibrary
Library           BuiltIn

*** Variables ***
${BASE_URL}       http://54.179.227.109/dev
${CONFIG_URL}     ${BASE_URL}/configs
${BROWSER}        Chrome

*** Test Cases ***

Test Front-End Accessibility
    [Documentation]    Verify the front-end is accessible and the title is correct.
    Open Browser       ${BASE_URL}    ${BROWSER}
    Wait Until Page Contains Element    id:main-content    10s
    Page Should Contain    Configuration Page
    [Teardown]    Close All Browsers

Test Configuration Endpoint
    [Documentation]    Verify the configuration endpoint is accessible and returns a valid response.
    ${response}=       GET    ${CONFIG_URL}
    Status Should Be   200
    Log To Console     ${response.status_code}
    Should Contain     ${response.body}    "configuration"
