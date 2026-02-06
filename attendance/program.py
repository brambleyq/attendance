import pandas as pd

class Youth:
    def __init__(self,path:str,months:tuple[str]):
        self.months = months
        self.data = ["Client_ID"]
        self.df = self.read(path)
        
    def read(self,path:str) -> pd.DataFrame:
        months_dicts = []
        for month in self.months:
            raw = pd.read_excel(path,sheet_name=month,index_col=None,skiprows=[0])
            rlen = len(raw)
            empty_cols = {c for c in raw.columns if str(c).startswith("Unnamed:")}
            dates = list(set(raw.columns)-set(self.data)-{"Total"}-empty_cols)
            # if a date is empty just remove it
            dates = [d for d in dates if raw[d].isna().sum() != rlen]
            months_dicts += [
                {"Student ID":row["Client_ID"],
                 "Date":date,
                 "Sessions":row[date]}
                    for date in dates
                    for _,row in raw.iterrows()
            ]
        
        df = pd.DataFrame(months_dicts)
        df["Student ID"] = df["Student ID"].astype(str)
        df["Date"] = df["Date"].astype("datetime64[us]")
        return df

    def get_df(self) -> pd.DataFrame:
        return self.df
        

class Youth_Info:
    def __init__(self,path:str):
        self.data = ["Client_ID", "Sex", "Grade level", "School District", "Provider", "Facility Name", "Program Type"]
        self.df = self.read(path)
        
    def read(self,path:str) -> pd.DataFrame:
        df = pd.read_excel(path,sheet_name="Student Information",index_col=None)
        df["Client_ID"] = df["Client_ID"].astype(str)
        df = df[self.data]
        rename = {"Client_ID":"Student ID",
                "Grade level": "Grade"}
        df.rename(columns=rename,inplace=True)
        df["Student ID"] = df["Student ID"].astype(str)
        return df

    def get_df(self) -> pd.DataFrame:
        return self.df
        