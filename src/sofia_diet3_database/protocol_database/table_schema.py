SQL_STATEMENTS = ['''
CREATE TABLE Session(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id DATETIME NOT NULL
);''', '''
CREATE TABLE Food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    calories FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    cost FLOAT NOT NULL
);''', '''

CREATE TABLE Meal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    recipe INT NOT NULL,
    FOREIGN KEY(recipe) REFERENCES Food(id)
);''', '''

CREATE TABLE Diet(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_day VARCHAR(255) NOT NULL,
    session_id DATETIME NOT NULL,
    meals INT NOT NULL,
    FOREIGN KEY(meals) REFERENCES Meal(id)
);''', '''

CREATE TABLE Exercise(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reps INT NOT NULL,
    sets INT NOT NULL,
    weight INT NOT NULL,
    name VARCHAR(255) NOT NULL
);''', '''

CREATE TABLE Workout(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercises INT NOT NULL,
    session_id DATETIME NOT NULL,
    week_day VARCHAR(255) NOT NULL,
    FOREIGN KEY(exercises) REFERENCES Exercise(id)
);''', '''

CREATE TABLE Fitness(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id DATETIME NOT NULL,
    maintanace_calories INT NOT NULL,
    muscle_mass INT NOT NULL,
    body_fat INT NOT NULL,
    weight FLOAT NOT NULL
);''', '''

CREATE TABLE Expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    session_id DATETIME NOT NULL
);''']
