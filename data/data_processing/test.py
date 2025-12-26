import pandas

df = pandas.read_csv("../processed/floods/Indonesia floods 2008-2025.csv")
for index, row in df.iterrows():
    if index == 1:
        print(type(row["FLOOD"]))
