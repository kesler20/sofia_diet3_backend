import json
from typing import Union, Any, Dict, TypedDict, Tuple
from dataclasses import dataclass, field


@dataclass
class DietBase:

    __name: str = "Diet Base"
    __total: Dict[str, Any] = field(default_factory=lambda: {"protein": 0, "calories": 0,
                                                             "cost": 0.0, "amount": 0.0, "name": []})

    def __add__(self, other):
        if type(other) == type(self):
            self.__total = {k: self[k] + other[k] for k in self.__total.keys()}
            self.__total["name"].append(other.name)
            return self
        else:
            raise TypeError

    def __repr__(self) -> str:
        return json.dumps({k.replace("_DietBase__", ""): self.__dict__[k] for k in self.__dict__.keys()})

    def __mul__(self, amount: Union[int, float]):
        if type(amount) == int or type(amount) == float:
            self.__total: Dict[str, Any] = {
                k: self[k] * amount for k in self.__total.keys()}
            return self
        else:
            raise TypeError

    def __getitem__(self, k):
        return self.__total[k]

    def set_name(self, name: str):
        self.__name = name
        return self

    def set_protein(self, protein: int):
        self.__total["protein"] = protein
        return self

    def set_calories(self, calories: int):
        self.__total["calories"] = calories
        return self

    def set_cost(self, cost: float):
        self.__total["cost"] = cost
        return self

    def set_amount(self, amount: float):
        self.__total["amount"] = amount
        return self

    def set_total(self, total: Dict[str, Any]):
        """the total dictionary requires { protein, calories, cost, amount}"""
        self.__total = total
        return self

    @property
    def total(self) -> Dict[str, Any]:
        return self.__total

    @property
    def name(self) -> str:
        return self.__name

    @property
    def protein(self):
        return self.__total["protein"]

    @property
    def calories(self):
        return self.__total["calories"]

    @property
    def cost(self):
        return self.__total["cost"]

    @property
    def amount(self):
        return self.__total["amount"]

    @property
    def data(self) -> Dict[str, Any]:
        return {**self.__total, **{k.replace("__", ""): self.__dict__[k] for k in self.__dict__.keys()}}

    @property
    def columns(self) -> Dict[str, Any]:
        return {k: type(self.data[k]) for k in self.data.keys()}
