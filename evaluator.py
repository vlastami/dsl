import re
from ast_nodes import Item, Category, FunctionCall
from typing import List, Union

def eval_expr(expr: str) -> float:
    try:
        return eval(expr, {"__builtins__": {}})
    except Exception as e:
        raise ValueError(f"Chyba při vyhodnocení výrazu '{expr}': {e}")

def evaluate(ast: List[Union[Item, Category, FunctionCall]]):
    all_items = []

    def flatten_items(node):
        if isinstance(node, Item):
            return [node]
        elif isinstance(node, Category):
            items = []
            for sub in node.items:
                items.extend(flatten_items(sub))
            return items
        else:
            return []

    for node in ast:
        all_items.extend(flatten_items(node))

    total = sum(eval_expr(item.value_expr) for item in all_items)

    for node in ast:
        if isinstance(node, FunctionCall):
            if node.name == "celkem":
                print(f"Celková cena: {total:.2f} Kč")

            elif node.name == "polozky":
                for item in all_items:
                    print(f"{item.name}: {eval_expr(item.value_expr):.2f} Kč")

            elif node.name == "filtrovano":
                try:
                    arg_match = re.match(r"min\s*=\s*([\d.]+)", node.argument)
                    if arg_match:
                        min_price = float(arg_match.group(1))
                        for item in all_items:
                            price = eval_expr(item.value_expr)
                            if price >= min_price:
                                print(f"{item.name}: {price:.2f} Kč")
                    else:
                        print(f"Neplatný argument pro filtrovano: {node.argument}")
                except Exception as e:
                    print(f"Chyba při filtrování: {e}")

            elif node.name == "suma":
                category_name = node.argument.strip()
                def suma_kategorie(nodes):
                    suma = 0.0
                    for n in nodes:
                        if isinstance(n, Category) and n.name == category_name:
                            for sub in flatten_items(n):
                                suma += eval_expr(sub.value_expr)
                    return suma
                print(f"Suma pro kategorii {category_name}: {suma_kategorie(ast):.2f} Kč")

            else:
                print(f"Neznámá funkce: {node.name}")
