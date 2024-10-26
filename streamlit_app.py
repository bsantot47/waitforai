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

# Étape 1 : Saisie de la question principale
st.write(f"### {translations[selected_language]['enter_question']}")
question = st.text_input("", placeholder="Comment vendre des bijoux sur internet ?")

if question:
    with st.spinner('🧠 Génération de la réponse initiale...'):
        # Générer la réponse initiale avec l'API Hugging Face en utilisant la question entrée par l'utilisateur
        prompt_principal = f"""
        Question principale :
        "{question}"
        Réponds à cette question principale avec une réponse détaillée et longue. Explique chaque aspect en profondeur.
        Ensuite, génère deux sous-questions (nommées 1.1 et 1.2) qui approfondissent des aspects spécifiques de la question principale, puis réponds à chacune des deux sous-questions.
        Pour chaque sous-question de niveau 1 (1.1 et 1.2), génère deux nouvelles sous-questions (nommées 1.1.1, 1.1.2, 1.2.1, et 1.2.2) qui explorent davantage les réponses, mais **ne génère pas de sous-questions supplémentaires** au-delà de celles-ci. Limite-toi uniquement à ces sous-questions.
        Format attendu :
        Question principale : [Question principale]
        Réponse : [Réponse principale]
        Sous-questions de Niveau 1 :
        1.1 [Première sous-question]
        Réponse : [Réponse à la sous-question 1.1]
        Sous-questions de Niveau 2 :
        1.1.1 [Sous-question dérivée de 1.1]
        Réponse : [Réponse à la sous-question 1.1.1]
        1.1.2 [Sous-question dérivée de 1.1]
        Réponse : [Réponse à la sous-question 1.1.2]
        1.2 [Deuxième sous-question]
        Réponse : [Réponse à la sous-question 1.2]
        Sous-questions de Niveau 2 :
        1.2.1 [Sous-question dérivée de 1.2]
        Réponse : [Réponse à la sous-question 1.2.1]
        1.2.2 [Sous-question dérivée de 1.2]
        Réponse : [Réponse à la sous-question 1.2.2]
        
        stop toi a ce nombre de sous questions
        """
        logging.debug(f"Prompt généré : {prompt_principal}")

        # Demande de réponse à l'API sans streaming
        response = client.chat_completion(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": prompt_principal}],
            max_tokens=6000
        )

        # Vérifier si la réponse est vide
        if not response:
            st.error("❌ Aucune réponse n'a été reçue de l'API.")
        else:
            # Extraire la réponse textuelle
            generated_response = response['choices'][0]['message']['content']
            st.write("### " + translations[selected_language]['initial_response'])
            st.write(f"**{translations[selected_language]['main_question']}** {question}")
            main_question_response = generated_response.split('Sous-questions de Niveau 1 :')[0].strip()
            st.write(f"**{translations[selected_language]['response']}** {main_question_response}")

            # Champ pour la réponse de l'utilisateur à la question principale
            st.subheader("💡 " + translations[selected_language]['your_response'])
            user_main_response = st.text_area(f"{translations[selected_language]['your_response']} {question}", placeholder="Entrez votre réponse ici...")

            # EXTRACTION des sous-questions générées dynamiquement à partir de la réponse de l'IA
            sous_questions = re.findall(r'(\d+\.\d+(?:\.\d+)? [^\n]+)', generated_response)
            ia_responses = re.findall(r'Réponse : ([^\n]+)', generated_response)  # Extraire les réponses IA après "Réponse :"

            # Vérifier que le nombre de sous-questions correspond au nombre de réponses IA
            if len(sous_questions) != len(ia_responses):
                st.warning(f"⚠️ Nombre de sous-questions ({len(sous_questions)}) ne correspond pas au nombre de réponses IA ({len(ia_responses)}).")

            # Vérifier si des sous-questions sont bien extraites
            if sous_questions:
                st.write("### " + translations[selected_language]['sub_questions_1'])
                for sq in sous_questions:
                    st.write(f"📌 {sq}")
            else:
                st.error("❌ Aucune sous-question n'a été extraite.")

            # Créer un formulaire pour que l'utilisateur puisse entrer ses réponses aux mêmes sous-questions
            st.subheader("💡 Vos réponses aux questions générées par l'IA")

            user_responses = {}
            response_sources = {}

            for idx, question in enumerate(sous_questions):
                question_id, question_text = question.split(' ', 1)

                # Carte pour chaque question
                with st.expander(f"**{question_id} : {question_text.strip()}**", expanded=True):
                    # Afficher la réponse de l'IA uniquement si elle existe
                    if idx < len(ia_responses):
                        st.write(f"**{translations[selected_language]['response']}** {ia_responses[idx]}")
                    else:
                        st.write(f"**{translations[selected_language]['response']}** Aucune réponse disponible.")

                    # Champ pour la réponse de l'utilisateur avec une clé unique
                    user_responses[question_id] = st.text_area(f"Votre réponse pour {question_id}", placeholder="Entrez votre réponse ici...", key=f"user_response_{question_id}")

                    # Niveau 1 : Choisir la catégorie générale
                    response_type = st.selectbox(f"Type d'origine de la réponse pour {question_id}",
                                                 ["Réponse personnelle", "IA", "Forum", "Réseaux sociaux",
                                                  "Vidéos en ligne", "Wikipedia", "Livre",
                                                  "Article scientifique", "Autre"],
                                                 key=f"type_{question_id}")

                    # Niveau 2 : Sous-choix en fonction du type sélectionné
                    if response_type == "Réponse personnelle":
                        origin_details = "Réponse fournie personnellement par l'utilisateur."

                    elif response_type == "IA":
                        ia_name = st.selectbox(f"Nom de l'IA pour {question_id}",
                                               ["ChatGPT", "Mistral", "Anthropic", "Bard", "Autre"],
                                               key=f"ia_{question_id}")
                        if ia_name == "Autre":
                            ia_name = st.text_input(f"Précisez le nom de l'IA pour {question_id}", key=f"ia_custom_{question_id}")

                        ia_model = st.selectbox(f"Modèle de l'IA pour {question_id}",
                                                ["GPT-3.5", "GPT-4", "Mistral-7B", "Claude 2", "Autre"],
                                                key=f"model_{question_id}")
                        if ia_model == "Autre":
                            ia_model = st.text_input(f"Précisez le modèle de l'IA pour {question_id}", key=f"model_custom_{question_id}")
                        origin_details = f"{ia_name}, modèle {ia_model}"

                    elif response_type == "Forum":
                        forum_name = st.selectbox(f"Nom du forum pour {question_id}",
                                                  ["Reddit", "Quora", "Stack Overflow", "Autre"],
                                                  key=f"forum_{question_id}")
                        if forum_name == "Autre":
                            forum_name = st.text_input(f"Précisez le nom du forum pour {question_id}", key=f"forum_custom_{question_id}")
                        forum_link = st.text_input(f"Lien vers la discussion du forum pour {question_id}", key=f"forum_link_{question_id}")
                        origin_details = f"Forum : {forum_name}, Lien : {forum_link}"

                    elif response_type == "Réseaux sociaux":
                        social_media = st.selectbox(f"Plateforme de réseaux sociaux pour {question_id}",
                                                    ["Twitter/X", "Facebook", "LinkedIn", "Instagram", "Autre"],
                                                    key=f"social_{question_id}")
                        if social_media == "Autre":
                            social_media = st.text_input(f"Précisez la plateforme pour {question_id}", key=f"social_custom_{question_id}")
                        social_link = st.text_input(f"Lien vers le post pour {question_id}", key=f"social_link_{question_id}")
                        origin_details = f"Réseau social : {social_media}, Lien : {social_link}"

                    elif response_type == "Vidéos en ligne":
                        video_platform = st.selectbox(f"Plateforme vidéo pour {question_id}",
                                                      ["YouTube", "Vimeo", "TikTok", "Autre"],
                                                      key=f"video_{question_id}")
                        if video_platform == "Autre":
                            video_platform = st.text_input(f"Précisez la plateforme vidéo pour {question_id}", key=f"video_custom_{question_id}")
                        video_link = st.text_input(f"Lien vers la vidéo pour {question_id}", key=f"video_link_{question_id}")
                        origin_details = f"Vidéo : {video_platform}, Lien : {video_link}"

                    elif response_type == "Wikipedia":
                        wiki_link = st.text_input(f"Lien vers l'article Wikipedia pour {question_id}", key=f"wiki_link_{question_id}")
                        origin_details = f"Wikipedia : {wiki_link}"

                    elif response_type == "Livre":
                        book_title = st.text_input(f"Titre du livre pour {question_id}", key=f"book_{question_id}")
                        book_author = st.text_input(f"Auteur du livre pour {question_id}", key=f"author_{question_id}")
                        origin_details = f"Livre : {book_title}, Auteur : {book_author}"

                    elif response_type == "Article scientifique":
                        article_title = st.text_input(f"Titre de l'article pour {question_id}", key=f"article_{question_id}")
                        journal_name = st.text_input(f"Nom du journal ou de la publication pour {question_id}", key=f"journal_{question_id}")
                        article_link = st.text_input(f"Lien ou DOI pour {question_id}", key=f"article_link_{question_id}")
                        origin_details = f"Article : {article_title}, Journal : {journal_name}, Lien/DOI : {article_link}"

                    else:  # Autre
                        origin_details = st.text_input(f"Précisez l'origine de la réponse pour {question_id}", key=f"other_{question_id}")

                    # Sauvegarder l'origine et les détails
                    response_sources[question_id] = {"type": response_type, "details": origin_details}

            # Si l'utilisateur a fourni des réponses, les afficher avec leur origine
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

    # Étape 4 : Reformulation finale
    if st.button(translations[selected_language]['generate_final_summary']):
        with st.spinner('📝 Génération de la reformulation finale...'):
            reformulation_prompt = f"Question principale : \"{question}\"\n\nRéponse initiale :\n{main_question_response}\n\n"
            reformulation_prompt += "Voici la réponse initiale à la question principale :\n"
            reformulation_prompt += f"{main_question_response}\n\n"
            reformulation_prompt += "Analyse des sous-questions et des réponses IA et utilisateur :\n\n"

            # Boucle sur les sous-questions et leurs réponses IA/utilisateur
            for question_id, ia_response in zip(sous_questions, ia_responses):
                user_response = user_responses.get(question_id, "Pas de réponse utilisateur")
                reformulation_prompt += f"Sous-question : {question_id}\n"
                reformulation_prompt += f"Réponse IA : {ia_response}\n"
                reformulation_prompt += f"Réponse utilisateur : {user_response}\n\n"

            # Ajout d'un rappel explicite pour reformuler la réponse principale en détail
            reformulation_prompt += (
                "\nReformule la réponse à la **question principale** en prenant en compte "
                "les informations des sous-questions et des réponses utilisateur et IA. "
                "La reformulation doit être longue, détaillée et répondre spécifiquement "
                "à la question principale tout en intégrant des informations pertinentes des "
                "sous-questions. Assure-toi que toutes les réponses des sous-questions "
                "soient utilisées pour enrichir la réponse."
            )

            logging.debug(f"Prompt pour reformulation finale : {reformulation_prompt}")

            reformulation_response = client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.3",
                messages=[{"role": "user", "content": reformulation_prompt}],
                max_tokens=6000
            )

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
                st.write("La reformulation a pris en compte les réponses IA et utilisateur pour chaque sous-question. Voici un résumé des éléments ajoutés ou modifiés :")

                for question_id, response in zip(sous_questions, ia_responses):
                    user_response = user_responses.get(question_id, "")
                    st.write(f"- **{question_id}** : Réponse IA : {response}, Réponse utilisateur : {user_response}")

            else:
                st.error("❌ Aucune reformulation finale n'a été reçue de l'API après plusieurs tentatives.")
