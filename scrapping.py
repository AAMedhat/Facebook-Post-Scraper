from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import re
import time
import csv
import os
import pandas as pd

# Set the Chrome options
option = Options()
option.add_argument('--headless')
option.add_argument('--disable-gpu')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

# Create the WebDriver instance
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=option)

def scrapping_photo(link,counter,save_directory_path):

    driver.get(link)
    driver.implicitly_wait(10)
    page = 1
    while(page<=counter):
        #open the webpage
        print("inloop")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        try:
            exit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close']"))).click()
        except Exception as e:
            print(e)
        # change from Most relevent to all comments
        AllComments = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div/div/span')

        driver.execute_script("arguments[0].click();", AllComments)
    #   wait time
        time.sleep(2)
        PressAllComments = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[3]/div[1]/div/div[2]/span')
        driver.execute_script("arguments[0].click();", PressAllComments)

    #     remove signup or login annoying container
        try:
            xpath_to_clear = "/html/body/div[1]/div/div[1]/div/div[4]/div/div"
            js_code = f'document.evaluate("{xpath_to_clear}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.innerHTML = "";'
            driver.execute_script(js_code)
        except Exception as e:
            print(e)   

        # press view more comments to load all comments availble
        WebDriverWait(driver, 150)
        viewMoreComments = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[4]/div[2]/div[1]/div[2]/span/span')


        try:
            while True:
                driver.execute_script("arguments[0].click();", viewMoreComments)
        except Exception as e:
               print(e)

        # press see More to load all comments availble
        WebDriverWait(driver, 50)
        try:
            while True:
                seeMore = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f']")))
                try:
                    while True:
                        driver.execute_script("arguments[0].click();", seeMore)
                except Exception as e:
                        print(e)

        except Exception as e:
            print(e)
        # Wait for the elements to be present
        try:
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            comment_elements = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, "div[class='x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi']")
            )
            print(comment_elements)
            print("*********************")
    #         try:
            post_comment = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]/span')
            post_comment_text = post_comment.text.strip()  # Remove leading/trailing whitespace
            post_comment_lines = post_comment_text.split('\n')
            print(post_comment_lines)
            print("***********************************************")
    #         except NoSuchElementException:
    #             post_comment_lines = ""
            try:
                post_date = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[1]/div[2]/div/div[2]/span/span/span[2]/span/a')
                post_date_text = post_date.text.strip()
            except Exception as e:
                print(e)
            try:
                post_commentno = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/span/div/div/div[1]/span')
                # post_commentno_text = post_commentno.text  
            except Exception as e:
                print(e)
            # Remove leading/trailing whitespace

    #         except NoSuchElementException:
    #             post_commentno_text = '0'


            try:
                post_likesno = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/span[2]/span/span')
                post_likesno_text = post_likesno.text  # Remove leading/trailing whitespace

            except NoSuchElementException:
                post_likesno_text = '0'
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            try:
                post_shareno = driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/span/div/div/div[1]/span')
                post_shareno_text = post_shareno.text  # Remove leading/trailing whitespace

            except NoSuchElementException:
                post_shareno_text = '0'

            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            authors = []
            comments = []
            replies = []
            likes = []
            date = []
            postcomment = []
            postcommentno = []
            postlikes = []
            postdate = []
            postshare = []
            print(comment_elements)
            print("######################################################################")
            # Iterate over the elements and separate the author, comment, and reply
            for element in comment_elements:
                text = element.text.strip()  # Remove leading/trailing whitespace
                lines = text.split('\n')  # Split into lines

                if lines[0].startswith('Author'):
                    replies.pop()  # Remove the last comment and use it as a reply
                    reply = ' '.join(lines[2:len(lines)-1])
                    replies.append(reply)

                else:
                    author = lines[0].strip()
                    authors.append(author)

                    postcomment.append(''.join(post_comment_lines))
                    postlikes.append(''.join(post_likesno_text))
                    postdate.append(''.join(post_date_text))
                    postshare.append(''.join(post_shareno_text))
                    # postcommentno.append(''.join(post_commentno_text))



                    reply = 'no reply'
                    replies.append(reply)

                    comment_text = []
                    i = 1
                    while i < len(lines) and not re.match(r'^\d+\s[w?m?h?d]\s?$', lines[i]):
                        comment_text.append(lines[i].strip())
                        i += 1

                    comments.append(' '.join(comment_text))

                    if i < len(lines) and re.match(r'^\d+\s[w?m?h?d]\s?$', lines[i]):
                        date.append(lines[i])
                        likes.append(lines[i + 1] if i + 1 < len(lines) and not lines[i + 1].startswith('Edited') else '0')
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        except Exception as e:
            print(e)    # Print the authors, comments, replies, likes, and date
        # postcommentno    , pcommentno
        for author, comment, reply, like, dt, pcomment, plikeno, pdt, pshareno in zip(authors, comments, replies, likes, date, postcomment, postlikes, postdate, postshare):
            print("Author:", author)
            print("Comment:", comment)
            print("Reply:", reply)
            print("Likes:", like)
            print("Date:", dt)
            print("post comment:", pcomment)
            print("post likes no:", plikeno)
            # print("post comment no:", pcommentno)
            print("post date:", pdt)
            print("post share no:", pshareno)
        
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # Write the author, comment, reply, likes, and date data to a CSV file with UTF-8 encoding
        with open((save_directory_path+"/"+(str(page)+".csv")), 'w', newline='', encoding='utf-8-sig') as csvfile:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            writer = csv.writer(csvfile)
            writer.writerow(["Author", "Comment", "Reply", "Likes", "Date", "post comment:", "post likes no:", "post comment no:", "post date:", "post share no:"])   # Write header row

            for author, comment, reply, like, dt, pcomment, plikeno, pdt, pshareno in zip(authors, comments, replies, likes, date, postcomment, postlikes, postdate, postshare):
                print(author)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                writer.writerow([author, comment, reply, like, dt, pcomment, plikeno, pdt, pshareno])
    #     quit web page
        print("*******************************************************")
        print("!!!!!!!!!!!!!! Done!!!!!!!!!!!!!!!!!")
        print("*******************************************************")
        try:
            # Wait for the element to be clickable
            next_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Next photo']")))

            # Move the mouse cursor to the element
            action = ActionChains(driver)
            action.move_to_element(next_button).perform()

            # Click the element
            next_button.click()

            print("done")

        except Exception as e:
            print(e)

        page+=1
        # Set the folder path where your CSV files are located


    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(save_directory_path) if file.endswith('.csv')]

    # Initialize an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate through each CSV file and append its data to the combined DataFrame
    for file in csv_files:
        file_path = os.path.join(save_directory_path, file)
        df = pd.read_csv(file_path)
        combined_df = combined_df.append(df, ignore_index=True)

    # Export the combined DataFrame to a new CSV file
    output_csv_path = save_directory_path+'/combined_data.csv'
    
    combined_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')

    print(f"Combined data exported to: {output_csv_path}")


#     driver.quit()


link = input("Enter the link: ")
# output_directory = input("Enter the output directory: ")
output_directory = "/home"
timeout = int(input("Enter the count to link you want to scrap: "))

# Call the function with the provided parameters
scrapping_photo(link,int(timeout),output_directory)