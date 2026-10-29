#!/usr/bin/env python3
"""
Railway Reservation System - Local API & Static File Server
Team 12 | PES University | Software Engineering Mini-Project

Directly bridges the modern Web UI with the project's data files:
- data/trains.dat
- data/reservations.dat
- data/schedules.dat
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from datetime import datetime

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(WEB_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")

TRAINS_FILE = os.path.join(DATA_DIR, "trains.dat")
RESERVATIONS_FILE = os.path.join(DATA_DIR, "reservations.dat")
SCHEDULES_FILE = os.path.join(DATA_DIR, "schedules.dat")

def load_trains():
    trains = []
    if not os.path.exists(TRAINS_FILE):
        return trains
    with open(TRAINS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 8:
                trains.append({
                    "trainId": parts[0],
                    "trainName": parts[1],
                    "source": parts[2],
                    "destination": parts[3],
                    "departureTime": parts[4],
                    "arrivalTime": parts[5],
                    "totalSeats": int(parts[6]),
                    "availableSeats": int(parts[7])
                })
    return trains

def save_trains(trains):
    with open(TRAINS_FILE, "w", encoding="utf-8") as f:
        f.write("# Train Data: trainId|trainName|source|destination|departureTime|arrivalTime|totalSeats|availableSeats\n")
        for t in trains:
            f.write(f"{t['trainId']}|{t['trainName']}|{t['source']}|{t['destination']}|{t['departureTime']}|{t['arrivalTime']}|{t['totalSeats']}|{t['availableSeats']}\n")
    return True

def load_reservations():
    reservations = []
    if not os.path.exists(RESERVATIONS_FILE):
        return reservations
    with open(RESERVATIONS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 8:
                reservations.append({
                    "reservationId": parts[0],
                    "trainId": parts[1],
                    "passengerName": parts[2],
                    "passengerAge": int(parts[3]),
                    "passengerGender": parts[4],
                    "journeyDate": parts[5],
                    "seatsBooked": int(parts[6]),
                    "status": int(parts[7])  # 1 = Confirmed, 2 = Cancelled
                })
    return reservations

def save_reservations(reservations):
    return save_reservations_atomically(reservations)

def load_schedules():
    schedules = []
    if not os.path.exists(SCHEDULES_FILE):
        return schedules
    with open(SCHEDULES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                schedules.append({
                    "trainId": parts[0],
                    "journeyDate": parts[1]
                })
    return schedules

def is_valid_journey_date(value):
    try:
        parsed = datetime.strptime(value, "%d-%m-%Y")
    except (TypeError, ValueError):
        return False
    return 2024 <= parsed.year <= 2030 and parsed.date() >= datetime.now().date()

def is_train_departure_upcoming(train, journey_date):
    try:
        departure = datetime.strptime(
            f"{journey_date} {train['departureTime']}", "%d-%m-%Y %H:%M"
        )
    except (KeyError, TypeError, ValueError):
        return False
    return departure > datetime.now()

def is_train_scheduled(train_id, journey_date, schedules=None):
    schedules = load_schedules() if schedules is None else schedules
    return any(s["trainId"] == train_id and s["journeyDate"] == journey_date for s in schedules)

def available_seats_for_journey(train, journey_date, reservations=None):
    reservations = load_reservations() if reservations is None else reservations
    booked = sum(
        r["seatsBooked"]
        for r in reservations
        if r["trainId"] == train["trainId"]
        and r["journeyDate"] == journey_date
        and r["status"] == 1
    )
    return max(0, train["totalSeats"] - booked)

def save_reservations_atomically(reservations):
    temporary_file = RESERVATIONS_FILE + ".tmp"
    try:
        with open(temporary_file, "w", encoding="utf-8") as f:
            f.write("# Reservation Data: reservationId|trainId|passengerName|passengerAge|passengerGender|journeyDate|seatsBooked|status\n")
            for r in reservations:
                f.write(f"{r['reservationId']}|{r['trainId']}|{r['passengerName']}|{r['passengerAge']}|{r['passengerGender']}|{r['journeyDate']}|{r['seatsBooked']}|{r['status']}\n")
        os.replace(temporary_file, RESERVATIONS_FILE)
        return True
    except OSError:
        try:
            os.remove(temporary_file)
        except OSError:
            pass
        return False

def generate_reservation_id(reservations):
    max_id = 0
    for r in reservations:
        rid = r.get("reservationId", "")
        if rid.startswith("RES") and len(rid) > 3:
            try:
                num = int(rid[3:])
                if num > max_id:
                    max_id = num
            except ValueError:
                pass
    return f"RES{max_id + 1:03d}"

class RailwayRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/trains":
            trains = load_trains()
            params = urllib.parse.parse_qs(parsed.query)
            journey_date = params.get("date", [""])[0].strip()
            if journey_date and not is_valid_journey_date(journey_date):
                self.send_json(400, {"success": False, "error": "Invalid journey date."})
                return
            reservations = load_reservations()
            schedules = load_schedules()
            for train in trains:
                if not journey_date:
                    train["availableSeats"] = train["totalSeats"]
                elif is_train_scheduled(train["trainId"], journey_date, schedules):
                    train["availableSeats"] = available_seats_for_journey(
                        train, journey_date, reservations
                    )
                else:
                    train["availableSeats"] = 0
            self.send_json(200, {"success": True, "data": trains})
            return

        if path == "/api/reservations":
            reservations = load_reservations()
            self.send_json(200, {"success": True, "data": reservations})
            return

        if path == "/api/reservation":
            params = urllib.parse.parse_qs(parsed.query)
            res_id = params.get("id", [""])[0].strip().upper()
            if not res_id:
                self.send_json(400, {"success": False, "error": "Reservation ID is required."})
                return

            reservations = load_reservations()
            target_res = None
            for r in reservations:
                if r["reservationId"].upper() == res_id:
                    target_res = r
                    break

            if not target_res:
                self.send_json(404, {"success": False, "error": f"Reservation {res_id} not found."})
                return

            trains = load_trains()
            target_train = None
            for t in trains:
                if t["trainId"] == target_res["trainId"]:
                    target_train = t
                    break

            if target_train:
                target_train["availableSeats"] = available_seats_for_journey(
                    target_train, target_res["journeyDate"], reservations
                )

            self.send_json(200, {
                "success": True,
                "reservation": target_res,
                "train": target_train
            })
            return

        if path == "/api/schedules":
            schedules = load_schedules()
            self.send_json(200, {"success": True, "data": schedules})
            return

        # Serve static frontend files from web/
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if path == "/" or path == "":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            data = json.loads(body.decode("utf-8"))
        except Exception:
            data = {}
        if not isinstance(data, dict):
            data = {}

        if path == "/api/book":
            try:
                train_id = str(data.get("trainId", "")).strip()
                name = str(data.get("name", "")).strip()
                age = int(data.get("age", 0))
                gender = str(data.get("gender", "")).strip()
                date = str(data.get("date", "")).strip()
                seats = int(data.get("seats", 1))
            except (TypeError, ValueError):
                self.send_json(400, {"success": False, "error": "Invalid booking input."})
                return

            if (not train_id or not name or not 1 <= age <= 120 or
                    gender not in {"M", "F", "Other"} or seats <= 0 or
                    not is_valid_journey_date(date)):
                self.send_json(400, {"success": False, "error": "Invalid booking input."})
                return

            trains = load_trains()
            target_train = None
            for t in trains:
                if t["trainId"] == train_id:
                    target_train = t
                    break

            if not target_train:
                self.send_json(404, {"success": False, "error": "Train not found."})
                return

            if not is_train_scheduled(train_id, date):
                self.send_json(400, {"success": False, "error": "This train is not scheduled on that date."})
                return

            if not is_train_departure_upcoming(target_train, date):
                self.send_json(400, {"success": False, "error": "The departure time for this journey has passed."})
                return

            reservations = load_reservations()
            available = available_seats_for_journey(target_train, date, reservations)
            if seats > available:
                self.send_json(400, {"success": False, "error": f"Only {available} seats available for this journey."})
                return

            new_id = generate_reservation_id(reservations)

            new_reservation = {
                "reservationId": new_id,
                "trainId": train_id,
                "passengerName": name,
                "passengerAge": age,
                "passengerGender": gender,
                "journeyDate": date,
                "seatsBooked": seats,
                "status": 1  # Confirmed
            }

            reservations.append(new_reservation)
            if not save_reservations(reservations):
                self.send_json(500, {"success": False, "error": "Could not save booking."})
                return

            target_train["availableSeats"] = available - seats

            self.send_json(200, {
                "success": True,
                "message": "Reservation created successfully.",
                "reservation": new_reservation,
                "train": target_train
            })
            return

        if path == "/api/cancel":
            reservation_id = str(data.get("reservationId", "")).strip().upper()
            if not reservation_id:
                self.send_json(400, {"success": False, "error": "Reservation ID is required."})
                return

            reservations = load_reservations()
            target_res = None
            for r in reservations:
                if r["reservationId"] == reservation_id:
                    target_res = r
                    break

            if not target_res:
                self.send_json(404, {"success": False, "error": f"Reservation {reservation_id} not found."})
                return

            if target_res["status"] == 2:
                self.send_json(400, {"success": False, "error": f"Reservation {reservation_id} is already cancelled."})
                return

            # Mark cancelled
            target_res["status"] = 2
            trains = load_trains()
            target_train = next((t for t in trains if t["trainId"] == target_res["trainId"]), None)
            if not save_reservations(reservations):
                target_res["status"] = 1
                self.send_json(500, {"success": False, "error": "Could not save cancellation."})
                return

            if target_train:
                target_train["availableSeats"] = available_seats_for_journey(
                    target_train, target_res["journeyDate"], reservations
                )

            self.send_json(200, {
                "success": True,
                "message": f"Reservation {reservation_id} cancelled. Seats restored.",
                "reservation": target_res,
                "train": target_train
            })
            return

        if path == "/api/undo_cancel":
            reservation_id = str(data.get("reservationId", "")).strip().upper()
            reservations = load_reservations()
            target_res = None
            for r in reservations:
                if r["reservationId"] == reservation_id:
                    target_res = r
                    break

            if not target_res:
                self.send_json(404, {"success": False, "error": "Reservation not found."})
                return

            if target_res["status"] != 2:
                self.send_json(400, {"success": False, "error": "Reservation is not cancelled."})
                return

            trains = load_trains()
            target_train = next((t for t in trains if t["trainId"] == target_res["trainId"]), None)
            if not target_train:
                self.send_json(404, {"success": False, "error": "Reservation train not found."})
                return

            available = available_seats_for_journey(target_train, target_res["journeyDate"], reservations)
            if target_res["seatsBooked"] > available:
                self.send_json(409, {"success": False, "error": "There are no longer enough seats to restore this reservation."})
                return

            target_res["status"] = 1
            if not save_reservations(reservations):
                target_res["status"] = 2
                self.send_json(500, {"success": False, "error": "Could not restore reservation."})
                return

            target_train["availableSeats"] = available - target_res["seatsBooked"]

            self.send_json(200, {
                "success": True,
                "message": f"Reservation {reservation_id} restored to confirmed.",
                "reservation": target_res,
                "train": target_train
            })
            return

        self.send_json(404, {"success": False, "error": "Endpoint not found."})

def run_server():
    os.makedirs(WEB_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), RailwayRequestHandler) as httpd:
        print(f"================================================================")
        print(f"  Railway Reservation System - Modern Web UI Server")
        print(f"  Team 12 | PES University | Software Engineering Mini-Project")
        print(f"  Live at: http://localhost:{PORT}")
        print(f"  Data store: {DATA_DIR}")
        print(f"================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
