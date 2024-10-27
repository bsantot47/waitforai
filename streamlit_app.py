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
selected_language_code = languages[selected_language]

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

# Utilisation des traductions pour les textes de l'interface
t = translations[selected_language]

st.write(f"### {t['enter_question']}")
question = st.text_input("", placeholder=t["enter_question"])

def get_response_with_retries(prompt, max_retries=5, max_tokens=1500, initial_delay=2):
    delay = initial_delay
    response_content = None
    for attempt in range(max_retries):
        try:
            response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2
            )
            if response and 'choices' in response and response['choices'][0]['message']['content'].strip():
                response_content = response['choices'][0]['message']['content'].strip()
                break
            else:
                logging.warning(f"Tentative {attempt + 1}: Réponse vide, nouvel essai dans {delay} secondes.")
        except Exception as e:
            logging.error(f"Erreur lors de la génération de la réponse : {e}")

        time.sleep(delay)
        delay *= 1.5

    if not response_content:
        response_content = "Aucune réponse disponible après plusieurs tentatives."

    return response_content

def generate_sub_questions(question, main_question_response):
    sub_questions = []

    # Première sous-question basée sur un aspect de la réponse
    prompt_sous_question_1 = (
        f"Voici une réponse : \"{main_question_response}\". "
        f"Identifie un premier aspect important de cette réponse et formule une sous-question unique pour cet aspect."
    )
    sous_question_1 = get_response_with_retries(prompt_sous_question_1)
    sub_questions.append(sous_question_1)

    # Seconde sous-question basée sur un aspect différent
    prompt_sous_question_2 = (
        f"Voici une réponse : \"{main_question_response}\". "
        f"Identifie un second aspect, différent du premier, et formule une sous-question unique pour cet aspect."
    )
    sous_question_2 = get_response_with_retries(prompt_sous_question_2)

    # Vérification pour éviter les doublons
    if sous_question_1 != sous_question_2:
        sub_questions.append(sous_question_2)
    else:
        sub_questions.append("Alternative sous-question.")

    return sub_questions



# Fonction pour générer un prompt d'analyse pour l'IA
def generate_comparison_prompt(initial_response, reformulated_response):
    prompt = (
        "Compare la qualité de ces deux réponses en analysant quatre aspects :\n\n"
        "1. **Structure et clarté :** Évalue la clarté de la présentation, la structure, et si les informations sont bien organisées.\n"
        "2. **Qualité des détails :** Compare la richesse et la précision des détails fournis dans chaque réponse.\n"
        "3. **Précision et richesse d'information :** Note si les informations sont complètes, précises et pertinentes pour le sujet.\n"
        "4. **Conviction et orientation vers l'action :** Évalue si la réponse incite ou oriente le lecteur vers une action.\n\n"
        "Après avoir analysé ces aspects, attribue un indice de qualité pour chaque réponse, "
        "et indique laquelle est la plus convaincante et utile dans l'ensemble.\n\n"
        f"Réponse initiale : \"{initial_response}\"\n\n"
        f"Réformulation : \"{reformulated_response}\"\n\n"
        "Produis une analyse détaillée avec un indice de qualité pour chaque réponse."
    )
    return prompt



def generate_sub_sub_questions(sub_question, sous_question_response):
    sub_sub_questions = []

    # Prompt pour la première sous-sous-question
    prompt_sous_sous_question_1 = (
        f"Langue : {selected_language_code}\n"
        f"Sous-question : \"{sub_question}\"\n"
        f"Réponse complète de la sous-question : \"{sous_question_response}\"\n\n"
        f"Identifie les deux points les plus significatifs dans cette réponse. Formule une première sous-sous-question pour explorer en détail le point le plus important."
    )
    sous_sous_question_1 = get_response_with_retries(prompt_sous_sous_question_1)
    sub_sub_questions.append((sous_sous_question_1, ""))

    # Prompt pour la seconde sous-sous-question
    prompt_sous_sous_question_2 = (
        f"Langue : {selected_language_code}\n"
        f"Sous-question : \"{sub_question}\"\n"
        f"Réponse complète de la sous-question : \"{sous_question_response}\"\n\n"
        f"Formule une seconde sous-sous-question pour explorer en détail le deuxième point le plus significatif de la réponse."
    )
    sous_sous_question_2 = get_response_with_retries(prompt_sous_sous_question_2)
    sub_sub_questions.append((sous_sous_question_2, ""))

    return sub_sub_questions


sub_sub_questions_responses = {}

