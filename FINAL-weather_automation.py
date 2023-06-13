#!/usr/bin/env python
# coding: utf-8

# In[3]:


from __future__ import print_function
def inputs():
    import os.path
    if os.path.exists('info.txt') == False:
        zip_code = zip_code = str(input("What zip code do you want?"))
        allergies = str(input("What type(s) of pollen are you allergic to?"))
        with open('info.txt', 'w') as info:
            info.write(f'{zip_code}\n{allergies}')
# temp and UVI
def automation():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.action_chains import ActionChains
    from datetime import datetime
    import time
    with open('info.txt','r') as info:
        infos = info.readlines()
        zip_code = infos[0].strip()
        allergies = infos[1]
        info.close()
    driver = webdriver.Chrome('/Applications/chromedriver')
    national = "https://www.weather.gov/"

    driver.get(national)
    search = driver.find_element(By.XPATH,'//*[@id="inputstring"]')

    search.click()
    search.send_keys(zip_code)
    search.send_keys("\t")
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    time.sleep(1)

    temp = driver.find_element(By.XPATH,'//*[@id="current_conditions-summary"]/p[2]').text
    temp = temp.split("°")
    temp = int(temp[0])
    with open('current_temp.txt', 'w') as current_temp:
        current_temp.write(str(temp))
        current_temp.close()
    hour_weather = driver.find_element(By.XPATH, '//*[@id="wxGraph"]')
    hour_weather.click()
    digital_go = driver.find_element(By.XPATH,'/html/body/table[5]/tbody/tr[4]/td/table[1]/tbody/tr[1]/td/a')
    digital_go.click()
    time.sleep(1)

    rains = []
    temps = []
    times = []
    current_rain = driver.find_element(By.XPATH,'/html/body/table[6]/tbody/tr[11]/td[2]/font/b').text
    for column in range(2,26):
        rains.append(driver.find_element(By.XPATH,f'/html/body/table[6]/tbody/tr[11]/td[{column}]/font/b').text)
        temps.append(driver.find_element(By.XPATH,f'/html/body/table[6]/tbody/tr[4]/td[{column}]/font/b').text)
        times.append(driver.find_element(By.XPATH,f'/html/body/table[6]/tbody/tr[3]/td[{column}]/font/b').text)
    temp_time = dict(zip(times,temps))
    rain_time = dict(zip(times,rains))
    current_rain = int(current_rain)
    current_time = int(times[0])
    maxtemp = 0
    maxtime = 0
    for hours, highs in temp_time.items():
        if int(hours) >= current_time and int(highs) > maxtemp:
            maxtemp = int(highs)
            maxtime = int(hours)
    high = maxtemp
    high_time = maxtime
    maxpercip = 0
    maxhour = 0
    for hour, percip in rain_time.items():
        if int(hour) >= current_time and int(percip) > maxpercip:
            maxpercip = int(percip)
            maxhour = int(hour)
    max_rain = maxpercip
    maxrain_time = maxhour
    high_time = datetime.strptime(str(high_time), "%H")
    high_time = str(high_time.strftime("%-I") +" " +high_time.strftime("%p"))
    maxrain_time = datetime.strptime(str(maxrain_time), "%H")
    maxrain_time = str(maxrain_time.strftime("%-I") +" " +maxrain_time.strftime("%p"))
    
    uvi = f"https://enviro.epa.gov/envirofacts/uv/search/results/zipcode/{zip_code}"
    driver.get(uvi)
    time.sleep(3)
    try:
        uv = driver.find_element(By.XPATH,'/html/body/div[2]/main/div/div/article/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div/img').get_attribute("alt")
        uv = uv.split()
        uv = int(uv[3])
    except:
        print("an error occured")
        driver.close()

    pollen_count = f'https://www.pollen.com/forecast/current/pollen/{zip_code}'
    driver.get(pollen_count)
    time.sleep(1)
    #pollen = driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[1]/p[1]').text
    pollen = driver.find_element(By.XPATH,'//*[@id="today"]/p[1]').text
    pollen_types = []
    for pollen_type in range(2,5):
        try:
            type_pollen = driver.find_element(By.XPATH,f'/html/body/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/ul/li[{pollen_type}]/a/span[2]').text
            pollen_types.append(type_pollen)
        except:
            print('There are less than three allergies')
    driver.close()
    #pollen = pollen.split()
    #pollen = float(pollen[0])
    pollen = float(pollen)
    return temp, high, high_time, current_rain, max_rain, maxrain_time, uv, pollen, pollen_types
