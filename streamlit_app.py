import logging
import streamlit as st
from huggingface_hub import InferenceClient
import re
import time

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)

# Initialisation du client Hugging Face avec la clé API
client = InferenceClient(api_key="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")

# Interface Streamlit
st.title("🤔 Explorateur de Sous-questions avec IA")

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
question = st.text_input("", placeholder="How to sell jewelry online?")

if question:
    # Détection de la langue de la question principale
    question_language = languages[selected_language]

    # Étape 1 : Génération de la réponse initiale
    def get_response_with_retries(prompt, max_retries=3, max_tokens=1000):
        retry_count = 0
        response = None
        while not response and retry_count < max_retries:
            response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            if not response:
                logging.warning(f"Tentative {retry_count + 1} échouée. Réessayer...")
                retry_count += 1
                max_tokens = max(500, max_tokens - 200)  # Réduire les tokens à chaque tentative
                time.sleep(2)
        return response

    with st.spinner('🤓 Génération de la réponse initiale...'):
        prompt_principal = f"Question principale : \"{question}\"\n\nRéponds à cette question principale avec une réponse détaillée."
        logging.debug(f"Prompt généré : {prompt_principal}")

        response = get_response_with_retries(prompt_principal)

        if not response:
            st.error("❌ Aucune réponse n'a été reçue de l'API après plusieurs tentatives.")
        else:
            generated_response = response['choices'][0]['message']['content']
            st.write(f"### {translations[selected_language]['initial_response']}")
            st.write(f"**{translations[selected_language]['main_question']}** {question}")
            main_question_response = generated_response.strip()
            st.write(f"**{translations[selected_language]['response']}** {main_question_response}")

            # Champ pour la réponse de l'utilisateur à la question principale
            st.subheader("💡 " + translations[selected_language]['your_response'])
            user_main_response = st.text_area(f"{translations[selected_language]['your_response']} {question}", placeholder="Entrez votre réponse ici...", key="user_main_response")
            if st.button(translations[selected_language]['validate_response'], key="validate_main_response"):
                logging.debug(f"Réponse utilisateur pour la question principale enregistrée : {user_main_response}")
                st.success("✅ Réponse principale enregistrée avec succès.")

    # Étape 2 : Génération des sous-questions de niveau 1
    with st.spinner('🔄 Génération des sous-questions de niveau 1...'):
        prompt_sous_questions_1 = f"Question principale : \"{question}\"\n\nGénère deux sous-questions (nommées 1.1 et 1.2) qui approfondissent des aspects spécifiques de la question principale. Assure-toi que ce sont des questions et non des affirmations. Donne une réponse détaillée pour chacune d'elles."
        response = get_response_with_retries(prompt_sous_questions_1)

        if not response:
            st.error("❌ Aucune réponse n'a été reçue de l'API pour les sous-questions de niveau 1 après plusieurs tentatives.")
        else:
            generated_response = response['choices'][0]['message']['content']
            sous_questions = re.findall(r'(\d+\.\d+ [^\n]+)', generated_response)
            ia_responses = re.findall(r'Réponse : ([^\n]+)', generated_response)

            if len(sous_questions) != len(ia_responses):
                st.warning(f"⚠️ Nombre de sous-questions ({len(sous_questions)}) ne correspond pas au nombre de réponses IA ({len(ia_responses)}).")

            if sous_questions:
                st.write(f"### {translations[selected_language]['sub_questions_1']}")
                user_responses_1 = {}

                for idx, question in enumerate(sous_questions):
                    question_id, question_text = question.split(' ', 1)
                    st.write(f"📍 **{question_id} :** {question_text.strip()}")
                    if idx < len(ia_responses):
                        st.write(f"**{translations[selected_language]['response']}** {ia_responses[idx]}")
                    else:
                        st.write(f"**{translations[selected_language]['response']}** Aucune réponse disponible.")

                    unique_key = f"user_response_{question_id}_1_{idx}"
                    user_responses_1[question_id] = st.text_area(f"Votre réponse pour {question_id}", placeholder="Entrez votre réponse ici...", key=unique_key)
                    logging.debug(f"Réponse utilisateur pour {question_id} avant validation : {user_responses_1[question_id]}")
                    if st.button(f"Valider la réponse pour {question_id}", key=f"validate_{question_id}_1_{idx}"):
                        logging.debug(f"Réponse utilisateur pour {question_id} enregistrée : {user_responses_1[question_id]}")
                        st.success(f"✅ Réponse pour {question_id} enregistrée avec succès.")

    # Étape 3 : Génération des sous-sous-questions de niveau 2
    with st.spinner('🔄 Génération des sous-sous-questions de niveau 2...'):
        prompt_sous_questions_2 = f"Question principale : \"{question}\"\n\nPour chaque sous-question de niveau 1 (1.1 et 1.2), génère deux nouvelles sous-questions (nommées 1.1.1, 1.1.2, 1.2.1, et 1.2.2) qui explorent davantage les réponses. Assure-toi que ce sont des questions et non des affirmations. Donne une réponse détaillée pour chacune d'elles."
        response = get_response_with_retries(prompt_sous_questions_2, max_tokens=2000)

        if not response:
            st.error("❌ Aucune réponse n'a été reçue de l'API pour les sous-sous-questions de niveau 2 après plusieurs tentatives.")
        else:
            generated_response = response['choices'][0]['message']['content']
            sous_sous_questions = re.findall(r'(\d+\.\d+\.\d+ [^\n]+)', generated_response)
            ia_responses_2 = re.findall(r'Réponse : ([^\n]+)', generated_response)

            if len(sous_sous_questions) != len(ia_responses_2):
                st.warning(f"⚠️ Nombre de sous-sous-questions ({len(sous_sous_questions)}) ne correspond pas au nombre de réponses IA ({len(ia_responses_2)}).")

            if sous_sous_questions:
                st.write(f"### {translations[selected_language]['sub_questions_2']}")
                user_responses_2 = {}

                for idx, question in enumerate(sous_sous_questions):
                    question_id, question_text = question.split(' ', 1)
                    st.write(f"📍 **{question_id} :** {question_text.strip()}")
                    if idx < len(ia_responses_2):
                        st.write(f"**{translations[selected_language]['response']}** {ia_responses_2[idx]}")
                    else:
                        st.write(f"**{translations[selected_language]['response']}** Aucune réponse disponible.")
                    unique_key = f"user_response_{question_id}_2_{idx}"
                    user_responses_2[question_id] = st.text_area(f"Votre réponse pour {question_id}", placeholder="Entrez votre réponse ici...", key=unique_key)
                    logging.debug(f"Réponse utilisateur pour {question_id} avant validation : {user_responses_2[question_id]}")
                    if st.button(f"Valider la réponse pour {question_id}", key=f"validate_{question_id}_2_{idx}"):
                        logging.debug(f"Réponse utilisateur pour {question_id} enregistrée : {user_responses_2[question_id]}")
                        st.success(f"✅ Réponse pour {question_id} enregistrée avec succès.")

    # Étape 4 : Reformulation finale
    if st.button(translations[selected_language]['generate_final_summary']):
        with st.spinner('📝 Génération de la reformulation finale...'):
            reformulation_prompt = f"Question principale : \"{question}\"\n\nRéponse initiale :\n{main_question_response}\n\n"
            reformulation_prompt += "\nAnalyse des sous-questions et sous-sous-questions :\n"

            for question_id, response in zip(sous_questions, ia_responses):
                user_response = user_responses_1.get(question_id, "")
                logging.debug(f"Utilisateur - {question_id} : {user_response}")
                reformulation_prompt += f"{question_id}\nRéponse IA : {response}\nRéponse utilisateur : {user_response}\n\n"

            for question_id, response in zip(sous_sous_questions, ia_responses_2):
                user_response = user_responses_2.get(question_id, "")
                logging.debug(f"Utilisateur - {question_id} : {user_response}")
                reformulation_prompt += f"{question_id}\nRéponse IA : {response}\nRéponse utilisateur : {user_response}\n\n"

            reformulation_prompt += f"\nReformule la réponse à la question principale en prenant en compte les informations supplémentaires apportées par les sous-questions et sous-sous-questions, et donne la réponse."

            logging.debug(f"Prompt pour reformulation finale : {reformulation_prompt}")

            reformulation_response = get_response_with_retries(reformulation_prompt, max_tokens=len(main_question_response.split()) + 50)

            if reformulation_response:
                final_summary = reformulation_response['choices'][0]['message']['content']
                st.write(f"### {translations[selected_language]['final_summary']}")
                st.write(final_summary)

                # Comparaison des réponses
                st.write(f"### {translations[selected_language]['compare_responses']}")
                st.write(f"**{translations[selected_language]['initial_response']}**")
                st.write(main_question_response)
                st.write(f"**{translations[selected_language]['final_response']}**")
                st.write(final_summary)

                st.write(f"### {translations[selected_language]['summary_details']}")
                st.write("La reformulation a pris en compte les réponses IA et utilisateur pour chaque sous-question et sous-sous-question. Voici un résumé des éléments ajoutés ou modifiés :")

                for question_id, response in zip(sous_questions, ia_responses):
                    user_response = user_responses_1.get(question_id, "")
                    st.write(f"- **{question_id}** : Réponse IA : {response}, Réponse utilisateur : {user_response}")

                for question_id, response in zip(sous_sous_questions, ia_responses_2):
                    user_response = user_responses_2.get(question_id, "")
                    st.write(f"- **{question_id}** : Réponse IA : {response}, Réponse utilisateur : {user_response}")

            else:
                st.error("❌ Aucune reformulation finale n'a été reçue de l'API après plusieurs tentatives.")

