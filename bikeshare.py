import time
import pandas as pd
import numpy as np

#Dictionary that contains the references to the 3 city files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }

#Color codes initialization
CYAN='\033[36m'
BOLD='\033[1m'
HEADER = '\033[95m'
FAIL = '\033[91m'
END = '\033[0m'

def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.

    '''
    print('Hello! Let\'s explore some US bikeshare data!\n')

    while True:
        city=input("From the 3 cities listed below;\nchicago\nnew york city\nwashington\n\nChoose a City to analyse: ").lower()
        if city not in ('chicago','new york city','washington'):
            input(FAIL+'\nPlease insert correct city name!! Press Enter to continue...'+END)
            print()
        else:
            break

    #call the function that filters based on month,day or none or both
    choice=filter_inquiry()

    #Based on the return of filter_inquiry() function,the month_input(),day_input() or both might be called
    if choice=='month':
         month=month_input()
         day='all'
    elif choice=='day':
         day=day_input()
         month='all'
    elif choice=='none':
        month='all'
        day='all'
    elif choice=='both':
         month=month_input()
         day=day_input()

    return city, month, day

def filter_inquiry():
    '''
    based on the chosen city,filter by month or day or both or none

    '''
    #use of the global variable (reference no.2 readme.txt)
    global inquiry

    #based on the list of choices expected,prompt the user to make a choice
    inquiry_expected=['month','day','both','none']
    while True:
                    inquiry=input("\nAny specific month or day of your interest?\nType 'month' for month\nType 'day' for day\nType 'both' if interested in both\nType 'none' for no specifics:  ").lower()
                    if (inquiry not in inquiry_expected):
                      input(FAIL+'\nIncorrect input!!!.Please choose from the 4 available choices. Press Enter to continue...'+END)
                      print()
                    else:
                      break
    return inquiry

def month_input():
    '''
    User prompted for specific month based on the 'months' list, then the entered month is return to caller

    '''
    global months,month
    months=['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month=input("\nFrom the following available months:\njanuary\nfebruary\nmarch\napril\nmay\njune\n\nchoose a month for example 'january': ").lower()
        if month not in months:
            input(FAIL+'\nPlease insert Correctly!!!.Choose from the available months provided...Press enter to continue'+END)
        else:
            break
    return month

def day_input():
    '''
    User prompted for specific day based on the 'days' list, then the entered day is return to caller

    '''
    days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    while True:
        day=input("\nChoose day from the following;\nmonday\ntuesday\nwednesday\nthursday\nfriday\nsaturday\nsunday\n\nInsert day e.g 'monday': ")
        if day not in days:
            input(FAIL+"\nPlease insert day correctly!!!.for example 'monday'...Press enter to continue"+END)
        else:
            break
    return day

def load_data(city, month, day):
    '''
     Loads data into a dataframe for the specified city,edit the dataframe to add columns
     and filter by month of day if applicable
     '''
    global months
    df=pd.read_csv(CITY_DATA[city])

    #convert the Start Time column to datetime(reference no.1 in readme.txt)
    df['Start Time']=pd.to_datetime(df['Start Time'])

    # extract month and day of the week from the Start Time column to create an month
    #and day of week column (reference no.1 in readme.txt)
    df['month']=df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filter by month if applicable (reference no.1 in readme.txt)
    if month!='all':
        month = months.index(month.lower())+1
        df=df[df['month']==month]

    #filter by day of week if applicable (reference no.1 in readme.txt)
    if day!='all':
        df = df[df['day_of_week']==day.title()]

    return df

def time_stats(df):

    """
    Displays statistics on the most frequent times of travel.
    """
    #Dictionary of month names as  in the file and there respective integer keys in a dataframe
    month_name={1:'January',2:'February',3:'March', 4:'April',5:'May',6:'June'}

    print(BOLD+HEADER+'\nCalculating The Most Frequent Times of Travel...\n'+END+END)

    #keep track of the starting time
    start_time = time.time()
    global inquiry

    #Find the most frequent month,day and hour of travel
    popular_month=df['month'].mode()[0]
    popular_day=df['day_of_week'].mode()[0]
    popular_hour=df['Start Time'].dt.hour.mode()[0]

    #Counts of each month,day and hour in the dataframe
    count_months=df['month'].value_counts()
    count_days=df['day_of_week'].value_counts()
    count_hours=df['Start Time'].dt.hour.value_counts()

#Based on the return in the filter_inquiry(),print output where applicable
    if inquiry=='month':
        print(CYAN+'Popular Day Of Week:'+END+' {}\n'.format(popular_day)+CYAN+'Count:'+END+'{}\n\n'.format(count_days[popular_day])+CYAN+'Popular Hour:'+END+ '{}\n'.format(popular_hour)+CYAN+'Count'+END+'{}'.format(count_hours[popular_hour]))

    elif inquiry=='day':
        print(CYAN+'Popular Month:'+END+'{}\n'.format(month_name[popular_month])+CYAN+'Count:'+END+'{}\n\n'.format(count_months[popular_month])+CYAN+'Popular Hour:'+END+'{}\n'.format(popular_hour)+CYAN+'Count:'+END+'{}'.format(count_hours[popular_hour]))
    elif inquiry=='both':
        print(CYAN+'Popular Hour:'+END+'{}\n'.format(popular_hour)+CYAN+'Count:'+END+'{}'.format(count_hours[popular_hour]))

    elif inquiry=='none':
       print(CYAN+'Popular Month:'+END+'{}\n'.format(month_name[popular_month])+CYAN+'Count:'+END+'{}\n\n'.format(count_months[popular_month])+CYAN+'Popular Day Of Week:'+END+'{}\n'.format(popular_day)+CYAN+'Count:'+END+'{}\n\n'.format(count_days[popular_day])+CYAN+'Popular Hour:'+END+'{}\n'.format(popular_hour)+CYAN+'Count:'+END+'{}'.format(count_hours[popular_hour]))

#print the total time for the program to run process and print output
    print(CYAN+"\nThis took %s seconds." % (time.time() - start_time)+END)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print(BOLD+HEADER+'\nCalculating The Most Popular Stations and Trip...\n'+END+END)
    start_time = time.time()
    global inquiry

	#find the most commonly used start station and end_station
    popular_start_station=df['Start Station'].mode()[0]
    popular_end_station=df['End Station'].mode()[0]

    #counts of all the start and end stations
    count_start_station_use=df['Start Station'].value_counts()
    count_end_station_use=df['End Station'].value_counts()

	#find the most common trip
    #load a dataframe grouping start and end station then find the row/group with the maximum count (refrence No.3 in readme.txt)
    df_trip=df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'Count'})
    popular_trip=df_trip[df_trip['Count']==df_trip['Count'].max()]

	#count of trips on the popular trip
    popular_trip_count=popular_trip['Count'].values[0]

	#display of popular trip and stations
    print(CYAN+'Popular Start Station:'+END+'{}\n'.format(popular_start_station)+CYAN+'Count:'+END+'{}\n\n'.format(count_start_station_use[popular_start_station])+CYAN+'Popular End Station:'+END+' {}\n'.format(popular_end_station)+CYAN+'Count:'+END+'{}\n\n'.format(count_end_station_use[popular_end_station])+CYAN+'Popular Trip:'+END+'{}'.format(popular_trip['Start Station'].values[0])+CYAN+'   to'+END+'  {}\n'.format(popular_trip['End Station'].values[0])+CYAN+'Count:'+END+'{}'.format(popular_trip_count))

	#display of processing time
    print(CYAN+"\nThis took %s seconds." % (time.time() - start_time)+END)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(BOLD+HEADER+'\nCalculating Trip Duration...\n'+END+END)
    start_time = time.time()

    #display total travel time
    print(CYAN+'Total Travel Time:'+END+'{}\n'.format(float(df['Trip Duration'].sum()))+CYAN+'Avg:'+END+'{}'.format(float(df['Trip Duration'].mean())))

    #display mean travel time
    print(CYAN+"\nThis took %s seconds." % (time.time() - start_time)+END)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(BOLD+HEADER+'\nCalculating User Stats...\n'+END+END)
    start_time = time.time()

	#Pandas series of 'user types' in the dataframe
    users=df['User Type'].value_counts()

	#Display counts for each user type
    for i in range(users.size):
        print(CYAN+'{}:'.format(users.index[i])+END+'{}'.format(users.values[i]))
    print()

    #Checking for existance of a column in dataframe (refrence no.4 in readme.txt file)
    if 'Gender' in df.columns:
        gender=df['Gender'].value_counts()

    #Display counts of gender
        for i in range(gender.size):
            print(CYAN+'{}:'.format(gender.index[i])+END+'{}'.format(gender.values[i]))
    print()

    #Display earliest, most recent, and most common year of birth
    if 'Birth Year'in df.columns:#checking for existance of column in dataframe (refrence no.4 in readme.txt)
        early_year=int(df['Birth Year'].min())
        recent_year=int(df['Birth Year'].max())
        common_year=int(df['Birth Year'].mode()[0])

        print(CYAN+'Earliest Birth Year:'+END+'{}\n'.format(early_year)+CYAN+'Most Recent Birth Year:'+END+'{}\n'.format(recent_year)+CYAN+'Common Birth Year:'+END+'{}'.format(common_year))

    print(CYAN+"\nThis took %s seconds." % (time.time() - start_time)+END)

def unedited_df(city):
    '''
    Returns a dataframe containing raw data from a file.
    raw meaning unedited (just as in file)

    '''
    raw_df=pd.read_csv(CITY_DATA[city])
    return raw_df

def raw_data(raw_df):
    '''
    prompt user to request for more information or not
    '''
    raw=input("\nDo you want to see some(5 rows) of detailed individual information? Enter yes or no.\n").lower()
    print()

	#check the response
    raw=yes_no_input(raw)

	#Display individual detail information
    if raw!='no':
        count=5
        for j in range(count):#five rows
            for i in range(len(raw_df.columns)):#information of each column in each of the five rows
                #display each column details for next 5 rows
                print(CYAN+'{}:'.format(raw_df.iloc[j].index[i])+END+'{}'.format(raw_df.iloc[j].values[i]))
            print()

        #prompt user for more data as long more data is available
        while True:

            #Check if more data exists
            if count<=len(raw_df.index)-1:#find number of rows in the dataframe (reference no.7 in readme.txt)
                raw=input("\nDo you want to see more(next 5 rows) of detailed individual information? Enter yes or no\n").lower()
                raw=yes_no_input(raw)
            else:
                print('\nThere is no more available data!!.')
                break

            #Display the data
            if raw!='no':
                for j in range(5):
                    for i in range(len(raw_df.columns)):#find number of columns in the dataframe (reference no.7 in readme.txt)
                        print(CYAN+'{}:'.format(raw_df.iloc[count+j].index[i])+END+'{}'.format(raw_df.iloc[count+j].values[i]))
                    print()
                count+=5
            else:
                break

def yes_no_input(response):
    '''
    check  if response is within right response

    '''
    right_response=['yes','no']
    while response not in right_response:
        #use of variable in input() function to refer to user input(reference no.5 in readme.txt)
        response=input(FAIL+"\nDoes '{}' mean yes or no? For clarity, Please enter yes or no:\n".format(response)+END).lower()

    return response

def main():
    while True:

        #call function to get user input
        city, month, day = get_filters()

        #create dataframe from user input
        df = load_data(city, month, day)

        #call the functions on each city chosen
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_df=unedited_df(city)
        raw_data(raw_df)

		#prompt user to repeat process for new input
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        restart=yes_no_input(restart)
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
