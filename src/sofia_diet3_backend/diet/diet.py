import json
from typing import Union, Any, Dict, List

Number = Union[int, float]


class DietBase(object):

    def __init__(self, name: str) -> None:
        self.__name = [name]
        self.__total: Dict[str, Number] = {}

    @property
    def name(self) -> str:
        return self.__name

    @property
    def total(self) -> Dict[str, Number]:
        return self.__total

    def set_total(self, total: Dict[str, Number]) -> Any:
        for k in total.keys():
            if k.find("name") == -1 and k.find("Name") == -1 and k.find("NAME") == -1:
                self.total[k] = total[k]
        return self

    def __add__(self, other: Any):
        if type(other) == type(self) and self.__total.keys() == other.total.keys():
            self.__total = {k: self.total[k] + ", " + other.total[k]
                            if type(other.total[k]) == str else self.total[k] + other.total[k] for k in self.__total.keys()}
            self.__name = self.name + other.name

        return self

    def __mul__(self, amount: Number):
        if type(amount) != int and type(amount) != float:
            return self

        self.__total = {k: self.total[k] if type(self.total[k]) == str else self.total[k] * amount for k in self.__total.keys()}
        return self

    def __repr__(self) -> str:
        return json.dumps({"name": self.name, **self.total})


class Food(DietBase):
    """To instantiate a food object

    ```python    
    # instantiate a new Food object
    new_food = Food(food["name"]).set_total(food)
    ```
    this can be done as set_total will return the new food object
    """
    pass


class DietBaseCollection(DietBase):

    def set_data(self, collection: List[Dict[str, Number]]):
        food_collection: List[Food] = [Food(food["name"]).set_total(food) for food in collection]
        initial_food = food_collection[0]
        for food in food_collection[1:]:
            initial_food = initial_food + food
        self.set_total({ "name" : initial_food.name, **initial_food.total})
        return self


class Meal(DietBaseCollection):
    pass


class Diet(DietBaseCollection):
    pass
