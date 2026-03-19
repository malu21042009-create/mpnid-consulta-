import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assistente MPNID", page_icon="🔍")

st.title("🤖 Assistente Virtual de MPNID")

@st.cache_data
def carregar_dados():
    try:
        # Tenta carregar o arquivo
        df = pd.read_excel("base.xlsx")
        # Remove espaços em branco dos nomes das colunas e dos dados
        df.columns = [str(c).strip() for c in df.columns]
        # Converte toda a planilha para texto e remove espaços extras nas células
        df = df.astype(str).apply(lambda x: x.str.strip())
        return df
    except Exception as e:
        st.error(f"Erro: O arquivo 'base.xlsx' não foi encontrado ou está com erro. Detalhe: {e}")
        return None

df = carregar_dados()

# Mostra para você se a planilha carregou (Isso ajuda a testar)
if df is not None:
    st.sidebar.success(f"Base carregada: {len(df)} registros encontrados.")
else:
    st.sidebar.error("Base não carregada.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite o nome ou ID:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if df is not None:
            # Busca ignorando maiúsculas/minúsculas
            termo = str(prompt).strip().lower()
            
            # Procura em todas as colunas
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(termo, na=False).any(), axis=1)
            resultado = df[mask]

            if not resultado.empty:
                res = resultado.iloc[0]
                resposta = "✅ **Encontrei estas informações:**\n\n"
                for col in df.columns:
                    resposta += f"**{col}:** {res[col]}\n\n"
            else:
                resposta = "Não encontrei essa informação na base de dados."
        else:
            resposta = "Erro: A base de dados está vazia ou não foi carregada."

        st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})
