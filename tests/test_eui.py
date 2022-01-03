

#test that `easy_user_input.easy_user_input` is 
#the same module as `easy_user_input.eui`
def test_easy_user_input_alias():
    from easy_user_input import eui
    from easy_user_input import easy_user_input
    assert eui == easy_user_input

