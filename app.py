import streamlit as st
import pandas as pd

# Configuração da página do chat
st.set_page_config(page_title="Assistente MPNID", page_icon="🔍")

st.title("🤖 Assistente Virtual de MPNID")
st.markdown("Consulte informações de revendedores e MPNIDs.")

# 1. Carregar a Base de Dados
@st.cache_data
def carregar_dados():
    try:
        # Carrega o arquivo base.xlsx (deve estar na mesma pasta no GitHub)
        df = pd.read_excel("base.xlsx")
        # Garante que os nomes das colunas não tenham espaços extras
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro: Certifique-se de que o arquivo 'base.xlsx' está no GitHub. Erro: {e}")
        return None

df = carregar_dados()

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de pergunta do usuário
if prompt := st.chat_input("Ex: Qual o MPNID da revenda X?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if df is not None:
            # Busca o termo em todas as colunas da planilha
            termo = str(prompt).strip().lower()
            
            # Filtra a planilha procurando o termo em qualquer uma das 4 colunas
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(termo).any(), axis=1)
            resultado = df[mask]

            if not resultado.empty:
                # Se encontrou, pega a primeira linha correspondente
                res = resultado.iloc[0]
                
                # Monta a resposta formatada com suas 4 colunas
                resposta = (
                    f"**Reseller Account:** {res['Reseller Account']}\n\n"
                    f"**Revendedor Indireto:** {res['Revendedor Indireto']}\n\n"
                    f"**MPNID Local:** {res['MPNID Local']}\n\n"
                    f"**MPNID Global:** {res['MPNID Global']}"
                )
            else:
                # Resposta obrigatória caso não encontre nada
                resposta = "Não encontrei essa informação na base de dados."
        else:
            resposta = "Erro ao acessar a base de dados."

        st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})