def outfit_text2(temp, high, high_time, current_rain, max_rain, maxrain_time, uv, pollen, pollen_types):
# Setting up Booleans
    with open('info.txt','r') as info:
        infos = info.readlines()
        allergies = infos[1]
        info.close()
    outfit = {"long_sleeve": False,
                   "short_sleeve": False,
                   "tank_top": False,
                   "pant": False,
                   "shorts": False,
                   "sunscreen": False,
                   "extra_layer": False,
                   "hoodie": False,
                   "raincoat": False}

    #pants
    with open('temp_scale.txt', 'r') as temps:
        tempss = temps.readlines()
        temps_dict = eval(tempss[0])
        temp_new = temps_dict[temp]
    if temp_new <= 70:
        outfit["pant"] = True
    elif temp_new > 70:
        outfit["shorts"] = True
        if uv <= 5: #don't change
            outfit["sunscreen"] = False
        elif uv >=6 and uv <= 11: # don't change
            outfit["sunscreen"] = True
    #shirt
    if temp_new <= 50:
        outfit["long_sleeve"] = True
        sunscreen = False
    elif temp_new > 50 and temp <= 95:
        outfit["short_sleeve"] = True
        if uv <= 5: #don't change
            outfit["sunscreen"] = False
        elif uv >=6 and uv <= 11: # don't change
            outfit["sunscreen"] = True
    #other layers
    if temp_new <= 65:
        outfit["hoodie"] = True
        outfit['sunscreen'] = False
    elif temp_new > 95:
        outfit["tank_top"] = True
        if uv <= 5: #don't change
            outfit["sunscreen"] = False
        elif uv >=6 and uv <= 11: # don't change
            outfit["sunscreen"] = True
    #extra layers
    if temp_new <= 45:
        outfit["extra_layer"] = True
        outfit["sunscreen"] = False
    if current_rain >= 65:
        outfit["raincoat"] = True
    else:
        outfit["raincoat"] = False
# Weather
    temp_text = ""
    clothes = ""
    summary = ""
    rain_coat = ""
    pollen_text = ""
    allergy_text = ""
    more_info = ""
    allergy_reminder = ""
    if current_rain == 0:
        temp_text = f"It is currently {temp}°F and there is currently no chance of rain."
        if max_rain == 0:
            temp_text += f"The high today is {high}°F at {high_time}. It appears that it will not rain today."
        else:
            temp_text += f"The high today is {high}°F (at {high_time}) with the highest predicted precipitation being {max_rain}% at {maxrain_time})."
    else:
        temp_text = f"It is currently {temp}°F and there is currently {current_rain} percent chance of rain. The high today is {high}°F (at {high_time}) with the highest predicted precipitation being {max_rain}% at {maxrain_time}. "
        clothes = "Based on the current weather you should wear "
        sun_text = f"The UV index today is {uv}. "
# Clothes
    clothes = "Based on the current weather you should wear "
    sun_text = f"The UV index today is {uv}. "
    if outfit["hoodie"] == True:
        if outfit["long_sleeve"] == True:
            if outfit["extra_layer"] == True:
                outfit += "pants, a long sleeve, a hoodie and"
                if temp_new < 40:
                    outfit += "a down jacket. "
                    summary = "Pants + long sleeve + hoodie + a down jacket + raincoat"
                elif temp_new >= 40:
                    outfit += "a light extra layer"
                    summary = "Pants + long sleeve + hoodie + a light extra layer + raincoat"
            else:
                clothes += "pants, a long sleeve shirt and a hoodie. "
                summary = "Pants + long sleeve + hoodie"
        elif outfit["pant"] == True and outfit["short_sleeve"] == True:
            clothes += "pants, a short sleeve shirt and a hoodie. "
            summary = "Pants + short sleeve + hoodie"
    else:
        if outfit["long_sleeve"] == True:
            clothes += "pants and a long sleeve shirt. "
            summary = "Pants + long sleeve"
        elif outfit["pant"] == True and outfit["short_sleeve"] == True:
            clothes += "pants and a short sleeve shirt. "
            summary = "Pants + short sleeve"
        elif outfit["shorts"] == True:
            if outfit["short_sleeve"] == True:
                clothes += "shorts and a short sleeve shirt. "
                summary = "Shorts + short sleeve"
            elif outfit["tank_top"] == True:
                clothes += "shorts and a tank top. "
                summary = "shorts + tank top"
