import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

def analisar_impacto_programa(caminho_processed):
    """
    Executa os testes de hipótese e modelagem regressiva para medir a 
    efetividade das capacitações do CORECON-PB no orçamento doméstico.
    """
    # 1. Carregar a base de dados tratada
    df = pd.read_csv(caminho_processed)
    
    # Separar dados pareados T0 e T1
    t0_scores = df[df['fase'] == 'T0'].sort_values('id_participante')['score_literacy']
    t1_scores = df[df['fase'] == 'T1'].sort_values('id_participante')['score_literacy']
    
    # 2. Teste t pareado para alteração no Score de Letramento Financeiro
    t_stat, p_val_score = stats.ttest_rel(t0_scores, t1_scores)
    
    print("=== AVALIAÇÃO DO GANHO DE LETRAMENTO FINANCEIRO ===")
    print(f"Média T0: {t0_scores.mean():.2f} | Média T1: {t1_scores.mean():.2f}")
    print(f"Estatística t: {t_stat:.4f} | P-valor: {p_val_score:.4e}\n")
    
    # 3. Regressão Logística: Determinantes da Inadimplência na fase T1
    model_logit = smf.logit(
        "dummy_inadimplente ~ score_literacy + C(metodo_registro) + C(renda_faixa)", 
        data=df[df['fase'] == 'T1']
    ).fit()
    
    print("=== MODELO REGRESSIVO: DETERMINANTES DA INADIMPLÊNCIA (FASE T1) ===")
    print(model_logit.summary())

if __name__ == "__main__":
    analisar_impacto_programa('data/processed/dados_painel_paraiba_sem_dividas.csv')
