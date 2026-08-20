from mcplane.server.mock_server import MockMcpServer


def test_mock_list_tools():
    s = MockMcpServer()
    result = s.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
    assert len(result["tools"]) == 2


def test_mock_echo():
    s = MockMcpServer()
    result = s.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                       "params": {"name": "echo", "arguments": {"text": "hi"}}})
    assert result["content"][0]["text"] == "hi"


def test_mock_calculator():
    s = MockMcpServer()
    result = s.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                       "params": {"name": "calculator", "arguments": {"expression": "1+2*3"}}})
    assert result["content"][0]["text"] == "7"


def test_mock_ping():
    s = MockMcpServer()
    assert s.handle({"method": "ping"}) == {}


def test_mock_unknown_method():
    s = MockMcpServer()
    result = s.handle({"method": "nope"})
    assert "error" in result
