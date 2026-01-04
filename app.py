import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Nice Leão Ateliê", page_icon="🪡")

st.title("🪡 Diagnóstico Nice Leão Ateliê")

# 1. Verificação da Chave nos Secrets
chave = st.secrets.get("GOOGLE_API_KEY")

if not chave:
    st.error("❌ A chave 'GOOGLE_API_KEY' não foi encontrada nos Secrets do Streamlit.")
    st.info("Vá em Settings > Secrets e verifique se o nome está correto.")
else:
    st.success("✅ Chave encontrada nos Secrets!")
    
    try:
        genai.configure(api_key=chave)
        
        # 2. Listar modelos disponíveis para esta chave
        st.write("Buscando modelos disponíveis para sua conta...")
        modelos = genai.list_models()
        
        lista_modelos = []
        for m in modelos:
            if 'generateContent' in m.supported_generation_methods:
                lista_modelos.append(m.name)
        
        if lista_modelos:
            st.write("### Modelos encontrados:")
            st.write(lista_modelos)
            
            # 3. Tentar usar o primeiro da lista
            modelo_escolhido = lista_modelos[0]
            st.info(f"Tentando conectar ao: {modelo_escolhido}")
            
            model = genai.GenerativeModel(modelo_escolhido)
            res = model.generate_content("Oi")
            st.success(f"🤖 O Bot respondeu: {res.text}")
            st.balloons()
            
        else:
            st.warning("⚠️ Sua chave foi aceita, mas o Google não retornou nenhum modelo disponível para ela.")
            
    except Exception as e:
        st.error(f"❌ Erro ao listar modelos: {e}")
        st.info("Isso geralmente acontece se a chave for inválida ou se houver bloqueio de região.")
