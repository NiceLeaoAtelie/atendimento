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
minha_chave = st.secrets.get("GOOGLE_API_KEY")

if not minha_chave:
    with st.sidebar:
        st.warning("Chave não encontrada nos Secrets.")
        minha_chave = st.text_input("Insira sua API Key manualmente:", type="password")

# --- CONTEÚDO DO ATELIÊ ---
st.title("🪡 Nice Leão Ateliê")
st.write("Assistente virtual de presentes personalizados.")

PROMPT_SISTEMA = """
Você é o assistente do Nice Leão Ateliê. Especialista em Costura Criativa e Sublimação.
PRODUTOS: Canecas, Kits (Caneca+Bag+Mug Rug), Copo Summer, Nécessaires P/M/G, Porta Livros/Documentos.
OBJETIVO: Ser acolhedor, perguntar o NOME do cliente e pedir o CEP para orçamento.
Responda sempre em Português do Brasil.
"""

if minha_chave:
    try:
        # Configuração forçada da API
        genai.configure(api_key=minha_chave)
        
        # Usando o nome completo do modelo para evitar o erro 404
        # 'models/gemini-1.5-flash' é o endereço estável oficial
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Exibir mensagens
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Como a Nice pode te ajudar hoje?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gerar resposta
            contexto = f"{PROMPT_SISTEMA}\n\nPergunta do cliente: {prompt}"
            
            # Chamada simplificada para garantir compatibilidade
            response = model.generate_content(contexto)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
    except Exception as e:
        # Se o erro 404 persistir, ele mostrará uma mensagem amigável
        st.error(f"Erro de conexão com o modelo: {e}")
        st.info("Dica: Verifique se sua chave no Google AI Studio está ativa.")
else:
    st.info("🌿 Por favor, configure a chave API nos Secrets do Streamlit para começar.")
