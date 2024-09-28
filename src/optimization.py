import numpy as np
import scipy.optimize as sco

def portfolio_performance(weights, mean_returns, cov_matrix):
    """Calcula o retorno esperado e o risco (volatilidade) da carteira."""
    returns = np.sum(mean_returns * weights)
    risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, risk

def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    """Calcula o Sharpe Ratio negativo, para maximização."""
    returns, risk = portfolio_performance(weights, mean_returns, cov_matrix)
    sharpe_ratio = (returns - risk_free_rate) / risk
    return -sharpe_ratio

def optimize_portfolio(mean_returns, cov_matrix, risk_free_rate):
    """Otimiza a carteira usando o Sharpe Ratio."""
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = sco.minimize(neg_sharpe_ratio, num_assets * [1. / num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    return result
