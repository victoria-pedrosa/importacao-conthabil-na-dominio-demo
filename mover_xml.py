import os
import shutil

# Pega automaticamente a pasta exata onde o seu terminal está aberto
caminho_base = os.getcwd()
ficheiro_registo = os.path.join(caminho_base, "registo_movimentacao_xml.txt")

def mover_arquivos_xml():
    print(f"\n--- A INICIAR A MOVIMENTAÇÃO DOS FICHEIROS ---")
    
    arquivos_movidos = 0
    pastas_verificadas = 0

    # Abre (ou cria) o ficheiro de registo para podermos reverter mais tarde
    with open(ficheiro_registo, "a", encoding="utf-8") as registo:
        for root, dirs, files in os.walk(caminho_base):
            nome_pasta_atual = os.path.basename(root).strip().upper()
            
            # Verifica se é uma pasta de Prestados ou Tomados
            if 'PRESTADO' in nome_pasta_atual or 'TOMADO' in nome_pasta_atual:
                pastas_verificadas += 1
                pasta_destino = os.path.dirname(root) # A pasta mãe (ex: 032026)
                
                for arquivo in files:
                    if arquivo.lower().endswith('.xml'):
                        origem = os.path.join(root, arquivo)
                        destino = os.path.join(pasta_destino, arquivo)
                        
                        try:
                            if not os.path.exists(destino):
                                shutil.move(origem, destino)
                                # Guarda a informação: local atual | local original
                                registo.write(f"{destino}|{origem}\n")
                                print(f"MOVIDO: {arquivo} -> Subiu para a pasta do mês.")
                                arquivos_movidos += 1
                            else:
                                print(f"AVISO: '{arquivo}' já existe na pasta de destino.")
                        except Exception as e:
                            print(f"ERRO ao mover '{arquivo}': {e}")

    if pastas_verificadas == 0:
        print("\nAVISO: Nenhuma pasta PRESTADOS ou TOMADOS foi encontrada!")
    else:
        print(f"\nSucesso! {arquivos_movidos} ficheiros XML foram movidos.")


def reverter_movimentacao():
    print(f"\n--- A INICIAR A REVERSÃO (DESFAZER) ---")
    
    if not os.path.exists(ficheiro_registo):
        print("AVISO: Não foi encontrado nenhum histórico de movimentação.")
        print("Não há nada para reverter neste momento.")
        return

    arquivos_revertidos = 0
    linhas_que_falharam = []

    # Lê o histórico
    with open(ficheiro_registo, "r", encoding="utf-8") as registo:
        linhas = registo.readlines()

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        partes = linha.split('|')
        if len(partes) == 2:
            local_onde_esta = partes[0]
            local_para_voltar = partes[1]

            if os.path.exists(local_onde_esta):
                try:
                    # Garante que a pasta original ainda existe (se não existir, recria)
                    pasta_original = os.path.dirname(local_para_voltar)
                    if not os.path.exists(pasta_original):
                        os.makedirs(pasta_original)

                    # Devolve o ficheiro à origem
                    shutil.move(local_onde_esta, local_para_voltar)
                    nome_pasta_origem = os.path.basename(pasta_original)
                    print(f"REVERTIDO: O ficheiro voltou para '{nome_pasta_origem}'.")
                    arquivos_revertidos += 1
                except Exception as e:
                    print(f"ERRO ao reverter '{local_onde_esta}': {e}")
                    linhas_que_falharam.append(linha) # Se deu erro, mantém no histórico
            else:
                print(f"IGNORADO: O ficheiro já não está lá ou já foi revertido.")
        else:
            linhas_que_falharam.append(linha)

    # Se a reversão foi um sucesso total, apaga o registo. Se falhou algum, guarda só os que falharam.
    if len(linhas_que_falharam) == 0:
        os.remove(ficheiro_registo)
    else:
        with open(ficheiro_registo, "w", encoding="utf-8") as registo:
            for l in linhas_que_falharam:
                registo.write(f"{l}\n")

    print(f"\nReversão concluída! {arquivos_revertidos} ficheiros voltaram às suas pastas originais.")


def main():
    while True:
        print("\n" + "="*50)
        print("    GESTOR DE FICHEIROS XML (PRESTADOS/TOMADOS)")
        print("="*50)
        print("1 - Mover ficheiros XML para a pasta principal (Avançar)")
        print("2 - Reverter ficheiros XML para as pastas originais (Desfazer)")
        print("0 - Sair do programa")
        
        opcao = input("\nEscolha uma opção (0, 1 ou 2) e pressione ENTER: ").strip()
        
        if opcao == '1':
            mover_arquivos_xml()
        elif opcao == '2':
            reverter_movimentacao()
        elif opcao == '0':
            print("A encerrar o programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    main()