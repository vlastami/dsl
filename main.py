from parser import parse_receipt_dsl
from evaluator import evaluate

import os

def main():
    path = os.path.join("sample", "nakup.receipt")
    with open(path, encoding="utf-8") as f:
        dsl_input = f.read()

    try:
        ast = parse_receipt_dsl(dsl_input)
        evaluate(ast)
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()
