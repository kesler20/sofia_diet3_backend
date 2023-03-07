import os
import pandas as pd
# FastAPI imports
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import json
from pathlib import Path
try:
    from excel_database.exceldatabase import ExcelDatabase
    from diet.diet import Food, Meal, Diet
except ModuleNotFoundError:
    from src.sofia_diet3_backend.excel_database.exceldatabase import ExcelDatabase
    from src.sofia_diet3_backend.diet.diet import Food, Meal, Diet

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

# ------------- FOOD --------------------


@app.post('/sofia-diet/food/CREATE')
async def handle_upload(food=Body(...)):

    # decode the response and turn that into a dictionary
    if type(food) != dict:
        food = json.loads(food.decode())

    # instantiate a new Food object
    new_food = Food(food["name"]).set_total(food)

    # put the new_food object into the database
    input_to_database = [new_food.name[0], *[new_food.total[k] for k in new_food.total.keys()]]
    db.put_table(["name", *list(new_food.total.keys())], input_to_database, "food")

    # print the result and confirmation
    print(db.get_table("food"))
    print("food created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/food/READ')
async def read_foods():
    return db.get_table("food").to_json()


@app.delete('/sofia-diet/food/DELETE')
async def delete_meals(mealID=Body(...)):
    try:
        food_id = json.loads(mealID.decode())
    except:
        print(type(food_id))

    db.delete_rows([food_id], "food")

    return {'response': 'okay'}

# ------------- MEAL --------------------


@app.post('/sofia-diet/meal/CREATE')
async def handle_meal_upload(meal=Body(...)):

    # decode the response and turn that into a dictionary
    if type(meal) != dict:
        meal = json.loads(meal.decode())

    # instantiate a new Food object
    new_meal = Meal(meal["mealName"]).set_data(meal["recipe"])

    # put the new_meal object into the database
    input_to_database = [new_meal.total[k] for k in new_meal.total.keys()]
    db.put_table(["name", "recipe", *list(new_meal.total.keys())], [meal["mealName"], json.dumps(meal["recipe"]), *input_to_database], "meals")

    # print the result and confirmation
    print(db.get_table("meals"))
    print("meal created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/meal/READ')
async def handle_meal_upload():
    return db.get_table("meals").to_json()


@app.delete('/sofia-diet/meal/DELETE')
async def delete_meals(mealID=Body(...)):
    try:
        meal_id = json.loads(mealID.decode())
    except:
        print(type(meal_id))

    db.delete_rows([meal_id], "meals")

    return {'response': 'okay'}

# ------------- DIET --------------------

@app.post('/sofia-diet/diet/CREATE')
async def handle_diet_upload(diet=Body(...)):

    # reset the diet every new week
    try:
        if db.query_table(lambda table: table["Weekday"] == "Sunday", "diet")["Weekday"].any():
            db.delete_table("diet")
    except KeyError:
        pass

    # decode the response and turn that into a dictionary
    if type(diet) != dict:
        diet = json.loads(diet.decode())
    
    # instantiate the Diet class
    new_diet = Diet(diet["weekDay"]).set_data(diet["meals"])

    # put the new_meal object into the database
    input_to_database = [new_diet.total[k] for k in new_diet.total.keys()]
    db.put_table(["week day", *list(new_diet.total.keys()), "meals"], [diet["weekDay"], *input_to_database, json.dumps(diet["meals"])], "diet")

    print(db.get_table("diet"))
    print("diet created successfully ✅")

    return {'response': 'okay'}


@app.get('/sofia-diet/diet/READ')
async def get_diet_file():
    diet_file = os.path.join(db.folder_name, "diet.xlsx")
    return FileResponse(diet_file, media_type="application/msexcel", filename="diet.xlsx")
