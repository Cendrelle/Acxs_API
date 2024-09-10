from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

download_dir = "C:/Users/Mselle FAIZOUN/Desktop/vscode/acxsapi/API/fichiers"

def setup_driver():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    return driver

def download_files():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.marches-publics.bj/plan-de-passation")

    plans_per_page = 20
    total_plans = 265
    total_pages = (total_plans // plans_per_page) + (1 if total_plans % plans_per_page != 0 else 0)

    for page_number in range(1, total_pages + 1):
        download_plan_details(driver, wait, page_number)
        if not go_to_next_page(driver, wait):
            break

    driver.quit()

def download_plan_details(driver, wait, page_number):
    details_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[mattooltip="Ouvrir la liste des réalisations"]')))
    for i, button in enumerate(details_buttons):
        try:
            details_buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[mattooltip="Ouvrir la liste des réalisations"]')))
            wait.until(EC.element_to_be_clickable(details_buttons[i])).click()
            export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-button-base img[alt='EXCEL']")))

            file_name = f"plan_de_passation_page_{page_number}_plan_{i + 1}.xlsx"
            file_path = os.path.join(download_dir, file_name)
            if not os.path.exists(file_path):
                export_button.click()
                time.sleep(5)
            else:
                print(f"Le fichier {file_name} existe déjà.")
            driver.back()

        except Exception as e:
            print(f"Erreur sur le plan de passation {i + 1} à la page {page_number}: {e}")

def go_to_next_page(driver, wait):
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.mat-paginator-navigation-next')))
        if next_button.is_enabled():
            next_button.click()
            return True
        return False
    except Exception as e:
        print(f"Erreur lors du passage à la page suivante: {e}")
        return False
