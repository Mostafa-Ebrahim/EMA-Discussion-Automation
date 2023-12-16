import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import vars
import utils


def main(url, filename, student_kind, sleep_time):
    data = pd.read_csv(filename)
    driver = utils.web_driver(url)
    time.sleep(2)

    element_list = [
        vars.length_list,
        vars.weight_list,
        vars.tansok_list,
        vars.sport_list,
        vars.month_list,
        vars.year_list,
        vars.tagneed_list,
        vars.status_list,
        vars.graduation_list,
        vars.degree_list,
        vars.grade_list,
        vars.percentage_list,
        vars.father_list,
        vars.mother_list,
        vars.danger_list,
    ]

    driver.find_element(By.ID, "user").click()
    driver.find_element(By.ID, "user").send_keys("hy2a_app")
    driver.find_element(By.ID, "password").click()
    driver.find_element(By.ID, "password").send_keys("Aa@12345")
    driver.find_element(By.CSS_SELECTOR, ".btn").click()
    time.sleep(3)

    driver.find_element(By.ID, "student_kind").click()
    dropdown = driver.find_element(By.ID, "student_kind")
    dropdown.find_element(By.XPATH, f"//option[. = '{student_kind}']").click()

    for val in data["STD_NO"].values:
        driver.find_element(By.ID, "student_no").click()
        driver.find_element(By.ID, "student_no").clear()
        driver.find_element(By.ID, "student_no").send_keys(str(val))
        driver.find_element(By.NAME, "student_no").send_keys(Keys.ENTER)
        time.sleep(sleep_time)

        try:
            length = driver.find_element(By.ID, "lenght").text
            weight = driver.find_element(By.ID, "weight").text
            tansok = driver.find_element(By.ID, "vision").text
            sport = driver.find_element(
                By.CSS_SELECTOR, "#sport-info-header > span"
            ).text
            month = driver.find_element(By.ID, "age_mon").text
            year = driver.find_element(By.ID, "age_year").text
            tagneed = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div[8]/div[1]/div/div/div/div[5]/p[2]"
            ).text
            status = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div[8]/div[1]/div/div/div/div[6]/p[2]"
            ).text
            graduation = driver.find_element(By.ID, "graduation").text
            degree = driver.find_element(By.ID, "post_graduation").text
            grade = driver.find_element(By.ID, "grade").text
            percentage = driver.find_element(By.ID, "pers").text

            father_name = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[2]/td[1]",
            ).text
            father_degree_birth = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[2]/td[2]",
            ).text
            father_degree_now = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[3]/td[1]",
            ).text
            father_work_birth = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[2]/td[3]",
            ).text
            father_work_now = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[3]/td[2]",
            ).text

            mother_name = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[4]/td[1]",
            ).text
            mother_degree_now = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[4]/td[2]",
            ).text
            mother_work_now = driver.find_element(
                By.XPATH,
                "/html/body/div/div/div/div[8]/div[4]/div/div/div/table/tbody/tr[4]/td[3]",
            ).text

            father = (
                father_name
                and father_degree_birth
                and father_degree_now
                and father_work_birth
                and father_work_now
            )
            mother = mother_name and mother_degree_now and mother_work_now

            vars.brothers_list.append(utils.check_duplicate("one", 5, driver))
            vars.not_brothers_list.append(utils.check_duplicate("two", 6, driver))
            vars.not_uncle_list.append(utils.check_duplicate("three", 7, driver))
            vars.uncle_list.append(utils.check_duplicate("four", 8, driver))

            if (
                vars.brothers_list[len(vars.brothers_list) - 1] == "EMPTY"
                and vars.not_brothers_list[len(vars.not_brothers_list) - 1] == "EMPTY"
                and vars.not_uncle_list[len(vars.not_uncle_list) - 1] == "EMPTY"
                and vars.uncle_list[len(vars.uncle_list) - 1] == "EMPTY"
            ):
                vars.danger_list.append("X")
            else:
                vars.danger_list.append(" ")

            element = [
                length,
                weight,
                tansok,
                sport,
                month,
                year,
                tagneed,
                status,
                graduation,
                degree,
                grade,
                percentage,
                father,
                mother,
            ]

            for i in range(len(element)):
                utils.check_element(element=element[i], element_list=element_list[i])

        except:
            print(f"Error in id = {val}")

            for i in range(len(element_list)):
                element_list[i].append("X")

            vars.brothers_list.append("X")
            vars.not_brothers_list.append("X")
            vars.uncle_list.append("X")
            vars.not_uncle_list.append("X")
            vars.danger_list.append("X")

    utils.save_file(std_no=data["STD_NO"], std_id=data["ID"])
    driver.find_element(By.CSS_SELECTOR, ".fa-sign-out-alt").click()
    print("sign-out clicked")


if __name__ == "__main__":
    main(
        url=vars.url["dawarat"],
        filename="Data.csv",
        student_kind="تأهيل معلمين مرحلة اولى ",
        sleep_time=0.7,
    )
