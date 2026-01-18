import pandas as pd

data = {
    "Calories": [420, 380, 390],
    "Duration": [50, 40, 45]
}

df = pd.DataFrame(data)
print(df.head())

print(df["Calories"])
print(df["Duration"])

print(df["Calories"].mean())

print("------- Read CSV with TIS-620 encoding -------")

df = pd.read_csv("datasets/1642645053.csv", encoding = "tis-620")
print(df.head(10))