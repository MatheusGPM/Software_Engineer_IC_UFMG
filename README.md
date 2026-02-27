# Software_Engineer_IC_UFMG

Repositório do projeto de Iniciação Científica (IC) focado em **geração de testes unitários com LLMs** e **comparação de cobertura (JaCoCo)** em projetos Java (Maven/JUnit).

## Objetivo
1) Medir a cobertura de testes (baseline) do projeto-alvo.  
2) Remover/alterar testes de desenvolvedores para um método-alvo.  
3) Gerar novos testes com LLM (prompts versionados).  
4) Comparar cobertura e registrar evidências (CSV/XML/prints).

## Estrutura do repositório
- `01_docs_2026-02-17_(comparativos-e-prints)`: prints e comparações visuais.
- `02_dados_2026-02-17_(jacoco-e-marcadores)`: XMLs do JaCoCo e arquivos “marcadores”.
- `03_prompts_2026-02-17_(llm)`: prompts usados para geração de testes.
- `04_resultados_2026-02-17_(...)`: resultados consolidados (CSVs, etc.).
- `05_scripts_2026-02-17_(pipeline)`: scripts do pipeline (extração, cobertura, relatórios).
- `06_metodos_2026-02-17_(webmagic-selecionados)`: lista/marcadores de métodos escolhidos.
- `07_repos_2026-02-17_(webmagic-orig-e-llm)`: variantes/referências do repositório-alvo.
- `08_repos_2026-02-18_(webmagic-sem-devtest-metodo1)`: variante do repo sem testes DEV do método 1.

## Como reproduzir (resumo)
> Ajuste os caminhos conforme seu ambiente (Windows/WSL/Linux).

1) Entrar no repo do projeto-alvo (ex.: WebMagic) e rodar testes com cobertura:
- `mvn test`
- `mvn test jacoco:report`

2) Exportar/armazenar o XML do JaCoCo e resultados na pasta `02_dados_...`.

3) Rodar os scripts do pipeline (pasta `05_scripts_...`) para:
- identificar cobertura por método,
- selecionar métodos-alvo,
- consolidar resultados em CSV.


