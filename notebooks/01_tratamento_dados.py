
# ==============================================================================
# ENTREGA 5: OBTENÇÃO, LIMPEZA E TRATAMENTO DOS DADOS (PIPELINE REPRODUZÍVEL)
# Projeto: Avaliação de Impacto - Programa Paraíba Sem Dívidas (CORECON-PB)
# Equipe: Carolina Maria, Larissa Sales e Taynara Ribeiro
# ==============================================================================

import pandas as pd
import numpy as np
import os
import datetime

# 1. OBTER E PRESERVAR: Configuração de caminhos e verificação dos dados originais
print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando o Pipeline de Dados...")

RAW_DIR = "../data/raw/"
PROCESSED_DIR = "../data/processed/"

# Leitura com verificação de integridade
path_t0 = os.path.join(RAW_DIR, "coleta_t0.csv")
path_t1 = os.path.join(RAW_DIR, "coleta_t1.csv")

if os.path.exists(path_t0) and os.path.exists(path_t1):
    df_t0_raw = pd.read_csv(path_t0)
    df_t1_raw = pd.read_csv(path_t1)
    print(f"Dados brutos carregados: T0 ({df_t0_raw.shape}) | T1 ({df_t1_raw.shape})")
else:
    print("Aviso: Arquivos brutos em data/raw/ não encontrados. Gerando estrutura do pipeline.")
    df_t0_raw = pd.DataFrame()
    df_t1_raw = pd.DataFrame()

# 2. INSPEÇÃO E LIMPEZA: Padronização de identificadores e unificação
if not df_t0_raw.empty and not df_t1_raw.empty:
    df_t0 = df_t0_raw.copy()
    df_t1 = df_t1_raw.copy()
    
    df_t0['fase'] = 'T0'
    df_t1['fase'] = 'T1'
    
    # Consolidação em painel longitudinal (Tidy Data)
    df_painel = pd.concat([df_t0, df_t1], ignore_index=True)
    
    # Padronização do identificador do participante
    df_painel['codigo_participante'] = df_painel['codigo_participante'].astype(str).str.strip().str.upper()
    
    # 3. TRANSFORMAR: Cálculo do Score de Letramento Financeiro (Bloco IV)
    gabarito_q1 = "Mais de R$ 124,00 (devido aos juros compostos)"
    gabarito_q2 = "Juros do crédito rotativo, que aumentam consideravelmente o valor da dívida"
    gabarito_q3 = "A taxa básica de juros da economia que influencia o custo dos empréstimos e investimentos"
    
    df_painel['score_q1'] = np.where(df_painel['bloco_4_q1'] == gabarito_q1, 1, 0)
    df_painel['score_q2'] = np.where(df_painel['bloco_4_q2'] == gabarito_q2, 1, 0)
    df_painel['score_q3'] = np.where(df_painel['bloco_4_q3'] == gabarito_q3, 1, 0)
    
    df_painel['score_letramento'] = df_painel['score_q1'] + df_painel['score_q2'] + df_painel['score_q3']
    
    # Transformação de inadimplência (Bloco III) em variável dummy (0 = Adimplente, 1 = Inadimplente)
    df_painel['dummy_inadimplente'] = np.where(df_painel['bloco_3_q3'] == 'Não (todas em dia)', 0, 1)
    
    # 4. VALIDAR E EXPORTAR: Testes de integridade e geração da base analítica
    assert len(df_painel) == len(df_t0_raw) + len(df_t1_raw), "Erro de integridade: número de linhas divergente!"
    
    output_path = os.path.join(PROCESSED_DIR, "base_painel_processada.csv")
    df_painel.to_csv(output_path, index=False)
    print(f"Base processada gerada com sucesso em: {output_path}")
