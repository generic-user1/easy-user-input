from simulatedIO import simulatedInput, simulatedOutput
from easy_user_input.eui import inputPath
from os import path

#path to a directory that is known to exist
EXISTING_DIRECTORY_PATH = path.join(path.split(__file__)[0], "existingDirectory")

#path to a file that is known to exist
EXISTING_FILE_PATH = path.join(EXISTING_DIRECTORY_PATH, "existingFile")

#verify that prompt text is displayed as expected
def test_prompt():

    #test default prompt
    with simulatedInput("testIn"), simulatedOutput() as outStream:
        inputPath()
        outPrompt = outStream.getvalue()
    assert outPrompt == "Please input a valid path (new file): "

    #test non-default prompt
    with simulatedInput("testIn"), simulatedOutput() as outStream:
        inputPath("test prompt")
        outPrompt = outStream.getvalue()
    assert outPrompt == "test prompt (new file): "

#verify that reject mode only accepts new files
def test_reject_mode():
    
    #test with a new file
    with simulatedInput("testIn"), simulatedOutput():
        acceptedPath = inputPath("test prompt", "reject")
    assert acceptedPath == path.abspath("testIn")
    
    #test with an existing file (followed by a new file)
    with simulatedInput(EXISTING_FILE_PATH+"\ntestIn"), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "reject")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath("testIn")
    assert outPrompt.startswith("test prompt (new file): Cannot use path")
    assert outPrompt.split("\n")[0].endswith("because it already exists!")


    #test with an existing directory (followed by a new file)
    with simulatedInput(EXISTING_DIRECTORY_PATH+"\ntestIn"), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "reject")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath("testIn")
    assert outPrompt.startswith("test prompt (new file): Cannot use path")
    assert outPrompt.split("\n")[0].endswith(" because it already exists!")


#verify that warn mode accepts new files and warns about existing ones
def test_warn_mode():
    
    #test with a new file
    with simulatedInput("testIn"), simulatedOutput():
        acceptedPath = inputPath("test prompt", "warn")
    assert acceptedPath == path.abspath("testIn")
    
    #test with an existing file (and accept)
    with simulatedInput(EXISTING_FILE_PATH+"\ny"), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "warn")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_FILE_PATH)
    assert outPrompt.startswith("test prompt (file): ")
    assert outPrompt.endswith("already exists.\nOverwrite? (y/n, default 'n'): ")

    #test with an existing file, reject, then with a new file
    with simulatedInput(EXISTING_FILE_PATH+"\nn\ntestIn"), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "warn")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath("testIn")
    assert outPrompt.startswith("test prompt (file): ")
    
#verify that accept mode accepts new and existing files
def test_accept_mode():
    
    #test with a new file
    with simulatedInput("testIn"), simulatedOutput():
        acceptedPath = inputPath("test prompt", "accept")
    assert acceptedPath == path.abspath("testIn")
    
    #test with an existing file 
    with simulatedInput(EXISTING_FILE_PATH), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "accept")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_FILE_PATH)
    assert outPrompt.startswith("test prompt (file): ")

#verify that require mode accepts only existing files
def test_require_mode():
    
    #test with an existing file directly
    with simulatedInput(EXISTING_FILE_PATH), simulatedOutput():
        acceptedPath = inputPath("test prompt", "require")
    assert acceptedPath == path.abspath(EXISTING_FILE_PATH)

    #test with a new file followed by an existing file
    with simulatedInput("testIn\n"+EXISTING_FILE_PATH), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "require")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_FILE_PATH)
    assert outPrompt.startswith("test prompt (file): Cannot use path ")
    assert outPrompt.split("\n")[0].endswith(" because it doesn't exist!")
    
    #test with an existing directory followed by an existing file
    with simulatedInput(EXISTING_DIRECTORY_PATH+"\n"+EXISTING_FILE_PATH), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "require")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_FILE_PATH)
    assert outPrompt.startswith("test prompt (file): Cannot use path ")
    assert outPrompt.split("\n")[0].endswith(" because it is a directory!")
    

#verify that directory mode accepts only existing directories
def test_directory_mode():
    
    #test with an existing directory directly
    with simulatedInput(EXISTING_DIRECTORY_PATH), simulatedOutput():
        acceptedPath = inputPath("test prompt", "directory")
    assert acceptedPath == path.abspath(EXISTING_DIRECTORY_PATH)

    #test with a new directory followed by an existing directory
    with simulatedInput("testIn\n"+EXISTING_DIRECTORY_PATH), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "directory")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_DIRECTORY_PATH)
    assert outPrompt.startswith("test prompt (directory): Cannot use path ")
    assert outPrompt.split("\n")[0].endswith(" because it is not a directory!")
    
    #test with an existing file followed by an existing directory
    with simulatedInput(EXISTING_FILE_PATH+"\n"+EXISTING_DIRECTORY_PATH), simulatedOutput() as outStream:
        acceptedPath = inputPath("test prompt", "directory")
        outPrompt = outStream.getvalue()
    assert acceptedPath == path.abspath(EXISTING_DIRECTORY_PATH)
    assert outPrompt.startswith("test prompt (directory): Cannot use path ")
    assert outPrompt.split("\n")[0].endswith(" because it is not a directory!")