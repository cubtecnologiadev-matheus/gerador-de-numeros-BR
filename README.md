# 📱 Gerador de Números de Celular BR (CLI)

Ferramenta em **Python** para gerar listas de **números de celular do Brasil** de forma segura e organizada.

- Suporta **todos os DDDs válidos da Anatel**
- Sempre usa **nono dígito iniciado em 9**
- Evita padrões triviais (ex: `99999999`, sequências 123456…)
- Garante **não repetir números** na mesma geração
- Salva em **CSV** e **TXT** nos formatos:
  - `+55DDDNXXXXXXXX` (E.164)
  - `(<DDD>) 9 XXXX-XXXX` (formato nacional)

---

## 🛠 Tecnologias

- **Python 3**
- Módulos padrão: `csv`, `random`, `datetime`, `pathlib`, etc.

---

## 📂 Estrutura do Projeto

```text
gerador-de-numeros-BR/
├── gerador_de_celulares_br.py     # Script principal (CLI interativo)
├── Rodar_Gerador_Celulares_BR.bat # Atalho para Windows (opcional)
└── (arquivos gerados *.csv / *.txt vão aparecer aqui)
▶️ Como usar
1. Requisitos
Python 3 instalado e configurado no PATH (comando python ou py)

Windows (para usar o .bat, mas o .py roda em qualquer sistema)

2. Executar pelo Python
No terminal / CMD, dentro da pasta do projeto:

bash
Copiar código
python gerador_de_celulares_br.py
ou, no Windows:

bash
Copiar código
py gerador_de_celulares_br.py
Você verá um fluxo interativo mais ou menos assim:

Quantos números deseja gerar?

Escolher o modo:

[1] Por DDD específico

[2] Aleatório em todos os DDDs do Brasil

Se escolher modo 1, informar o DDD (ex: 11, 21, 31 etc.)

Informar o nome base do arquivo (ENTER para usar numeros_br)

O script então:

gera os números

salva em:

NOME_BASE_ddd_<DDD>_YYYYMMDD_HHMMSS.csv

NOME_BASE_ddd_<DDD>_YYYYMMDD_HHMMSS.txt

mostra alguns exemplos no terminal.

3. Executar pelo .BAT (atalho no Windows)
Você também pode usar o atalho:

bat
Copiar código
Rodar_Gerador_Celulares_BR.bat
Ele basicamente chama o Python apontando para gerador_de_celulares_br.py
(útil para quem não quer digitar comando toda vez).

📄 Saída dos arquivos
Arquivo CSV
Nome: numeros_br_ddd_11_20251011_034214.csv (exemplo)

Colunas:

text
Copiar código
e164,nacional,ddd,numero
+55119987654321,(11) 9 9876-5432,11,998765432
...
Arquivo TXT
Nome: numeros_br_ddd_11_20251011_034214.txt

Conteúdo: um número E.164 por linha

text
Copiar código
+55119987654321
+55119400100200
...
🔍 Modo de auto-teste (opcional)
O script possui um modo de teste rápido embutido para validar o gerador:

bash
Copiar código
python gerador_de_celulares_br.py --selftest
Ele verifica:

se os números têm 9 dígitos e começam com 9

se o DDD está correto

se não há duplicatas

se os arquivos .csv e .txt de saída são gerados corretamente

Se tudo der certo, aparece:

text
Copiar código
[SELFTEST] OK
⚠ Aviso de uso
Esta ferramenta é apenas para:

Testes, simulação de bases de dados e estudos

Geração de números fictícios para sistemas de QA e desenvolvimento

Não garante que os números existam de fato nem que sejam válidos em operadoras reais.

👨‍💻 Autor
Matheus – Cub Tecnologia Dev
Soluções em Python, PHP e Node.js para automação e ferramentas internas.
📧 cubtecnologia.dev@gmail.com
