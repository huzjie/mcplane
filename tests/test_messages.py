from mcplane.spec.messages import (
    Tool, ListToolsResult, CallToolResult, ContentBlock, InputRequiredResult,
)


def test_tool_to_dict():
    t = Tool(name="echo", description="echo back")
    d = t.to_dict()
    assert d["name"] == "echo"
    assert d["description"] == "echo back"


def test_list_tools_result():
    r = ListToolsResult(tools=[Tool(name="a")])
    d = r.to_dict()
    assert d["tools"][0]["name"] == "a"


def test_call_tool_result_error_flag():
    r = CallToolResult(content=[ContentBlock(text="boom")], is_error=True)
    d = r.to_dict()
    assert d["isError"] is True


def test_input_required():
    r = InputRequiredResult(question="confirm?", options=["yes", "no"])
    d = r.to_dict()
    assert d["resultType"] == "input_required"
    assert d["question"] == "confirm?"
