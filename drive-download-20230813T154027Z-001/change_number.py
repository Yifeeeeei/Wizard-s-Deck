import os
import pandas as pd

for f in os.listdir("."):
    if f.endswith("xlsx"):
        current_sheets = pd.read_excel(
            f,
            sheet_name=None,
            header=0,
        )
        for sheet_name, df in current_sheets.items():
            for i in range(len(df)):
                if "编号" not in df.iloc[i].keys():
                    continue
                # print(df.iloc[i])
                if pd.isnull(df.iloc[i, 0]):
                    continue
                old_number = str(df.iloc[i, 0])
                new_number = old_number
                new_number = (
                    old_number[0] + old_number[2] + old_number[1] + old_number[3:6]
                )
                df.iloc[i, 0] = int(new_number)
        with pd.ExcelWriter("new_" + f) as writer:
            for sheet_name, df in current_sheets.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
