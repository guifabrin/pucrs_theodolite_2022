import json
import os

import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression


def demand(exp_id, directory, threshold, warmup_sec):
    raw_runs = []
    # Compute SLI, i.e., lag trend, for each tested configuration
    filenames = [filename for filename in os.listdir(directory) if
                 filename.startswith(f"exp{exp_id}_") and "lag-trend" in filename and filename.endswith(".csv")]
    for filename in filenames:
        run_params = filename[:-4].split("_")
        dim_value = run_params[1]
        instances = run_params[2]
        df = pd.read_csv(os.path.join(directory, filename))
        input = df
        input['sec_start'] = input.loc[0:, 'timestamp'] - input.iloc[0]['timestamp']
        regress = input.loc[input['sec_start'] >= warmup_sec]  # Warm-Up
        X = regress.iloc[:, 3].values.reshape(-1, 1)  # values converts it into a numpy array
        Y = regress.iloc[:, 2].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        linear_regressor.predict(X)  # make predictions
        trend_slope = linear_regressor.coef_[0][0]
        row = {'load': int(dim_value), 'resources': int(instances), 'trend_slope': trend_slope}
        raw_runs.append(row)
    runs = pd.DataFrame(raw_runs)
    # Group by the load and resources to handle repetitions, and take from the reptitions the median
    # for even reptitions, the mean of the two middle values is used
    medians = runs.groupby(by=['load', 'resources'], as_index=False).median()
    # Set suitable = True if SLOs are met, i.e., lag trend slope is below threshold
    medians["suitable"] = medians.apply(lambda row: row['trend_slope'] < threshold, axis=1)
    suitable = medians[medians.apply(lambda x: x['suitable'], axis=1)]
    # Compute minimal demand per load intensity
    demand_per_load = suitable.groupby(by=['load'], as_index=False)['resources'].min()
    return demand_per_load


if __name__ == '__main__':
    results_dir = './temp'
    total_exp = 0
    try:
        f = open("{}/expID.txt".format(results_dir), "r")
        total_exp = int(f.read())
        f.close()
    except:
        pass
    for experiment_id in range(0, total_exp + 1):
        try:
            f = open("{}/exp{}-benchmark-configuration".format(results_dir, experiment_id), "r")
            benchmark_configuration = json.loads(f.read())
            f.close()
            f = open("{}/exp{}-execution-configuration".format(results_dir, experiment_id), "r")
            execution_configuration = json.loads(f.read())
            f.close()
            result = demand(experiment_id, results_dir, 1000, 0)
            result.to_csv(os.path.join(results_dir, f'exp{experiment_id}_demand.csv'), index=False)
            chart = sns.barplot(x='load', y='resources', data=result, ci=None, line_kws={'color': 'red'})
            chart.set(xlabel='messages', ylabel='minimum instances')
            chart.fig.set_size_inches(5, 5)
            chart.savefig('{}/exp{}.png'.format(results_dir, experiment_id))
        except:
            pass