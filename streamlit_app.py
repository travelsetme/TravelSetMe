from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import random
import base64
import re
from email.message import EmailMessage
import ssl
import smtplib
import time
import requests
import os
import json
import pymongo
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table
import string
import multiprocessing


class Process(multiprocessing.Process):
    def __init__(self, id):
        super(Process, self).__init__()
        self.id = id
                 
    def run(self):
        time.sleep(1)




class TravelOptions:

    def __init__(self):

        self.get_user_input()
        
    def empty_dataframe(my_df=None):
        if(my_df is None):
            my_df = pd.DataFrame()
        #stuff to do if it's not empty
        if(len(my_df) != 0):
            print(my_df)
        elif(len(my_df) == 0):
            print("Nothing")
        return my_df    
    
    global default_empty_dataframe
    
    default_empty_dataframe = empty_dataframe(None)
    
    def get_user_input(self):
        global selected_city
        global selected_flight_budget
        global selected_hotel_budget
        global selected_restorants_budget
        global user_email
        #global df_list_airports
        #global df_airports
        #global app_flights
        global our_email
        ############################### city choose ################################

        def get_base64(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

        def set_background(png_file):
            bin_str = get_base64(png_file)
            page_bg_img = '''
                    <style>
                    .stApp {
                    background-image: url("data:image/png;base64,%s");
                    background-size: cover;
                    }
                    </style>
                    ''' % bin_str
            st.markdown(page_bg_img, unsafe_allow_html=True)

        set_background(r"vacation_travel_picture.png")

        st.title("Travel All In One")
       
       
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        check_email = 'N'
        keys = random.sample(range(1000, 9999), 1)
        ################################### check email format #########################################################
            
        def check(email):
            
            email = email.strip()

            if (re.fullmatch(regex, email)):

                check_email = 'Y'

            else:

                check_email = 'N'

            return check_email
        
        global letters
        global letters_random
        
        global form_random_key
        
        
        
        letters = string.ascii_lowercase
        #letters_random = ''.join(random.choice(letters) for i in range(10))
        form_random_key = 'my_form' + letters
        
        #st.write(form_random_key)
            
        form = st.form(key=f"{form_random_key}")
            

        #form = st.form(key='my_form',clear_on_submit=True)


        selected_city = form.selectbox(
            'Enter Your Travel City : ',
            ('New York', 'San Francisco', 'Honolulu', 'Bankok', 'Barcelona', 'Dubai', 'Paris', 'london', 'Tel Aviv'))

        ############################### flight budget choose ########################

        global selected_flight_budget

        selected_flight_budget = form.selectbox(
            'Enter Your Flight Budget : ',
            ('500', '1000', '1500'))

        ########################### Hotel Budget Choose ######################################
        global selected_hotel_budget

        selected_hotel_budget = form.selectbox(
            'Enter Your Hotel Budget : ',
            ('50', '100', '150'))
        ########################### Restorants Budget Choose ######################################
        global selected_restorants_budget

        selected_restorants_budget = form.selectbox(
            'Enter Your Restorant Budget : ',
            ('50', '100', '150'))

        user_email = form.text_input(label='Enter Your Email', key=1)

        

        submit_counter = 0
        
        submit_button = form.form_submit_button(label='Submit')
        
        if submit_counter == 0:
            letters = string.ascii_lowercase
            form_random_key = 'my_form' + letters
            submit_counter = submit_counter + 1
        else:
            letters = string.ascii_lowercase
            letters_random = ''.join(random.choice(letters) for i in range(10))
            form_random_key = 'my_form' + letters_random
            form = st.form(key=f"{form_random_key}") 
            



        # user_email = st.text_input('Please Enter Your Email :')
        for i in keys:
            if submit_button:
                
                letters = string.ascii_lowercase
                letters_random = ''.join(random.choice(letters) for i in range(10))
                form_random_key = 'my_form' + letters_random
                form = st.form(key=f"{form_random_key}")

                if check(user_email) == 'N':
                    st.write('The email is invalid please type again and press submit')
                    None
                else:
                    self.Process_User_Input()
                    self.send_to_user_email(user_email)
                    form = st.empty()
                    submit_button = st.empty()
                    
                    letters = string.ascii_lowercase
                    letters_random = ''.join(random.choice(letters) for i in range(10))
                    form_random_key = 'my_form' + letters_random
                    form = st.form(key=f"{form_random_key}")
                    break




    def Process_User_Input(self):

        with st.spinner('Your Vacation Is On Its Way,Please Wait...'):
            
            app_flights = Flights().find_flight(selected_city)
            app_hotels = Hotels().find_hotels(selected_city)
            app_restorants = Restorants().find_restorants(selected_city)
            time.sleep(5)
            
        st.success('Done! Please Check Your Email For Your Vacation Recommendations for ' +  selected_city + '(Your Flights Are Listed Below) ')
        st.balloons()

    def send_to_user_email(self, user_email):

            email_sender = 'travel.app.flyer@gmail.com'
            email_password = 'efotfjtutkrsxzby'
            email_receiver = user_email

            subject = 'Check out your travel recommendations for ' + selected_city
            flights_list = ' '.join(map(str,df_list_airports))
            

            if df_airports_for_email.empty:
                flights_output = 'no flights available'
            else:
                flights_output = build_table(df_airports_for_email, 'blue_light')


            if df_hotels_for_email.empty:
                hotels_output = 'no hotels available'
            else:
                hotels_output = build_table(df_hotels_for_email, 'blue_light')


            ##print('hotels_output :',hotels_output)


            if df_restorants_for_email.empty:
                restorants_output = 'no restorants available'

            else:
                restorants_output = build_table(df_restorants_for_email, 'blue_light')

            body = "\n\n\n Your Recommended Travel Information Are - \n\n\n" + "\n\n\n FLIGHTS \n\n\n " + flights_output + "\n\n HOTELS \n\n " + hotels_output + "\n\n RESTORANTS \n\n " + restorants_output
            body_content = body
            message = MIMEMultipart()
            message.attach(MIMEText(body_content, "html"))
            message["Subject"] =  'Check out your travel recommendations for ' + selected_city
            msg_body = message.as_string()

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(msg_body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, msg_body)

        


class Flights():
    
   

    def find_flight(self, city):

        global df_list_airports
        global df_airports
        global df_airports_string

        global df_airports_for_email

        df_airports_for_email = default_empty_dataframe


        # print(city)
        url = "https://travel-advisor.p.rapidapi.com/airports/search"

        uri = 'mongodb+srv://tsafrir:tsafrir@cluster0.frf1eeg.mongodb.net/?retryWrites=true&w=majority'
        myclient = pymongo.MongoClient(uri)
        mydb = myclient["travel_app"]
        mycol = mydb["Flights"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        querystring = {"query": city, "locale": "en_US"}

        headers = {
            "X-RapidAPI-Key": "fe42155845mshc3b183a04c42514p1fc16djsnbb15492b29c4",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        list_json = json.loads(response.text)
        list_length = len(list_json)

        for i in range(0, list_length):
            # print(list_json[i])
            var_price = random.randint(900, 1000)
            var_flight_number = random.randint(10000, 15000)
            list_json[i]['flight_number'] = 'NY' + str(var_flight_number)
            list_json[i]['price_in_dollars'] = var_price
            mycol.insert_one(list_json[i])

        data = pd.DataFrame(list(mycol.find()))

        data_length = data.shape[0]

        data['Price'] = np.random.randint(900, 1000, data.shape[0])

        updated = data['longitude']

        data = data.applymap(str)

        df_airports = data.loc[:, ["name", "flight_number", "price_in_dollars"]]

        df_airports = df_airports.loc[
            df_airports["price_in_dollars"].apply(pd.to_numeric) <= int(selected_flight_budget)]

        df_list_airports = df_airports.values.tolist()

        df_airports.sort_values(by=['price_in_dollars'], ascending=False).head(3)

        df_airports = df_airports.head(3)

        try:
            df_airports_for_email = df_airports
        except Exception:
            df_airports_for_email = 'no flights found'


        df_airports_string = df_airports.to_string()

        def cell_colours(series):
            red = 'background-color: red;'
            yellow = 'background-color: yellow;'
            turquoise = 'background-color: turquoise;'
            default = ''

            return [red if data == "failed" else yellow if data == "error" else green if data == "passed"
            else turquoise for data in series]

        headers = {
            'selector': 'th.col_heading',
            'props': 'background-color: #000066; color: white;'
        }
        df_airports = df_airports.style.set_table_styles([headers]) \
            .apply(cell_colours)


        #styles = [dict(selector="caption", props=[("font-size", "100%"),
        #                                          ("font-weight", "bold")])]

        #df_airports.style.set_caption('Flights').set_table_styles(styles)

        #df_airports = df_airports.style.set_properties(**{
        #    'background-color': 'turquoise',
        #    'font-size': '15pt',
        #})




        st.table(df_airports)
        #print(df_list_airports)
        return df_list_airports


class Hotels():
    
 

    def find_hotels(self, city):

        global df_hotels_for_email
        global df_hotels_string

        df_hotels_for_email = default_empty_dataframe

        if city == 'New York':
            city = "60763"
        elif city == 'bangkok':
            city = "301643"
        elif city == 'Barcelona':
            city = "1465497"

        url = "https://travel-advisor.p.rapidapi.com/airports/search"

        uri = 'mongodb+srv://tsafrir:tsafrir@cluster0.frf1eeg.mongodb.net/?retryWrites=true&w=majority'
        myclient = pymongo.MongoClient(uri)
        mydb = myclient["travel_app"]
        mycol = mydb["Hotels"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        url = "https://travel-advisor.p.rapidapi.com/hotels/list"

        querystring = {"location_id": city, "adults": "1", "rooms": "1", "nights": "2", "offset": "0",
                       "currency": "USD", "order": "asc", "limit": "10", "sort": "recommended", "lang": "en_US"}

        headers = {
            "X-RapidAPI-Key": "fe42155845mshc3b183a04c42514p1fc16djsnbb15492b29c4",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }



        response_hotels = requests.request("GET", url, headers=headers, params=querystring)

        dict_json = json.loads(response_hotels.text)

        try:

                #print(' dict json :',dict_json)

                json_length = len(dict_json)

                #print('hotels_list_length :', json_length)

                for list_json in dict_json.values():

                    list_length = len(list_json)


                    try:
                        for i in range(0, list_length):
                            try:
                                # print(f"The value for your request is {list_json[i]}")
                                None
                                var_price = random.randint(50, 150)
                                var_flight_number = random.randint(10000, 15000)

                                list_json[i]['price_in_dollars'] = var_price

                                mycol.insert_one(list_json[i])
                            except KeyError:
                                None
                                # print(f"There is no parameter with the '{list_json[i]}' key. ")
                    except:
                        None


                df_hotels = pd.DataFrame(list(mycol.find()))

                #df_hotels = df_hotels.reset_index(inplace=True)

                additional_cols = ['price_in_dollars']

                df_hotels = df_hotels.reindex(df_hotels.columns.tolist(), axis=1)

                df_hotels = df_hotels.applymap(str)

                df_hotels = df_hotels.loc[:, ["name", "hotel_class", "price_in_dollars"]]

                df_hotels = df_hotels.loc[df_hotels["price_in_dollars"].apply(pd.to_numeric) <= int(selected_hotel_budget)]

                # df_hotels['hotel_class'] = df_hotels['hotel_class'].astype('int')

                df_hotels.sort_values(by=['hotel_class'], ascending=False).head(3)

                df_hotels = df_hotels.head(3)

                try:
                    df_hotels_for_email = df_hotels
                except Exception:
                    df_hotels_for_email = 'no hotels found'

                df_hotels_string = df_hotels.to_string()

                def cell_colours(series):
                    red = 'background-color: red;'
                    yellow = 'background-color: yellow;'
                    turquoise = 'background-color: turquoise;'
                    default = ''

                    return [red if data == "failed" else yellow if data == "error" else green if data == "passed"
                    else turquoise for data in series]

                headers = {
                    'selector': 'th.col_heading',
                    'props': 'background-color: #000066; color: white;'
                }
                df_hotels = df_hotels.style.set_table_styles([headers]) \
                    .apply(cell_colours)

                st.table(df_hotels)

        except Exception:
                df_hotels_string = 'Hotels API didn`t return results'
                st.write('Hotels API didn`t return results')

class Restorants():
    
  

    def find_restorants(self, city):

        global df_restorants_for_email
        global df_restorants_string

        df_restorants_for_email = default_empty_dataframe


        if city == 'New York':
            city = "60763"
        elif city == 'bangkok':
            city = "301643"
        elif city == 'Barcelona':
            city = "1465497"

        uri = 'mongodb+srv://tsafrir:tsafrir@cluster0.frf1eeg.mongodb.net/?retryWrites=true&w=majority'
        myclient = pymongo.MongoClient(uri)
        mydb = myclient["travel_app"]
        mycol = mydb["Restorants"]

        x = mycol.delete_many({})

        client = pymongo.MongoClient("mongodb://localhost:27017/")

        url = "https://travel-advisor.p.rapidapi.com/restaurants/list"

        querystring = {"location_id": city, "restaurant_tagcategory": "10591",
                       "open_now": "false", "lang": "en_US"}

        headers = {
            "X-RapidAPI-Key": "fe42155845mshc3b183a04c42514p1fc16djsnbb15492b29c4",
            "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
        }



        response_restorants = requests.request("GET", url, headers=headers, params=querystring)

        dict_json = json.loads(response_restorants.text)

        try:

                for list_json in dict_json.values():
                    # print(list_json)
                    list_length = len(list_json)

                    # print(list_length)
                    try:
                        for i in range(0, list_length):
                            try:
                                # print(f"The value for your request is {list_json[i]}")
                                None
                                var_price = random.randint(50, 150)
                                var_flight_number = random.randint(10000, 15000)
                                list_json[i]['price_in_dollars'] = var_price

                                mycol.insert_one(list_json[i])
                            except KeyError:
                                None
                                # print(f"There is no parameter with the '{list_json[i]}' key. ")
                    except:
                        None

                df_restorants = pd.DataFrame(list(mycol.find()))

                df_restorants = df_restorants.applymap(str)

                df_restorants = df_restorants.loc[:, ["name", "rating", "price_in_dollars"]]

                df_restorants = df_restorants.loc[
                    df_restorants["price_in_dollars"].apply(pd.to_numeric) <= int(selected_restorants_budget)]

                # df_restorants['rating'] = df_restorants['rating'].astype('int')

                df_restorants.sort_values(by=['rating'], ascending=False).head(3)

                df_restorants = df_restorants.head(3)

                try:
                    df_restorants_for_email = df_restorants
                except Exception:
                    df_restorants_for_email = 'no restorants found'

                df_restorants_string = df_restorants.to_string()

               # print(df_restorants)

                def cell_colours(series):
                    red = 'background-color: red;'
                    yellow = 'background-color: yellow;'
                    turquoise = 'background-color: turquoise;'
                    default = ''

                    return [red if data == "failed" else yellow if data == "error" else green if data == "passed"
                    else turquoise for data in series]

                headers = {
                    'selector': 'th.col_heading',
                    'props': 'background-color: #000066; color: white;'
                }
                df_restorants = df_restorants.style.set_table_styles([headers]) \
                    .apply(cell_colours)

                st.table(df_restorants)

                df = pd.DataFrame(
                    np.random.randn(1000, 2) / [50, 50] + [40.69, -74],
                    columns=['lat', 'lon'])

                st.map(df)

        except Exception:
                df_restorants_string = 'Restorants API didn`t return Results'
                TravelOptions().send_to_user_email(user_email)
                st.write('Restorants API didn`t return Results') 
    
    
        
if __name__ == '__main__':

    TravelOptions()
