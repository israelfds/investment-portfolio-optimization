import pandas as pd
import numpy as np
from utils import download_data, calculate_annualized_returns, calculate_covariance_matrix
from visualization import plot_efficient_frontier, plot_asset_allocation, plot_performance_history
from optimization import optimize_portfolio

def main():
    # Defina os parâmetros
    tickers = ['TSLA', 'BTC-USD', 'NVDA', 'PBR', 'BBAS3.SA']
    start_date = '2023-09-27'
    end_date = '2024-09-27'
    risk_free_rate = 0.05  # Taxa livre de risco

    # Baixar os dados
    data = download_data(tickers, start=start_date, end=end_date)
    
    # Calcular retornos anualizados e matriz de covariância
    mean_returns = calculate_annualized_returns(data)
    cov_matrix = calculate_covariance_matrix(data)

    # Otimizar a carteira
    optimized_result = optimize_portfolio(mean_returns, cov_matrix, risk_free_rate)
    optimized_weights = optimized_result.x

    # Plotar a fronteira eficiente
    plot_efficient_frontier(mean_returns, cov_matrix, risk_free_rate)

    # Plotar a alocação de ativos otimizada
    plot_asset_allocation(optimized_weights, tickers)

    # Plotar a evolução do retorno e risco
    plot_performance_history(data)

if __name__ == "__main__":
    main()
