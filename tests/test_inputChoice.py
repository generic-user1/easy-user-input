from easy_user_input.eui import inputChoice
from tests.simulatedIO import simulatedInput, simulatedOutput

TEST_CHOICES_NO_DESCRIPTIONS = ["choice 1", "choice 2", "choice 3"]
TEST_CHOICES_WITH_DESCRIPTIONS = [
    ("choice 1", "description 1"), 
    ("choice 2", "description 2"), 
    ("choice 3", "description 3")
    ]
TEST_CHOICES_MIXED_DESCRIPTIONS = [
    "choice 1", 
    ("choice 2", "description 2"), 
    "choice 3"
    ]
ALL_TEST_CHOICE_SETS = (
    TEST_CHOICES_NO_DESCRIPTIONS, 
    TEST_CHOICES_WITH_DESCRIPTIONS, 
    TEST_CHOICES_MIXED_DESCRIPTIONS
    )

#verify that the user prompt is displayed as expected
#verify that custom prompts are displayed as expected
def test_prompt():
    
    choices = TEST_CHOICES_NO_DESCRIPTIONS

    #check with default prompt text
    with simulatedInput("1"), simulatedOutput() as outStream:
        inputChoice(choices)
        outPrompt = outStream.getvalue()
    assert "Please select an option (number from 1 to 3):" in outPrompt

    #check with custom prompt text
    with simulatedInput("1"), simulatedOutput() as outStream:
        inputChoice(choices, promptText="{DELIMITER}")
        outPrompt = outStream.getvalue()
    assert "{DELIMITER} (number from 1 to 3):" in outPrompt

#verify that the prompt range is correct with different numbers of options
def test_prompt_range():

    #test with a single choice
    choices = ["single choice"]
    with simulatedInput("1"), simulatedOutput() as outStream:
        inputChoice(choices, promptText="{DELIMITER}")
        outPrompt = outStream.getvalue()
    promptText = outPrompt.split("{DELIMITER}")[1]
    assert promptText.startswith(" (number from 1 to 1): ")

    #test with two choices
    choices = ["choice 1", "choice 2"]
    with simulatedInput("1"), simulatedOutput() as outStream:
        inputChoice(choices, promptText="{DELIMITER}")
        outPrompt = outStream.getvalue()
    promptText = outPrompt.split("{DELIMITER}")[1]
    assert promptText.startswith(" (number from 1 to 2): ")

    #test with 25 choices
    choices = ["choice x"]*25
    with simulatedInput("1"), simulatedOutput() as outStream:
        inputChoice(choices, promptText="{DELIMITER}")
        outPrompt = outStream.getvalue()
    promptText = outPrompt.split("{DELIMITER}")[1]
    assert promptText.startswith(" (number from 1 to 25): ")


#verify that when a default value is set, it appears in the prompt correctly
def test_prompt_default_value():
    
    #test with no descriptions, with all descriptions, and with mixed descriptions
    #all the return values for each of these sets should be the same
    for choices in ALL_TEST_CHOICE_SETS:

        #test default of 0 (choice 1)
        with simulatedInput("\n"), simulatedOutput() as outStream:
            inputChoice(choices, promptText="{DELIMITER}", default=0)
            outPrompt = outStream.getvalue()
        #get the prompt and echoed value from the full output prompt
        promptText = outPrompt.split("{DELIMITER}")[1]
        assert promptText.startswith(" (number from 1 to 3, default '1' - choice 1)")

        #test default of 1 (choice 2)
        with simulatedInput("\n"), simulatedOutput() as outStream:
            inputChoice(choices, promptText="{DELIMITER}", default=1)
            outPrompt = outStream.getvalue()
        #get the prompt and echoed value from the full output prompt
        promptText = outPrompt.split("{DELIMITER}")[1]
        assert promptText.startswith(" (number from 1 to 3, default '2' - choice 2)")

        #test default of 2 (choice 3)
        with simulatedInput("\n"), simulatedOutput() as outStream:
            inputChoice(choices, promptText="{DELIMITER}", default=2)
            outPrompt = outStream.getvalue()
        #get the prompt and echoed value from the full output prompt
        promptText = outPrompt.split("{DELIMITER}")[1]
        assert promptText.startswith(" (number from 1 to 3, default '3' - choice 3)")


#verify that options are displaying properly
def test_options_listing():

    #define expected prompt values for each choice set
    assertionValues = (
        "1: choice 1\n2: choice 2\n3: choice 3\n\n",
        "1: choice 1 - description 1\n2: choice 2 - description 2\n3: choice 3 - description 3\n\n",
        "1: choice 1\n2: choice 2 - description 2\n3: choice 3\n\n"
    )

    #test with no descriptions, all descriptions, and mixed descriptions
    for choices, assertionVal in zip(ALL_TEST_CHOICE_SETS, assertionValues):

        with simulatedInput("1"), simulatedOutput() as outStream:
            inputChoice(choices, promptText="{DELIMITER}")
            outPrompt = outStream.getvalue()
        
        #split the output text by {DELIMITER} (the custom prompt text)
        #and only test the option list, not the prompt or response
        choicesStr = outPrompt.split("{DELIMITER}")[0]
        assert choicesStr == assertionVal


