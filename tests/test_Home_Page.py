from streamlit.testing.v1 import AppTest


# This might be problematic
# 1. Some updated elements aren't present in AppTest
# 2. Can't even print some present elements

def test_no_interaction():
    at = AppTest.from_file("../Home_Page.py")
    at.run()
    # assert at.session_state["authentication_status"] is None
    print("text_input: ", len(at.text_input))
    print("warning: ", len(at.warning))
    print("success: ", len(at.success))
    print("button: ", len(at.button))
    print("All TextInputs: ")
    print(at.get(element_type="TextInput"))
    print("All buttons: ")
    print(at.get(element_type="button"))
    print("All text: ")
    print(at.get(element_type="text"))
    print("All radios: ")
    print(at.get(element_type="radio"))
    print("All dividers: ")
    print(at.get(element_type="divider"))

    print("All date_inputs: ")
    print(at.get(element_type="date_input"))
    print("All sidebars: ")
    print(at.get(element_type="sidebar"))
    print("All titles: ")
    print(at.get(element_type="title"))
    print("All markdowns: ")
    print(at.get(element_type="markdown"))
    print("All captions: ")
    print(at.get(element_type="caption"))
    print("All tabs: ")
    print(at.get(element_type="tabs"))
    print("All columnss: ")
    print(at.get(element_type="columns"))

    assert len(at.text_input) == 7
    assert len(at.warning) == 0
    assert len(at.success) == 0
    assert len(at.button) == 0
    assert at.text_input[0].value == ""


def test_incorrect_password():
    at = AppTest.from_file("../Home_Page.py")
    at.secrets["password"] = "streamlit"
    at.run()
    at.text_input[0].input("balloon").run()
    assert at.session_state["status"] == "incorrect"
    assert len(at.text_input) == 1
    assert len(at.warning) == 1
    assert len(at.success) == 0
    assert len(at.button) == 0
    assert at.text_input[0].value == ""
    assert "Incorrect password" in at.warning[0].value


def test_correct_password():
    at = AppTest.from_file("app.py")
    at.secrets["password"] = "streamlit"
    at.run()
    at.text_input[0].input("streamlit").run()
    assert at.session_state["status"] == "verified"
    assert len(at.text_input) == 0
    assert len(at.warning) == 0
    assert len(at.success) == 1
    assert len(at.button) == 1
    assert "Login successful" in at.success[0].value
    assert at.button[0].label == "Log out"


def test_log_out():
    at = AppTest.from_file("app.py")
    at.secrets["password"] = "streamlit"
    at.session_state["status"] = "verified"
    at.run()
    at.button[0].click().run()
    assert at.session_state["status"] == "unverified"
    assert len(at.text_input) == 1
    assert len(at.warning) == 0
    assert len(at.success) == 0
    assert len(at.button) == 0
    assert at.text_input[0].value == ""


test_no_interaction()
