import pandas as pd
import re
df = pd.read_csv("all_electronics.csv")
def clean_name(name):
    if pd.isna(name):
        return name
    return re.sub(r"[\(\[].*?[\)\]]", "", str(name)).strip()

df.iloc[:, 0] = df.iloc[:, 0].apply(clean_name)
df.to_csv("all_electronics_cleaned.csv", index=False)
print("Cleaned file saved as 'all_electronics_cleaned.csv'")