import streamlit as st
import logging
from huggingface_hub import InferenceClient
import re

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

# Récupération de la clé API Hugging Face depuis les secrets de Streamlit
api_key = st.secrets["HUGGINGFACE_API_KEY"]

# Initialisation du client Hugging Face avec la clé API récupérée
client = InferenceClient(api_key=api_key)

# Interface Streamlit
st.title("🧐 Explorateur de Sous-questions avec IA")

# Fonction pour appeler l'API Hugging Face avec un prompt spécifique
def get_ia_response(prompt, max_tokens=600):
    response = client.chat_completion(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    if response:
        return response['choices'][0]['message']['content']
    else:
        st.error("Erreur dans la réponse de l'API.")
        return ""

# Fonction pour générer les sous-questions et les réponses IA à chaque niveau
def generate_subquestions(question, level):
    prompt = f"""
    Question : "{question}"
    Réponds avec deux sous-questions de niveau {level} qui approfondissent des aspects spécifiques de cette question.
    Fournis également une réponse détaillée à chaque sous-question.
    """
    response = get_ia_response(prompt)
    if response:
        subquestions = re.findall(r'(\d+\.\d+(?:\.\d+)? [^\n]+)', response)
        ia_responses = re.findall(r'Réponse : ([^\n]+)', response)
        return subquestions, ia_responses
    return [], []

# Sélecteur de langue
languages = {
    "English": "en",
    "Français": "fr",
    "Español": "es",
    "Português": "pt",
    "العربية": "ar",
    "Русский": "ru",
    "हिन्दी": "hi",
    "Deutsch": "de",
    "日本語": "ja"
}
selected_language = st.selectbox("Sélectionnez la langue", list(languages.keys()))

# Textes fixes traduits
translations = {
    "English": {
        "enter_question": "Enter a main question:",
        "initial_response": "Complete response generated:",
        "main_question": "Main question:",
        "response": "Response:",
        "your_response": "Your response to the main question:",
        "validate_response": "Validate main response",
        "sub_questions_1": "Sub-questions Level 1:",
        "sub_questions_2": "Sub-sub-questions Level 2:",
        "final_summary": "Final summary:",
        "compare_responses": "Compare responses:",
        "initial_response": "Initial response:",
        "final_response": "Final response:",
        "summary_details": "Summary details:",
        "generate_final_summary": "Generate final summary"
    },
    "Français": {
        "enter_question": "Entrez une question principale :",
        "initial_response": "Réponse complète générée :",
        "main_question": "Question principale :",
        "response": "Réponse :",
        "your_response": "Votre réponse à la question principale :",
        "validate_response": "Valider la réponse principale",
        "sub_questions_1": "Sous-questions de Niveau 1 :",
        "sub_questions_2": "Sous-sous-questions de Niveau 2 :",
        "final_summary": "Reformulation finale :",
        "compare_responses": "Comparaison des réponses :",
        "initial_response": "Réponse initiale :",
        "final_response": "Réponse reformulée :",
        "summary_details": "Détails des étapes de reformulation :",
        "generate_final_summary": "Générer la reformulation finale"
    },
    "Español": {
        "enter_question": "Introduce una pregunta principal:",
        "initial_response": "Respuesta completa generada:",
        "main_question": "Pregunta principal:",
        "response": "Respuesta:",
        "your_response": "Tu respuesta a la pregunta principal:",
        "validate_response": "Validar respuesta principal",
        "sub_questions_1": "Subpreguntas de Nivel 1:",
        "sub_questions_2": "Sub-subpreguntas de Nivel 2:",
        "final_summary": "Resumen final:",
        "compare_responses": "Comparar respuestas:",
        "initial_response": "Respuesta inicial:",
        "final_response": "Respuesta reformulada:",
        "summary_details": "Detalles del resumen:",
        "generate_final_summary": "Generar resumen final"
    },
    "Português": {
        "enter_question": "Insira uma pergunta principal:",
        "initial_response": "Resposta completa gerada:",
        "main_question": "Pergunta principal:",
        "response": "Resposta:",
        "your_response": "Sua resposta à pergunta principal:",
        "validate_response": "Validar resposta principal",
        "sub_questions_1": "Subperguntas de Nível 1:",
        "sub_questions_2": "Sub-subperguntas de Nível 2:",
        "final_summary": "Resumo final:",
        "compare_responses": "Comparar respostas:",
        "initial_response": "Resposta inicial:",
        "final_response": "Resposta reformulada:",
        "summary_details": "Detalhes do resumo:",
        "generate_final_summary": "Gerar resumo final"
    },
    "العربية": {
        "enter_question": "أدخل سؤالاً رئيسياً:",
        "initial_response": "الإجابة الكاملة المولدة:",
        "main_question": "السؤال الرئيسي:",
        "response": "الإجابة:",
        "your_response": "إجابتك على السؤال الرئيسي:",
        "validate_response": "تحقق من الإجابة الرئيسية",
        "sub_questions_1": "الأسئلة الفرعية مستوى 1:",
        "sub_questions_2": "الأسئلة الفرعية الفرعية مستوى 2:",
        "final_summary": "الملخص النهائي:",
        "compare_responses": "مقارنة الإجابات:",
        "initial_response": "الإجابة الأولية:",
        "final_response": "الإجابة المعدلة:",
        "summary_details": "تفاصيل الملخص:",
        "generate_final_summary": "إنشاء الملخص النهائي"
    },
    "Русский": {
        "enter_question": "Введите основной вопрос:",
        "initial_response": "Полный ответ сгенерирован:",
        "main_question": "Основной вопрос:",
        "response": "Ответ:",
        "your_response": "Ваш ответ на основной вопрос:",
        "validate_response": "Подтвердить основной ответ",
        "sub_questions_1": "Подвопросы Уровень 1:",
        "sub_questions_2": "Под-подвопросы Уровень 2:",
        "final_summary": "Итоговое резюме:",
        "compare_responses": "Сравнить ответы:",
        "initial_response": "Первоначальный ответ:",
        "final_response": "Переформулированный ответ:",
        "summary_details": "Детали резюме:",
        "generate_final_summary": "Сгенерировать итоговое резюме"
    },
    "हिन्दी": {
        "enter_question": "एक मुख्य सवाल दर्ज करें:",
        "initial_response": "पूरा उत्तर उत्पन्न:",
        "main_question": "मुख्य सवाल:",
        "response": "उत्तर:",
        "your_response": "आपका मुख्य सवाल का उत्तर:",
        "validate_response": "मुख्य उत्तर की पुष्टि करें",
        "sub_questions_1": "उप-सवाल स्तर 1:",
        "sub_questions_2": "उप-उप-सवाल स्तर 2:",
        "final_summary": "अंतिम सारांश:",
        "compare_responses": "उत्तरों की तुलना करें:",
        "initial_response": "प्रारंभिक उत्तर:",
        "final_response": "पुनर्व्यवस्थित उत्तर:",
        "summary_details": "सारांश विवरण:",
        "generate_final_summary": "अंतिम सारांश उत्पन्न करें"
    },
    "Deutsch": {
        "enter_question": "Geben Sie eine Hauptfrage ein:",
        "initial_response": "Vollständige Antwort generiert:",
        "main_question": "Hauptfrage:",
        "response": "Antwort:",
        "your_response": "Ihre Antwort auf die Hauptfrage:",
        "validate_response": "Hauptantwort überprüfen",
        "sub_questions_1": "Unterfragen Ebene 1:",
        "sub_questions_2": "Unter-Unterfragen Ebene 2:",
        "final_summary": "Endzusammenfassung:",
        "compare_responses": "Antworten vergleichen:",
        "initial_response": "Erste Antwort:",
        "final_response": "Umformulierte Antwort:",
        "summary_details": "Zusammenfassungsdetails:",
        "generate_final_summary": "Endzusammenfassung generieren"
    },
    "日本語": {
        "enter_question": "主要な質問を入力してください:",
        "initial_response": "完全な応答が生成されました:",
        "main_question": "主要な質問:",
        "response": "応答:",
        "your_response": "主要な質問へのあなたの応答:",
        "validate_response": "主要な応答を検証する",
        "sub_questions_1": "サブ質問レベル1:",
        "sub_questions_2": "サブサブ質問レベル2:",
        "final_summary": "最終的な要約:",
        "compare_responses": "応答を比較する:",
        "initial_response": "初期応答:",
        "final_response": "改訂された応答:",
        "summary_details": "要約の詳細:",
        "generate_final_summary": "最終的な要約を生成する"
    }
}

# Étape 1 : Saisie de la question principale
st.write(f"### {translations[selected_language]['enter_question']}")
question = st.text_input("", placeholder="Comment vendre des bijoux sur internet ?", label_visibility="collapsed")

# Stocker toutes les réponses IA et utilisateur dans un dictionnaire structuré
responses = {"main_question": question, "ia_response": None, "user_response": None, "sub_questions": {}}

if question:
    # Génération de la réponse IA à la question principale
    with st.spinner('🧠 Génération de la réponse initiale...'):
        main_response = get_ia_response(f"Réponds à la question principale : {question}")
        st.write(f"### {translations[selected_language]['initial_response']}")
        st.write(f"**{translations[selected_language]['main_question']}** {question}")
        st.write(f"**{translations[selected_language]['response']}** {main_response}")
        responses["ia_response"] = main_response

    # Réponse de l'utilisateur à la question principale
    user_main_response = st.text_area(f"{translations[selected_language]['your_response']} {question}", placeholder="Entrez votre réponse ici...", key="user_main_response")
    responses["user_response"] = user_main_response

    # Étape 2 : Générer les sous-questions de niveau 1
    st.write(f"### {translations[selected_language]['sub_questions_1']}")
    subquestions_1, ia_responses_1 = generate_subquestions(question, level=1)

    for idx, (subq, ia_resp) in enumerate(zip(subquestions_1, ia_responses_1)):
        st.write(f"**{subq}**")
        st.write(f"Réponse IA : {ia_resp}")
        
        user_response = st.text_area(f"Votre réponse pour {subq}", placeholder="Entrez votre réponse ici...", key=f"user_response_{subq}")
        responses["sub_questions"][subq] = {"ia_response": ia_resp, "user_response": user_response, "sub_sub_questions": {}}

        # Générer les sous-questions de niveau 2 pour chaque sous-question de niveau 1
        st.write(f"### {translations[selected_language]['sub_questions_2']} pour {subq}")
        sub_subquestions, sub_ia_responses = generate_subquestions(subq, level=2)

        for sub_idx, (sub_subq, sub_ia_resp) in enumerate(zip(sub_subquestions, sub_ia_responses)):
            st.write(f"**{sub_subq}**")
            st.write(f"Réponse IA : {sub_ia_resp}")

            sub_user_response = st.text_area(f"Votre réponse pour {sub_subq}", placeholder="Entrez votre réponse ici...", key=f"user_response_{sub_subq}")
            responses["sub_questions"][subq]["sub_sub_questions"][sub_subq] = {
                "ia_response": sub_ia_resp,
                "user_response": sub_user_response
            }

    # Étape 3 : Générer la reformulation finale basée sur toutes les réponses
    if st.button(translations[selected_language]['final_summary']):
        with st.spinner('📝 Génération de la reformulation finale...'):
            reformulation_prompt = f"Question principale : {question}\n\nRéponse initiale : {main_response}\n\n"
            for subq, sub_data in responses["sub_questions"].items():
                reformulation_prompt += f"Sous-question : {subq}\nRéponse IA : {sub_data['ia_response']}\nRéponse utilisateur : {sub_data['user_response']}\n"
                for sub_subq, sub_sub_data in sub_data["sub_sub_questions"].items():
                    reformulation_prompt += f"Sous-sous-question : {sub_subq}\nRéponse IA : {sub_sub_data['ia_response']}\nRéponse utilisateur : {sub_sub_data['user_response']}\n"

            reformulation_prompt += (
                "Reformule la réponse à la **question principale** en intégrant les informations des sous-questions et des sous-sous-questions, "
                "en utilisant les réponses IA et utilisateur pour chaque niveau."
            )

            final_summary = get_ia_response(reformulation_prompt)
            st.write(f"### {translations[selected_language]['final_summary']}")
            st.write(final_summary)
