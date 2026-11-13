"""Toy model: representation ambiguity and information-flow boundaries.

This is an explanatory finite model, not a serializer or security proof.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Payload:
    raw: bytes
    schema: str | None = None
    label: str = "public"

def interpret(payload: Payload, schema: str | None = None):
    selected = schema or payload.schema
    if selected == "utf8":
        return payload.raw.decode("utf-8")
    if selected == "uint8":
        return int.from_bytes(payload.raw, "big")
    if selected is None:
        return payload.raw
    raise ValueError(f"unsupported schema: {selected}")

def may_flow(source: str, destination: str) -> bool:
    # Simplified two-level policy: public may flow anywhere; secret only to secret.
    return source == "public" or destination == "secret"

if __name__ == "__main__":
    raw = b"A"
    untyped = Payload(raw)
    typed_text = Payload(raw, schema="utf8")
    typed_number = Payload(raw, schema="uint8")
    assert interpret(untyped) == b"A"
    assert interpret(typed_text) == "A"
    assert interpret(typed_number) == 65
    assert may_flow("public", "secret")
    assert not may_flow("secret", "public")
    print("same bytes, three interpretations:", interpret(untyped), interpret(typed_text), interpret(typed_number))
    print("flow secret -> public:", may_flow("secret", "public"))
