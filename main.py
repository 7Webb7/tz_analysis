import pandas as pd
import re

df_sales = pd.read_csv("data_files/t_sales.csv")
sales = pd.DataFrame(df_sales)

df_branches = pd.read_csv("data_files/t_branches.csv")
branches = pd.DataFrame(df_branches)

df_products = pd.read_csv("data_files/t_products.csv")
products = pd.DataFrame(df_products)

df_cities = pd.read_csv("data_files/t_cities.csv")
cities = pd.DataFrame(df_cities)

sales.rename(columns={"Unnamed: 0": "Index", "Филиал": "Ссылка"}, inplace=True)
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
merged_b_s = pd.merge(sales, branches, on="Ссылка")

#Здесь топ 10 склад и магазинов по количеству продаж

sales_number_types = merged_b_s.groupby(["Тип", "Ссылка", "Наименование"])["Количество"].sum().reset_index()
warehouses_sales = sales_number_types[sales_number_types["Тип"] == "Склад"]
shops_sales = sales_number_types[sales_number_types["Тип"] == "Магазин"]
shops_sales_ten = shops_sales.sort_values(by="Количество", ascending=False).head(10).reset_index()
warehouses_sales_ten = warehouses_sales.sort_values(by="Количество", ascending=False).head(10).reset_index()
print(shops_sales_ten)
print(warehouses_sales_ten)

#здесь топ-10 товаров по продажам на складах и магазинах
pattern = r"доставка|отгрузка|обработка"

products.rename(columns={"Ссылка": "Номенклатура"}, inplace=True)
merged_b_s_p = pd.merge(merged_b_s, products, on="Номенклатура")

merged_b_s_p = merged_b_s_p[~merged_b_s_p["Наименование_y"].str.contains(pattern, case=False, regex=True)]
products_sales = merged_b_s_p.groupby(["Номенклатура", "Наименование_y", "Тип"])["Количество"].sum().reset_index()
warehouses_products = products_sales[products_sales["Тип"] == "Склад"]
shops_products = products_sales[products_sales["Тип"] == "Магазин"]
warehouses_products_top_ten = warehouses_products.sort_values(by="Количество", ascending=False).head(10).reset_index()
shops_products_top_ten = shops_products.sort_values(by="Количество", ascending=False).head(10).reset_index()
print(warehouses_products_top_ten)
print(shops_products_top_ten)

#Топ-10 городов p.s. Корявый index, ибо в юпитере inplace через задницу без перезапуска ядра
cities.rename(columns={"Ссылка": "Город"}, inplace=True)
merged_b_s_c = pd.merge(cities, merged_b_s, on="Город")
cities_sales = merged_b_s_c.groupby(["Наименование_x"])["Количество"].sum().reset_index()
cities_sales.rename(columns={"Наименование_x": "Город"}, inplace=True)
cities_sales = cities_sales.sort_values(by="Количество", ascending=False).head(10)
cities_sales.reset_index()
print(cities_sales)
