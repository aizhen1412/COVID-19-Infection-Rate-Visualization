import pandas as pd
import plotly.express as px

# 文件路径
cases_file = "my_cases.csv"
population_file = "my_world_population.csv"

# 加载数据
cases_data = pd.read_csv(cases_file)
population_data = pd.read_csv(population_file)

# 转换日期格式为年份
cases_data["Year"] = pd.to_datetime(cases_data["Date"]).dt.year

# 合并数据，确保使用了正确的合并键
merged_data = pd.merge(cases_data, population_data, on=["ISO3", "Year"])

# 计算感染人数占总人口的比例
merged_data["Infection_rate"] = (
    merged_data["Cumulative_cases"] / merged_data["Population"]
)

# 计算死亡人数占感染的比例
merged_data["Death_rate"] = (
    merged_data["Cumulative_deaths"] / merged_data["Cumulative_cases"]
)

# 确定颜色显示的最大值和最小值
color_min = 0  # 设置最小值
color_max = merged_data["Infection_rate"].max()  # 设置最大值

# 创建动态地图
fig = px.choropleth(
    merged_data,
    locations="ISO3",
    locationmode="ISO-3",
    animation_frame="Date",
    color="Infection_rate",
    hover_name="Country",
    hover_data={
        "Cumulative_cases": True,
        "Cumulative_deaths": True,
        "Infection_rate": ":.4f",  # 显示感染率，保留四位小数
        "Death_rate": ":.4f",  # 显示死亡率，保留四位小数
        "Population": True,
    },
    color_continuous_scale="viridis",
    range_color=(color_min, color_max),  # 设置颜色显示的范围
    color_continuous_midpoint=merged_data[
        "Infection_rate"
    ].median(),  # 设置中点为感染率的中位数
    projection="natural earth",
    title="COVID-19 Infection Rate",
)

# 自定义布局
fig.update_geos(
    showcountries=True,
    countrycolor="darkgrey",
    showcoastlines=True,
    coastlinecolor="white",
    showland=True,
    landcolor="whitesmoke",
    showocean=True,
    oceancolor="lightblue",
    showlakes=True,
    lakecolor="lightblue",
    showrivers=True,
    rivercolor="lightblue",
)

# 第一行数据来源注释，添加可点击的链接
fig.add_annotation(
    text='<a href="https://data.worldbank.org/indicator/SP.POP.TOTL">Data Source:World Bank</a>',
    xref="paper",
    yref="paper",
    x=0.95,
    y=-0.1,
    showarrow=False,
    align="right",
    xanchor="right",
    yanchor="top",
    font=dict(size=10, color="blue"),
)

# 第二行数据来源注释，添加可点击的链接
fig.add_annotation(
    text='<a href="https://data.who.int/dashboards/covid19/data">World Health Organization</a>',
    xref="paper",
    yref="paper",
    x=0.95,
    y=-0.15,  # 调整y值以在第一行注释下方显示
    showarrow=False,
    align="right",
    xanchor="right",
    yanchor="top",
    font=dict(size=10, color="blue"),
)

# 显示图表
fig.show()
