
import pandas as pd
import json
import os

# Caminhos dos arquivos
ARQUIVO_ESCOLAS = "dados/Tabela_Escola_2025_V2.csv"
ARQUIVO_MATRICULAS = "dados/Tabela_Matricula_2025_V2.csv"
PASTA_RESULTADO = "resultado"
ARQUIVO_JSON = os.path.join(
    PASTA_RESULTADO,
    "instituicoes_pb_2025.json"
)

# Campos que deverão aparecer no JSON
campos = [
    "NO_ENTIDADE",
    "CO_ENTIDADE",
    "NO_UF",
    "SG_UF",
    "CO_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "NO_REGIAO_GEOG_INTERM",
    "CO_REGIAO_GEOG_INTERM",
    "NO_REGIAO_GEOG_IMED",
    "CO_REGIAO_GEOG_IMED",
    "NU_ANO_CENSO",
    "NO_REGIAO",
    "CO_REGIAO",
    "QT_MAT_BAS",
    "QT_MAT_INF",
    "QT_MAT_FUND",
    "QT_MAT_MED",
    "QT_MAT_PROF",
    "QT_MAT_EJA",
    "QT_MAT_ESP"
]

# Verifica se os arquivos existem
if not os.path.exists(ARQUIVO_ESCOLAS):
    raise FileNotFoundError("Arquivo de escolas não encontrado.")

if not os.path.exists(ARQUIVO_MATRICULAS):
    raise FileNotFoundError("Arquivo de matrículas não encontrado.")

print("Lendo os dados do Censo Escolar 2025...")

# Leitura dos arquivos CSV
escolas = pd.read_csv(
    ARQUIVO_ESCOLAS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

matriculas = pd.read_csv(
    ARQUIVO_MATRICULAS,
    sep=";",
    encoding="latin1",
    low_memory=False
)

# Padroniza os nomes das colunas
escolas.columns = escolas.columns.str.upper().str.strip()
matriculas.columns = matriculas.columns.str.upper().str.strip()

# Filtra as instituições da Paraíba
escolas_pb = escolas[
    escolas["CO_UF"] == 25
].copy()

# Seleciona as informações de matrícula
colunas_matricula = [
    "CO_ENTIDADE",
    "QT_MAT_BAS",
    "QT_MAT_INF",
    "QT_MAT_FUND",
    "QT_MAT_MED",
    "QT_MAT_PROF",
    "QT_MAT_EJA",
    "QT_MAT_ESP"
]

matriculas = matriculas[colunas_matricula]

# Relaciona as escolas com suas matrículas
dados = pd.merge(
    escolas_pb,
    matriculas,
    on="CO_ENTIDADE",
    how="left"
)

# Seleciona somente os campos solicitados
dados = dados[campos]

# Substitui valores ausentes por zero nas matrículas
campos_matricula = campos[14:]

dados[campos_matricula] = dados[
    campos_matricula
].fillna(0)

# Converte os nomes das colunas para minúsculas
dados.columns = dados.columns.str.lower()

# Cria a pasta de resultado
os.makedirs(PASTA_RESULTADO, exist_ok=True)

# Exporta os dados para JSON
dados.to_json(
    ARQUIVO_JSON,
    orient="records",
    force_ascii=False,
    indent=4
)

print("Extração concluída!")
print(f"Instituições encontradas: {len(dados)}")
print(f"Arquivo gerado: {ARQUIVO_JSON}")
