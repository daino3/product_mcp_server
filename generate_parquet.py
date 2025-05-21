import pandas as pd
import ipdb
# Read the CSV

ipdb.set_trace()

df = pd.read_csv("data/fake_users.csv")
# Save as Parquet
df.to_parquet("data/fake_users.parquet", index=False)