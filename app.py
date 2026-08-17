import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

# 1. Carregar variáveis de ambiente
load_dotenv()

# 2. Configuração Visual da Página
st.set_page_config(
    page_title="BilingIA - STEM & Biodiversidade Moçambique",
    page_icon="🇲🇿",
    layout="wide"
)

# 3. ESTILIZAÇÃO CUSTOMIZADA
st.markdown("""
    <style>
    /* Cores da Bandeira de Moçambique:
       Verde: #009A44 | Amarelo/Ouro: #FCD116 | Vermelho: #D21034 | Preto: #1E1E1E */

    /* Título Principal com Gradiente nas Cores da Bandeira */
    .moz-title-flag {
        font-size: 2.3rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #009A44 0%, #009A44 35%, #D21034 65%, #D21034 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }

    .moz-sub-banner {
        color: #333333;
        font-weight: 600;
        font-size: 1.05rem;
        border-left: 4px solid #FCD116;
        padding-left: 10px;
        margin-top: 6px;
        margin-bottom: 15px;
    }

    /* Linha sutil de separação tricolor */
    .moz-flag-divider {
        height: 3px;
        width: 100%;
        background: linear-gradient(90deg, #009A44 0% 33%, #FCD116 33% 66%, #D21034 66% 100%);
        border-radius: 2px;
        margin-bottom: 20px;
    }

    /* Ajuste visual para o botão Popover (+) */
    div[data-testid="stPopover"] {
        margin-top: 5px;
    }
    div[data-testid="stPopover"] > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #009A44;
        color: #009A44;
        font-weight: bold;
    }
    div[data-testid="stPopover"] > button:hover {
        background-color: #009A44;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 4. Inicializar o Cliente Oficial do Gemini
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Chave GEMINI_API_KEY não encontrada no ficheiro .env ou nos Secrets do Streamlit. Por favor, verifique a configuração.")
    st.stop()

client = genai.Client(api_key=api_key)

# 5. PAINEL LATERAL (SIDEBAR) SIMPLES
with st.sidebar:
    st.image("logot.png", width=150)
    st.caption("Ecossistema de Aprendizado Bilíngue com IA | Moçambique")
    st.write("---")

    # Menu 1: Modo de Interação
    modo_interacao = st.radio(
        "Escolha o Modo de Interação:",
        ["💬 Chat STEM+L", "📸 Reconhecimento de Imagem"],
        help="Alterne entre o assistente de conversação/diagramas e a análise de imagem por câmara/galeria."
    )
    st.write("---")

    # Menu 2: Seleção de Língua Local
    lingua_selecionada = st.selectbox(
        "Selecione a Língua Local:",
        ["Xichangana", "Gitonga", "Emakhuwa (Em breve)", "Cisena (Em breve)"]
    )

    # Menu 3: Seleção da Área STEM
    area_selecionada = st.selectbox(
        "Selecione a Área de Ensino:",
        ["Ciências Naturais", "Física", "Química", "Matemática", "Robótica & Programação", "Ciências Sociais"]
    )

    st.write("---")
    st.markdown("**Sobre a Plataforma:**")
    st.info(
        "O **BilingIA** é uma solução educacional moçambicana concebida para apoiar a aprendizagem de "
        "STEM e Conservação Ambiental através de línguas nacionais e Português."
    )

    if st.button("Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        if "chat_uploaded_image" in st.session_state:
            st.session_state.chat_uploaded_image = None
        st.rerun()

    st.write("---")
    # --- SECÇÃO DE IDENTIDADE E CONTACTO DO AUTOR ---
    st.markdown(
        """
        <div style="font-size: 0.82rem; color: #555555; line-height: 1.4;">
            <p style="margin-bottom: 4px;"><strong>Idealização & Desenvolvimento:</strong></p>
            <p style="margin-bottom: 8px; font-weight: 500; color: #111111;">Moisés Alberto Namburete</p>
            <p style="margin-bottom: 4px;">📩 <em>moisesluzi@gmail.com</em></p>
            <p style="margin-bottom: 0px;">📞 <em>+258 845160049 / +258 871880847</em></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("© 2026 BilingIA — Todos os direitos reservados")

# 6. TÍTULO PRINCIPAL COLORIDO
st.markdown("""
    <h1 class="moz-title-flag">BilingIA — Mudyondzisi wa STEAM+L</h1>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="moz-sub-banner">
        🇲🇿 Língua Ativa: <b>{lingua_selecionada}</b> + Português &nbsp;|&nbsp; Modo: <b>{modo_interacao}</b>
    </div>
    <div class="moz-flag-divider"></div>
""", unsafe_allow_html=True)

# ==============================================================================
# MODO 1: CHAT STEM+L (COM MENU SUSPENSO '+' PARA MIDIA)
# ==============================================================================
if modo_interacao == "💬 Chat STEM+L":
    st.markdown(f"### Módulo Interativo de {area_selecionada}")

    SYSTEM_PROMPT_STEM = f"""
    Você é o "Mudyondzisi wa STEM" (Professor de STEM), um assistente educacional interativo da plataforma BilingIA em Moçambique.

    CONFIGURAÇÃO ATUAL DA AULA:
    - Língua de Ensino: {lingua_selecionada}
    - Área do Conteúdo: {area_selecionada}

    SEU OBJETIVO:
    Ensinar conceitos da área de {area_selecionada} de forma clara, pedagogicamente adequada e culturalmente acolhedora para alunos moçambicanos, utilizando a língua {lingua_selecionada}.

    ANÁLISE MULTIMODAL E VISUAL (DIAGRAMAS, DESENHOS E FIGURAS):
    Quando o utilizador enviar uma imagem/desenho (ex: figura geométrica, órgãos como o coração, circuito elétrico, fórmula ou problema em imagem):
    1. RECONHECIMENTO E NOMENCLATURA: Identifique a figura/diagrama e faça a legendagem/nomenclatura das suas partes principais.
    2. RECONHECIMENTO DE TEXTO (OCR): Leia e interprete qualquer texto ou equação presente na imagem.
    3. EXPLICAÇÃO CONCEITUAL: Explique a função de cada parte ou resolva o problema passo a passo.

    GLOSSÁRIO DE REFERÊNCIA DE STEM (CHANGANA LOCAL):
    - Água: Māti
    - Chuva: Mpfula (ou Npfula)
    - Sol: Dyambu
    - Nuvem / Nuvens: Papana / Mapapa
    - Rio: Nambu (pl. Minambu)
    - Céu: Tilweni / Tilo
    - Terra / Solo: Misava
    - Calor / Quente: Hisa / Kuhlula
    - Frio / Arrefecer: Titimela / Kuhola
    - Panela: Mpotso
    - Fumaça / Vapor: Musi
    - Subir / Evaporar: Kukhandziya / Kutlhatlha
    - Cair / Chover: Kuwa / Kuna

    REGRAS RÍGIDAS DE RESPOSTA E INTEGRIDADE LINGUÍSTICA:
    1. PUREZA LINGUÍSTICA ABSOLUTA: Responda APENAS na língua selecionada ({lingua_selecionada}). 
       É ESTRITAMENTE PROIBIDO misturar palavras ou gramática de outras línguas locais.

    2. PROTOCOLO DE VOCABULÁRIO AUSENTE OU NÃO VALIDADO:
       Se você não tiver certeza absoluta do vocábulo científico ou da tradução exata na língua selecionada ({lingua_selecionada}):
       - NÃO INVENTE nem use palavras de outra língua bantu.
       - Responda de forma transparente e amigável em Português indicando que a tradução exata nesta língua está em fase de validação no BilingIA.

    3. TRADUÇÃO DE APOIO: Forneça a tradução/explicação em Português logo em seguida para garantir o reforço bilíngue.
    4. ADAPTAÇÃO PEDAGÓGICA: Adapte os exemplos à área selecionada ({area_selecionada}) com analogias do cotidiano moçambicano.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibir histórico de conversa
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- BARRA SUPERIOR CLEAN PARA ANEXOS (MENU SUSPENSO '+') ---
    col_menu, col_input = st.columns([0.10, 0.90])

    image_to_send = None

    with col_menu:
        # Botão + que abre um menu suspenso retrátil
        with st.popover("➕", help="Clique para anexar imagem ou usar a câmara"):
            st.markdown("##### 📎 Anexar Recurso Visual")
            opcao_anexo = st.radio(
                "Fonte da Imagem:",
                ["📁 Galeria / Ficheiro", "📸 Usar Câmara"],
                key="chat_media_source"
            )

            if opcao_anexo == "📁 Galeria / Ficheiro":
                image_to_send = st.file_uploader(
                    "Carregar imagem:", 
                    type=["jpg", "jpeg", "png"],
                    key="chat_popover_file"
                )
            else:
                image_to_send = st.camera_input(
                    "Fotografar:", 
                    key="chat_popover_cam"
                )

    with col_input:
        user_input = st.chat_input(f"Escreva a sua dúvida sobre {area_selecionada}...")

    # Indicador visual discreto caso haja uma imagem pronta no menu +
    if image_to_send is not None:
        st.info("📎 **Imagem anexada no menu (+).** Escreva a sua pergunta abaixo e prima Enter para enviar.")

    # Processar envio da mensagem
    if user_input:
        texto_mensagem = user_input
        if image_to_send is not None:
            texto_mensagem = f"📷 [Imagem Anexada] {user_input}"

        st.session_state.messages.append({"role": "user", "content": texto_mensagem})
        with st.chat_message("user"):
            if image_to_send is not None:
                img_preview = Image.open(image_to_send)
                st.image(img_preview, width=250, caption="Anexo da Pergunta")
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Mudyondzisi wa BilingIA a tsala nhlamulo... (O professor está a analisar e a escrever a resposta...)"):
                try:
                    contents_payload = [user_input]
                    if image_to_send is not None:
                        img_obj = Image.open(image_to_send)
                        contents_payload = [img_obj, user_input]

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=contents_payload,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT_STEM,
                            temperature=0.3
                        )
                    )
                    bot_response = response.text
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})

                except Exception as e:
                    st.error(f"Erro ao ligar ao serviço do Gemini: {e}")

# ==============================================================================
# MODO 2: RECONHECIMENTO DE BIODIVERSIDADE E IMAGEM
# ==============================================================================
elif modo_interacao == "📸 Reconhecimento de Imagem":
    st.markdown("### 🌿 Identificação de Espécies, Fauna, Flora & Recursos Naturais")
    st.caption("Capture com a câmara ou envie uma fotografia da galeria para análise por IA.")

    metodo_captura = st.radio(
        "Escolha como deseja fornecer a fotografia:",
        ["📸 Usar Câmara do Telemóvel/PC", "📁 Carregar da Galeria/Ficheiro"],
        horizontal=True
    )

    uploaded_image = None

    if metodo_captura == "📸 Usar Câmara do Telemóvel/PC":
        uploaded_image = st.camera_input("Tire uma fotografia da espécie ou recurso natural:")
    else:
        uploaded_image = st.file_uploader(
            "Selecione uma fotografia da galeria:", 
            type=["jpg", "jpeg", "png"]
        )

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Fotografia em Análise", use_container_width=True)

        if st.button("🔎 Identificar Espécie / Xiyaxiya", type="primary"):
            with st.spinner("A analisar a biodiversidade e a consultar o ecossistema moçambicano..."):
                
                SYSTEM_PROMPT_BIO = f"""
                Você é um Botânico, Zoólogo e Ecologista especialista na biodiversidade, fauna, flora e recursos naturais de Moçambique, integrado no ecossistema BilingIA.

                AO ANALISAR A IMAGEM FORNECIDA:
                1. IDENTIFICAÇÃO E NOMEAÇÃO:
                   - Nome Comum em Português.
                   - Nome Científico (em itálico).
                   - Nome na Língua Local ({lingua_selecionada}) (se houver correspondência validada no vocabulário oficial, caso contrário forneça o termo descritivo respeitando a ortografia oficial).

                2. IMPORTÂNCIA ECOLÓGICA E CONSERVAÇÃO:
                   - Papel no ecossistema (ex: conservação do solo, fertilidade, retenção de água, polinização, cadeia alimentar).
                   - Relação com parques, reservas naturais ou ecossistemas de Moçambique (ex: Gorongosa, Maputo, Niassa, Bazaruto, Áreas Protegidas).
                   - Estado de conservação, valor medicinal ou comunitário tradicional.

                3. REFORÇO BILÍNGUE OBRIGATÓRIO:
                   - Apresente a explicação organizada em dois blocos claros: primeiro em {lingua_selecionada} e em seguida a correspondente explicação detalhada em Português.
                """

                prompt_analise = "Identifique esta espécie/recurso natural, forneça o nome comum, científico e em língua local, e explique a sua importância para o ecossistema de Moçambique."

                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[img, prompt_analise],
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT_BIO,
                            temperature=0.2
                        )
                    )

                    st.markdown("---")
                    st.markdown("### 🌿 Resultado da Análise / Swilo swa Nhova:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Erro ao analisar a imagem com o Gemini: {e}")