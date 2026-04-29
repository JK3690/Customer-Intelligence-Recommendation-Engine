import pandas as pd

df = pd.read_csv("data/shopping_trends.csv")

print(df.shape)
print(df.columns)
print(df.head())