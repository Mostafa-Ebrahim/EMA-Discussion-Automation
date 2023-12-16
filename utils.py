from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import datetime

import vars


def web_driver(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver


def check_duplicate(table_number, element, driver):
    len_brothers = driver.find_element(
        By.CSS_SELECTOR, f"#relatives-{table_number}-header > span"
    ).text

    temp_list = []
    try:
        ID_num = int(len_brothers)

        for num in range(1, ID_num + 1):
            name = driver.find_element(
                By.XPATH,
                f"/html/body/div/div/div/div[8]/div[{element}]/div/div/div[2]/table/tbody/tr[{num}]/td[1]",
            ).text
            temp_str = str(name).split(" ")[:2]
            temp_list.append(" ".join(temp_str))
        check_names = set(temp_list)

        if ID_num != len(check_names):
            return "X"

        else:
            return " "
    except:
        return "EMPTY"


def check_element(element, element_list):
    if not element:
        element_list.append("X")
    else:
        element_list.append(" ")


def save_file(std_no, std_id):
    result = {
        "رقم القيد": std_no,
        "الرقم القومي": std_id,
        "خطر": vars.danger_list,
        "الطول": vars.length_list,
        "الوزن": vars.weight_list,
        "التناسق": vars.tansok_list,
        "الشهر": vars.month_list,
        "السنة": vars.year_list,
        "الموقف التجنيدي": vars.tagneed_list,
        "الحالة": vars.status_list,
        "التخصص": vars.graduation_list,
        "الدرجة العلمية": vars.degree_list,
        "التقدير": vars.grade_list,
        "النسبة": vars.percentage_list,
        "الأختبار الرياضي": vars.sport_list,
        "بيانات الأب": vars.father_list,
        "بيانات الأم": vars.mother_list,
        "الأخوة الأشقاء": vars.brothers_list,
        "الأخوة غير الأشقاء": vars.not_brothers_list,
        "الأعمام والعمات": vars.uncle_list,
        "الأخوال والخالات": vars.not_uncle_list,
    }
    result_dataframe = pd.DataFrame(data=result)

    result_dataframe.to_excel(
        "problems/problems-{}.xlsx".format(
            datetime.datetime.now().strftime("%m%d-%H%M")
        ),
        index=False,
    )
