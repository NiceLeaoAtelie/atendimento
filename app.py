import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO VISUAL (Cores do Ateliê - Verde Oliva) ---
st.set_page_config(page_title="Nice Leão Ateliê", page_icon="🪡")

# Estilização com CSS para o tom Verde Oliva
st.markdown("""
    <style>
    .stApp {
        background-color: #fcfdf9;
    }
    .st-emotion-cache-10trblm {
        color: #556b2f !important;
    }
    h1 {
        color: #556b2f !important;
        font-family: 'Georgia', serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪡 Nice Leão Ateliê")
st.subheader("Presentes Personalizados e Costura Criativa")

# --- CONFIGURAÇÃO DA CHAVE ---
with st.sidebar:
    st.header("Configuração")
    minha_chave = st.text_input("Insira sua API Key:", type="password")
    st.info("O verde oliva representa nosso ateliê! 🌿")

# --- REGRAS DE NEGÓCIO (CÉREBRO DO BOT) ---
PROMPT_SISTEMA = """
Você é o assistente virtual do 'Nice Leão Ateliê'.
Seu tom de voz deve ser: Acolhedor, artesanal, educado e criativo.

PRODUTOS E PREÇOS (Informe valores quando solicitado):
- Caneca branca personalizada.
- Caneca colorida (alça e interior coloridos).
- Xícaras personalizadas.
- Kit Caneca/Xícara (inclui 1 bag 100% algodão e 1 mug rug dupla face).
- Copo de vidro Summer personalizado.
- Nécessaires de tecido (P, M, G).
- Nécessaire toalhinha (comum ou personalizada).
- Porta livros, Porta documentos infantil, Porta joias (em tecido).
- Kit Caneca Box com infusor personalizado.

OBJETIVOS DE ATENDIMENTO:
1. Tirar dúvidas sobre os itens acima.
2. Capturar o NOME do cliente logo no início da conversa.
3. Capturar o CEP para cálculo de frete quando o cliente se interessar por um produto.
4. Informar que, como são itens personalizados, o prazo de produção deve ser consultado.
5. Se não souber o preço exato de algo, diga que a Nice entrará em contato para passar o orçamento detalhado.
"""

if minha_chave = st.secrets["GOOGLE_API_KEY"]
        try:

        # Seleção automática de modelo
        if "modelo_ativo" not in st.session_state:
            modelos = genai.list_models()
            for m in modelos:
                if 'generateContent' in m.supported_generation_methods:
                    st.session_state.modelo_ativo = m.name
                    break
        
        model = genai.GenerativeModel(st.session_state.modelo_ativo)

        if "historico" not in st.session_state:
            st.session_state.historico = []

        # Exibir chat
        for m in st.session_state.historico:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        # Entrada do usuário
        if prompt := st.chat_input("Olá! Em que posso ajudar hoje?"):
            st.session_state.historico.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Gerar resposta com contexto
            contexto = f"{PROMPT_SISTEMA}\n\nHistórico: {st.session_state.historico}\n\nPergunta atual: {prompt}"
            response = model.generate_content(contexto)
            
            st.session_state.historico.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)

    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.info("🌿 Bem-vindo! Por favor, insira a chave na barra lateral para começarmos o atendimento.")