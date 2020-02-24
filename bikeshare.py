import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Define valid month options
months = ['january', 'february', 'march', 'april', 'may', 'june']
#Define day options
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Lets explore US bikeshare data!")
    # TO DO: get user input for city (chicago, new york city, washington).
    city = input("\nWould you like to see data for Chicago, New York City, or Washington?\n").lower()
    # while loop to handle invalid inputs. Error message built into alternate input.
    while city not in CITY_DATA:
        city = input('\nInvalid selection. Please enter "Chicago", "New York City", or "Washington".\n').lower()

    #While loop to handle invalid month/day inputs.
    while True:
        #Input for month/day/none selection
        time_filter = input("\nWould you like to filter the data by month or day?  Type 'none' for no time filter.\n").lower()
        #Define conditional input if user selects month
        if time_filter == 'month':
            month = input('\nWhich month - January, February, March, April, May, or June?\n').lower()
            #Embedded while loop to handle invalid month inputs.  References earlier "months" list at the beginning of the program.
            while month not in months:
                month = input("Invalid selection. Enter one of the following: January, February, March, April, May, or June?\n").lower()
            day = 'all'
            break
        #Define conditional input if user selects day
        if time_filter == 'day':
            day = input("\nWhich day - Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday?\n").lower()
            #Embedded while loop to handle invalid day inputs.  References earlier "days" list at the beginning of the program.
            while day not in days:
                day = input("Invalid selection. Enter one of the following: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday.\n").lower()
            month = 'all'
            break
        #Define day and month if "none" is chosen.
        if time_filter == 'none':
            day = 'all'
            month = 'all'
            break
        else:
            print('\nYou must enter "month", "day", or "none".  Please Try again.\n')

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) +1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
# find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('\nMost Frequent Start Hour:', popular_hour)

#Extract month and return a value that can be used as an index
    df['month'] = df['Start Time'].dt.month - 1
#Calculate most popular month and return index of that month
    popular_month_index = df['month'].mode()[0]
    #Use popular month index to look up in month options list and return the month name as result.
    popular_month = months[popular_month_index]
    print('\nMost Frequent Start Month:', popular_month)

#Calculate most popular day
    popular_day = df['day_of_week'].mode()[0]
    print('\nMost Frequent day:', popular_day)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

#display most commonly used start station
    start_station_mode = df['Start Station'].mode().iloc[0]
    print("\nMost popular start station: ", start_station_mode)
#display most commonly used end station
    end_station_mode = df['End Station'].mode().iloc[0]
    print("\nMost popular destination: ", end_station_mode)
#display most frequent combination of start station and end station trip
    combo_station_mode = (df['Start Station']+' --> '+ df['End Station']).mode()[0]
    print("\nMost popular trip: ", combo_station_mode)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\ntotal travel time:', total_travel_time)

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('\naverage travel time:', avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nCount of User Types:\n', user_types)

 # Display counts of gender.  Because Washington DC doesn't have gender data, code is enclosed in a try so that it can handle the key error and skip this code when we look up stats on Washington.
    try:
        gender_count = df.groupby(['Gender'])['Gender'].count()
    except KeyError:
        print("\nNo gender data available for Washington\n")
    else:
        print("\nGender Demographics:\n", gender_count)



# Display earliest, most recent, and most common year of birth.  Using Try because Washington doesn't have birth year data and I want to skip this code if we are looking up Washington

    try:
        birth_year_min = df['Birth Year'].min().astype(int)
        birth_year_max = df['Birth Year'].max().astype(int)
        birth_year_mode = df['Birth Year'].mode().iloc[0].astype(int)
    except KeyError:
        print("\nNo birth date data available for Washington\n")
    else:
        print ('\nEarliest birth year: ', birth_year_min, '\nlatest birth year: ', birth_year_max,'\nmost common birth year: ', birth_year_mode)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
#function gives the user the ability to look at the first 5 rows and then gives them the option to iterate through 5 lines at a time if they'd like to inspect further.
#used a while loop to keep iterating as long as user continues to answer "yes" or exit and move on when they don't.
    i = 0
    data = input("\nwould you like to view the first 5 lines of raw bikeshare data?\n").lower()
    if data != 'yes':
        print("skipping raw data display.")
    else:
        while True:
            window = df[(i * 5):5 +(i * 5)]
            print(window)
            i += 1
            re_raw = input("\nWould you like to see the next 5 rows of raw data?\n")
            if re_raw.lower() != 'yes':
                break



def main():
    #allow the user to re-run or exit if they so choose.
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
