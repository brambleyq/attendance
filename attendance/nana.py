import pandas as pd

class Nana:
    def __init__(self,path:str,months:tuple[str]):
        self.months = months
        self.data = ["Student ID"]
        self.df = self.read(path)

    def read(self,path:str) -> pd.DataFrame:
        months_dicts = []
        for month in self.months:
            raw = pd.read_excel(path,sheet_name=month,index_col=None,skiprows=[0,2])
            rlen = len(raw)
            empty_cols = {c for c in raw.columns if str(c).startswith("Unnamed:")}
            dates = list(set(raw.columns)-set(self.data)-{"Bus #","Rider Absent", "Rider to Home", "Rider to Afterschool Program","Early Dismissal"}-empty_cols)
            # if a date is empty just remove it
            dates = [d for d in dates if raw[d].isna().sum() != rlen]
            months_dicts += [
                {"Student ID":row["Student ID"],
                 "Bus #":row["Bus #"],
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

    
if __name__ == "__main__":
    n = Nana("Nanna Transportation Program Attendance - DeidentifiedAMM.xlsx",("September","October","November","December","January"))
    print(n.df)