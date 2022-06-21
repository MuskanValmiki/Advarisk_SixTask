# from cProfile import label
# import constantly
# from playwright.sync_api import sync_playwright
# from requests import head

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False,slow_mo=50)
#     page = browser.new_page()
#     page.goto("https://electoralsearch.in/##resultArea")
#     page.click('id=continue')
#     page.click('text=पहचान-पत्र क्र. द्वारा खोज/Search by EPIC No.')
#     page.fill('#name','501');
#     page.click('id=epicStateList')
#     page.select_option('#t in statedata','Andhra Pradesh')
#     # const selectValue = page.$eval('#t in statedata',(element)=>element.value);
#     # expect(selectValue).toContain('Andhra Pradesh')
#     import pdb;pdb.set_trace()

