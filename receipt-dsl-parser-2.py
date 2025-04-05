import re
import json

def parse_receipt_dsl(dsl_text):
    item_pattern = re.compile(r"^\s*(.+?)\s*=\s*([\d.]+)\s*$")
    items = []

    for line in dsl_text.strip().split("\n"):
        if not line.strip():
            continue
        match = item_pattern.match(line)
        if match:
            name = match.group(1)
            price = float(match.group(2))
            items.append({"item": name, "price": price})
        else:
            print(f"❌ Neplatný řádek: {line}")
    
    return items

def main():
    dsl_input = """
    rohlík = 3.5
    mléko = 28
    čokoláda = 24.90
    """

    parsed = parse_receipt_dsl(dsl_input)
    total = sum(item["price"] for item in parsed)

    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    print(f"Celkem: {total:.2f} Kč")

if __name__ == "__main__":
    main()
