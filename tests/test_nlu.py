from backend.nlu.parser import parse_message, list_intents


def test_intent_listing():
    assert set(list_intents()) >= {"join", "done"}


def test_join_intent():
    assert parse_message("I would like to JOIN the programme") == "join"
    assert parse_message("start") == "join"


def test_done_intent():
    assert parse_message("done") == "done"
    assert parse_message("I've completed") == "done"


def test_unknown_intent():
    assert parse_message("foo bar baz") == "unknown"


def test_spanish_join_intent():
    assert parse_message("¡Únete ahora!") == "join"


def test_hindi_done_intent():
    assert parse_message("मैंने पूरा किया") == "done"