from typing import List
from dataclasses import dataclass, field
try:
    from diet._base import DietBase
except ModuleNotFoundError:
    from src.protocol_backend.diet._base import DietBase


class Food(DietBase):
    # keep the following fields in lowercase
    __vendor_name: str = ""

    def set_vendor(self, vendor: str):
        self.__vendor_name = vendor

    @property
    def vendor_name(self):
        return self.__vendor_name


@dataclass
class Meal(DietBase):
    __recipe: List[Food] = field(
        default_factory=lambda: [Food()])

    @property
    def recipe(self):
        return self.__recipe

    def set_recipe(self, recipe: List[Food]):
        initial_food = Food()
        for food in recipe:
            initial_food += food
        # when you set a new recipe you update the previous total
        self.set_total(initial_food.total)

        self.__recipe = recipe
        return self

    def add_food_to_recipe(self, food: Food):
        if self.__recipe == [Food()]:
            self.__recipe[0] = food
        else:
            self.__recipe.append(food)
        return self


@dataclass
class Diet(DietBase):
    __meals: List[Meal] = field(
        default_factory=lambda: [Meal()])

    def set_meals(self, meals: List[Meal]):
        initial_meal = Meal()
        for meal in meals:
            initial_meal += meal
        self.set_total(initial_meal.total)

        self.__meals = meals
        return self

    @property
    def meals(self):
        return self.__meals

    def add_meal_to_meals(self, meal: Meal):
        if self.__meals == [Meal()]:
            self.__meals[0] = meal
        else:
            self.__meals.append(meal)
        return self
