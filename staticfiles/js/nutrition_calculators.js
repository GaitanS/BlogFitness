/**
 * Nutrition Calculators JavaScript
 * Implementează calculatoarele de nutriție conform formulelor din Excel
 */

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const validateForm = function(formId) {
        const form = document.getElementById(formId);
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
        return form.checkValidity();
    };

    // ======= CALCULATOR NUTRIȚIE UNIFICAT =======
    
    const nutritionForm = document.getElementById('nutritionForm');
    const nutritionResult = document.getElementById('nutritionResult');
    
    if (nutritionForm) {
        nutritionForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (validateForm('nutritionForm')) {
                const gender = document.getElementById('nutrition-gender').value;
                const goal = document.getElementById('nutrition-goal').value;
                const weight = parseFloat(document.getElementById('nutrition-weight').value);
                const height = parseFloat(document.getElementById('nutrition-height').value);
                const age = parseInt(document.getElementById('nutrition-age').value);
                
                // Calculează BMR în funcție de gen
                let bmr;
                if (gender === 'male') {
                    // Formula pentru bărbați: 66+(13.397*Greutate)+(4.799*Înălțime)-(5.677*Vârstă)
                    bmr = 66 + (13.397 * weight) + (4.799 * height) - (5.677 * age);
                } else {
                    // Formula pentru femei: 655.1+(9.563*Greutate)+(1.85*Înălțime)-(4.676*Vârstă)
                    bmr = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age);
                }
                
                // Calculează caloriile pentru zi fără/cu antrenament în funcție de obiectiv
                let caloriesRest, caloriesTraining;
                let proteinRestPercent, carbsRestPercent, fatRestPercent;
                let proteinTrainingPercent, carbsTrainingPercent, fatTrainingPercent;
                let noteText;
                
                switch (goal) {
                    case 'maintenance':
                        // Nutriție pentru Menținere
                        caloriesRest = Math.round(bmr * 1.1);
                        caloriesTraining = Math.round(bmr * 1.3);
                        proteinRestPercent = 0.35;
                        carbsRestPercent = 0.3;
                        fatRestPercent = 0.35;
                        proteinTrainingPercent = 0.35;
                        carbsTrainingPercent = 0.3;
                        fatTrainingPercent = 0.35;
                        noteText = "Pentru menținerea greutății, este important să menții un echilibru între aportul caloric și consumul energetic. Aceste valori sunt calculate pentru a menține greutatea actuală.";
                        break;
                    
                    case 'weight-loss':
                        // Nutriție pentru Pierderea în Greutate
                        caloriesRest = Math.round(bmr - 300);
                        
                        // Diferență în funcție de gen pentru zi cu antrenament
                        if (gender === 'male') {
                            caloriesTraining = Math.round((bmr + 350) - 500);
                        } else {
                            caloriesTraining = Math.round((bmr + 300) - 500);
                        }
                        
                        proteinRestPercent = 0.4;
                        carbsRestPercent = 0.3;
                        fatRestPercent = 0.3;
                        proteinTrainingPercent = 0.4;
                        carbsTrainingPercent = 0.3;
                        fatTrainingPercent = 0.3;
                        noteText = "Pentru pierderea în greutate, este recomandat un deficit caloric moderat și un aport crescut de proteine pentru a menține masa musculară în timpul procesului de slăbire.";
                        break;
                    
                    case 'muscle-gain':
                        // Nutriție pentru Creșterea Greutății
                        caloriesRest = Math.round(bmr * 1.3);
                        caloriesTraining = Math.round(bmr * 1.5);
                        proteinRestPercent = 0.3;
                        carbsRestPercent = 0.4;
                        fatRestPercent = 0.3;
                        proteinTrainingPercent = 0.3;
                        carbsTrainingPercent = 0.4;
                        fatTrainingPercent = 0.3;
                        noteText = "Pentru creșterea masei musculare, este necesar un surplus caloric și un aport crescut de carbohidrați pentru a susține antrenamentele intense și recuperarea musculară.";
                        break;
                }
                
                // Calculează macronutrienții pentru zi fără antrenament
                const proteinRestCalories = Math.round(caloriesRest * proteinRestPercent);
                const proteinRest = Math.round(proteinRestCalories / 4);
                const proteinRestPercentDisplay = Math.round(proteinRestPercent * 100);
                
                const carbsRestCalories = Math.round(caloriesRest * carbsRestPercent);
                const carbsRest = Math.round(carbsRestCalories / 4);
                const carbsRestPercentDisplay = Math.round(carbsRestPercent * 100);
                
                const fatRestCalories = Math.round(caloriesRest * fatRestPercent);
                const fatRest = Math.round(fatRestCalories / 9);
                const fatRestPercentDisplay = Math.round(fatRestPercent * 100);
                
                // Calculează macronutrienții pentru zi cu antrenament
                const proteinTrainingCalories = Math.round(caloriesTraining * proteinTrainingPercent);
                const proteinTraining = Math.round(proteinTrainingCalories / 4);
                const proteinTrainingPercentDisplay = Math.round(proteinTrainingPercent * 100);
                
                const carbsTrainingCalories = Math.round(caloriesTraining * carbsTrainingPercent);
                const carbsTraining = Math.round(carbsTrainingCalories / 4);
                const carbsTrainingPercentDisplay = Math.round(carbsTrainingPercent * 100);
                
                const fatTrainingCalories = Math.round(caloriesTraining * fatTrainingPercent);
                const fatTraining = Math.round(fatTrainingCalories / 9);
                const fatTrainingPercentDisplay = Math.round(fatTrainingPercent * 100);
                
                // Afișează rezultatele
                document.getElementById('nutritionBMR').textContent = Math.round(bmr);
                document.getElementById('nutritionCaloriesRest').textContent = caloriesRest;
                document.getElementById('nutritionCaloriesTraining').textContent = caloriesTraining;
                
                document.getElementById('nutritionProteinRest').textContent = proteinRest;
                document.getElementById('nutritionProteinRestPercent').textContent = proteinRestPercentDisplay;
                document.getElementById('nutritionCarbsRest').textContent = carbsRest;
                document.getElementById('nutritionCarbsRestPercent').textContent = carbsRestPercentDisplay;
                document.getElementById('nutritionFatRest').textContent = fatRest;
                document.getElementById('nutritionFatRestPercent').textContent = fatRestPercentDisplay;
                
                document.getElementById('nutritionProteinTraining').textContent = proteinTraining;
                document.getElementById('nutritionProteinTrainingPercent').textContent = proteinTrainingPercentDisplay;
                document.getElementById('nutritionCarbsTraining').textContent = carbsTraining;
                document.getElementById('nutritionCarbsTrainingPercent').textContent = carbsTrainingPercentDisplay;
                document.getElementById('nutritionFatTraining').textContent = fatTraining;
                document.getElementById('nutritionFatTrainingPercent').textContent = fatTrainingPercentDisplay;
                
                document.getElementById('nutritionNote').textContent = noteText;
                
                // Afișează rezultatele
                nutritionResult.classList.remove('d-none');
            }
        });
    }
    
    // ======= CALCULATOR BMI =======
    
    const bmiForm = document.getElementById('bmiForm');
    const bmiResult = document.getElementById('bmiResult');
    
    if (bmiForm) {
        bmiForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (validateForm('bmiForm')) {
                const gender = document.getElementById('gender').value;
                const age = parseInt(document.getElementById('age').value);
                const height = parseInt(document.getElementById('height').value) / 100; // convert to meters
                const weight = parseFloat(document.getElementById('weight').value);
                
                // Calculate BMI
                const bmi = weight / (height * height);
                
                // Calculate ideal weight (Hamwi formula)
                let idealWeight;
                if (gender === 'male') {
                    idealWeight = 48 + 2.7 * ((height * 100) - 152.4) / 2.54;
                } else {
                    idealWeight = 45.5 + 2.2 * ((height * 100) - 152.4) / 2.54;
                }
                
                // Calculate daily calories (Mifflin-St Jeor)
                let bmr;
                if (gender === 'male') {
                    bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5;
                } else {
                    bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161;
                }
                const dailyCalories = Math.round(bmr * 1.55); // moderate activity
                
                // Determine BMI category and recommendations
                let category, categoryClass, recommendation;
                
                if (bmi < 18.5) {
                    category = "Subponderal";
                    categoryClass = "bg-warning text-dark";
                    recommendation = "Rezultatele indică faptul că ai o greutate sub cea recomandată. Este important să consumi suficiente calorii și nutrienți pentru a atinge o greutate sănătoasă. Recomandăm consultarea unui nutriționist pentru un plan alimentar personalizat.";
                } else if (bmi < 25) {
                    category = "Greutate normală";
                    categoryClass = "bg-success text-white";
                    recommendation = "Felicitări! Ai o greutate în intervalul normal. Continuă să menții un stil de viață activ și o alimentație echilibrată pentru a-ți păstra sănătatea.";
                } else if (bmi < 30) {
                    category = "Supraponderal";
                    categoryClass = "bg-warning text-dark";
                    recommendation = "Rezultatele indică faptul că ai o greutate ușor peste intervalul recomandat. Recomandăm creșterea activității fizice și ajustarea dietei pentru a reduce treptat greutatea.";
                } else if (bmi < 35) {
                    category = "Obezitate (Gradul I)";
                    categoryClass = "bg-danger text-white";
                    recommendation = "Rezultatele indică obezitate de gradul I. Recomandăm consultarea unui medic și a unui nutriționist pentru un plan personalizat de scădere în greutate.";
                } else if (bmi < 40) {
                    category = "Obezitate (Gradul II)";
                    categoryClass = "bg-danger text-white";
                    recommendation = "Rezultatele indică obezitate de gradul II. Este important să consulți un medic pentru evaluare și recomandări personalizate.";
                } else {
                    category = "Obezitate (Gradul III)";
                    categoryClass = "bg-danger text-white";
                    recommendation = "Rezultatele indică obezitate de gradul III. Recomandăm consultarea urgentă a unui medic pentru evaluare și plan de tratament.";
                }
                
                // Display results
                document.getElementById('bmiValue').textContent = bmi.toFixed(1);
                document.getElementById('bmiCategoryText').textContent = category;
                document.getElementById('bmiCategory').className = `bmi-category p-2 rounded text-center mb-2 ${categoryClass}`;
                document.getElementById('idealWeight').textContent = idealWeight.toFixed(1);
                document.getElementById('dailyCalories').textContent = dailyCalories;
                document.getElementById('bmiRecommendation').textContent = recommendation;
                
                bmiResult.classList.remove('d-none');
            }
        });
    }
    
    // ======= CALCULATOR GRĂSIME CORPORALĂ =======
    
    const bodyFatForm = document.getElementById('bodyFatForm');
    const bodyFatResult = document.getElementById('bodyFatResult');
    const genderSelect = document.getElementById('bf-gender');
    const hipField = document.querySelector('.female-only');
    
    if (genderSelect) {
        genderSelect.addEventListener('change', function() {
            if (this.value === 'female') {
                hipField.classList.remove('d-none');
                document.getElementById('bf-hip').setAttribute('required', '');
            } else {
                hipField.classList.add('d-none');
                document.getElementById('bf-hip').removeAttribute('required');
            }
        });
    }
    
    if (bodyFatForm) {
        bodyFatForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (validateForm('bodyFatForm')) {
                const gender = document.getElementById('bf-gender').value;
                const height = parseInt(document.getElementById('bf-height').value);
                const weight = parseFloat(document.getElementById('bf-weight').value);
                const neck = parseFloat(document.getElementById('bf-neck').value);
                const waist = parseFloat(document.getElementById('bf-waist').value);
                
                let bodyFatPercentage;
                
                if (gender === 'male') {
                    // U.S. Navy formula for men
                    bodyFatPercentage = 495 / (1.0324 - 0.19077 * Math.log10(waist - neck) + 0.15456 * Math.log10(height)) - 450;
                } else {
                    // U.S. Navy formula for women
                    const hip = parseFloat(document.getElementById('bf-hip').value);
                    bodyFatPercentage = 495 / (1.29579 - 0.35004 * Math.log10(waist + hip - neck) + 0.22100 * Math.log10(height)) - 450;
                }
                
                // Calculate fat mass and lean mass
                const fatMass = (bodyFatPercentage / 100) * weight;
                const leanMass = weight - fatMass;
                
                // Determine body fat category and recommendations
                let category, categoryClass, recommendation;
                
                if (gender === 'male') {
                    if (bodyFatPercentage < 6) {
                        category = "Esențial";
                        categoryClass = "bg-info text-white";
                        recommendation = "Ai un nivel foarte scăzut de grăsime corporală, specific atleților de performanță. Acest nivel poate fi dificil de menținut pe termen lung și poate afecta funcțiile hormonale. Asigură-te că urmezi un plan nutrițional adecvat.";
                    } else if (bodyFatPercentage < 14) {
                        category = "Atletic";
                        categoryClass = "bg-success text-white";
                        recommendation = "Ai un nivel atletic de grăsime corporală. Acest nivel este excelent pentru performanță sportivă și definire musculară.";
                    } else if (bodyFatPercentage < 18) {
                        category = "Fitness";
                        categoryClass = "bg-success text-white";
                        recommendation = "Ai un nivel de fitness al grăsimii corporale. Acest nivel este sănătos și estetic, oferind un bun echilibru între definire și sănătate.";
                    } else if (bodyFatPercentage < 25) {
                        category = "Acceptabil";
                        categoryClass = "bg-warning text-dark";
                        recommendation = "Ai un nivel acceptabil de grăsime corporală. Pentru îmbunătățirea compoziției corporale, poți considera un program de antrenament cu rezistență și ajustări în alimentație.";
                    } else {
                        category = "Obezitate";
                        categoryClass = "bg-danger text-white";
                        recommendation = "Nivelul tău de grăsime corporală indică obezitate. Recomandăm consultarea unui specialist pentru un plan personalizat de scădere în greutate.";
                    }
                } else {
                    if (bodyFatPercentage < 14) {
                        category = "Esențial";
                        categoryClass = "bg-info text-white";
                        recommendation = "Ai un nivel foarte scăzut de grăsime corporală, specific atletelor de performanță. Acest nivel poate fi dificil de menținut pe termen lung și poate afecta funcțiile hormonale. Asigură-te că urmezi un plan nutrițional adecvat.";
                    } else if (bodyFatPercentage < 21) {
                        category = "Atletic";
                        categoryClass = "bg-success text-white";
                        recommendation = "Ai un nivel atletic de grăsime corporală. Acest nivel este excelent pentru performanță sportivă și definire musculară.";
                    } else if (bodyFatPercentage < 25) {
                        category = "Fitness";
                        categoryClass = "bg-success text-white";
                        recommendation = "Ai un nivel de fitness al grăsimii corporale. Acest nivel este sănătos și estetic, oferind un bun echilibru între definire și sănătate.";
                    } else if (bodyFatPercentage < 32) {
                        category = "Acceptabil";
                        categoryClass = "bg-warning text-dark";
                        recommendation = "Ai un nivel acceptabil de grăsime corporală. Pentru îmbunătățirea compoziției corporale, poți considera un program de antrenament cu rezistență și ajustări în alimentație.";
                    } else {
                        category = "Obezitate";
                        categoryClass = "bg-danger text-white";
                        recommendation = "Nivelul tău de grăsime corporală indică obezitate. Recomandăm consultarea unui specialist pentru un plan personalizat de scădere în greutate.";
                    }
                }
                
                // Display results
                document.getElementById('bodyFatValue').textContent = bodyFatPercentage.toFixed(1) + '%';
                document.getElementById('bodyFatCategoryText').textContent = category;
                document.getElementById('bodyFatCategory').className = `bf-category p-2 rounded text-center mb-2 ${categoryClass}`;
                document.getElementById('fatMass').textContent = fatMass.toFixed(1);
                document.getElementById('leanMass').textContent = leanMass.toFixed(1);
                document.getElementById('bodyFatRecommendation').textContent = recommendation;
                
                bodyFatResult.classList.remove('d-none');
            }
        });
    }
});
