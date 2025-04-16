import streamlit as st
import qrcode
import io
import pandas as pd

st.set_page_config(page_title="AlfaProvas - Demo", layout="centered")

st.title("📝 AlfaProvas - Sistema de Provas (DEMO)")
st.caption("Criado por @sales_brito | Instagram: @salesbrito_")

st.sidebar.header("Menu")
menu = st.sidebar.radio("Selecione uma opção", ["Upload de Prova", "Simular Resposta do Aluno", "QR Code da Prova"])

# Armazenamento simulado
if "gabarito" not in st.session_state:
    st.session_state["gabarito"] = []

# === Upload de Prova ===
if menu == "Upload de Prova":
    st.subheader("📤 Envie sua prova")

    modo = st.radio("Como deseja criar a prova?", ["Digitar questões", "Enviar PDF (somente exibição)"])

    if modo == "Digitar questões":
        num_q = st.number_input("Número de questões", min_value=1, max_value=20, step=1)
        questoes = []
        gabarito = []

        for i in range(int(num_q)):
            q = st.text_input(f"Questão {i+1}")
            alt = st.selectbox(f"Gabarito da questão {i+1}", ["A", "B", "C", "D", "E"], key=f"alt{i}")
            questoes.append(q)
            gabarito.append(alt)

        if st.button("Salvar Gabarito"):
            st.session_state["gabarito"] = gabarito
            st.success("✅ Gabarito salvo com sucesso!")

    elif modo == "Enviar PDF (exibição apenas)":
        pdf = st.file_uploader("Escolha o arquivo PDF da prova", type="pdf")
        if pdf:
            st.success(f"Arquivo {pdf.name} enviado com sucesso! (visualização não implementada)")

# === Simular resposta do aluno ===
elif menu == "Simular Resposta do Aluno":
    st.subheader("🎯 Corrigir Prova")

    if st.session_state["gabarito"]:
        respostas = []
        for i, resp_certa in enumerate(st.session_state["gabarito"]):
            r = st.selectbox(f"Resposta do aluno para questão {i+1}", ["A", "B", "C", "D", "E"], key=f"resp{i}")
            respostas.append(r)

        if st.button("Corrigir"):
            acertos = sum([1 for a, b in zip(respostas, st.session_state["gabarito"]) if a == b])
            total = len(st.session_state["gabarito"])
            nota = (acertos / total) * 10
            st.success(f"Resultado: {acertos}/{total} acertos")
            st.info(f"Nota final: {nota:.1f}")

    else:
        st.warning("⚠️ Nenhum gabarito foi salvo ainda.")

# === QR Code ===
elif menu == "QR Code da Prova":
    st.subheader("🔗 Gerar QR Code de acesso")

    url = st.text_input("Link para prova do aluno", value="https://alfaprovas.streamlit.app/aluno")
    if st.button("Gerar QR Code"):
        img = qrcode.make(url)
        buf = io.BytesIO()
        img.save(buf)
        st.image(buf.getvalue(), caption="QR Code gerado")
