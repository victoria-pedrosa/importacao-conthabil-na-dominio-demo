# Demonstração — Preparação de arquivos do Conthabil para a Domínio

> Projeto de portfólio de **Victória Pedrosa**. **Demonstração** de preparação de arquivos do Conthabil para a Domínio — versão com dados fictícios (nomes, CNPJs, e-mails e IDs internos substituídos).

## Problema de negócio
Arquivos gerados pelo Conthabil precisavam de ajuste de apelidos e organização antes da importação na Domínio.

## Antes x depois
| | Antes | Depois |
|---|---|---|
| Como é feito | Renomeação e movimentação manual de XML. | Scripts aplicam os apelidos da Domínio e movem os XML, com registro para reverter. |

## Ganho
- Importação preparada sem retrabalho.

## Tecnologias
Python, SQLite

## Arquivos
- `apelido_dominio.py`
- `mover_xml.py`
- `requirements.txt`

## Como rodar
1. `pip install -r requirements.txt`
2. Copie `.env.exemplo` para `.env` e preencha os caminhos.
3. Execute o script principal.

## Autora
Victória Pedrosa — Product Owner do Time de IA, automação de processos contábeis e fiscais.
