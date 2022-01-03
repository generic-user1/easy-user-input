

#test that `from easy_user_input import easy_user_input` is 
#the same as `from easy_user_input import eui`
def test_alias_from():
    from easy_user_input import eui
    from easy_user_input import easy_user_input
    assert eui == easy_user_input


#test that `import easy_user_input.easy_user_input` is 
#the same as `import easy_user_input.eui`
def test_alias_direct():
    import easy_user_input.eui
    import easy_user_input.easy_user_input #type: ignore
    #pylance incorrectly reports missing import here, so it is silenced
    assert easy_user_input.eui == easy_user_input.easy_user_input