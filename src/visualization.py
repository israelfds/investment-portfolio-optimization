import matplotlib.pyplot as plt
import numpy as np
from optimization import portfolio_performance  # Certifique-se de que o arquivo optimization.py está correto

def generate_random_weights(num_assets, num_portfolios):
    """Gera pesos aleatórios para portfólios que somam 1."""
    return np.random.dirichlet(np.ones(num_assets), num_portfolios)

def plot_efficient_frontier(mean_returns, cov_matrix, risk_free_rate):
    """Plota a fronteira eficiente com o Sharpe Ratio."""
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    
    # Gerar pesos de portfólio com somatório de 1
    weights_matrix = generate_random_weights(len(mean_returns), num_portfolios)
    
    for i in range(num_portfolios):
        weights = weights_matrix[i]
        returns, risk = portfolio_performance(weights, mean_returns, cov_matrix)
        sharpe_ratio = (returns - risk_free_rate) / risk
        
        results[0, i] = returns
        results[1, i] = risk
        results[2, i] = sharpe_ratio
    
    # Identificar o portfólio com maior Sharpe Ratio
    max_sharpe_idx = np.argmax(results[2])
    
    # Plotando a fronteira eficiente
    plt.figure(figsize=(10, 7))
    plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', marker='o')
    plt.colorbar(label='Sharpe Ratio')
    
    # Destaque para o portfólio com maior Sharpe Ratio
    plt.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], color='r', marker='*', s=200, label='Máx. Sharpe Ratio')
    
    plt.xlabel('Risco (Volatilidade)')
    plt.ylabel('Retorno Esperado')
    plt.title('Fronteira Eficiente: Risco vs Retorno')
    plt.legend()
    plt.grid(True)
    plt.savefig('fronteira_eficiente.png')
    plt.close()

def plot_asset_allocation(weights, tickers):
    """Plota a distribuição de ativos na carteira, removendo ativos estritamente com 0% de participação."""
    
    # Filtrar ativos com peso maior que um valor mínimo, como 0.01% para não ocultar valores muito pequenos
    min_percentage = 0.001  # 0.1% para o gráfico
    non_zero_weights = [(ticker, weight) for ticker, weight in zip(tickers, weights) if weight > min_percentage]
    
    # Separar os tickers e os pesos filtrados
    if len(non_zero_weights) == 0:
        print("Todos os ativos possuem pesos muito pequenos.")
        return

    filtered_tickers, filtered_weights = zip(*non_zero_weights)
    
    # Definir explode para destacar fatias com pesos relevantes, opcionalmente
    explode = [0.05 if w > 0.15 else 0 for w in filtered_weights]  # Explode para fatias > 15%
    
    # Plotando o gráfico de pizza
    plt.figure(figsize=(7, 7))
    plt.pie(filtered_weights, labels=filtered_tickers, autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
            startangle=140, explode=explode, colors=plt.cm.Paired.colors, wedgeprops={'edgecolor': 'black'})
    
    plt.axis('equal')  # Garante que o gráfico seja desenhado como um círculo
    plt.title('Distribuição de Ativos na Carteira')
    plt.savefig('distribuicao_ativos.png')  # Salva o gráfico como imagem
    plt.close()  # Fecha a figura
    
def plot_performance_history(data):
    """Plota a evolução dos retornos e riscos ao longo do tempo."""
    log_returns = np.log(data / data.shift(1))
    
    # Retorno cumulativo
    cumulative_returns = (1 + log_returns).cumprod()
    
    plt.figure(figsize=(10, 7))
    for column in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[column], label=column)
    
    plt.title('Evolução do Retorno Cumulativo ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Retorno Cumulativo')
    plt.legend()
    plt.grid(True)
    plt.savefig('evolucao_retorno.png')
    plt.close()

    # Volatilidade ao longo do tempo (21 dias de média)
    rolling_volatility = log_returns.rolling(window=21).std()
    
    plt.figure(figsize=(10, 7))
    
    for column in rolling_volatility.columns:
        plt.plot(rolling_volatility.index, rolling_volatility[column], label=column, linewidth=1.5)
    
    plt.title('Evolução da Volatilidade ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Volatilidade (21 dias)')
    plt.legend()
    plt.grid(True)
    plt.savefig('evolucao_risco.png')
    plt.close()
