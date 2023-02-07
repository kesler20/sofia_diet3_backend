import os
import pandas as pd
# FastAPI imports
from fastapi import FastAPI, Body, UploadFile, Depends, BackgroundTasks, Response, status
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.requests import Request
import json
import pickle

try:
    from protocol_database.exceldatabase import ExcelDatabase
    from diet.diet import Food, Meal, Diet
except ModuleNotFoundError:
    from src.protocol_backend.protocol_database.exceldatabase import ExcelDatabase
    from src.protocol_backend.diet.diet import Food, Meal, Diet

'''
The application backend will take requrest from any client "see origins list set as *"
Nevertheless, the endpoint architecture will take the following form

/application-name/HTTP METHOD/custom

In the case of sofiaApi the custom topic will refer to the name of the Table 
of interest in lowercase
'''

# ---------------------------------------------------#
#                                                    #
#     INITIALIZE APPLICATION AND CONFIGURATIONS      #
#                                                    #
# ---------------------------------------------------#

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

db = ExcelDatabase()
BASE_FOOD_AMOUNT = 100

@app.get("/", tags=["root"])
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

# ----------------------------------- #
#                                     #
#         APPLICATIONS ENDPOINTS      #
#                                     #
# ------------------------------------#


#----------------- SOFIA DIET ---------------#

@app.post('/sofia-diet/food/CREATE')
async def handle_upload(food=Body(...)):
    try:
        food = json.loads(food.decode())
    except:
        print(type(food))

    # initialise food objects with base amount
    food = Food().set_name(
        food["name"]
    ).set_cost(
        float(food["cost"])
    ).set_protein(
        float(food["protein"])
    ).set_calories(
        int(food["calories"])
    ).set_vendor(str(food["vendor"]))

    # db.create_table(
    #     "food",
    #     ["Name", "Cost (£)", "calories (g/amount)", "protein (g/amount)", "amount (g)"],
    #     [[food.name], [food.cost], [food.calories], [food.protein], [100]]
    # )
    db.append_row(
        [food.name, food.cost, food.calories, food.protein, BASE_FOOD_AMOUNT],
        "food"
    )

    print(db.get_table("food"))
    print("food created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/food/READ')
async def read_foods():
    df1 = db.get_table("food")
    df2 = pd.DataFrame(data={"name": df1["Name"], "cost": df1["Cost (£)"],
                       "calories": df1["calories (g/amount)"], "protein": df1["protein (g/amount)"]})
    print(df2)
    return df2.to_json()


@app.delete('/sofia-diet/food/DELETE')
async def delete_meals(mealID=Body(...)):
    try:
        mealID = json.loads(mealID.decode())
    except:
        print(type(mealID))

    db.delete_rows([mealID], "food")

    return {'response': 'okay'}


@app.post('/sofia-diet/meal/CREATE')
async def handle_meal_upload(meal=Body(...)):
    try:
        meal: 'list[dict]' = json.loads(meal.decode())
    except:
        print(type(meal))

    recipe = []  # a collection of foods
    for food in meal["recipe"]:
        amount = float(food["amount"]/BASE_FOOD_AMOUNT)
        if len(list(food.keys())) == 1:
            pass
        else:
            recipe.append(
                Food().set_name(
                    food["name"]
                ).set_cost(
                    float(food["cost"])
                ).set_protein(
                    float(food["protein"])
                ).set_calories(
                    int(food["calories"])
                ) * amount
            )

    meal = Meal().set_name(meal["mealName"]).set_recipe(recipe)

    db.create_table(
        "meals",
        ["Name", "Cost (£)", "calories (g/amount)", "protein (g/amount)", "recipe"],
        [meal.name, meal.cost, meal.calories, meal.protein, meal.recipe]
    )
    # db.append_row(
    #     [meal.name, meal.cost, meal.calories, meal.protein, meal.recipe],
    #     "meals"
    # )

    print(db.get_table("meals"))

    print("meal created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/meal/READ')
async def handle_meal_upload():
    df1 = db.get_table("meals")
    df2 = pd.DataFrame(data={"name": df1["Name"], "cost": df1["Cost (£)"],
                       "calories": df1["calories (g/amount)"], "protein": df1["protein (g/amount)"]})
    print(df2)
    return df2.to_json()


@app.delete('/sofia-diet/meal/DELETE')
async def delete_meals(mealID=Body(...)):
    try:
        mealID = json.loads(mealID.decode())
    except:
        print(type(mealID))

    db.delete_rows([mealID], "meals")

    return {'response': 'okay'}


@app.post('/sofia-diet/diet/CREATE')
async def handle_diet_upload(diet=Body(...)):
    try:
        diet: 'list[dict]' = json.loads(diet.decode())
    except:
        print(type(diet))
    
    print(diet)

    new_diet = Diet().set_meals([
        Meal().set_name(
            meal["name"]
        ).set_cost(
            float(meal["cost"])
        ).set_protein(
            float(meal["protein"])
        ).set_calories(
            int(meal["calories"])
        ) * float(meal["amount"]/BASE_FOOD_AMOUNT)
        for meal in diet["meals"]
    ])

    # db.create_table(
    #     "diet",
    #     ["Weekday", "Name", "Cost (£)", "calories (g/amount)", "protein (g/amount)", "recipe"],
    #     [[diet["weekDay"]], [new_diet.total["name"][0]], [new_diet.cost], [new_diet.calories], [new_diet.protein], [new_diet.meals[0].recipe]]
    # )

    # reset the diet every new week
    if db.query_table(lambda table: table["Weekday"] == "Sunday", "diet")["Weekday"].any():
        db.delete_table("diet")

    for meal in new_diet.meals:
        db.append_row([diet["weekDay"], meal.name, meal.cost, meal.calories, meal.protein, meal.recipe], "diet")

    print(db.get_table("diet"))

    print("diet created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/diet/READ')
async def get_diet_file():
    diet_file = os.path.join(db.folder_name, "diet.xlsx")
    return FileResponse(diet_file, media_type="application/msexcel", filename="diet.xlsx")
