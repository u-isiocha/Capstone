import numpy as np
import os
import xlsxwriter
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from scipy.stats import qmc, norm

kernel = ConstantKernel(1.0) * RBF(length_scale=1.0)

gp = GaussianProcessRegressor(
    kernel=kernel,
    alpha=1e-6,          # Measurement noise
    normalize_y=True,
    n_restarts_optimizer=10
)

def to_str(x):
    print(x.replace(' ', '-'))

def create_search_grid(array, n_candidates=5000):
    bounds = list(zip(array.min(axis=0), array.max(axis=0)))
    if array.shape[1] < 3:
        space = [np.linspace(i[0], i[1], array.shape[0]**2) for i in bounds]
        grid = np.meshgrid(*space)
        X_grid = np.column_stack([i.ravel() for i in grid])
    elif array.shape[1] > 2:
        dimensions = len(bounds)
        sampler = qmc.Sobol(d=dimensions)
        X = sampler.random(n=4096)
        lower = np.array([b[0] for b in bounds])
        upper = np.array([b[1] for b in bounds])
        X_grid = qmc.scale(X, lower, upper)
    return X_grid                          
                          
    
    
def ucb_acquisition(X, gp, beta=2.0):
    """
    Upper Confidence Bound (UCB) acquisition function.

    Parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        Candidate input locations.
    gp : GaussianProcessRegressor
        Trained Gaussian Process model.
    beta : float, optional
        Exploration parameter. Larger values encourage exploration.

    Returns
    -------
    ucb : ndarray
        UCB value at each candidate point.
    """
    # Predict mean and standard deviation
    mu, sigma = gp.predict(X, return_std=True)

    # Upper Confidence Bound
    ucb = mu + beta * sigma

    return ucb

def expected_improvement(X, gp, y_best, xi=0.01):
    """
    Expected Improvement (EI) acquisition function.

    Parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        Candidate input locations.
    gp : GaussianProcessRegressor
        Trained Gaussian Process model.
    y_best : float
        Best observed objective value.
    xi : float, optional
        Exploration parameter. Larger values encourage exploration.

    Returns
    -------
    ei : ndarray
        Expected Improvement at each candidate point.
    """

    # GP prediction
    mu, sigma = gp.predict(X, return_std=True)

    sigma = sigma.reshape(-1)
    mu = mu.reshape(-1)

    # Improvement
    improvement = mu - y_best - xi

    # Avoid division by zero
    Z = np.zeros_like(improvement)
    mask = sigma > 0
    Z[mask] = improvement[mask] / sigma[mask]

    ei = np.zeros_like(improvement)
    ei[mask] = (
        improvement[mask] * norm.cdf(Z[mask]) +
        sigma[mask] * norm.pdf(Z[mask])
    )

    return ei


def probability_improvement(X, gp, y_best, xi=0.01):
    """
    Probability of Improvement (PI) acquisition function.

    Parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        Candidate input locations.
    gp : GaussianProcessRegressor
        Trained Gaussian Process model.
    y_best : float
        Best observed objective value.
    xi : float, optional
        Exploration parameter.

    Returns
    -------
    pi : ndarray
        Probability of Improvement.
    """

    # GP prediction
    mu, sigma = gp.predict(X, return_std=True)

    sigma = sigma.reshape(-1)
    mu = mu.reshape(-1)

    improvement = mu - y_best - xi

    Z = np.zeros_like(improvement)
    mask = sigma > 0
    Z[mask] = improvement[mask] / sigma[mask]

    pi = np.zeros_like(improvement)
    pi[mask] = norm.cdf(Z[mask])

    return pi

betas = {'function_1': 2,
                'function_2': 1,
                'function_3': 5,
                'function_4': 2,
                'function_5': 2,
                'function_6': 2,
                'function_7': 0.1,
                'function_8': 0.1}

acq_function = {'function_1': expected_improvement,
                'function_2': expected_improvement,
                'function_3': expected_improvement,
                'function_4': ucb_acquisition,
                'function_5': expected_improvement,
                'function_6': probability_improvement,
                'function_7': ucb_acquisition,
                'function_8': ucb_acquisition}

directory = r"C:\Users\uisio\PycharmProjects\Machine Learning and AI\Capstone"

excel_path = os.path.join(directory, 'Capstone.xlsx')
function_path = os.path.join(directory, 'initial_data')
nexcel = os.path.join(directory, 'Capstone2.xlsx')

inputs = {}
outputs = {}
dfs = {}
functions = []
writer = pd.ExcelWriter(nexcel, engine='xlsxwriter')
for function in os.listdir(function_path):
    # folder_path = os.path.join(function_path, function)
    # ip = os.path.join(folder_path, "initial_inputs.npy")
    # op = os.path.join(folder_path, "initial_outputs.npy")
    # inputs = np.load(ip)
    # outputs = np.load(op)
    # cols = [f'input_{i+1}' for i in range(inputs.shape[1])]
    # idf = pd.DataFrame(data=inputs, columns=cols)
    # odf = pd.DataFrame(data=outputs, columns=['output'])
    # df = pd.concat([idf, odf], axis=1)
    # df.to_excel(writer, sheet_name=function, index=False)
    dfs[function] = pd.read_excel(excel_path, sheet_name=function)
    functions.append(function)

skip = ()     

for function in functions:
    df = dfs[function]
    cols = [f'input_{i+1}' for i in range(len(df.columns)-1)]
    inputs = np.array(df[cols])[:-1]
    output = np.array(df['output'])[:-1]
    X_candidates = create_search_grid(inputs)
    gp.fit(inputs, output)
    acquisition_function = ucb_acquisition
    if acquisition_function is ucb_acquisition:
        args = X_candidates, gp, betas[function]
    else:
        args = X_candidates, gp, max(output)
    result = acquisition_function(*args)
    next_point = X_candidates[np.argmax(result)]
    pt = list(np.round(next_point, 6))
    print_out = "-".join(map(str, pt))
    print(f'Next point for {function}: {print_out}')
    if int(function[-1]) not in skip:
        new_inputs = np.vstack((inputs, next_point))
    else:
        new_inputs = inputs
    ndf = pd.DataFrame(data=new_inputs, columns=cols)
    odf = pd.DataFrame(data=output, columns = ['output'])
    ndf = pd.concat([ndf, odf], axis=1)
    ndf.to_excel(writer, sheet_name=function, index=False)

writer.close()
    