import yfinance as yf
import numpy as np

def download_data(tickers, start, end):
    """Baixa dados históricos de ativos usando o yfinance."""
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    return data

def calculate_annualized_returns(data):
    """Calcula os retornos anualizados dos ativos."""
    log_returns = np.log(data / data.shift(1))
    return log_returns.mean() * 252  # 252 dias de negociação no ano

def calculate_covariance_matrix(data):
    """Calcula a matriz de covariância dos retornos dos ativos."""
    log_returns = np.log(data / data.shift(1))
    return log_returns.cov() * 252
