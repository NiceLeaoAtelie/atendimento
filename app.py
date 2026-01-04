import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Nice Leão Ateliê", page_icon="🪡")

# Estilo Verde Oliva
st.markdown("""
    <style>
    .stApp { background-color: #fcfdf9; }
    h1, h2, h3 { color: #556b2f !important; font-family: 'Georgia', serif; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA CHAVE ---
minha_chave = st.secrets.get("GOOGLE_API_KEY")

# --- CONTEÚDO DO ATELIÊ ---
st.title("🪡 Nice Leão Ateliê")
st.subheader("Presentes Personalizados e Costura Criativa")

# Instruções para a IA
PROMPT_SISTEMA = """
Você é o assistente virtual do 'Nice Leão Ateliê'.
Seu tom de voz: Acolhedor, artesanal, educado e criativo.

PRODUTOS:
- Canecas (Brancas, Coloridas, Xícaras).
- Kits: Caneca/Xícara + Bag de Algodão + Mug Rug Dupla Face.
- Copos de Vidro Summer.
- Nécessaires de tecido (P, M, G) e Nécessaire toalhinha.
- Porta livros, Porta documentos infantil, Porta joias em tecido.
- Kit Caneca Box com infusor.

REGRAS:
1. Sempre pergunte o NOME do cliente no início.
2. Peça o CEP para que a Nice possa calcular o frete e o prazo.
3. Se o cliente perguntar preço e você não tiver certeza, diga que a Nice enviará o orçamento detalhado.
"""

if minha_chave:
    try:
        genai.configure(api_key=minha_chave)
        
        # USANDO O MODELO QUE FUNCIONOU NO SEU TESTE
        model = genai.GenerativeModel('models/gemini-2.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Exibir histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat
        if prompt := st.chat_input("Olá! Como posso te ajudar?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Resposta com o contexto do Ateliê
            contexto = f"{PROMPT_SISTEMA}\n\nPergunta do cliente: {prompt}"
            response = model.generate_content(contexto)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Erro ao conversar com o assistente: {e}")
else:
    st.info("🌿 Bem-vindo! Por favor, configure a chave API nos Secrets do Streamlit.")
