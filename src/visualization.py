import matplotlib.pyplot as plt
import numpy as np
from optimization import portfolio_performance  # Adicione esta linha

def plot_efficient_frontier(mean_returns, cov_matrix, risk_free_rate):
    """Plota a fronteira eficiente com o Sharpe Ratio."""
    # Criando uma série de portfólios
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights /= np.sum(weights)
        returns, risk = portfolio_performance(weights, mean_returns, cov_matrix)
        sharpe_ratio = (returns - risk_free_rate) / risk
        
        results[0,i] = returns
        results[1,i] = risk
        results[2,i] = sharpe_ratio
        
    # Plotando
    plt.figure(figsize=(10, 7))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Risco (Volatilidade)')
    plt.ylabel('Retorno Esperado')
    plt.title('Fronteira Eficiente: Risco vs Retorno')
    plt.grid()
    plt.savefig('fronteira_eficiente.png')  # Salva o gráfico como imagem
    plt.close()  # Fecha a figura

def plot_asset_allocation(weights, tickers):
    """Plota a distribuição de ativos na carteira."""
    plt.figure(figsize=(7, 7))
    plt.pie(weights, labels=tickers, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Distribuição de Ativos na Carteira')
    plt.savefig('distribuicao_ativos.png')  # Salva o gráfico como imagem
    plt.close()  # Fecha a figura

def plot_performance_history(data):
    """Plota a evolução dos retornos e riscos ao longo do tempo."""
    log_returns = np.log(data / data.shift(1))
    cumulative_returns = (1 + log_returns).cumprod()
    
    plt.figure(figsize=(10, 7))
    plt.plot(cumulative_returns, label='Retorno Cumulativo')
    plt.title('Evolução do Retorno Cumulativo ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Retorno Cumulativo')
    plt.legend()
    plt.savefig('evolucao_retorno.png')  # Salva o gráfico como imagem
    plt.close()  # Fecha a figura

    # Plotando a volatilidade ao longo do tempo
    rolling_volatility = log_returns.rolling(window=21).std()  # Volatilidade de 21 dias
    plt.figure(figsize=(10, 7))
    plt.plot(rolling_volatility, label='Volatilidade (21 dias)')
    plt.title('Evolução da Volatilidade ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Volatilidade')
    plt.legend()
    plt.savefig('evolucao_risco.png')  # Salva o gráfico como imagem
    plt.close()  # Fecha a figura
