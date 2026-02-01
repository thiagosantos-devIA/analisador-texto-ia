try:
    import streamlit as st
except ModuleNotFoundError:
    print("\033[1mPara iniciar o código corretamente digite:\n"
          "streamlit run app.py\033[0m")
    exit()
from openai import OpenAI
import time

if "tela" not in st.session_state:
    st.session_state.tela = "entrada"

if "resultado_ia" not in st.session_state:
    st.session_state.resultado_ia = ""

if "openai_key" not in st.session_state:
    st.session_state.openai_key = None

if st.session_state.openai_key is None:
    st.title("🔑 Configuração Inicial")

    st.write("Para usar a IA, insira sua OpenAI API Key.")

    chave = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    if st.button("Confirmar chave"):
        if chave.strip() == "":
            st.error("A chave não pode estar vazia.")
        else:
            st.session_state.openai_key = chave.strip()
            st.success("Chave configurada com sucesso!")
            st.rerun()

    st.stop()

def analisar_com_ia(texto, tema, publico, api_key):
    client = OpenAI(api_key=api_key)

    prompt = f"""
Você é um especialista em análise de textos.

Tema: {tema}
Público: {publico}

Texto:
{texto}

Forneça:
- Análise geral
- Pontos positivos
- Sugestões de melhoria
"""

    try:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de textos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return resposta.choices[0].message.content

    except Exception as e:
        return f"❌ Erro ao acessar a IA:\n{e}"

# -------------------------------------

if st.session_state.tela == "entrada":

    st.title("Analisador de Texto com IA")

    st.subheader("Informações do Texto")

    tema = st.text_input("Tema (opcional)")

    publico = st.selectbox(
        "Público (opcional)",
        ["Não definido", "Formal", "Informal", "Jovem", "Adolescente", "Infantil"]
    )

    st.subheader("Texto")
    texto = st.text_area("Cole o texto aqui")

    MIN_CARACTERES = 30

    if st.button("Analisar"):
        texto_limpo = texto.strip()
        quantidade = len(texto_limpo)

        if quantidade == 0:
            st.error("Você precisa preencher o texto.")

        elif quantidade < MIN_CARACTERES:
            st.error(
                f"O texto precisa ter pelo menos {MIN_CARACTERES} caracteres. "
                f"Atualmente tem {quantidade}."
            )

        else:
            tema_final = tema if tema else "Não informado"
            publico_final = "Não informado" if publico == "Não definido" else publico

            with st.spinner("A IA está analisando o texto..."):
                time.sleep(2)
                resultado = analisar_com_ia(
                    texto_limpo,
                    tema_final,
                    publico_final,
                    st.session_state.openai_key
                )

            # salva o resultado e troca de tela
            st.session_state.resultado_ia = resultado
            st.session_state.tela = "resultado"
            st.rerun()

# -------------------------------------

if st.session_state.tela == "resultado":

    # botão de voltar (seta)
    if st.button("⬅ Voltar"):
        st.session_state.tela = "entrada"
        st.rerun()

    st.title("Resultado da Análise")

    st.write(st.session_state.resultado_ia)

# streamlit run Untitled-1.py