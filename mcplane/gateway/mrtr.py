"""Multi Round-Trip Requests (MRTR) handler.

In the stateless spec, a server can request additional input mid-flight by
returning ``resultType == "input_required"``. The client then re-issues the
same request with an ``inputResponses`` body, up to a configurable maximum
number of round trips, all without a session.
"""

from typing import Any, Dict, Optional

from ..errors import ProtocolError
from ..spec.messages import InputRequiredResult


class MultiRoundTripHandler:
    def __init__(self, max_round_trips: int = 8):
        self.max_round_trips = max_round_trips

    def needs_input(self, result: Any) -> bool:
        return (
            isinstance(result, dict)
            and result.get("resultType") == "input_required"
        )

    def extract_question(self, result: Dict) -> InputRequiredResult:
        return InputRequiredResult(
            question=str(result.get("question", "")),
            options=[str(o) for o in (result.get("options") or [])],
        )

    def build_responses(self, request_id, method: str, params: Dict,
                        responses: list) -> Dict:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": {
                **params,
                "inputResponses": responses,
            },
        }

    def guard(self, round_trip: int):
        if round_trip > self.max_round_trips:
            raise ProtocolError(
                "exceeded max round trips (%d)" % self.max_round_trips
            )
