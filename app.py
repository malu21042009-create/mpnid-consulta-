import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assistente MPNID", page_icon="🔍")

st.title("🤖 Assistente de Consulta")

@st.cache_data
def carregar_dados():
    try:
        # Lê a planilha base.xlsx
        df = pd.read_excel("base.xlsx")
        # Converte tudo para texto e remove espaços extras
        df = df.astype(str).apply(lambda x: x.str.strip())
        return df
    except Exception as e:
        st.error(f"Erro ao ler base.xlsx. Verifique se o arquivo é um Excel válido. Erro: {e}")
        return None

df = carregar_dados()

if df is not None:
    st.sidebar.success(f"Base carregada: {len(df)} linhas.")

if prompt := st.chat_input("Pesquise por Nome ou ID:"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if df is not None:
            termo = str(prompt).strip().lower()
            
            # Busca o termo em qualquer lugar da planilha
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(termo, na=False).any(), axis=1)
            resultado = df[mask]

            if not resultado.empty:
                # Se encontrar várias, mostra a primeira
                res = resultado.iloc[0]
                resposta = "✅ **Informações encontradas:**\n\n"
                
                # Esse código percorre as colunas independente do nome delas
                for col in df.columns:
                    resposta += f"**{col}:** {res[col]}\n\n"
                st.markdown(resposta)
            else:
                st.markdown("Não encontrei essa informação na base de dados.")
