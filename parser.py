import re
from ast_nodes import Item, Category, FunctionCall

def parse_receipt_dsl(dsl_text: str):
    lines = dsl_text.strip().split("\n")
    i = 0
    ast = []

    def parse_block(indent_level=0):
        nonlocal i
        block = []

        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            if line.startswith("kategorie "):
                match = re.match(r'kategorie\s+(\w+)\s*\{', line)
                if not match:
                    raise SyntaxError(f"Neplatná syntaxe kategorie: {line}")
                name = match.group(1)
                i += 1
                items = parse_block(indent_level + 1)
                block.append(Category(name=name, items=items))

            elif line == "}":
                i += 1
                break

            elif "=" in line and not line.startswith("filtrovano") and not line.startswith("suma"):
                name, expr = line.split("=", 1)
                block.append(Item(name.strip(), expr.strip()))
                i += 1

            elif "(" in line and line.endswith(")"):
                match = re.match(r"(\w+)\((.*?)\)", line)
                if match:
                    func_name = match.group(1)
                    argument = match.group(2).strip()
                    block.append(FunctionCall(name=func_name, argument=argument))
                    i += 1
                else:
                    raise SyntaxError(f"Neplatná syntaxe funkce: {line}")

            else:
                raise SyntaxError(f"Neznámý řádek: {line}")

        return block

    ast = parse_block()
    return ast
