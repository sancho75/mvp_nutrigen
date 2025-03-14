import streamlit as st
import pandas as pd
import os

#########################
#  Dictionnaires de texte
#########################
translations = {
    "it": {
        "app_title": "Sondaggio Nutrizionale - MVP",
        "question1": "1) Qual è il tuo peso e altezza?",
        "question2": "2) Qual è il tuo livello di attività fisica?",
        "question3": "3) Quali sono le tue preferenze alimentari?",
        "question4": "4) Sei un tipo notturno o mattiniero?",
        "question5": "5) Qual è il tuo obiettivo?",
        "submit_button": "Invia e Ottieni Consigli",
        "bmi_label": "Il tuo BMI è:",
        "macro_advice": "**Consigli sui macronutrienti:**",
        "calorie_advice": "**Fabbisogno calorico aggiuntivo:**",
        "diet_advice": "**Consigli alimentari in base alle preferenze:**",
        "meal_advice": "**Consigli su orario dei pasti:**",
        "goal_advice": "**Consigli in base al tuo obiettivo:**",
        # Nouvelles chaînes pour le feedback
        "feedback_question": "Hai qualche altro suggerimento o richiesta?",
        "feedback_button": "Invia feedback e salva",
        "feedback_thanks": "Grazie per il tuo feedback!"
    },
    "en": {
        "app_title": "Nutritional Survey - MVP",
        "question1": "1) What is your weight and height?",
        "question2": "2) What is your physical activity level?",
        "question3": "3) What are your dietary preferences?",
        "question4": "4) Are you a night owl or a morning person?",
        "question5": "5) What is your goal?",
        "submit_button": "Submit and Get Advice",
        "bmi_label": "Your BMI is:",
        "macro_advice": "**Macronutrient Advice:**",
        "calorie_advice": "**Additional Caloric Needs:**",
        "diet_advice": "**Nutritional Advice Based on Preferences:**",
        "meal_advice": "**Meal Timing Advice:**",
        "goal_advice": "**Advice Based on Your Goal:**",
        # Feedback
        "feedback_question": "Any other suggestions or requests?",
        "feedback_button": "Send feedback and save",
        "feedback_thanks": "Thank you for your feedback!"
    },
    "fr": {
        "app_title": "Sondage Nutritionnel - MVP",
        "question1": "1) Quel est votre poids et votre taille ?",
        "question2": "2) Quel est votre niveau d'activité physique ?",
        "question3": "3) Quelles sont vos préférences alimentaires ?",
        "question4": "4) Êtes-vous un couche-tard ou un lève-tôt ?",
        "question5": "5) Quel est votre objectif ?",
        "submit_button": "Envoyer et Obtenir des Conseils",
        "bmi_label": "Votre IMC est :",
        "macro_advice": "**Conseils sur les macronutriments :**",
        "calorie_advice": "**Besoin calorique supplémentaire :**",
        "diet_advice": "**Conseils alimentaires selon vos préférences :**",
        "meal_advice": "**Conseils sur l'horaire des repas :**",
        "goal_advice": "**Conseils basés sur votre objectif :**",
        # Feedback
        "feedback_question": "Avez-vous d'autres suggestions ou demandes ?",
        "feedback_button": "Envoyer le feedback et sauvegarder",
        "feedback_thanks": "Merci pour votre feedback !"
    },
}

activity_options = {
    "it": ["Sedentario", "Attivo", "Atleta"],
    "en": ["Sedentary", "Active", "Athlete"],
    "fr": ["Sédentaire", "Actif", "Athlète"],
}

diet_options = {
    "it": ["Onnivoro", "Vegetariano", "Vegano"],
    "en": ["Omnivore", "Vegetarian", "Vegan"],
    "fr": ["Omnivore", "Végétarien", "Vegan"],
}

sleep_options = {
    "it": ["Notturno", "Mattiniero"],
    "en": ["Night owl", "Morning person"],
    "fr": ["Couche-tard", "Lève-tôt"],
}

goal_options = {
    "it": ["Perdere peso", "Mantenere il peso", "Performance sportiva"],
    "en": ["Lose weight", "Maintain weight", "Sports performance"],
    "fr": ["Perdre du poids", "Maintenir le poids", "Performance sportive"],
}


