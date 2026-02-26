from flask import Flask, request, jsonify, render_template
from datetime import datetime
from src.schedule.service import get_schedule_for_date_and_groups

app = Flask(__name__)

@app.route("/")
def home():
    last_group = 17
    groups = range(1, last_group + 1) 
    return render_template("index.html", groups=groups)

@app.route("/schedule", methods=["GET"])
def get_schedule():
    date_str = request.args.get("selected_date")
    group_seminaria = request.args.get("group_seminaria")
    group_cwiczenia = request.args.get("group_cwiczenia")
    group_zajecia = request.args.get("group_zajecia")

    if not date_str or not group_seminaria or not group_cwiczenia or not group_zajecia:
        return jsonify({"error": "Missing parameter"}), 400

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    schedule_data = get_schedule_for_date_and_groups(selected_date, group_seminaria, group_cwiczenia, group_zajecia)

    # return jsonify(schedule_data)
    return render_template("schedule.html", schedule_data=schedule_data)

if __name__ == "__main__":
    app.run(debug=True)