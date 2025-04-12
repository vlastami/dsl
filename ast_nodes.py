from dataclasses import dataclass
from typing import List, Union

@dataclass
class Item:
    name: str
    value_expr: str  

@dataclass
class Category:
    name: str
    items: List[Union['Item', 'Category']]  # rekurzivní struktura

@dataclass
class FunctionCall:
    name: str
    argument: str = None
