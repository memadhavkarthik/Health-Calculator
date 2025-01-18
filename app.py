from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_body_fat(weight, waist, wrist=None, hip=None, forearm=None):
    # Using the US Navy Body Fat Formula for calculation
    # For simplicity, we will assume the user is male
    body_fat = 495 / (1.0324 - 0.19077 * (waist / 2.54) + 0.15456 * (weight / 0.453592)) - 450
    return round(body_fat, 2)

def convert_weight(weight, unit):
    if unit == 'kg_to_lbs':
        return round(weight * 2.20462, 2)
    elif unit == 'lbs_to_kg':
        return round(weight / 2.20462, 2)
    return weight

def convert_height(height, unit):
    if unit == 'feet_to_cm':
        return round(height * 30.48, 2)
    elif unit == 'cm_to_feet':
        return round(height / 30.48, 2)
    return height

def calculate_maintenance_calories(weight, height, age, gender, activity_level):
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    if activity_level == 'sedentary':
        maintenance_calories = bmr * 1.2
    elif activity_level == 'lightly_active':
        maintenance_calories = bmr * 1.375
    elif activity_level == 'moderately_active':
        maintenance_calories = bmr * 1.55
    elif activity_level == 'very_active':
        maintenance_calories = bmr * 1.725
    else:
        maintenance_calories = bmr * 1.9
    
    return round(maintenance_calories, 2)

def calculate_protein_intake(weight, body_fat):
    lean_body_mass = weight * (1 - body_fat / 100)
    protein_intake = lean_body_mass * 2.2 # Recommended protein intake is 2.2 grams per kg of lean body mass
    return round(protein_intake, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    body_fat = None
    converted_weight = None
    maintenance_calories = None
    protein_intake = None
    
    if request.method == 'POST':
        if 'calculate_body_fat' in request.form:
            weight = float(request.form['weight'])
            waist = float(request.form['waist'])
            wrist = request.form.get('wrist')
            hip = request.form.get('hip')
            forearm = request.form.get('forearm')
            
            body_fat = calculate_body_fat(weight, waist, wrist, hip, forearm)
            protein_intake = calculate_protein_intake(weight, body_fat)
        
        if 'convert_weight' in request.form:
            weight = float(request.form['weight_convert'])
            unit = request.form['unit']
            converted_weight = convert_weight(weight, unit)
        
        if 'calculate_maintenance_calories' in request.form:
            weight = float(request.form['weight_mc'])
            height = float(request.form['height_mc'])
            height_unit = request.form['height_unit_mc']
            age = int(request.form['age_mc'])
            gender = request.form['gender_mc']
            activity_level = request.form['activity_level_mc']
            
            # Convert height to cm if input is in feet
            if height_unit == 'feet':
                height = convert_height(height, 'feet_to_cm')
            
            maintenance_calories = calculate_maintenance_calories(weight, height, age, gender, activity_level)
    
    return render_template('index.html', body_fat=body_fat, converted_weight=converted_weight,
                           maintenance_calories=maintenance_calories, protein_intake=protein_intake)

@app.route('/convert', methods=['POST'])
def convert():
    converted_weight = None
    if request.method == 'POST':
        weight = float(request.form['weight_convert'])
        unit = request.form['unit']
        converted_weight = convert_weight(weight, unit)
    
    return render_template('index.html', converted_weight=converted_weight)

if __name__ == '__main__':
    app.run(debug=True)