import pandas as pd
import numpy as np
from tensorflow import keras


def main():

    model = keras.models.load_model('my_model')

    df = pd.read_csv('adjacent_Counties_DataFrame.csv')

    df['Difference in Population'] = df['Population'] - df['Adjacent Population']

    df['Difference in Population Density'] = df['County Population Density'] - df['Adjacent County Population Density']

    df['Difference in Previous Cases'] = df['Previous Cases'] - df['Adjacent Previous Cases']

    data = df[['Cases', 'Adjacent Cases', 'County Population Density', 'Difference in Population Density', 'Population', 'Difference in Population', 'Previous Cases', 'Difference in Previous Cases']]

    avg_error = 0.0

    avg_RMSE = 0.0

    most_accurate = 100.0

    least_accurate = 0.0

    for i in range(100):

        wholeRow = data.sample(1)

        sample = wholeRow.loc[:, wholeRow.columns != 'Adjacent Cases']

        actual = wholeRow.loc[:, wholeRow.columns == 'Adjacent Cases']

        actual_case = actual['Adjacent Cases'].values[0]

        prediction = model.predict(sample)[0][0]

        rmse = np.sqrt(np.square(actual_case - prediction))

        difference = actual_case - prediction

        print('Row from sample: ')

        print(sample.iloc[[0]])

        print('Accuracy ')

        print('Prediction: ', prediction)

        print('Actual: ', actual_case)

        print('Difference(Actual - Prediction): ', difference)

        print('RMSE: ', rmse)

        avg_error += difference

        avg_RMSE += rmse

        if(most_accurate > np.absolute(difference)):

            most_accurate = np.absolute(difference)

        if(least_accurate < np.absolute(difference)):

            least_accurate = np.absolute(difference)

        print(' ')

    print("------------------------------------------------------")

    print(' ')

    print('Average Difference: ', avg_error/100.0)

    print('Average Rmse: ', avg_RMSE/100.0)

    print('Most Accurate Prediction: ', most_accurate)

    print('Least Accurate Prediction: ', least_accurate)

    print(' ')

    print("------------------------------------------------------")

    print(' ')



main()
