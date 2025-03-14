import streamlit as st
import pandas as pd
import os

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
    if livello_attivita == "Sedentario":
        return "Basso fabbisogno calorico aggiuntivo"
    elif livello_attivita == "Attivo":
        return "Medio fabbisogno calorico aggiuntivo"
    else:  # Atleta
        return "Alto fabbisogno calorico aggiuntivo"

def consigli_alimentari(preferenze):
    """
    Suggerisce alimenti in base alle preferenze alimentari.
    """
    if preferenze == "Onnivoro":
        return "Puoi includere fonti proteiche animali e vegetali, frutta e verdura di stagione."
    elif preferenze == "Vegetariano":
        return (
            "Concentrati su legumi, uova, latticini (se consentiti), frutta e verdura. "
            "Attenzione al fabbisogno di proteine e ferro."
        )
    else:  # Vegano
        return (
            "Focalizzati su legumi, cereali integrali, frutta secca e semi. "
            "Monitora l'apporto di vitamina B12, ferro e calcio."
        )

def consigli_orari_pasti(cronotipo):
    """
    Consigli su orari dei pasti in base al cronotipo.
    """
    if cronotipo == "Notturno":
        return (
            "Potresti preferire colazioni più tardive e cene più vicine all'orario di riposo. "
            "Mantieni regolari gli spuntini per non sregolare il metabolismo."
        )
    else:  # Mattiniero
        return (
            "Sfrutta la mattina per una colazione abbondante e pianifica cene più leggere. "
            "Attenzione a non saltare i pasti se ti alzi molto presto."
        )

def consigli_obiettivo(obiettivo):
    """
    Personalizza consigli in base all'obiettivo.
    """
    if obiettivo == "Perdere peso":
        return (
            "Riduci gradualmente l’apporto calorico e aumenta l’attività fisica. "
            "Focalizzati su cibi nutrienti e riduci zuccheri e grassi saturi."
        )
    elif obiettivo == "Mantenere il peso":
        return (
            "Mantieni un apporto calorico bilanciato, in linea con il tuo fabbisogno. "
            "Continua con un esercizio fisico regolare."
        )
    else:  # Performance sportiva
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

def main():
    st.title("Sondaggio Nutrizionale - MVP")

    # 1) Peso e altezza
    st.subheader("1) Qual è il tuo peso e altezza?")
    peso = st.number_input("Inserisci il tuo peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
    altezza = st.number_input("Inserisci la tua altezza (cm)", min_value=50.0, max_value=250.0, value=175.0, step=0.5)

    # 2) Livello di attività fisica
    st.subheader("2) Qual è il tuo livello di attività fisica?")
    livello_attivita = st.selectbox(
        "Scegli il tuo livello",
        ("Sedentario", "Attivo", "Atleta")
    )

    # 3) Preferenze alimentari
    st.subheader("3) Quali sono le tue preferenze alimentari?")
    preferenze = st.selectbox(
        "Scegli le tue preferenze",
        ("Onnivoro", "Vegetariano", "Vegano")
    )

    # 4) Cronotipo
    st.subheader("4) Sei un tipo notturno o mattiniero?")
    cronotipo = st.selectbox(
        "Scegli il tuo cronotipo",
        ("Notturno", "Mattiniero")
    )

    # 5) Obiettivo
    st.subheader("5) Qual è il tuo obiettivo?")
    obiettivo = st.selectbox(
        "Scegli il tuo obiettivo",
        ("Perdere peso", "Mantenere il peso", "Performance sportiva")
    )

    if st.button("Invia e Ottieni Consigli"):
        # Creiamo un dizionario con tutte le risposte
        risposte_utente = {
            "Peso (kg)": peso,
            "Altezza (cm)": altezza,
            "LivelloAttività": livello_attivita,
            "PreferenzeAlimentari": preferenze,
            "Cronotipo": cronotipo,
            "Obiettivo": obiettivo
        }

        # Salviamo le risposte in CSV
        salva_risposte_in_csv(risposte_utente)

        # Calcolo BMI
        bmi = calcola_bmi(peso, altezza)
        st.write(f"**Il tuo BMI è:** {bmi if bmi else 'Valore non calcolabile'}")

        # Consigli su macro
        st.write("**Consigli sui macronutrienti:**")
        st.write(consigli_macronutrienti(bmi))

        # Consigli su fabbisogno calorico
        st.write("**Fabbisogno calorico aggiuntivo:**")
        st.write(fabbisogno_calorico_base(livello_attivita))

        # Consigli alimentari
        st.write("**Consigli alimentari in base alle preferenze:**")
        st.write(consigli_alimentari(preferenze))

        # Consigli orari pasti
        st.write("**Consigli su orario dei pasti:**")
        st.write(consigli_orari_pasti(cronotipo))

        # Consigli in base all'obiettivo
        st.write("**Consigli in base al tuo obiettivo:**")
        st.write(consigli_obiettivo(obiettivo))

if __name__ == "__main__":
    main()
