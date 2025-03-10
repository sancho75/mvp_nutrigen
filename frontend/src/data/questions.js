const questions = [
    {
        id: 1,
        text: "Quel est ton poids et ta taille ?",
        type: "numeric",
        placeholder: "Exemple : 70kg, 175cm",
        name: "weightHeight",
    },
    {
        id: 2,
        text: "Quel est ton niveau d’activité physique ?",
        type: "multiple-choice",
        options: ["Sédentaire", "Modéré", "Actif", "Athlète"],
        name: "activityLevel",
    },
    {
        id: 3,
        text: "Quelles sont tes préférences alimentaires ?",
        type: "multiple-choice",
        options: ["Omnivore", "Végétarien", "Vegan"],
        name: "dietPreference",
    },
    {
        id: 4,
        text: "Es-tu un lève-tôt ou un couche-tard ?",
        type: "multiple-choice",
        options: ["Matinier", "Nocturne", "Neutre"],
        name: "sleepPattern",
    },
    {
        id: 5,
        text: "Quel est ton objectif principal ?",
        type: "multiple-choice",
        options: ["Perdre du poids", "Maintenir", "Augmenter la masse", "Performance sportive"],
        name: "goal",
    },
];

export default questions;
