import pandas as pd
import re
data_branches = pd.read_csv("data_files/t_branches.csv")
df_branches = pd.DataFrame(data_branches)

data_sales = pd.read_csv("data_files/t_sales.csv")
df_sales = pd.DataFrame(data_sales)

df_branches.fillna('', inplace=True)


def determine_building_type(first, second):
    pattern = re.compile(r'\b[сc][кk][лl][аa][дd]\b', re.IGNORECASE)

    if pattern.search(first) or pattern.search(second):
        return "Склад"
    else:
        return "Магазин"


df_branches['Тип'] = df_branches.apply(
    lambda row: determine_building_type(row['Наименование'], row['КраткоеНаименование']), axis=1)
df_branches.rename(columns={"Ссылка": "Филиал"}, inplace=True)
df_merged = pd.merge(df_branches, df_sales, on="Филиал")

df_by_sales = df_merged.groupby(["Филиал", "Наименование", "Тип"])["Продажа"].size().reset_index()

df_by_sales_shops = df_by_sales[df_by_sales["Тип"] == "Магазин"]

df_top_by_sales_shops = df_by_sales_shops.sort_values(by="Продажа", ascending=False).head(10).reset_index()
df_top_by_sales_shops.drop(columns=["index"], inplace=True)
print(df_top_by_sales_shops) #Топ 10 магазинов по продажам

df_by_sales_warehouses = df_by_sales[df_by_sales["Тип"] == "Склад"]
df_top_by_sales_warehouses = df_by_sales_warehouses(by="Продажа", ascending=False).head(10).reset_index()
df_top_by_sales_shops.drop(columns=["index"], inplace=True)
print(df_top_by_sales_warehouses)
