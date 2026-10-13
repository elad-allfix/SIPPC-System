"""A scripted model client for testing the strategist plumbing (not model quality)."""


class FakeModelClient:
    def __init__(self, script):
        self.script = list(script)
        self.requests = []

    async def stream_turn(self, spec, system, messages, tools):
        self.requests.append({"model": spec.model, "messages": messages, "tools": [t["name"] for t in tools]})
        if not self.script:
            raise RuntimeError("fake model: script exhausted")
        step = self.script.pop(0)
        if isinstance(step, Exception):
            raise step
        content, stop = step
        for block in content:
            if block["type"] == "text":
                yield {"type": "text", "text": block["text"]}
            elif block["type"] in ("tool_use", "server_tool_use"):
                yield {"type": "tool_input", "name": block["name"], "id": block["id"], "input": block["input"]}
            elif block["type"].endswith("_tool_result"):
                yield {"type": "server_tool_result", "block": block}
        yield {"type": "final", "content": content, "stop_reason": stop, "model": spec.model,
               "usage": {"input_tokens": 10, "output_tokens": 5}}


def text(t, citations=None):
    b = {"type": "text", "text": t}
    if citations:
        b["citations"] = citations
    return b


def tool(id_, name, input_):
    return {"type": "tool_use", "id": id_, "name": name, "input": input_}