# Raincoat
    if outfit["sunscreen"] == True:
        if outfit["raincoat"] == True:
            rain_coat = "With the current chance of rain you should also wear a raincoat. You may have to reapply. "
        elif max_rain > 80:
            rain_coat = "With the chance of rain today you should bring a raincoat. You may have to reapply sunscreen more frequently than every two hours today. " 
    else:
        if outfit["raincoat"] == True:
            rain_coat = "With the current chance of rain you should also wear a raincoat."
        elif max_rain > 80:
            rain_coat = "With the chance of rain today you should bring a raincoat."
# Sunscreen
    if outfit["sunscreen"] == True:
        if uv == 6 or uv == 7:
            sun_text += "You should wear sunscreen (SPF 15) today. If needed, wear a wide brimmed hat and sunglasses."
            more_info = "If you are going outside make sure to find shade. Without sunscreen it will take around 30 minutes to reach a sunburn with this UV index. Make sure to reapply sunscreen every two hours. "
        elif uv >=8 and uv <= 10:
            sun_text += "You definitely should wear sunscreen (SPF 30+) today. "
            more_info = "If you are going outside make sure to find shade you may want to wear a hat today. Without sunscreen it will take around 20 minutes to reach a sunburn with this UV index. Sand and other bright surfaces reflect UV and can double UV exposure. Make sure to reapply sunscreen every two hours. "
        elif uv >= 11:
            sun_text += "You need to wear sunscreen (SPF 30+) today."
            more_info = "If you are going outside make sure to find shade you may want to wear a hat today. Without sunscreen it will take less than 15 minutes to reach a sunburn with this UV index. . Sand and other bright surfaces reflect UV and can double UV exposure. Make sure to reapply sunscreen every two hours. "
    else:
        if outfit['pant'] == True and (outfit['long_sleeve'] == True or outfit["hoodie"] == True or outfit["extra_layer"] == True):
            sun_text = "You shouldn’t have to worry about sunscreen today."
            if temp < 35:
                more_info = "Snow can almost double UV exposure. "
        elif uv <= 2:
            sun_text += "If needed, wear sunglasses today. "
            more_info = " If you are going outside make sure to find shade. Without sunscreen it will take over an hour to reach a sunburn with this UV index. Make sure to reapply sunscreen every two hours. "
        elif uv >=3 and uv <= 5:
            sun_text += "You should think about wearing sunscreen (SPF 15) today. If needed, wear a hat or sunglasses as a precaution."
            more_info = "Try to reduce your exposure to UV radiation by finding some shade. Without sunscreen it will take around 40 minutes to reach a sunburn with this UV index. Make sure to reapply sunscreen every two hours. "
        elif uv == 6 or uv == 7:
            sun_text += "You should wear sunscreen (SPF 15) today. If needed, wear a wide brimmed hat and sunglasses."
            more_info = "If you are going outside make sure to find shade. Without sunscreen it will take around 30 minutes to reach a sunburn with this UV index. Make sure to reapply sunscreen every two hours. "
        elif uv >=8 and uv <= 10:
            sun_text += "You definitely should wear sunscreen (SPF 30+) today. "
            more_info = "If you are going outside make sure to find shade you may want to wear a hat today. Without sunscreen it will take around 20 minutes to reach a sunburn with this UV index. Sand and other bright surfaces reflect UV and can double UV exposure. Make sure to reapply sunscreen every two hours. "
        elif uv >= 11:
            sun_text += "You need to wear sunscreen (SPF 30+) today."
            more_info = "If you are going outside make sure to find shade you may want to wear a hat today. Without sunscreen it will take less than 15 minutes to reach a sunburn with this UV index. . Sand and other bright surfaces reflect UV and can double UV exposure. Make sure to reapply sunscreen every two hours. "
