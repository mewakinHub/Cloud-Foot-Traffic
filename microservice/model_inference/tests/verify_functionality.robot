*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            http://54.179.227.109/dev/configs
${BROWSER}        Chrome

*** Test Cases ***
Test Front-End Availability
    [Documentation]    Open the front-end URL and verify it loads successfully.
    Open Browser    ${URL}    ${BROWSER}
    Wait Until Page Contains Element    body    timeout=10s
    [Teardown]      Close All Browsers
