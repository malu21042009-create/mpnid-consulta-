import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assistente MPNID", page_icon="🔍")

st.title("🤖 Assistente de Consulta")

@st.cache_data
def carregar_dados():
    try:
        # Lê a planilha
        df = pd.read_excel("base.xlsx")
        
        # 1. Remove colunas que estão totalmente vazias
        df = df.dropna(axis=1, how='all')
        
        # 2. Remove linhas que estão totalmente vazias
        df = df.dropna(axis=0, how='all')

        # 3. Mapear as colunas para nomes amigáveis (ajuste a ordem se necessário)
        # Como o seu print mostrou que os dados estão nas últimas colunas:
        novos_nomes = [
            "Reseller Account", 
            "Revendedor Indireto", 
            "MPNID Local", 
            "MPNID Global"
        ]
        
        # Pega apenas as colunas que realmente têm dados e renomeia
        if len(df.columns) >= len(novos_nomes):
            # Pega as últimas 4 colunas (que são as que têm dados no seu print)
            df = df.iloc[:, -4:] 
            df.columns = novos_nomes

        # Limpa espaços extras
        df = df.astype(str).apply(lambda x: x.str.strip())
        return df
    except Exception as e:
        st.error(f"Erro ao ler base.xlsx: {e}")
        return None

df = carregar_dados()

if df is not None:
    st.sidebar.success(f"Base carregada com {len(df)} registros.")

if prompt := st.chat_input("Pesquise por Nome ou ID:"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if df is not None:
            termo = str(prompt).strip().lower()
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(termo, na=False).any(), axis=1)
            resultado = df[mask]

            if not resultado.empty:
                res = resultado.iloc[0]
                resposta = "✅ **Informações encontradas:**\n\n"
                for col in df.columns:
                    # Se o dado for 'nan', ele mostra 'Não informado'
                    valor = res[col] if res[col] != "nan" else "---"
                    resposta += f"**{col}:** {valor}\n\n"
                st.markdown(resposta)
            else:
                st.markdown("Não encontrei essa informação na base de dados.")
            
