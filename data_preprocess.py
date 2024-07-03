import pandas as pd
import pycountry

df_world_population = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_23.csv", skiprows=3)
df_cases = pd.read_csv("WHO-COVID-19-global-data.csv")

# population data
# 选择需要保留的列，即国家名称、国家代码、2020年以及之后的数据
df_world_population = df_world_population[
    [
        "Country Name",
        "Country Code",
        "2020",
        "2021",
        "2022",
        "2023",
    ]
]

# 将 "Country Code" 列名改为 "ISO3"
df_world_population = df_world_population.rename(columns={"Country Code": "ISO3"})
df_world_population = df_world_population.rename(columns={"Country Name": "Country"})

# 使用melt函数将宽格式数据转换为长格式
melted_df = pd.melt(
    df_world_population,
    id_vars=["Country", "ISO3"],
    var_name="Year",
    value_name="Population",
)
# 将 ISO3 列移到数据框的开始位置
cols = melted_df.columns.tolist()
cols.insert(0, cols.pop(cols.index("ISO3")))
melted_df = melted_df[cols]
# 保存处理后的数据到新文件
melted_df.to_csv("my_world_population.csv", index=False)


# cases data
# 选择需要保留的列，即日期、国家代码、国家名称、累计病例数、累计死亡数
df_cases = df_cases[
    [
        "Date_reported",
        "Country",
        "Cumulative_cases",
        "Cumulative_deaths",
    ]
]


# 将国家名称转换为 ISO-3 代码
def convert_to_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except LookupError:
        return None


# 添加 ISO-3 国家代码列（如果感染数据没有 ISO3 列）
df_cases["ISO3"] = df_cases["Country"].apply(convert_to_iso3)
df_cases = df_cases.rename(columns={"Date_reported": "Date"})
# 过滤掉无法转换为 ISO-3 代码的行
df_cases = df_cases.dropna(subset=["ISO3"])
df_cases["Date"] = pd.to_datetime(df_cases["Date"])
# 选择需要保留的列，即日期、国家代码、国家名称、累计病例数、累计死亡数
df_cases = df_cases[["Date", "Cumulative_cases", "Cumulative_deaths", "ISO3"]]


# 将 ISO3 列移到数据框的开始位置
cols = df_cases.columns.tolist()
cols.insert(0, cols.pop(cols.index("ISO3")))
df_cases = df_cases[cols]

# 将数据按ISO3和每月最后一天进行分组，并获取每个国家每月的累计病例和累计死亡
df_cases = (
    df_cases.groupby(["ISO3", df_cases["Date"].dt.to_period("M")])
    .agg({"Cumulative_cases": "last", "Cumulative_deaths": "last"})
    .reset_index()
)

# 保存处理后的数据到新文件
df_cases.to_csv("my_cases.csv", index=False)
