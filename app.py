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
        genai.configure(api_key=minha_chave)
        
        # --- LÓGICA DE TENTATIVA E ERRO PARA O MODELO ---
        if "modelo_confirmado" not in st.session_state:
            # Lista de nomes possíveis que o Google aceita dependendo da versão
            tentativas = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]
            sucesso = False
            
            for nome in tentativas:
                try:
                    teste_model = genai.GenerativeModel(model_name=nome)
                    # Tenta uma resposta curtinha só para validar
                    teste_model.generate_content("oi") 
                    st.session_state.modelo_confirmado = nome
                    sucesso = True
                    break
                except:
                    continue
            
            if not sucesso:
                st.error("Não conseguimos conectar com os modelos Gemini. Verifique se sua chave API está correta e ativa no Google AI Studio.")

        # Se encontrou um modelo que funciona
        if "modelo_confirmado" in st.session_state:
            model = genai.GenerativeModel(model_name=st.session_state.modelo_confirmado)

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Como a Nice pode te ajudar hoje?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                contexto = f"{PROMPT_SISTEMA}\n\nPergunta: {prompt}"
                response = model.generate_content(contexto)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                with st.chat_message("assistant"):
                    st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
else:
    st.info("🌿 Por favor, configure a chave API nos Secrets para começar.")
