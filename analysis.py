import pandas
import re
import os
import numpy as np

'''
Author: Julius Blusevičius
Program: Reads the information related to kindergarten , performs some data-related operations and prints results to logs
'''



#simple function for generating log file
def generate_log(filename, text):
    file = open(filename, 'w',encoding='utf-8')
    file.write(text)

#creates abbreviation based on record row
def create_name(row):
    return row["SCHOOL_NAME"][:3] \
    + "_" + re.split('\W+',row['TYPE_LABEL'])[1] \
    + "_" + re.split('\W+',row['TYPE_LABEL'])[4] \
    + "_" + row["LAN_LABEL"][:4]

#NUSKAITYTI DUOMENIS Į ATMINTĮ IŠ .CSV TIPO FAILO.
#------------------------------------------------
#reads file into pandas dataframe
df = pandas.read_csv("input.txt", sep=";")
#------------------------------------------------

#IŠVESTI Į EKRANĄ DIDŽIAUSIĄ IR MAŽIAUSIĄ STULPELIO „CHILDS_COUNT“ REIKŠMĘ.(maxmin.txt)
#--------------------------------------------------------------------------
#getting rows where childs_count is biggest and smallest
max_row = df.loc[df['CHILDS_COUNT'].idxmax()]
min_row = df.loc[df['CHILDS_COUNT'].idxmin()]
max_row_text = "Max childs count value:  " + str(max_row['CHILDS_COUNT'])
min_row_text = "Min childs count value:  " + str(min_row['CHILDS_COUNT'])
print(max_row_text)
print(min_row_text)
generate_log("maxmin.txt", max_row_text + os.linesep + min_row_text)
#--------------------------------------------------------------------------

#SURASTI EILUTES, KURIOSE STULPELIO „CHILDS_COUNT“ REIKŠMĖ YRA DIDŽIAUSIA IR MAŽIAUSIA, IŠ RASTŲ EILUČIŲ SUFORMUOTI ŽODĮ(abbreviations.txt)
#-----------------------------------------------------------------------------------------------------------------------
#getting abbreviations from min and max rows
max_name = create_name(max_row)
min_name = create_name(min_row)
max_name_text = "Max row's abbreviation: " + max_name
min_name_text = "Min row's abbreviation: " + min_name
generate_log("abbreviations.txt", max_name_text + os.linesep + min_name_text)
#-----------------------------------------------------------------------------------------------------------------------

#SURASKITE, KURIOS KALBOS DARŽELIAI TURI DAUGIAUSIAI LAISVŲ VIETŲ PROCENTAIS.(maxpercentage.txt)
#----------------------------------------------------------------------------
#first we get percentage column
percentage = df["FREE_SPACE"].divide(df["CHILDS_COUNT"])
#then we add that column into datframe
df.insert(value=percentage, loc=df.shape[1], column="PERCENTAGE")
# replacing all rows which got inf in PERCENTAGE column with nan and then dropping rows with nan field
df_clean = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["PERCENTAGE"], how="all")
# grouping by LAN_LABEL , getting mean , sorting and rounding the result
free_schools = df_clean.groupby(['LAN_LABEL']).mean().sort_values(by=["PERCENTAGE"], ascending=False).round(2)
generate_log("maxpercentage.txt",free_schools.iloc[[0]]['PERCENTAGE'].to_string(header=False))
#----------------------------------------------------------------------------


#IŠRINKTI VISUS DARŽELIUS, KURIUOSE YRA NUO 2 IKI 4 LAISVŲ VIETŲ. SUGRUPUOTI GAUTUS DARŽELIUS PAGAL PAVADINIMĄ IR IŠRŪŠIUOTI NUO Z IKI A.(2to4schools.txt)
#----------------------------------------------------------------------------------------------------------------------------------------
# selecting all rows which satisfies condition , summing free spaces and sorting in descending oder by SCHOOL_NAME
result = df[(df["FREE_SPACE"] >= 2)  & (df["FREE_SPACE"] <= 4)].groupby(["SCHOOL_NAME", "DARZ_ID"]).sum().sort_values(by=['SCHOOL_NAME'], ascending=False)
# we only need fields which was grouped by and the summed FREE_SPACE
result_cleaned = result[["FREE_SPACE"]].copy()
generate_log("2to4schools.txt", result_cleaned.to_string())
#----------------------------------------------------------------------------------------------------------------------------------------
