import pandas as pd
from attendance.afterschool import Afterschool
from attendance.nana import Nana
from attendance.program import Youth, Youth_Info
import seaborn as sns
from matplotlib import pyplot as plt

def present(row:pd.Series) -> str:
    ap = row["Attendance Aft"]
    np = row["Attendance Nana"]
    yp = row["Sessions"]
    a = ap =='P' or ap == 'L'
    n = np =='P' or np == 'L'
    y = yp > 0
    if pd.isna(ap) and pd.isna(np) and pd.isna(yp):
        return 'A'
    if a and n and y:
        return "F:N:Y"
    if a and n:
        return "F:N"
    if a and y:
        return "F:Y"
    if n and y:
        return "N:Y"
    if a:
        return "F"
    if n:
        return "N"
    if y:
        return "Y"
    return "A"

def main():
    rd = Afterschool("Afterschool Program Attendance 2025-2026.xlsx",("October","November","December","January"))
    na = Nana("Nanna Transportation Program Attendance.xlsx",("September","October","November","December","January"))
    yti = Youth_Info("Student Attendance_Aug_Dec25.xlsx")
    yt = Youth("Student Attendance_Aug_Dec25.xlsx",("December 2025","November 2025", "October 2025", "September 2025", "August 2025"))
    aft_sch_df = rd.get_df()
    nana_df = na.get_df()
    youth_df = yt.get_df()
    youth_info_df = yti.get_df()
    both = pd.merge(aft_sch_df,nana_df,"outer",["Student ID","Date"],suffixes=(" Aft"," Nana"))
    all = pd.merge(youth_df,both,"outer","Student ID",suffixes=(" Yth",""))
    
    all = all[~all["Student ID"].isna()]
    
    no_date = all[all["Date"].isna()]
    
    all = all[~all["Date"].isna()]

    all = all.drop_duplicates(("Student ID","Date"))

    first = all["Date"].min()
    all["Day"] = all["Date"].apply(lambda d:(d-first).days)
    all["Attendance"] = all.apply(present,axis=1)
    all = all[all["Attendance"] != 'A']

        
    order = ("F:N:Y","F","F:Y","Y","Y:N","N","F:N","A")
    palette = {"F:N:Y":"white","F":"red","F:Y":"orange","Y":"yellow","Y:N":"green","N":"blue","F:N":"purple","A":"black"}
    h = sns.histplot(all,x="Date",hue="Attendance",hue_order=order,palette=palette,binwidth=1,multiple="stack")
    plt.xticks(rotation=30)
    plt.show()
    print()
    # by_dates = nana_df[['Day',"Present"]].groupby('Day').sum()
    # by_dates = by_dates[by_dates["Present"] > 0]
    # sns.boxplot(by_dates,x="Day",y="Present")
    # plt.show()
    

    


if __name__ == "__main__":
    main()