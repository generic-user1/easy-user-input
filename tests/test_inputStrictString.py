from easy_user_input.eui import inputStrictString
from tests.simulatedIO import simulatedInput, simulatedOutput


#verify the prompt text is displayed as expected
def test_prompt():

    #test without a default value
    with simulatedInput("testIn"), simulatedOutput() as outStream:
        inputStrictString("test prompt")
        outPrompt = outStream.getvalue()
    assert outPrompt == "test prompt: "

    #test with a default value
    with simulatedInput("testIn"), simulatedOutput() as outStream:
        inputStrictString("test prompt", default="default value")
        outPrompt = outStream.getvalue()
    assert outPrompt == "test prompt (default 'default value'): "

#verify the return value with and without defaults
def test_return_value():
    
    #TODO: potentially add more test values
    testValues = ("testIn", "test_in", "TEST_in3234")
    
    #test without a default
    for testVal in testValues:
        with simulatedInput(testVal):
            returnVal = inputStrictString("test prompt")

        assert returnVal == testVal
    
    #test with a default value
    #despite having a default value, all of the standard test values
    #should still return as normal
    for testVal in testValues:
        with simulatedInput(testVal):
            returnVal = inputStrictString("test prompt", default="default string")

        assert returnVal == testVal

    #test default value with no input
    with simulatedInput("\n"):
        returnVal = inputStrictString("test prompt", default="default string")
    
    assert returnVal == "default string"


#validate that charset based rejection functions with different charsets
#and the warning output when invalid input is entered
def test_charset():

    #test default charset
    with simulatedInput("bad input**\ngoodinput"), simulatedOutput() as outStream:
        inputStrictString("{DELIMITER}")
        outPrompt = outStream.getvalue()

    warningText = outPrompt.split("{DELIMITER}")[1]

    assert warningText == ": Invalid input: 'bad input**'\n"

    #test custom charset
    with simulatedInput("bad input\n1234"), simulatedOutput() as outStream:
        inputStrictString("{DELIMITER}", allowedChars="123456789")
        outPrompt = outStream.getvalue()

    warningText = outPrompt.split("{DELIMITER}")[1]

    assert warningText == ": Invalid input: 'bad input'\n"
