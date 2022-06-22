import pandas as pd

# Series
print('Series')
a = [1, 7, 2]
myvar = pd.Series(a)
print(myvar)

data = {
    "calories": [420, 380, 390],
    "duration": [50, 40, 45]
}

# load data into a DataFrame object:
print('dataframe')
df = pd.DataFrame(data)
print(df)

# read csv
print('csv')
pd.options.display.max_rows = 9999
df = pd.read_csv('assets/data.csv')
print(df)

# read json
print('json')
df = pd.read_json('assets/data.json')
print(df.to_string())
