import React, { useState } from "react";
import questions from "../data/questions";
import axios from "axios";

const SurveyForm = () => {
    const [responses, setResponses] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setResponses({ ...responses, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:5000/api/survey", responses);
            console.log("Données envoyées :", response.data);
        } catch (error) {
            console.error("Erreur lors de l'envoi", error);
        }
    };

    return (
        <div className="container mt-5">
            <h2>Sondage Nutritionnel</h2>
            <form onSubmit={handleSubmit}>
                {questions.map((question) => (
                    <div key={question.id} className="mb-3">
                        <label>{question.text}</label>
                        {question.type === "numeric" ? (
                            <input
                                type="text"
                                name={question.name}
                                placeholder={question.placeholder}
                                className="form-control"
                                onChange={handleChange}
                            />
                        ) : (
                            <select name={question.name} className="form-select" onChange={handleChange}>
                                <option value="">Sélectionne une option</option>
                                {question.options.map((option, index) => (
                                    <option key={index} value={option}>{option}</option>
                                ))}
                            </select>
                        )}
                    </div>
                ))}
                <button type="submit" className="btn btn-primary">Envoyer</button>
            </form>
        </div>
    );
};

export default SurveyForm;
