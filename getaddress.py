import pandas as pd
from rapidfuzz import process, fuzz

# 1. 官方新加坡 55 个规划区清单
SINGAPORE_PLANNING_AREAS = [
    "Ang Mo Kio", "Bedok", "Bishan", "Boon Lay", "Bukit Batok",
    "Bukit Merah", "Bukit Panjang", "Bukit Timah", "Central Water Catchment",
    "Changi", "Changi Bay", "Choa Chu Kang", "Clementi", "Downtown Core",
    "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang",
    "Lim Chu Kang", "Mandai", "Marina East", "Marina South", "Marine Parade",
    "Museum", "Newton", "North-Eastern Islands", "Novena", "Orchard",
    "Outram", "Pasir Ris", "Paya Lebar", "Pioneer", "Punggol",
    "Queenstown", "River Valley", "Rochor", "Seletar", "Sembawang",
    "Sengkang", "Serangoon", "Simpang", "Singapore River", "Southern Islands",
    "Sungei Kadut", "Tampines", "Tanglin", "Tengah", "Toa Payoh",
    "Tuas", "Western Islands", "Western Water Catchment", "Woodlands", "Yishun"
]


def process_excel_planning_areas(input_file, output_file, address_column):
    # 读取 Excel
    print(f"正在读取 Excel 文件: {input_file}...")
    # 确保安装了 openpyxl: pip install openpyxl
    df = pd.read_excel(input_file)

    def get_match(text):
        if pd.isna(text) or text == "":
            return None, 0
        # 使用 WRatio 匹配，对带有街道信息的长字符串效果很好
        res = process.extractOne(str(text), SINGAPORE_PLANNING_AREAS, scorer=fuzz.WRatio)
        return (res[0], res[1]) if res else (None, 0)

    print(f"正在对列 '{address_column}' 进行模糊匹配，请稍候...")

    # 执行匹配
    matches = df[address_column].apply(get_match)

    # 将匹配结果拆分为“规划区”和“匹配得分”两列
    df['Matched_Planning_Area'] = matches.apply(lambda x: x[0])
    df['Match_Score'] = matches.apply(lambda x: x[1])

    # --- 修正点：保存为 Excel (.xlsx) ---
    print(f"正在保存到 Excel: {output_file}...")
    df.to_excel(output_file, index=False)
    print("处理完成！")


# --- 路径设置 ---
INPUT_PATH = "/Users/admin/Desktop/tableau数据分析项目/jobstreet_jobs_clean.xlsx"
# 注意：这里后缀改成了 .xlsx
OUTPUT_PATH = "/Users/admin/Desktop/tableau数据分析项目/jobstreet_jobs_district.xlsx"
COLUMN_NAME = "小区域"

process_excel_planning_areas(INPUT_PATH, OUTPUT_PATH, COLUMN_NAME)