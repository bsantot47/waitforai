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

# Fonction pour générer une réponse
def generate_response(prompt):
    try:
        response = client.text_generation("mistralai/Mistral-7B-Instruct-v0.3", inputs=prompt, parameters={"max_length": 1000})
        return response.get("generated_text", "Erreur lors de la génération.")
    except Exception as e:
        logging.error(f"Erreur lors de la génération de la réponse : {e}")
        return "Erreur lors de la génération de la réponse."

# Fonction pour extraire les sous-questions
def extract_sub_questions(response):
    return re.findall(r'(\d+\.\d+(?:\.\d+)? [^\n]+)', response)

# Fonction pour générer la synthèse finale
def generate_final_summary(question, main_question_response, sous_questions, ia_responses, user_responses):
    reformulation_prompt = f"Question principale : \"{question}\"\n\n"
    reformulation_prompt += "Voici la réponse initiale à la question principale :\n"
    reformulation_prompt += f"{main_question_response}\n\n"
    reformulation_prompt += "Analyse des sous-questions et des réponses IA et utilisateur :\n\n"

    for question_id, ia_response in zip(sous_questions, ia_responses):
        user_response = user_responses.get(question_id, "Pas de réponse utilisateur")
        reformulation_prompt += f"Sous-question : {question_id}\n"
        reformulation_prompt += f"Réponse IA : {ia_response}\n"
        reformulation_prompt += f"Réponse utilisateur : {user_response}\n\n"

    reformulation_prompt += f"\nMaintenant, reformule la **réponse à la question principale** : \"{question}\" en prenant en compte les informations des sous-questions et des réponses IA et utilisateur."
    
    return generate_response(reformulation_prompt)

# Étape 1 : Saisie de la question principale
st.write(f"### {translations[selected_language]['enter_question']}")
question = st.text_input("", placeholder="Comment vendre des bijoux sur internet ?")

if question:
    with st.spinner('🧠 Génération de la réponse initiale...'):
        prompt_principal = f"""
        Question principale :
        "{question}"

        Réponds à cette question principale avec une réponse détaillée et longue. Explique chaque aspect en profondeur.

        Ensuite, génère deux sous-questions (nommées 1.1 et 1.2) qui approfondissent des aspects spécifiques de la question principale, puis réponds à chacune des deux sous-questions.

        Pour chaque sous-question de niveau 1 (1.1 et 1.2), génère deux nouvelles sous-questions (nommées 1.1.1, 1.1.2, 1.2.1, et 1.2.2) qui explorent davantage les réponses, mais **ne génère pas de sous-questions supplémentaires** au-delà de celles-ci. Limite-toi uniquement à ces sous-questions.
        """
        logging.debug(f"Prompt généré : {prompt_principal}")

        # Demande de réponse au modèle
        generated_response = generate_response(prompt_principal)

        if not generated_response:
            st.error("❌ Aucune réponse n'a été reçue du modèle.")
        else:
            st.write("### " + translations[selected_language]['initial_response'])
            st.write(f"**{translations[selected_language]['main_question']}** {question}")
            main_question_response = generated_response.split('Sous-questions de Niveau 1 :')[0].strip()
            st.write(f"**{translations[selected_language]['response']}** {main_question_response}")

            st.subheader("💡 " + translations[selected_language]['your_response'])
            user_main_response = st.text_area(f"{translations[selected_language]['your_response']} {question}", placeholder="Entrez votre réponse ici...")

            sous_questions = extract_sub_questions(generated_response)
            ia_responses = re.findall(r'Réponse : ([^\n]+)', generated_response)

            if len(sous_questions) != len(ia_responses):
                st.warning(f"⚠️ Nombre de sous-questions ({len(sous_questions)}) ne correspond pas au nombre de réponses IA ({len(ia_responses)}).")

            if sous_questions:
                st.write("### " + translations[selected_language]['sub_questions_1'])
                for sq in sous_questions:
                    st.write(f"📌 {sq}")
            else:
                st.error("❌ Aucune sous-question n'a été extraite.")

            st.subheader("💡 Vos réponses aux questions générées par l'IA")
            user_responses = {}
            response_sources = {}

            for idx, question in enumerate(sous_questions):
                question_id, question_text = question.split(' ', 1)

                with st.expander(f"**{question_id} : {question_text.strip()}**", expanded=True):
                    if idx < len(ia_responses):
                        st.write(f"**{translations[selected_language]['response']}** {ia_responses[idx]}")
                    else:
                        st.write(f"**{translations[selected_language]['response']}** Aucune réponse disponible.")

                    user_responses[question_id] = st.text_area(f"Votre réponse pour {question_id}", placeholder="Entrez votre réponse ici...")

                    response_type = st.selectbox(f"Type d'origine de la réponse pour {question_id}",
                                                 ["Réponse personnelle", "IA", "Forum", "Réseaux sociaux",
                                                  "Vidéos en ligne", "Wikipedia", "Livre",
                                                  "Article scientifique", "Autre"],
                                                 key=f"type_{question_id}")

                    origin_details = st.text_input(f"Détails pour {response_type} ({question_id})", key=f"details_{question_id}")

                    response_sources[question_id] = {"type": response_type, "details": origin_details}

            if st.button("✅ Envoyer vos réponses"):
                st.subheader("🔍 Vos réponses soumises :")
                if user_main_response:
                    st.write(f"**Question principale :** {user_main_response}")
                else:
                    st.write(f"**Question principale :** Aucune réponse soumise.")

                for question_id in user_responses:
                    user_answer = user_responses[question_id]
                    if user_answer:
                        st.write(f"**{question_id} :** {user_answer}")
                        source_info = response_sources[question_id]
                        st.write(f"Origine de votre réponse : {source_info['type']}")
                        if source_info['details']:
                            st.write(f"Détails supplémentaires : {source_info['details']}")
                    else:
                        st.write(f"**{question_id} :** Aucune réponse soumise.")

    if st.button(translations[selected_language]['generate_final_summary']):
        with st.spinner('📝 Génération de la reformulation finale...'):
            final_summary = generate_final_summary(question, main_question_response, sous_questions, ia_responses, user_responses)

            if final_summary:
                st.write(f"### {translations[selected_language]['final_summary']}")
                st.write(final_summary)

                st.write(f"### {translations[selected_language]['compare_responses']}")
                st.write(f"**{translations[selected_language]['initial_response']}**")
                st.write(main_question_response)
                st.write(f"**{translations[selected_language]['final_response']}**")
                st.write(final_summary)
            else:
                st.error("❌ Aucune reformulation finale n'a été reçue du modèle.")
