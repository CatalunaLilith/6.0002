# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy


# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

the_climates = Climate("data.csv")
# print(the_climates. get_daily_temp("SEATTLE", 1, 2, 2000))

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """

    #innitialize empty list
    models_list = []
    #run poly fit for each degree in degs, store to list
    for deg in degs:
        a_model = pylab.polyfit(x,y, deg)
        models_list.append(a_model)
    #return list
    return models_list



test_models = (generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2]))
"""
Should print something close to
[array([ -1.10000000e+00, 2.15270000e+03]),
 array([ 6.83828238e-14, -1.10000000e+00, 2.15270000e+03])]
"""

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    #calc mean error
    error = ((estimated-y)**2).sum()
    mean_error = error / len(y)
    #calc varience
    var = (abs(y - y.mean())**2).mean()
    #calc r squared
    r_squared = 1 - (mean_error / var)
    return r_squared
    


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        x = numpy.rint(x)
        y = pylab.array(y)
        #create array of estimated y values, based on model
        y_est = pylab.polyval(model,x) 
        model_order = (len(model) -1)
        r_squared_value = round(r_squared(y, y_est),3)
        #create plot with measured y values (blue dots) and estimated y values (red line)
        pylab.figure()
        # pylab.xticks(x) #uncomment to force axis to show all year values
        pylab.plot(x, y_est, "r-", label = "model estimated y values")
        pylab.plot(x, y, "bo", label = "measured y values")
        pylab.xlabel("Year")
        pylab.ylabel("Degrees C")
        #for order 1 model, add ratio of standard error over the slope to title
        if model_order == 1:
            se_over_slope_value = round(se_over_slope(x, y, y_est, model), 4)
            pylab.title("Average Yearly Temperatures" + "\n" + " Model of order "  + str(model_order) + ", R squared = " + str(r_squared_value) + ", Ratio of standard error over slope = " + str(se_over_slope_value))
        else:
            pylab.title("Average Yearly Temperatures" + "\n" + " Model of order " + str(model_order) + ", R squared = " + str(r_squared_value))
        pylab.legend()
        pylab.show()
        
        
# x =  pylab.array([1961, 1962, 1963])
# y = pylab.array([-4.2, -5.6, -6.4])
# evaluate_models_on_training(x, y, test_models)


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    national_yearly_average_value_list = []
    for year in years:
        national_yearly_average_list = []
        for city in multi_cities:
            #calc average temp for city, add to list of average temp for cities, for a given year
            city_yearly_average_array = climate.get_yearly_temp(city, year)
            city_yearly_average_value = numpy.mean(city_yearly_average_array )
            national_yearly_average_list.append(city_yearly_average_value)
        #calc average temp for cities, for a given year
        national_yearly_average_array = pylab.array(national_yearly_average_list)
        national_yearly_average_value = numpy.mean(national_yearly_average_array)
        #make list of average temps of cities, for each year in interval
        national_yearly_average_value_list.append(national_yearly_average_value)
    return national_yearly_average_value_list


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    #assume WL=5 
    moving_average_list = []
    #find average and append for y[0] to y[3]
    moving_average_list.append(y[0])
    moving_average_list.append((y[0]+y[1])/2)
    moving_average_list.append((y[0]+y[1]+y[2])/3)
    moving_average_list.append((y[0]+y[1]+y[2]+y[3])/4)
    #find average and append for y[4] to y[n]
    for i in range(4,len(y)):
        average = (y[i-4]+y[i-3]+y[i-2]+y[i-1]+y[i])/5
        moving_average_list.append(average)
    #convert moving_average_list to array
    moving_average_array = pylab.array(moving_average_list)
    #return moving_average_array
    return moving_average_array
    
# y = pylab.array([1,2,3,4,5,6,7,8,9,10])
# print(moving_average(y, 5))
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    top_sum = 0 
    for i in range(len(y)):
        top = (y[i] - estimated[i]) ** 2
        top_sum += top
    bottom = len(y)
    RMSE = (top_sum / bottom) ** 0.5
    return RMSE 
        
# y = pylab.array([1,2,3,4,5,6,7,8,9,10])
# estimated = pylab.array([10,2,3,4,5,6,7,8,9,10])
# print(rmse(y,estimated))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_list = []
    #calc std of daily averages, for all years
    for year in years:
        #calc average temp across all cities, for each day
        alldays_all_cities_temp_with_nan_list = []
        for month in range(1,13):
            for day in range(1,32):
                #calc temp for a day, average across all cities
                aday_all_cities_temp_list  = []
                for city in multi_cities:
                    if day in climate.rawdata[city][year][month]:
                        aday_acity_temp_value = climate.get_daily_temp(city, month, day, year)
                        aday_all_cities_temp_list.append(aday_acity_temp_value)
                aday_all_cities_temp_value = numpy.mean(aday_all_cities_temp_list)
                alldays_all_cities_temp_with_nan_list.append(aday_all_cities_temp_value)
                alldays_all_cities_temp_with_nan_array = pylab.array(alldays_all_cities_temp_with_nan_list)
                alldays_all_cities_temp_array = alldays_all_cities_temp_with_nan_array[numpy.logical_not(numpy.isnan(alldays_all_cities_temp_with_nan_array))]
        #calc std of the daily averages for one year, store to std_list
        an_std = numpy.std(alldays_all_cities_temp_array)
        std_list.append(an_std)
    return std_list

# years = pylab.array(TRAINING_INTERVAL)
# result = gen_std_devs(the_climates, ['SEATTLE'], years)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        x = numpy.rint(x)
        y = pylab.array(y)
        #create array of estimated y values, based on model
        y_est = pylab.polyval(model,x) 
        model_order = (len(model) -1)
        rmse_value = round(rmse(y, y_est),3)
        #create plot with measured y values (blue dots) and estimated y values (red line)
        pylab.figure()
        # pylab.xticks(x) #uncomment to force axis to show all year values
        pylab.plot(x, y_est, "r-", label = "model estimated y values")
        pylab.plot(x, y, "bo", label = "measured y values")
        pylab.xlabel("Year")
        pylab.ylabel("Degrees C")
        pylab.title("Temperatures" + "\n" + " Model of order " + str(model_order) + ", RMSE = " + str(rmse_value))
        pylab.legend()
        pylab.show()

if __name__ == '__main__':

    the_climates = Climate("data.csv")
    #convert TRAINING_INTERVAl from range to list to array
    TRAINING_INTERVAL_list = list(TRAINING_INTERVAL)
    TRAINING_INTERVAL_array = pylab.array(list(TRAINING_INTERVAL))
    #convert TESTING_INTERVAl from range to list to array
    TESTING_INTERVAL_list = list(TESTING_INTERVAL)
    TESTING_INTERVAL_array = pylab.array(list(TESTING_INTERVAL))
    

    # # Part A.4i
    # #generate data samples for January 10th New Your City in trainign interval
    # training_jan10_NYC_yvals = []
    # for year in TRAINING_INTERVAL:
    #     training_jan10_NYC_yvals.append(the_climates.get_daily_temp("NEW YORK", 1, 10, year))
    # training_jan10_NYC_vyals = pylab.array(training_jan10_NYC_yvals)
    # #fit your data to a degree-one polynomial with generate_models
    # training_jan10_NYC_models = generate_models(TRAINING_INTERVAL_array, training_jan10_NYC_yvals, [1])
    # #plot the regression results using evaluate_models_on_training
    # evaluate_models_on_training(TRAINING_INTERVAL_array, training_jan10_NYC_yvals, training_jan10_NYC_models)
    
    # # Part A.4ii
    # #generate data samples for yearly average New York City in training interval
    # training_yearly_NYC_yvals = []
    # for year in TRAINING_INTERVAL:
    #     year_daily_temps_array = the_climates.get_yearly_temp("NEW YORK", year)
    #     year_average_value = numpy.mean(year_daily_temps_array)
    #     training_yearly_NYC_yvals.append(year_average_value)
    # training_yearly_NYC_yvals = pylab.array(training_yearly_NYC_yvals)
    # #fit your data to a degree-one polynomial with generate_models 
    # training_yearly_NYC_models = generate_models(TRAINING_INTERVAL_array,training_yearly_NYC_yvals, [1])
    # #plot the regression results with evaluate_models_on_training
    # evaluate_models_on_training(TRAINING_INTERVAL_array, training_yearly_NYC_yvals, training_yearly_NYC_models)


    # Part B
    #Training Interval, Yearly average temperature, National Average
    training_yearly_national_yvals = gen_cities_avg(the_climates, CITIES, TRAINING_INTERVAL_list)

    # # Part C
    #moving average temperatures of national yearly temperatures with a window size of 5, in TRAINING INTERVAL
    training_moving_average_yvals = moving_average(training_yearly_national_yvals, 5)
    #fit the (year, moving average) samples a to a degree-one polynomial with generate_models
    # training_moving_average_models = generate_models(TRAINING_INTERVAL_array, training_moving_average_yvals, [1])
    #plot the regression results with evaluate_models_on_training.
    # evaluate_models_on_training(TRAINING_INTERVAL_array, training_moving_average_yvals, training_moving_average_models)


    # Part D.2i
    #Compute 5-year moving averages of the national yearly temperature on TRAINING_INTERVAL
    training_moving_average_yvals = moving_average(training_yearly_national_yvals, 5)
    #Fit the samples to polynomials of degree 1, 2 and 20 with generate_models
    training_moving_average_models_1_2_20 = generate_models(TRAINING_INTERVAL_array, training_moving_average_yvals, [1,2,20])
    #Use evaluate_models_on_training to plot your fitting results
    evaluate_models_on_training(TRAINING_INTERVAL_array, training_moving_average_yvals, training_moving_average_models_1_2_20)

    # Part D.2ii
    testing_yearly_national_yvals = gen_cities_avg(the_climates, CITIES, TESTING_INTERVAL_list)
    #Compute 5-year moving averages of the national yearly temperature on TEST_INTERVAL
    testing_moving_average_yvals = moving_average(testing_yearly_national_yvals, 5)
    #use generated models from D.2i
    #use evaluate_models_on_testing to plot your fitting results
    evaluate_models_on_testing(TESTING_INTERVAL_array, testing_moving_average_yvals, training_moving_average_models_1_2_20)


    # Part E
    # Use gen_std_devs, over all 21 cities, over theyears in the training interval
    training_std_devs_national_y_vals = gen_std_devs(the_climates, CITIES, TRAINING_INTERVAL_list)
    #Compute 5-year moving averages on the yearly standard deviations.
    training_std_devs_national_5year_moving_average_yvals = moving_average(training_std_devs_national_y_vals, 5)
    #fit your data to a degree-one polynomial with generate_models 
    training_std_devs_national_models = generate_models(TRAINING_INTERVAL_array, training_std_devs_national_5year_moving_average_yvals, [1])
    #plot the regression results with evaluate_models_on_training
    evaluate_models_on_training(TRAINING_INTERVAL_array, training_std_devs_national_5year_moving_average_yvals, training_std_devs_national_models)
