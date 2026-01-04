import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nice Leão Ateliê", page_icon="🪡")

# Estilo Verde Oliva
st.markdown("""
    <style>
    .stApp { background-color: #fcfdf9; }
    h1, h2, h3 { color: #556b2f !important; font-family: 'Georgia', serif; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA CHAVE ---
# Usando .get para evitar erros de sintaxe
minha_chave = st.secrets.get("GOOGLE_API_KEY")

if not minha_chave:
    with st.sidebar:
        st.warning("Chave não encontrada nos Secrets do Streamlit.")
        minha_chave = st.text_input("Insira sua API Key manualmente:", type="password")

# --- CONTEÚDO DO ATELIÊ ---
st.title("🪡 Nice Leão Ateliê")
st.write("Assistente virtual de presentes personalizados.")

PROMPT_SISTEMA = """
Você é o assistente do Nice Leão Ateliê. Especialista em Costura Criativa e Sublimação.
PRODUTOS: Canecas, Kits (Caneca+Bag+Mug Rug), Copo Summer, Nécessaires P/M/G, Porta Livros/Documentos.
OBJETIVO: Ser acolhedor, perguntar o NOME do cliente e pedir o CEP para orçamento.
"""

if minha_chave:
    try:
        genai.configure(api_key=minha_chave)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Como a Nice pode te ajudar hoje?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            model = genai.GenerativeModel('gemini-1.5-flash')
            contexto = f"{PROMPT_SISTEMA}\n\nPergunta: {prompt}"
            response = model.generate_content(contexto)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("🌿 Por favor, configure a chave API para começar.")
