from inference.voting_classifier.main import predictions_df
import streamlit as st
import pandas as pd
from utils.save_new_data import save_new_file
from drive.drive_upload_files import upload_dataframe

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
1. Prepare uma **planilha em formato CSV** contendo, pelo menos, as seguintes colunas (nesta ordem):  
   - `Title` → título do trabalho  
   - `Abstract` → resumo do trabalho  
   - `Keywords` → palavras-chave associadas  

2. Faça o **upload do arquivo CSV** no campo abaixo.

3. Aguarde o processamento: cada linha será analisada pelo modelo.
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
    help="A planilha deve conter, no mínimo, as colunas: Title, Abstract e Keywords.",
)

if uploaded_file is not None:
    try:
        # Lê o CSV em um DataFrame
        df = pd.read_csv(uploaded_file, index_col=0)
        df = df.reset_index(drop=True)

        st.success("✅ Arquivo carregado com sucesso!")

        st.markdown("#### 🔎 Pré-visualização dos dados enviados")
        st.dataframe(df.head(), use_container_width=True)

        st.markdown("----")
        st.markdown("#### 🧠 Resultados da classificação (prova de conceito)")

        proba, user = predictions_df(df)

        st.caption(
            "As predições abaixo são **experimentais** e fazem parte da etapa de validação do modelo."
        )
        st.dataframe(user, use_container_width=True)

        st.info(
            "💡 Se possível, anote casos em que o modelo errou ou gerou dúvidas "
            "e compartilhe esse feedback. Isso ajuda muito a calibrar futuras versões."
        )

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
