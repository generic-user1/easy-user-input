from easy_user_input.eui import inputYesNo
from simulatedIO import simulatedInput, simulatedOutput

#verify that the default prompt text is as expected,
#and the prompt structure is normal
def test_default_prompt():

    with simulatedInput("y"), simulatedOutput() as promptStream:
        inputYesNo()
        promptText = promptStream.getvalue()

    assert promptText == "Choose yes or no (y/n): "

#verify that custom prompts are displayed properly
def test_custom_prompt():

    with simulatedInput("y"), simulatedOutput() as promptStream:
        inputYesNo("**custom prompt**")
        promptText = promptStream.getvalue()
    assert promptText == "**custom prompt** (y/n): "


#verify that default values are displayed properly and accepted when no input is given
def test_default_values():

    with simulatedInput("\n"), simulatedOutput() as promptStream:
        result = inputYesNo("", default=True)
        promptText = promptStream.getvalue()

    assert result == True
    assert promptText == " (y/n, default 'y'): No response; defaulting to 'y'\n"

    with simulatedInput("\n"), simulatedOutput() as promptStream:
        result = inputYesNo("", default=False)
        promptText = promptStream.getvalue()

    assert result == False
    assert promptText == " (y/n, default 'n'): No response; defaulting to 'n'\n"


#verify that all accepted forms of 'yes' result in a boolean True
def test_yes():
    
    yesAliases = ("y", "Y", "yes", "YES", "YeS", "yES", "YEs")
    for yesAlias in yesAliases:
        with simulatedInput(yesAlias):
            result = inputYesNo()
        assert result == True


#verify that all accepted forms of 'no' result in a boolean True
def test_no():
    
    noAliases = ("n", "N", "no", "NO", "No", "nO")
    for noAlias in noAliases:
        with simulatedInput(noAlias):
            result = inputYesNo()
        assert result == False


#verify the output for cases when the user's input is invalid
def test_invalid_input():

    #test with no default
    with simulatedInput("something invalid\ny"), simulatedOutput() as promptStream:
        inputYesNo("")
        promptText = promptStream.getvalue()

    assert promptText == ' (y/n): Invalid input: "something invalid". Please choose (y)es or (n)o.\n (y/n): '

    #test with default yes
    with simulatedInput("something invalid\ny"), simulatedOutput() as promptStream:
        inputYesNo("", True)
        promptText = promptStream.getvalue()

    assert promptText == " (y/n, default 'y'): Invalid input: \"something invalid\". Please choose (y)es or (n)o.\n (y/n, default 'y'): "

    #test with default no
    with simulatedInput("something invalid\ny"), simulatedOutput() as promptStream:
        inputYesNo("", False)
        promptText = promptStream.getvalue()

    assert promptText == " (y/n, default 'n'): Invalid input: \"something invalid\". Please choose (y)es or (n)o.\n (y/n, default 'n'): "
