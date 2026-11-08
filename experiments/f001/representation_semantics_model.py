#!/usr/bin/env python3
"""F-001-J: compare AST evaluation with a tiny stack-bytecode implementation."""


def interpret(expr, env):
    op = expr[0]
    if op == "const":
        return expr[1]
    if op == "var":
        return env[expr[1]]
    if op == "add":
        return interpret(expr[1], env) + interpret(expr[2], env)
    if op == "mul":
        return interpret(expr[1], env) * interpret(expr[2], env)
    raise ValueError(f"unknown expression: {expr!r}")


def compile_expr(expr):
    op = expr[0]
    if op == "const":
        return [("PUSH", expr[1])]
    if op == "var":
        return [("LOAD", expr[1])]
    if op in ("add", "mul"):
        instruction = "ADD" if op == "add" else "MUL"
        return compile_expr(expr[1]) + compile_expr(expr[2]) + [(instruction,)]
    raise ValueError(f"unknown expression: {expr!r}")


def execute(code, env):
    stack = []
    for instruction in code:
        op = instruction[0]
        if op == "PUSH":
            stack.append(instruction[1])
        elif op == "LOAD":
            stack.append(env[instruction[1]])
        elif op in ("ADD", "MUL"):
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right if op == "ADD" else left * right)
        else:
            raise ValueError(f"unknown instruction: {instruction!r}")
    if len(stack) != 1:
        raise RuntimeError(f"invalid final stack: {stack!r}")
    return stack[0]


def main():
    expression = (
        "add",
        ("mul", ("const", 3), ("var", "x")),
        ("const", 2),
    )
    environment = {"x": 4}
    ast_result = interpret(expression, environment)
    bytecode = compile_expr(expression)
    vm_result = execute(bytecode, environment)

    assert ast_result == 14
    assert vm_result == ast_result
    print(f"AST interpreter result: {ast_result}")
    print(f"bytecode evaluator result: {vm_result}")
    print(f"generated instructions: {len(bytecode)}")
    print("PASS: representation semantics assertions satisfied")


if __name__ == "__main__":
    main()
