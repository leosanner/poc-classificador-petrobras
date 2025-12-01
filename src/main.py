from inference.voting_classifier.main import predictions_df
import streamlit as st
import pandas as pd
from utils.csv_utils import check_index_column
from cloud.onedrive.upload_files import upload_dataframe

# Configurações básicas da página
st.set_page_config(
    page_title="Classificação de Trabalhos por AIA",
    page_icon="🌱",
    layout="wide",
)

# ========= LAYOUT LATERAL (SIDEBAR) =========
with st.sidebar:
    st.markdown("### ℹ️ Sobre esta aplicação")
    st.markdown(
        """
Esta interface é uma **prova de conceito (PoC)** para testar um classificador de
trabalhos acadêmicos relacionados à **Avaliação de Impacto Ambiental (AIA)**.

O objetivo é:

- Explorar o **modelo**;
- Coletar **feedback de uso**;
- Identificar **melhorias** para futuras versões.
"""
    )
    st.markdown("---")
    st.markdown("### 🧪 Importante")
    st.markdown(
        """
- Os resultados são **experimentais**.  
- Podem ocorrer **erros de classificação**.  
"""
    )
    st.markdown("---")
    st.markdown("### 💬 Feedback")
    st.markdown(
        """
Se possível, compartilhe:

- Casos em que o modelo errou;
- Ideias de melhorias;
- Comentários sobre a interface.

Isso é essencial para evoluir a ferramenta.
"""
    )

# ========= CABEÇALHO PRINCIPAL =========
st.title("🌱 Classificador de Trabalhos Relacionados à Avaliação de Impacto Ambiental")

st.markdown(
    """
Esta aplicação demonstra, em caráter de **prova de conceito**, um sistema de 
**classificação automática** de trabalhos acadêmicos em relação à temática de 
**Avaliação de Impacto Ambiental (AIA)**.

O foco atual é **testar o fluxo de uso** e a **qualidade das predições** 
em cenários reais.
"""
)

st.info(
    "🔬 **Prova de conceito:** esta não é uma versão final. "
    "Os resultados podem conter erros e serão utilizados para orientar ajustes futuros."
)

st.markdown("---")

# ========= INSTRUÇÕES =========
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📂 Como testar o classificador")

    st.markdown(
        """
1. Prepare uma **planilha em formato CSV** com os dados dos trabalhos.
   O modelo utilizará o conteúdo textual das colunas para realizar a classificação.

2. Faça o **upload do arquivo CSV** no campo abaixo.

3. Aguarde o processamento: cada linha será analisada pelo modelo.

4. **Muito Importante:** o único requisito é ter uma coluna nomeada como *  *Title**
"""
    )

    st.markdown(
        """
Os resultados serão exibidos em uma **tabela interativa**, com as colunas originais
e as informações calculadas pelo modelo.
"""
    )

with col2:
    st.subheader("🧾 Observações")
    st.markdown(
        """
- Arquivos muito grandes podem levar mais tempo para processar.   
- Caso ocorra erro, verifique o formato das colunas.
"""
    )

st.markdown("---")

# ========= SEÇÃO DE UPLOAD =========
st.subheader("📤 Envie sua planilha CSV para teste")

uploaded_file = st.file_uploader(
    "Selecione sua planilha em formato CSV",
    type=["csv"],
)


OPTIONS_SEP = {
    "Vírgula (,)": ",",
    "Ponto e vírgula (;)": ";",
    "Tab (\\t)": "\t",
    "Pipe (|)": "|",
}

user_name = st.text_input("Insira seu nome")

sep = st.selectbox(
    "Escolha um delimitador (';' é o padrão, porém caso ocorram erros altere):",
    OPTIONS_SEP.keys(),
)

run = st.button("Gerar predições")

if (uploaded_file is not None) and run:

    if not sep:
        sep = ";"

    else:
        sep = OPTIONS_SEP[sep]

    try:
        # Lê o CSV em um DataFrame
        # Tenta ler sem assumir index_col primeiro
        df = pd.read_csv(uploaded_file, sep=sep)

        # Check for index column
        if check_index_column(df):
            st.info("ℹ️ Index column detected and removed.")
            df = df.iloc[:, 1:]

        # Vamos limpar colunas vazias ou "Unnamed" que as vezes aparecem
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        st.success("✅ Arquivo carregado com sucesso!")

        st.markdown("#### 🔎 Pré-visualização dos dados enviados")
        st.dataframe(df.head(), width="stretch")

        st.markdown("----")
        st.markdown("#### 🧠 Resultados da classificação (prova de conceito)")

        proba, user = predictions_df(df)

        try:
            upload_dataframe(proba, username=user_name)
            st.toast("Dados enviados para nuvem com sucesso!", icon="☁️")

        except Exception as e:
            st.warning(
                "⚠️ Não foi possível enviar os dados para a nuvem. A classificação foi realizada, mas o registro falhou."
            )

            print(e)

        st.caption(
            "As predições abaixo são **experimentais** e fazem parte da etapa de validação do modelo."
        )
        st.dataframe(user, width="stretch")

        st.info(
            "💡 Se possível, anote casos em que o modelo errou ou gerou dúvidas "
            "e compartilhe esse feedback. Isso ajuda muito a calibrar futuras versões."
        )

    except pd.errors.EmptyDataError:
        st.error("❌ O arquivo enviado está vazio.")
    except pd.errors.ParserError:
        st.error("❌ Erro ao ler o arquivo CSV. Verifique o formato.")
    except Exception as e:
        st.error("❌ Ocorreu um erro ao processar o arquivo.")
        st.exception(e)
else:
    st.warning(
        "Nenhum arquivo foi enviado ainda. Faça o upload de um CSV para iniciar os testes."
    )
    st.caption(
        "Dica: utilize um subconjunto dos seus dados para testar primeiro (por exemplo, 100–500 linhas)."
    )
