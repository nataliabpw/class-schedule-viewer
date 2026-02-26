from flask import Flask, request, jsonify, render_template
from datetime import datetime
from src.schedule.service import get_schedule_for_date_and_groups

app = Flask(__name__)

LAST_GROUP = 17
groups = range(1, LAST_GROUP + 1) 

@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html", 
        groups=groups, 
        selected_date=None, 
        selected_group_seminaria=None, 
        selected_group_cwiczenia=None, 
        selected_group_zajecia=None
    )

@app.route("/schedule", methods=["GET"])
def get_schedule():
    date_str = request.args.get("selected_date")
    group_seminaria = request.args.get("group_seminaria", type=int)
    group_cwiczenia = request.args.get("group_cwiczenia")
    group_zajecia = request.args.get("group_zajecia")

    if not date_str or not group_seminaria or not group_cwiczenia or not group_zajecia:
        return render_template(
            "index.html", 
            errors = "Wybierz wszystkie parametry zapytania!", 
            groups=groups,
            selected_date=date_str,
            selected_group_seminaria=group_seminaria,
            selected_group_cwiczenia=group_cwiczenia,
            selected_group_zajecia=group_zajecia
        ), 400

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return render_template(
            "index.html", 
            errors = "Błąd przetwarzania daty", 
            groups=groups, 
            selected_date=date_str,
            selected_group_seminaria=group_seminaria,
            selected_group_cwiczenia=group_cwiczenia,
            selected_group_zajecia=group_zajecia
        ), 400

    if not (1 <= int(group_seminaria) <= LAST_GROUP):
        return render_template(
            "index.html", 
            errors = "Niepoprawna grupa seminaryjna!", 
            groups=groups,
            selected_date=date_str,
            selected_group_seminaria=group_seminaria,
            selected_group_cwiczenia=group_cwiczenia,
            selected_group_zajecia=group_zajecia
        ), 400
    
    if not validate_group(group_cwiczenia, ['a', 'b']):
        return render_template(
            "index.html", 
            errors = "Niepoprawna grupa ćwiczeniowa!", 
            groups=groups,
            selected_date=date_str,
            selected_group_seminaria=group_seminaria,
            selected_group_cwiczenia=group_cwiczenia,
            selected_group_zajecia=group_zajecia
        ), 400

    if not validate_group(group_zajecia, ['a', 'b', 'c']):
        return render_template(
            "index.html", 
            errors = "Niepoprawna grupa zajęciowa!", 
            groups=groups,
            selected_date=date_str,
            selected_group_seminaria=group_seminaria,
            selected_group_cwiczenia=group_cwiczenia,
            selected_group_zajecia=group_zajecia
        ), 400

    schedule_data = get_schedule_for_date_and_groups(selected_date, group_seminaria, group_cwiczenia, group_zajecia)

    # return jsonify(schedule_data)
    return render_template("schedule.html", schedule_data=schedule_data)

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