#verify that inputChoice returns the correct value
def test_return_value():

    #test with no descriptions, with all descriptions, and with mixed descriptions
    #all the return values for each of these sets should be the same
    
    for choices in ALL_TEST_CHOICE_SETS:

        with simulatedInput("1"):
            selectedChoice = inputChoice(choices)
        assert selectedChoice == 0

        with simulatedInput("2"):
            selectedChoice = inputChoice(choices)
        assert selectedChoice == 1
        
        with simulatedInput("3"):
            selectedChoice = inputChoice(choices)
        assert selectedChoice == 2
        

#verify that inputChoice returns the correct value
#when a default is used
def test_default_return_value():

    #test with no descriptions, with all descriptions, and with mixed descriptions
    #all the return values for each of these sets should be the same

    for choices in ALL_TEST_CHOICE_SETS:
        #test each default value
        for defaultVal in range(3):
            with simulatedInput("\n"):
                returnVal = inputChoice(choices, default=defaultVal)
            assert returnVal == defaultVal

        #test default values with user input
        for defaultVal in range(3):
            with simulatedInput("3"):
                returnVal = inputChoice(choices, default=defaultVal)
            assert returnVal == 2

            with simulatedInput("2"):
                returnVal = inputChoice(choices, default=defaultVal)
            assert returnVal == 1

            with simulatedInput("1"):
                returnVal = inputChoice(choices, default=defaultVal)
            assert returnVal == 0


#verify that inputChoice prints the correct value back to the user
#when an option is selected
def test_echo():

    #create assertion values for each option
    assertionValues = (
        " (number from 1 to 3): Selected '1' - choice 1\n",
        " (number from 1 to 3): Selected '2' - choice 2\n",
        " (number from 1 to 3): Selected '3' - choice 3\n"
        )
    
    #test with and without descriptions
    #all the values for these sets should be the same
    for choices in ALL_TEST_CHOICE_SETS:

        #test each option
        for index, assertionValue in enumerate(assertionValues):

            with simulatedInput(str(index + 1)), simulatedOutput() as outputStream:
                inputChoice(choices, promptText="{DELIMITER}")
                outputPrompt = outputStream.getvalue()
            #get the prompt and echoed value from the full output prompt
            promptAndEcho = outputPrompt.split("{DELIMITER}")[1]
            assert promptAndEcho == assertionValue


#verify that inputChoice prints the correct value back to the user
#when no input is entered an a default value is set
def test_echo_default_value():

    #define assertion values for each default value
    assertionValues = (
        "No response; defaulting to '1' - choice 1\n",
        "No response; defaulting to '2' - choice 2\n",
        "No response; defaulting to '3' - choice 3\n"
    )

    #test with and without descriptions
    #all the values for these sets should be the same
    for choices in ALL_TEST_CHOICE_SETS:
        #test default 0 (choice 1)
        for defaultVal, assertionVal in enumerate(assertionValues):
            with simulatedInput("\n"), simulatedOutput() as outputStream:
                inputChoice(choices, promptText="{DELIMITER}", default=defaultVal)
                outputPrompt = outputStream.getvalue()
            assert outputPrompt.endswith(assertionVal)


#verify the output for cases where the user's input is invalid
def test_invalid_input():

    #test with and without descriptions
    #all the values for these sets should be the same
    for choices in ALL_TEST_CHOICE_SETS:
        with simulatedInput("something invalid\n1"), simulatedOutput() as outputStream:
            inputChoice(choices, promptText="{DELIMITER}")
            outputPrompt = outputStream.getvalue()
        invalidWarningText = outputPrompt.split("{DELIMITER}")[1]
        assert invalidWarningText.startswith(' (number from 1 to 3): Invalid input: "something invalid". Please choose a number from 1 to 3.')

        #test with default value
        with simulatedInput("something invalid\n1"), simulatedOutput() as outputStream:
            inputChoice(choices, promptText="{DELIMITER}", default=0)
            outputPrompt = outputStream.getvalue()
        invalidWarningText = outputPrompt.split("{DELIMITER}")[1]
        assert invalidWarningText.startswith(" (number from 1 to 3, default '1' - choice 1): Invalid input: \"something invalid\". Please choose a number from 1 to 3.")

        
    #test with a different number of choices
    choices = ["choice"]*5
    with simulatedInput("something invalid\n1"), simulatedOutput() as outputStream:
        inputChoice(choices, promptText="{DELIMITER}")
        outputPrompt = outputStream.getvalue()
    invalidWarningText = outputPrompt.split("{DELIMITER}")[1]
    assert invalidWarningText.startswith(' (number from 1 to 5): Invalid input: "something invalid". Please choose a number from 1 to 5.')