if question:
    with st.spinner('🤓 Génération de la réponse initiale...'):
        prompt_principal = (
            f"Langue : {selected_language_code}\n"
            f"Question principale : \"{question}\"\n\n"
            f"Réponds de manière détaillée (400 mots max)."
        )
        main_question_response = get_response_with_retries(prompt_principal)
        st.write(f"### {t['initial_response']}")
        st.write(f"**Question principale** : {question}")
        st.write(f"**Réponse** : {main_question_response}")
        main_user_response = st.text_area("Votre réponse à la question principale :", key="main_response")

    sous_questions = generate_sub_questions(question, main_question_response)
    sous_questions_responses = []
    user_responses_1 = {}
    with st.spinner("🔄 Génération des sous-questions de niveau 1 et leurs réponses..."):
        for i, sous_question in enumerate(sous_questions, start=1):
            st.write(f"📍 **1.{i} :** {sous_question}")

            prompt_response = (
                f"Langue : {selected_language_code}\n"
                f"Sous-question : \"{sous_question}\"\n"
                f"Réponds de manière détaillée (400 mots max)."
            )
            sous_question_response = get_response_with_retries(prompt_response)
            sous_questions_responses.append(sous_question_response)
            st.write(f"**Réponse pour 1.{i} :** {sous_question_response}")
            user_responses_1[f"1.{i}"] = st.text_area(f"Votre réponse pour 1.{i} :", key=f"user_response_1_{i}")

            sub_sub_questions = generate_sub_sub_questions(sous_question, sous_question_response)
            sub_sub_questions_responses[f"1.{i}"] = sub_sub_questions

            user_responses_2 = {}
            for j, (sub_sub_question, sub_sub_question_response) in enumerate(sub_sub_questions, start=1):
                st.write(f"📍 **1.{i}.{j} :** {sub_sub_question}")

                prompt_response_sub = (
                    f"Langue : {selected_language_code}\n"
                    f"Sous-sous-question : \"{sub_sub_question}\"\n"
                    f"Réponds de manière détaillée (400 mots max)."
                )
                sub_sub_question_response = get_response_with_retries(prompt_response_sub)
                st.write(f"**Réponse pour sous-sous-question 1.{i}.{j} :** {sub_sub_question_response}")
                user_responses_2[f"1.{i}.{j}"] = st.text_area(f"Votre réponse pour la sous-sous-question 1.{i}.{j} :", key=f"user_response_2_{i}_{j}")

            user_responses_1[f"1.{i}"] = user_responses_2

def reformulate_section(section_prompt):
    try:
        return get_response_with_retries(section_prompt, max_tokens=512)
    except Exception as e:
        logging.error(f"Erreur lors de la reformulation d'une section : {e}")
        return "Erreur dans la reformulation de cette section."

if st.button("🔧 Générer la reformulation finale"):
    with st.spinner('📝 Génération de la reformulation en cours...'):
        logging.info("Début de la génération du prompt de reformulation.")
        
        reformulations_par_section = []
        for i, (sous_question, response) in enumerate(zip(sous_questions, sous_questions_responses), start=1):
            user_response = user_responses_1.get(f"1.{i}", "")
            section_prompt = (
                f"Langue : {selected_language_code}\n"
                f"Sous-question {i} : \"{sous_question}\"\n"
                f"Réponse IA : {response}; Réponse utilisateur : {user_response}\n"
                "Synthétise cette réponse en intégrant les éléments clés."
            )
            reformulated_section = reformulate_section(section_prompt)
            reformulations_par_section.append(f"Sous-question {i} reformulée : {reformulated_section}")

            for j, (sub_sub_question, sub_sub_response) in enumerate(sub_sub_questions_responses[f"1.{i}"], start=1):
                user_sub_response = user_responses_1[f"1.{i}"].get(f"1.{i}.{j}", "")
                sub_section_prompt = (
                    f"Langue : {selected_language_code}\n"
                    f"Sous-sous-question {i}.{j} : \"{sub_sub_question}\"\n"
                    f"Réponse IA : {sub_sub_response}; Réponse utilisateur : {user_sub_response}\n"
                    "Fournis une synthèse de cette réponse en intégrant les éléments importants."
                )
                reformulated_sub_section = reformulate_section(sub_section_prompt)
                reformulations_par_section.append(f"Sous-sous-question {i}.{j} reformulée : {reformulated_sub_section}")

        final_synthesis_prompt = (
            f"Langue : {selected_language_code}\n"
            f"Question principale : \"{question}\"\n\n"
            f"Résumé des sections reformulées :\n" + "\n".join(reformulations_par_section) +
            "\n\nSynthétise toutes les informations pour une réponse finale complète et detaillés (500 mots max)."
        )

        try:
            final_summary = get_response_with_retries(final_synthesis_prompt, max_tokens=4000)
            st.write("### Reformulation finale :")
            st.write(final_summary)
            logging.info("Reformulation finale générée avec succès.")
            # Après la génération de la reformulation finale, produire l'évaluation comparative
            if final_summary:
                comparison_prompt = generate_comparison_prompt(main_question_response, final_summary)
                comparison_evaluation = get_response_with_retries(comparison_prompt)
                st.write("### Évaluation comparative de la qualité")
                st.write(comparison_evaluation)

        except Exception as e:
            st.error("La reformulation finale n'a pas pu être générée.")
            logging.error(f"Erreur lors de la génération de la reformulation finale : {e}")
