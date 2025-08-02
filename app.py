from flask import Flask, request, jsonify, send_file
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def scoreboard():
    return send_file('scoreboard.html')


@app.route('/admin')
def admin():
    return send_file('admin.html')


@app.route('/teams')
def get_teams():
    return jsonify(load_data())


@app.route('/data')
def get_data():
    return jsonify(load_data())


@app.route('/update', methods=['POST'])
def update():
    new_team = request.get_json()
    data = load_data()

    # Update if team exists, else add
    for i, team in enumerate(data):
        if team['Team'].lower() == new_team['Team'].lower():
            data[i] = new_team
            break
    else:
        data.append(new_team)

    save_data(data)
    return jsonify({'status': 'success', 'team': new_team})


@app.route('/delete', methods=['POST'])
def delete_team():
    data = request.get_json()
    team_name = data.get("Team", "").strip().lower()
    if not team_name:
        return jsonify({"error": "Team name is required"}), 400

    teams = load_data()
    updated_teams = [team for team in teams if team.get("Team", "").strip().lower() != team_name]
    save_data(updated_teams)

    return jsonify({"message": f"Team '{team_name}' deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
