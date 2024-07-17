import pandas as pd
import re
df_sales = pd.read_csv("data_files/t_sales.csv")
sales = pd.DataFrame(df_sales)

df_branches = pd.read_csv("data_files/t_branches.csv")
branches = pd.DataFrame(df_branches)

df_products = pd.read_csv("data_files/t_products.csv")
products = pd.DataFrame(df_products)

sales.rename(columns = {"Unnamed: 0" : "Index", "Филиал" : "Ссылка"}, inplace = True)
#sales.set_index("Index", inplace = True)

branches.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
df_branches.fillna('', inplace=True)


def determine_building_type(first, second):
    pattern = re.compile(r'\b[сc][кk][лl][аa][дd]\b', re.IGNORECASE)

    if pattern.search(first) or pattern.search(second):
        return "Склад"
    else:
        return "Магазин"


branches['Тип'] = branches.apply(lambda row: determine_building_type(row['Наименование'], row['КраткоеНаименование']),
                                 axis=1)
merged_b_s = pd.merge(sales, branches, on = "Ссылка")

sales_number_types = merged_b_s.groupby(["Тип", "Ссылка", "Наименование"])["Количество"].sum().reset_index()
warehouses_sales = sales_number_types[sales_number_types["Тип"] == "Склад"]
shops_sales = sales_number_types[sales_number_types["Тип"] == "Магазин"]
shops_sales_ten = shops_sales.sort_values(by = "Количество", ascending = False).head(10).reset_index()
warehouses_sales_ten = warehouses_sales.sort_values(by = "Количество", ascending = False).head(10).reset_index()
print(shops_sales_ten)
print(warehouses_sales_ten)
