import os
import re

def gerar_arquivos(pattern, ep_inicio, ep_fim, diretorio):
    # Compila o padrão fornecido
    regex = re.compile(pattern)

    # Cria o diretório se não existir
    os.makedirs(diretorio, exist_ok=True)

    # Gera os arquivos para cada episódio no intervalo especificado
    for ep in range(ep_inicio, ep_fim + 1):
        # Substitui os grupos no padrão pelo número do episódio

        if ep < 10:
            nome_arquivo = regex.sub(rf"\g<0>{ep:1}", pattern).replace("\\d+", f"{ep:1}") + ".txt"
        else: 
            nome_arquivo = regex.sub(rf"\g<0>{ep:2}", pattern).replace("\\d+", f"{ep:2}") + ".txt"

        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        
        # Cria e escreve no arquivo
        with open(caminho_arquivo, "w") as arquivo:
            conteudo = f"Este é o episódio {ep}"
            arquivo.write(conteudo)

    print(f"Arquivos gerados no diretório '{diretorio}'.")


# Exemplos de uso
patterns = [
    "S(\\d+)E(\\d+)", 
    "s(\\d+)e(\\d+)", 
    "EP(\\d+)", 
    "ep(\\d+)", 
    "EP.(\\d+)", 
    "ep.(\\d+)", 
    "S(\\d+) E(\\d+)", 
    "s(\\d+) e(\\d+)"
]


# Gerar arquivos para cada padrão de 1 a 26 episódios
for pattern in patterns:
    gerar_arquivos("ep.\\d+", 1, 26, diretorio="ReNam\\tests\\dummy_files\\test_b")
