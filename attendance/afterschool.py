import pandas as pd

class Afterschool:
    def __init__(self,path:str,months:tuple[str]):
        self.months = months
        self.data = ["Student ID", "School"]
        self.df = self.read(path)

    def read(self,path:str) -> pd.DataFrame:
        months_dicts = []
        for month in self.months:
            raw = pd.read_excel(path,sheet_name=month,index_col=None,skiprows=[0,2])
            rlen = len(raw)
            empty_cols = {c for c in raw.columns if str(c).startswith("Unnamed:") or c == ' '}
            dates = list(set(raw.columns)-set(self.data)-{"Present","Late","Absent"}-empty_cols)
            # if a date is empty just remove it
            dates = [d for d in dates if raw[d].isna().sum() != rlen]
            months_dicts += [
                {"Student ID":row["Student ID"],
                 "School":row["School"],
                 "Date":date,
                 "Attendance":row[date]}
                    for date in dates
                    for _,row in raw.iterrows()
            ]
        
        df = pd.DataFrame(months_dicts)
        df["Student ID"] = df["Student ID"].astype(str)
        df["Date"] = df["Date"].astype("datetime64[us]")
        return df

    def get_df(self) -> pd.DataFrame:
        return self.df