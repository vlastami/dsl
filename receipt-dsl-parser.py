import re
import json
import sys
from pathlib import Path

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
    if len(sys.argv) < 2:
        print("Použití: python receipt_dsl_parser.py <soubor.receipt>")
        return

    receipt_file = Path(sys.argv[1])
    if not receipt_file.exists():
        print(f"Soubor {receipt_file} neexistuje.")
        return

    dsl_input = receipt_file.read_text(encoding="utf-8")
    parsed = parse_receipt_dsl(dsl_input)
    total = sum(item["price"] for item in parsed)

    print("📦 Položky:")
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    print(f"\n💰 Celkem: {total:.2f} Kč")

if __name__ == "__main__":
    main()