# Pollen
    pollen_bool = False
    if " " in allergies and "," not in allergies:
        allergies = allergies.lower().split()
    elif "," in allergies:
        allergies = allergies.lower().split(',')
        for item in allergies:
            item.strip()
    else:
        allergies = [allergies]

    pollen_text = "The allergy index today is "
    if pollen >= 0 and pollen <2.4:
        pollen_text += f"low ({pollen}). "
    elif pollen >= 2.5 and pollen <= 4.8:
        pollent_text += f"low-medium ({pollen}). "
        if pollen >= 4.0:
            pollen_bool = True
    elif pollen >= 4.9 and pollen <= 7.2:
        pollen_text += f"medium ({pollen}). "
        pollen_bool = True
    elif pollen >= 7.3 and pollen <= 9.6:
        pollen_text += f"medium-high ({pollen}). "
        pollen_bool = True
    elif pollen >= 9.7 and pollen <= 12.0:
        pollen_text += f"high ({pollen}). "
        pollen_bool = True
    allergy_info = "The allergy index is measured from 0.0 to 12.0."
    venn_allergy = []
    for pollen_type in pollen_types:
        if pollen_type.lower() in allergies:
            venn_allergy.append(pollen_type.lower())
        else:
            continue
    if pollen_bool == True:
        if len(allergies) == 1:
            if len(venn_allergy) == 1:
                allergy_text = f"Your pollen allergy ({venn_allergy[0]}) is in the top three types of pollen today. "
        elif len(allergies) == 2:
            nums = dict({1:['One','is'], 
                    2:['All', 'are']})
        elif len(allergies) == 3:
            nums = dict({1:['One','is'], 
                    2:['Two', 'are'], 
                    3:['All', 'are']})
        elif len(allergies) > 3:
            nums = dict({1:['One','is'], 
                    2:['Two', 'are'], 
                    3:['Three', 'are']})
    if pollen_bool == True:
        if len(venn_allergy) > 0 and len(venn_allergy)!= 1:
            # fix the allergies part so that it is allergy if there is only one allergy. 
            allergy_text = f"{nums[len(venn_allergy)][0]} of your pollen allergies"
            if len(venn_allergy) > 1:
                for allergy in range(len(venn_allergy)):
                    if len(venn_allergy) - allergy != 1:
                        allergy_text += f"{venn_allergy[allergy]}"
                    else:
                        allergy_text += f"{venn_allergy[allergy]}"
            else:
                allergy += f"{venn_allergy[0]}"
            allergy_text += f") {nums[len(venn_allergy)][1]} in the top three types of pollen today. "
        allergy_text += "Make sure to take your allergy pill today!"
    return [temp_text, clothes, rain_coat, sun_text, more_info, pollen_text, allergy_text, allergy_info, summary]
def gcal_event(temp, summary, temp_text, clothes, rain_coat, sun_text, pollen_text, allergy_text):
    import datetime
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from datetime import date
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    description = f'{temp_text}\n{clothes}'
    if rain_coat != "":
        description += rain_coat
    description += f'{sun_text}\n{pollen_text}{allergy_text}'
    service = build('calendar', 'v3', credentials=creds)
    today = date.today()
    event = {
      'summary': f'{temp}, {summary}',
      'description': description,
      'start': {
        'date': f'{today}',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'date': f'{today}',
        'timeZone': 'America/Los_Angeles',
      }
    }
    event = service.events().insert(calendarId='c_ed6821d9e8e539dee69255be285495d5972ea09095baf7e6b9bc4a958813113a@group.calendar.google.com',body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
def main():
    inputs()
    print("fetching information...")
    temp, high, high_time, current_rain, max_rain, maxrain_time, uv, pollen, pollen_types = automation()
    print("automation complete")
    temp_text, clothes, rain_coat, sun_text, more_info, pollen_text, allergy_text, allergy_info, summary = outfit_text2(temp = temp, high = high, high_time = high_time, current_rain = current_rain, max_rain = max_rain,maxrain_time = maxrain_time, uv = uv, pollen = pollen, pollen_types = pollen_types)
    print("creating google calender event...")
    gcal_event(temp, summary, temp_text, clothes, rain_coat, sun_text, pollen_text, allergy_text)
if __name__ == '__main__':
    main()


# In[ ]:




