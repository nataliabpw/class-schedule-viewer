from flask import Flask, request, jsonify, render_template
from datetime import datetime
from src.schedule.service import get_schedule_for_date_and_groups
import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)

LAST_GROUP = 17
groups = range(1, LAST_GROUP + 1) 

@app.route("/", methods=["GET"])
def home():
    try:
        return render_template("index.html", groups=groups)
    except Exception as e:
        logger.exception("Error rendering template index.html")
        return f"Template render error: {e}", 500

@app.route("/api/schedule", methods=["GET"])
def get_schedule_api():
    date_str = request.args.get("selected_date")
    group_seminaria = request.args.get("group_seminaria", type=int)
    group_cwiczenia = request.args.get("group_cwiczenia")
    group_zajecia = request.args.get("group_zajecia")    

    if not date_str:
        return jsonify({
            "error": "Wybierz datę!"
        }), 400 

    if group_seminaria is None:
        return jsonify({
            "error": "Wybierz grupę seminaryjną!"
        }), 400 
    
    if not group_cwiczenia or not group_zajecia:
        return jsonify({
            "error": "Wybierz grupy ćwiczeniową i zajęciową!"
        }), 400 
    
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "error": "Błąd przetwarzania daty"
        }), 400

    if not (1 <= group_seminaria <= LAST_GROUP):
        return jsonify({
            "error": "Niepoprawna grupa seminaryjna!"
        }), 400
    
    if not validate_group(group_cwiczenia, ['a', 'b']):
        return jsonify({
            "error": "Niepoprawna grupa ćwiczeniowa!"
        }), 400

    if not validate_group(group_zajecia, ['a', 'b', 'c']):
        return jsonify({
            "error": "Niepoprawna grupa zajęciowa!"
        }), 400

    schedule_data = get_schedule_for_date_and_groups(selected_date, group_seminaria, group_cwiczenia, group_zajecia)

    if not schedule_data:
        return jsonify({
            "error": "Nie znaleziono planu dla podanych parametrów"
        }), 404

    return jsonify(schedule_data), 200

def validate_group(group, letters):
    letter = group[-1]

    if letter not in letters:
        return False
    
    number_part = group[:-1]
    if not number_part.isdigit():
        return False
    
    number = int(number_part)
    if not (1 <= number <= LAST_GROUP):
        return False
    
    return True


if __name__ == "__main__":
    app.run(debug=True)