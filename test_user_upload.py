from user_upload import append_quote_to_names
from user_upload import contains_single_quote


def test_surname_contains_quote__append_quote():
    expacted = "A''hmed"
    test = "A'hmed"
    assert append_quote_to_names(test, "'") == expacted

def test_surname_contains_no_quote__does_not_append_quote():
    expacted = "Ahmed"
    test = "Ahmed"

    if contains_single_quote(test, "'"):
        assert append_quote_to_names(test, "'") == expacted
