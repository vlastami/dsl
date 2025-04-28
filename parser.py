from parsy import string, regex, seq, alt, generate
from ast_nodes import Item, Category, FunctionCall

# --- Parsování základních věcí (tokenů) ---

whitespace = regex(r'[ \t]*')
newline = regex(r'\s*\n\s*')
comment = regex(r'#.*').skip(newline.optional())
empty_line = whitespace.skip(newline)

ignored = (whitespace >> (comment | empty_line).many())

identifier = regex(r'[a-zA-ZÀ-ſ_][a-zA-Z0-9À-ſ_]*')
number = regex(r'\d+(\.\d+)?')
expression = regex(r'.+')  

lbrace = ignored.then(string('{')).skip(ignored)
rbrace = ignored.then(string('}')).skip(ignored)
equals = ignored.then(string('=')).skip(ignored)

# --- Parsování konstrukcí jazyka (item, funkce, kategorie) ---

@generate
def item():
    yield ignored
    name = yield identifier.skip(whitespace)   # název položky
    yield equals                               # rovnítko
    expr = yield expression.map(str.strip)     # výraz napravo
    yield (newline | ignored).optional()       # nový řádek (nebo konec)
    return Item(name=name, value_expr=expr)

@generate
def function_call():
    yield ignored
    func_name = yield identifier               # název funkce
    yield string('(')
    arg = yield regex(r'[^)]*').map(str.strip)  # argument vevnitř (cokoliv až do ')')
    yield string(')')
    yield (newline | ignored).optional()
    return FunctionCall(name=func_name, argument=arg)

@generate
def category():
    yield ignored
    yield string('kategorie').skip(whitespace)  # slovo "kategorie"
    cat_name = yield identifier.skip(whitespace)  # jméno kategorie
    yield lbrace
    items = yield block                         # vnořený blok
    yield rbrace
    yield (newline | ignored).optional()
    return Category(name=cat_name, items=items)

# --- Rekurzivní blok věcí uvnitř (položky, funkce, kategorie) ---

@generate
def block():
    statements = yield (ignored.then(item | function_call | category)).many()
    return statements

# --- Vstupní bod - hlavní parser ---

def parse_receipt_dsl(text: str):
    try:
        result = block.parse(text.strip())  # začnu parsovat od začátku
        return result
    except Exception as e:
        raise SyntaxError(f"Chyba při parsování: {e}")
