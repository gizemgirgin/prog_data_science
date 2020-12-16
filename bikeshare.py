from datetime import timedelta
import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    
    
    validity = False 

    while True: 
      
        
        city = str(input("\nplease select a city(ies) (chicago, new york city, washington): ").strip().lower())

        if city not in ("chicago", "new york city", "washington"):
            print("\nPlease write one of chicago, new york or washington cities")
            continue
        else:
            print("\nYou will see the data of this city: '{}' ".format(city.title()))
            validityprocess()
            break

    while True:
        month = str(input("\nplease write a month name from January to June or all : ").strip().lower())

        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("\nPlease enter a month name (or \"all\" to select every month)")
            continue
        else:
            print("\nYou will see values for this month: '{}' ".format(month.title()))
            validityprocess()
            break

    while True:
        day = str(input("\nEnter a day of the week: ").strip().lower())

        if day not in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday" , "sunday", "all"):
            print("Please enter the name a day")
            continue
        else:
            print("\nYou will see a value for this day '{}' ".format(day.title()))
            validityprocess()
            break

    print("\nYou chose '{}' as city, '{}' as month, and '{}' as day. \nFiltering by your parameters....".format(city.title(), month.title(), day.title()))
    print()
    print('-'*40)
    return city, month, day

def validityprocess(): 
    
    while True: 
        validity = str(input("Are your entries correct? please enter "y" for yes, "n" for no and restart: \n").strip().lower())
        if validity not in ("y", "n"):
            print("\nYou entered an invalid value. Please enter "y" or "n"")
            continue
        elif validity == 'y':
            break
        else: 
            get_filters()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

   
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour

  
    if month != 'all':
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        
      
        month = months.index(month) + 1

     
        df = df[df['Month'] == month]


  
    if day != 'all':
       
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
     
        
        
        df = df[df['Day_of_Week'] == day.title()]
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nThe most popular times for travel are calculated...\n')
    start_time = time.time()

    # look_up dictionary 
    look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
        '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}

    #  the most popular month
    popular_month = df['Month'].mode()[0]
    month_in_string = look_up[str(popular_month)]
    print("1. Most popular month selected: ", month_in_string)

    # the most popular day
    popular_day = df['Day_of_Week'].mode()[0]
    print("2. Most popular day selected: {}".format(popular_day))

    # the most popular start hour
    popular_hour = df['Hour'].mode()[0]
    print('3. Most popular start hour selected:', popular_hour)


    print("\nIt tooks %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    

    start_station = df['Start Station'].mode()[0]
    print("1. most used station: '{}'".format(start_station))

    

    end_station = df['End Station'].mode()[0]
    print("2. most used station: '{}'".format(end_station))
    
    

    pair_final = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name="counts")
    
    frequent_start_pair = pair_final['Start Station'][0]
    frequent_end_pair = pair_final['End Station'][0]

    print("3. most used station combinations is '{}' and the end station is '{}'".format(frequent_start_pair, frequent_end_pair))

    print("\nIt tooks %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nTrip Duration is calculating...\n')
    start_time = time.time()

 

    total_travel_time = df['Trip Duration'].sum()

    t2 = total_travel_time.astype('float64', copy=False)
    time_in_duration = timedelta(seconds=t2)

    print("The total travel time in seconds is: '{}' which converts to '{}' in duration. ".format(total_travel_time, time_in_duration))

  
    mean_travel_time = df['Trip Duration'].mean()
    print("Average Mean travel time is: '{}' seconds ".format(mean_travel_time))

    print("\nIt tooks  %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

 

    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    
    if "Gender" in df.columns: 
        gender_count = df["Gender"].value_counts()

        
        nan_values = df["Gender"].isna().sum()

        print("\nCounts by Gender: \n{}\n \n*Note: there were '{}' NaN values for 'Gender' column".format(gender_count,nan_values))
    else:
        print("\nThere is no such 'Gender' in this dataset")

    #earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:

        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nEarliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(earliest, most_recent, most_common))

    else:
        print("\nThere is no such 'Birth Year' in this dataset")

        print("\nIt tooks %s seconds." % (time.time() - start_time))
        print('-'*40)

  


def raw_data(df): 
    
    
    display_raw_input = input("\nDo you want to see individual raw data? Enter 'yes' or 'no'\n").strip().lower()    
    if display_raw_input in ("yes", "y"):
        i = 0
        
        
        while True: 
                               
            if (i + 5 > len(df.index) - 1):
                
                print(df.iloc[i:len(df.index), :])
                print("you came to the last rows")
                break

            
            print(df.iloc[i:i+5, :])
            i += 5
            
           
            show_next_five_input = input("\nDo you want to see the next 5 lines? Enter 'yes' or 'no'\n").strip().lower()
            if show_next_five_input not in ("yes", "y"):
                break 


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWell, would you like to start over? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
