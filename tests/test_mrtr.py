from mcplane.gateway.mrtr import MultiRoundTripHandler
from mcplane.errors import ProtocolError


def test_needs_input():
    h = MultiRoundTripHandler()
    assert h.needs_input({"resultType": "input_required", "question": "x"})
    assert not h.needs_input({"resultType": "complete"})


def test_extract_question():
    h = MultiRoundTripHandler()
    q = h.extract_question({"resultType": "input_required", "question": "ok?"})
    assert q.question == "ok?"


def test_guard_exceeded():
    h = MultiRoundTripHandler(max_round_trips=2)
    try:
        h.guard(3)
        assert False
    except ProtocolError:
        pass
