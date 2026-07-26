from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load model, preprocessor, and label encoder
model = joblib.load("models/gradient_boosting_classifier.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


# Risk level mapping
risk_mapping = {
    "A": "Low",
    "B": "Moderate",
    "C": "Moderate",
    "D": "High",
    "E": "High",
    "F": "Critical",
    "G": "Moderate",
    "H": "High"
}


# Recommendations
recommendations = {
    "Low": [
        "Maintain a healthy lifestyle.",
        "Continue regular physical activity.",
        "Practice mindfulness regularly."
    ],
    "Moderate": [
        "Monitor your mental well-being.",
        "Talk with friends or family.",
        "Maintain a healthy sleep schedule."
    ],
    "High": [
        "Consider speaking with a counselor.",
        "Reduce academic stress where possible.",
        "Practice relaxation techniques daily."
    ],
    "Critical": [
        "Seek professional mental health support immediately.",
        "Inform a trusted family member or mentor.",
        "Do not ignore persistent symptoms."
    ]
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    gender = request.form["gender"]
    ghq = float(request.form["ghq"])
    depression = float(request.form["depression"])
    anxiety = float(request.form["anxiety"])
    stress = float(request.form["stress"])
    brs = float(request.form["brs"])

    input_data = pd.DataFrame({
        "Gender": [gender],
        "GHQ": [ghq],
        "Depression": [depression],
        "Anxiety": [anxiety],
        "Stress": [stress],
        "BRS": [brs]
    })

    processed = preprocessor.transform(input_data)

    prediction = model.predict(processed)

    cluster = label_encoder.inverse_transform(prediction)[0]

    confidence = model.predict_proba(processed).max() * 100

    risk = risk_mapping.get(cluster, "Unknown")

    return render_template(
        "result.html",
        cluster=cluster,
        risk=risk,
        confidence=round(confidence, 2),
        recommendations=recommendations[risk]
    )


if __name__ == "__main__":
    app.run(debug=True)