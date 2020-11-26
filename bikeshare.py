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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    valid_cities = ['chicago','new york city','washington']
    city = input("Enter city (Chicago, New York City, Washington): ").lower()

    while True: 

        if city in valid_cities:
           break
        else:
           city = input("\nCity not in Chicago, New York City, or Washington.  Try again: ").lower()   


    # get user input for month (all, january, february, ... , june)

    valid_months = ['all','january','february','march','april','may','june']
    month = input("Enter month ('All','January','February','March','April','May','June'): ").lower()

    while True: 

        if month in valid_months:
           break
        else:
           month = input("\nMonth not in 'All','January','February','March','April','May','June'. Try again: ").lower()   


    # get user input for day of week (all, monday, tuesday, ... sunday)

    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    day = input("Enter day ('All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'): ").lower()

    while True: 

        if day in valid_days:
           break
        else:
           day = input("\nMonth not in 'All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'. Try again: ").lower()   


    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # fill NaN values
    if city != 'washington': 
       df['Gender'] = df['Gender'].fillna('Not Provided')

    df['User Type'] = df['User Type'].fillna('Not Provided')

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # find the most popular hour
    common_month = df['month'].mode()[0]

    # convert to month name
    month_names = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}
    common_month_name = month_names.get(common_month)
    
    print("\nMost common month:  {}".format(common_month_name.title())) 

    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print("\nMost common day:  {}".format(common_day.title())) 

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost common start hour:  {}".format(popular_hour)) 


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_start = df['Start Station'].mode()[0]
    print("\nMost common start station:  {}".format(popular_start)) 

    # display most commonly used end station

    popular_end = df['End Station'].mode()[0]
    print("\nMost common end station:  {}".format(popular_end)) 

    # display most frequent combination of start station and end station trip

    df['start end'] = df['Start Station'] + " / " + df['End Station']
    popular_combo = df['start end'].mode()[0]
    print("\nMost frequent combination:  {}".format(popular_combo)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    #  Help with displaying time in HH:MM:SS format from 
    #  https://stackoverflow.com/questions/62198128/python-elapsed-time-as-days-hours-minutes-seconds    

    duration_total = df['Trip Duration'].sum()
    duration_format = time.strftime('%H:%M:%S', time.gmtime(duration_total))
    print("\nTotal Trip Duration (HH:MM:SS):  {}".format(duration_format))    

    # display mean travel time

    duration_mean = df['Trip Duration'].mean()
    duration_mean_format = time.strftime('%H:%M:%S', time.gmtime(duration_mean))
    print("\nTotal Trip Duration Mean (HH:MM:SS):  {}".format(duration_mean_format))    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types = df.groupby(['User Type'])['User Type'].count()
    
    print("\n")
    print(user_types)


    if city != 'washington': 
       # Display counts of gender
     
       genders = df.groupby(['Gender'])['Gender'].count()
       print("\n")
       print(genders)

       # Display earliest, most recent, and most common year of birth

       print("\nEarliest Birth Year:  {}".format(int(df['Birth Year'].min())))
       print("\nMost Recent Birth Year:  {}".format(int(df['Birth Year'].max())))
       print("\nMost Common Birth Year:  {}".format(int(df['Birth Year'].mean())))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data_display(df,city):
    """Displays raw data by request."""

    valid_YN = ['yes','no']
    response = input("Would you like to see some raw data (Yes, No): ").lower()

    while True: 

        if response in valid_YN:
           break
        else:
           response = input("\nPlease respond with (Yes, No):  Try again: ").lower()   

    if response == 'yes':
       df_rows = df['User Type'].count()
       raw_start = 0
       if df_rows <= 5:
          raw_end = df_rows - 1
       else:
          raw_end = 4

    #  Help with iloc from https://www.sharpsightlabs.com/blog/pandas-iloc/
   
       while True: 
          for i in range(raw_start,raw_end + 1):
              print("\n*******************************************")
              print("Start Time:  {}".format(df['Start Time'].iloc[i])) 
              print("End Time:  {}".format(df['End Time'].iloc[i]))
              print("Trip Duration:  {}".format(df['Trip Duration'].iloc[i]))
              print("Start Station:  {}".format(df['Start Station'].iloc[i]))
              print("End Station:  {}".format(df['End Station'].iloc[i]))
              print("User Type:  {}".format(df['User Type'].iloc[i]))
              if city != 'washington':
                 print("Gender:  {}".format(df['Gender'].iloc[i]))
                 print("Birth Year:  {}".format(df['Birth Year'].iloc[i]))
              print("*******************************************\n")


        # if the end of the raw data is at the end of the data frame exit
          if raw_end + 1 == df_rows:
             break
            
          response = input("Would you like to see more raw data (Yes, No): ").lower()

          while True: 

              if response in valid_YN:
                 break
              else:
                 response = input("\nPlease respond with (Yes, No):  Try again: ").lower()   
         
          if response == "yes":
             raw_start += 5
             raw_end += 5
         #adjust end if at the end of the dataframe 
             if raw_end > df_rows - 1: 
                raw_end = df_rows - 1
          else:
             break   


def main():
    while True:
       city, month, day = get_filters()
       df = load_data(city, month, day)
       time_stats(df)
       station_stats(df)
       trip_duration_stats(df)
       user_stats(df,city)
       raw_data_display(df,city)

       restart = input('\nWould you like to restart? Enter yes or no.\n')
       if restart.lower() != 'yes':
           break


if __name__ == "__main__":
	main()