#########################
#     Funzioni esistenti
#########################
def calcola_bmi(peso, altezza):
    """
    Calcolo del BMI:
    BMI = peso (kg) / [altezza (m)]^2
    """
    try:
        altezza_m = altezza / 100  # convertiamo cm in metri
        bmi = peso / (altezza_m ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return None

def consigli_macronutrienti(bmi):
    """
    Fornisce un consiglio di base sui macronutrienti in base al BMI.
    Nota: Logica semplificata, personalizzabile.
    """
    if bmi is None:
        return "Non è stato possibile calcolare il BMI."
    if bmi < 18.5:
        return (
            "Sei sotto il peso forma. Aumenta l'apporto calorico "
            "con una quota maggiore di carboidrati complessi e proteine."
        )
    elif 18.5 <= bmi < 25:
        return (
            "Hai un BMI normale. Mantieni un equilibrio tra carboidrati, proteine e grassi. "
            "Assumi carboidrati complessi, proteine magre e grassi sani."
        )
    elif 25 <= bmi < 30:
        return (
            "Sei in sovrappeso. Riduci i carboidrati raffinati e aumenta l'assunzione "
            "di proteine e grassi sani. Focalizzati su porzioni moderate."
        )
    else:
        return (
            "Sei in una fascia di obesità. Riduci i carboidrati semplici e incrementa "
            "l'apporto di proteine di qualità e grassi insaturi. Consulta uno specialista."
        )

def fabbisogno_calorico_base(livello_attivita):
    """
    Esempio di calcolo (semplificato) del fabbisogno calorico aggiuntivo
    in base al livello di attività fisica.
    """
    if livello_attivita in ["Sedentario", "Sédentaire", "Sedentary"]:
        return "Basso fabbisogno calorico aggiuntivo"
    elif livello_attivita in ["Attivo", "Actif", "Active"]:
        return "Medio fabbisogno calorico aggiuntivo"
    else:  # "Atleta", "Athlète", "Athlete"
        return "Alto fabbisogno calorico aggiuntivo"

def consigli_alimentari(preferenze):
    """
    Suggerisce alimenti in base alle preferenze alimentari.
    """
    if preferenze in ["Onnivoro", "Omnivore"]:
        return "Puoi includere fonti proteiche animali e vegetali, frutta e verdura di stagione."
    elif preferenze in ["Vegetariano", "Végétarien", "Vegetarian"]:
        return (
            "Concentrati su legumi, uova, latticini (se consentiti), frutta e verdura. "
            "Attenzione al fabbisogno di proteine e ferro."
        )
    else:  # "Vegano", "Vegan"
        return (
            "Focalizzati su legumi, cereali integrali, frutta secca e semi. "
            "Monitora l'apporto di vitamina B12, ferro e calcio."
        )

def consigli_orari_pasti(cronotipo):
    """
    Consigli su orari dei pasti in base al cronotipo.
    """
    if cronotipo in ["Notturno", "Night owl", "Couche-tard"]:
        return (
            "Potresti preferire colazioni più tardive e cene più vicine all'orario di riposo. "
            "Mantieni regolari gli spuntini per non sregolare il metabolismo."
        )
    else:  # "Mattiniero", "Morning person", "Lève-tôt"
        return (
            "Sfrutta la mattina per una colazione abbondante e pianifica cene più leggere. "
            "Attenzione a non saltare i pasti se ti alzi molto presto."
        )

def consigli_obiettivo(obiettivo):
    """
    Personalizza consigli in base all'obiettivo.
    """
    if obiettivo in ["Perdere peso", "Lose weight", "Perdre du poids"]:
        return (
            "Riduci gradualmente l’apporto calorico e aumenta l’attività fisica. "
            "Focalizzati su cibi nutrienti e riduci zuccheri e grassi saturi."
        )
    elif obiettivo in ["Mantenere il peso", "Maintain weight", "Maintenir le poids"]:
        return (
            "Mantieni un apporto calorico bilanciato, in linea con il tuo fabbisogno. "
            "Continua con un esercizio fisico regolare."
        )
    else:  # "Performance sportiva", "Sports performance", "Performance sportive"
        return (
            "Assicurati un apporto adeguato di proteine e carboidrati di qualità. "
            "Considera l’integrazione e un piano di allenamento specifico."
        )

def salva_risposte_in_csv(risposte):
    """
    Salva le risposte in un file CSV.
    Se il file non esiste, scrive l'header. Altrimenti, fa append senza header.
    """
    df = pd.DataFrame([risposte])
    csv_file = "risultati_sondaggio.csv"

    # Se il file non esiste, crealo e scrivi l'header
    if not os.path.exists(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        df.to_csv(csv_file, mode='a', header=False, index=False)

#########################
#       Main App
#########################
def main():
    # Pour mémoriser les réponses (et le feedback) entre deux clics
    if "risposte_utente" not in st.session_state:
        st.session_state["risposte_utente"] = None
    if "show_suggestions" not in st.session_state:
        st.session_state["show_suggestions"] = False

    # Sélecteur de langue
    language_choice = st.sidebar.selectbox(
        "Seleziona la lingua / Select language / Choisissez la langue:",
        ("Italiano", "English", "Français")
    )
    # Déterminer la clé de langue
    if language_choice == "Italiano":
        lang = "it"
    elif language_choice == "English":
        lang = "en"
    else:
        lang = "fr"

    # Titre principal
    st.title(translations[lang]["app_title"])

    # 1) Peso e altezza
    st.subheader(translations[lang]["question1"])
    peso = st.number_input("Inserisci il tuo peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
    altezza = st.number_input("Inserisci la tua altezza (cm)", min_value=50.0, max_value=250.0, value=175.0, step=0.5)

    # 2) Livello di attività fisica
    st.subheader(translations[lang]["question2"])
    livello_attivita = st.selectbox("", activity_options[lang])

    # 3) Preferenze alimentari
    st.subheader(translations[lang]["question3"])
    preferenze = st.selectbox("", diet_options[lang])

    # 4) Cronotipo
    st.subheader(translations[lang]["question4"])
    cronotipo = st.selectbox("", sleep_options[lang])

    # 5) Obiettivo
    st.subheader(translations[lang]["question5"])
    obiettivo = st.selectbox("", goal_options[lang])

    # Bouton principal (affiche les conseils, sans enregistrer tout de suite)
    if st.button(translations[lang]["submit_button"]):
        # On stocke les réponses dans la session (pas encore dans le CSV)
        st.session_state["risposte_utente"] = {
            "Lingua": language_choice,
            "Peso (kg)": peso,
            "Altezza (cm)": altezza,
            "LivelloAttività": livello_attivita,
            "PreferenzeAlimentari": preferenze,
            "Cronotipo": cronotipo,
            "Obiettivo": obiettivo
        }
        # Activer l'affichage des suggestions
        st.session_state["show_suggestions"] = True

    # Si on doit afficher les suggestions (après avoir cliqué sur le premier bouton)
    if st.session_state["show_suggestions"] and st.session_state["risposte_utente"] is not None:
        risposte_utente = st.session_state["risposte_utente"]

        # Calcolo BMI
        bmi = calcola_bmi(risposte_utente["Peso (kg)"], risposte_utente["Altezza (cm)"])
        st.write(f"{translations[lang]['bmi_label']} {bmi if bmi else 'Valore non calcolabile'}")

        # Consigli su macro
        st.write(translations[lang]["macro_advice"])
        st.write(consigli_macronutrienti(bmi))

        # Consigli su fabbisogno calorico
        st.write(translations[lang]["calorie_advice"])
        st.write(fabbisogno_calorico_base(risposte_utente["LivelloAttività"]))

        # Consigli alimentari
        st.write(translations[lang]["diet_advice"])
        st.write(consigli_alimentari(risposte_utente["PreferenzeAlimentari"]))

        # Consigli orari pasti
        st.write(translations[lang]["meal_advice"])
        st.write(consigli_orari_pasti(risposte_utente["Cronotipo"]))

        # Consigli in base all'obiettivo
        st.write(translations[lang]["goal_advice"])
        st.write(consigli_obiettivo(risposte_utente["Obiettivo"]))

        # Nouvelle zone de texte pour feedback
        st.subheader(translations[lang]["feedback_question"])
        feedback = st.text_area("", placeholder="Scrivi qui il tuo feedback...")

        # Bouton pour tout enregistrer
        if st.button(translations[lang]["feedback_button"]):
            # Ajouter le feedback aux réponses
            risposte_utente["Feedback"] = feedback
            # Enregistrer dans le CSV
            salva_risposte_in_csv(risposte_utente)

            st.success(translations[lang]["feedback_thanks"])
            # On peut réinitialiser show_suggestions si on veut
            st.session_state["show_suggestions"] = False


if __name__ == "__main__":
    main()
