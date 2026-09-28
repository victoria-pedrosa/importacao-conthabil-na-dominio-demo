import os
import csv
from dotenv import load_dotenv
load_dotenv()  # lê o .env local (não vai para o GitHub)

# Definir os caminhos
caminho_base = os.getenv("CAMINHO_BASE_CONTHABIL")
caminho_planilha = "APELIDO DOMINIO.xlsx - Planilha1.csv"
caminho_saida = "APELIDO_DOMINIO_ATUALIZADO.csv"

def normalizar_nome(nome):
    # Remove espaços extras e deixa maiúsculo para facilitar a comparação
    return str(nome).strip().upper()

def obter_duas_primeiras_palavras(texto):
    palavras = texto.split()
    return " ".join(palavras[:2]) if len(palavras) >= 2 else texto

def main():
    empresas = []
    
    print("A iniciar o processo... Por favor, aguarde.")
    
    # 1. Carregar a planilha CSV usando a biblioteca nativa do Python
    try:
        with open(caminho_planilha, mode='r', encoding='utf-8') as file:
            leitor = csv.DictReader(file, delimiter=',')
            for linha in leitor:
                razao_social = linha.get('Razão Social', '')
                busca = obter_duas_primeiras_palavras(normalizar_nome(razao_social))
                linha['Busca'] = busca
                linha['Status Modificacao'] = 'Não encontrada/Não modificada'
                empresas.append(linha)
    except FileNotFoundError:
        print(f"ERRO: O ficheiro '{caminho_planilha}' não foi encontrado. Verifique se ele está na mesma pasta deste script.")
        return
    except Exception as e:
        print(f"ERRO ao ler o ficheiro CSV: {e}")
        return

    # 2. Listar todas as pastas no diretório especificado
    try:
        pastas = [f for f in os.listdir(caminho_base) if os.path.isdir(os.path.join(caminho_base, f))]
    except FileNotFoundError:
        print(f"ERRO: O diretório '{caminho_base}' não foi encontrado. Verifique se a pasta existe.")
        return

    # 3. Iterar sobre as pastas para renomear
    for pasta_atual in pastas:
        caminho_pasta_atual = os.path.join(caminho_base, pasta_atual)
        
        # Verificar se a pasta tem o delimitador '-'
        if '-' in pasta_atual:
            # Pegar o texto depois do primeiro '-'
            parte_apos_hifen = pasta_atual.split('-', 1)[1]
            identificador_pasta = obter_duas_primeiras_palavras(normalizar_nome(parte_apos_hifen))
            
            # Buscar na lista de empresas
            empresa_encontrada = None
            for empresa in empresas:
                if empresa['Busca'] == identificador_pasta:
                    empresa_encontrada = empresa
                    break
            
            if empresa_encontrada:
                codigo = str(empresa_encontrada['Código']).strip()
                apelido = str(empresa_encontrada['Apelido']).strip()
                
                # Montar o novo nome
                novo_nome = f"{codigo}-{apelido}"
                caminho_nova_pasta = os.path.join(caminho_base, novo_nome)
                
                # Renomear a pasta se o nome novo for diferente
                if pasta_atual != novo_nome:
                    try:
                        os.rename(caminho_pasta_atual, caminho_nova_pasta)
                        empresa_encontrada['Status Modificacao'] = 'Modificada com Sucesso'
                        print(f"SUCESSO: '{pasta_atual}' -> '{novo_nome}'")
                    except Exception as e:
                        empresa_encontrada['Status Modificacao'] = f'Erro ao renomear: {e}'
                        print(f"ERRO: Não foi possível renomear '{pasta_atual}' -> '{novo_nome}' ({e})")
                else:
                    empresa_encontrada['Status Modificacao'] = 'Nome já estava correto'
            else:
                print(f"AVISO: Nenhuma correspondência na planilha para a pasta '{pasta_atual}'")

    # 4. Salvar a planilha atualizada
    if empresas:
        campos = list(empresas[0].keys())
        if 'Busca' in campos:
            campos.remove('Busca') # Remove a coluna auxiliar
        
        with open(caminho_saida, mode='w', encoding='utf-8', newline='') as file:
            escritor = csv.DictWriter(file, fieldnames=campos, delimiter=',')
            escritor.writeheader()
            for empresa in empresas:
                if 'Busca' in empresa:
                    del empresa['Busca'] # Apaga do dicionário também
                escritor.writerow(empresa)
                
        print(f"\nProcesso concluído! O resultado foi salvo em '{caminho_saida}'.")
        
    input("\nPressione ENTER para fechar...")

if __name__ == '__main__':
    main()