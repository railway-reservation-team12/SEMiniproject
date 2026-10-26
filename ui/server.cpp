// Local web UI server. Reuses the team's existing modules UNCHANGED.
// Build (from repo root):
//   g++ -std=c++17 -pthread -Isrc -Iui ui/server.cpp $(ls src/*.cpp | grep -v main.cpp) -o rrs_web
// Windows/MinGW: add -lws2_32.  Run from repo root, then open http://127.0.0.1:8080
#include "httplib.h"
#include "booking.h"
#include "cancellation.h"
#include "data_store.h"
#include "reservation.h"
#include "validation.h"

#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>

static std::mutex mtx;                       // serialises requests (modules use global cin/cout)
static std::vector<Train> trains;
static std::vector<Reservation> reservations;

// Feeds scripted input to cin and captures cout while a module's prompt-based flow runs.
struct IoCapture {
    std::istringstream in;
    std::ostringstream out;
    std::streambuf *oldIn, *oldOut;
    explicit IoCapture(const std::string& input) : in(input) {
        oldIn = std::cin.rdbuf(in.rdbuf());
        oldOut = std::cout.rdbuf(out.rdbuf());
    }
    ~IoCapture() { std::cin.rdbuf(oldIn); std::cout.rdbuf(oldOut); }
};

static std::string trim(const std::string& s) {
    size_t a = s.find_first_not_of(" \t\r\n"), b = s.find_last_not_of(" \t\r\n");
    return a == std::string::npos ? "" : s.substr(a, b - a + 1);
}
static std::string lower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(),
                   [](unsigned char c) { return (char)std::tolower(c); });
    return s;
}
static std::string esc(const std::string& s) {
    std::string o;
    for (unsigned char c : s) {
        if (c == '"') o += "\\\"";
        else if (c == '\\') o += "\\\\";
        else if (c >= 0x20) o += (char)c;
    }
    return o;
}
static void send(httplib::Response& r, int code, const std::string& body) {
    r.status = code;
    r.set_content(body, "application/json");
}
static void fail(httplib::Response& r, int code, const std::string& msg) {
    send(r, code, "{\"error\":\"" + esc(msg) + "\"}");
}
static std::string trainJson(const Train& t) {
    return "{\"trainId\":\"" + esc(t.trainId) + "\",\"trainName\":\"" + esc(t.trainName) +
           "\",\"source\":\"" + esc(t.source) + "\",\"destination\":\"" + esc(t.destination) +
           "\",\"departureTime\":\"" + esc(t.departureTime) + "\",\"arrivalTime\":\"" +
           esc(t.arrivalTime) + "\",\"totalSeats\":" + std::to_string(t.totalSeats) +
           ",\"availableSeats\":" + std::to_string(t.availableSeats) + "}";
}
static std::string resJson(const Reservation& r) {
    std::string trainName, route;
    for (const auto& t : trains)
        if (t.trainId == r.trainId) { trainName = t.trainName; route = t.source + " to " + t.destination; }
    return "{\"reservationId\":\"" + esc(r.reservationId) + "\",\"trainId\":\"" + esc(r.trainId) +
           "\",\"trainName\":\"" + esc(trainName) + "\",\"route\":\"" + esc(route) +
           "\",\"passengerName\":\"" + esc(r.passengerName) + "\",\"age\":" +
           std::to_string(r.passengerAge) + ",\"gender\":\"" + esc(r.passengerGender) +
           "\",\"journeyDate\":\"" + esc(r.journeyDate) + "\",\"seats\":" +
           std::to_string(r.seatsBooked) + ",\"status\":\"" + esc(getStatusString(r.status)) + "\"}";
}

int main() {
    trains = loadTrains();
    reservations = loadReservations();
    if (trains.empty()) { std::cerr << "No train data loaded. Run from the repo root (needs data/trains.dat).\n"; return 1; }

    httplib::Server svr;

    svr.Get("/", [](const httplib::Request&, httplib::Response& res) {
        std::ifstream f("ui/web/index.html");
        std::stringstream ss; ss << f.rdbuf();
        res.set_content(ss.str(), "text/html; charset=utf-8");
    });

    svr.Get("/api/trains", [](const httplib::Request&, httplib::Response& res) {
        std::lock_guard<std::mutex> lk(mtx);
        std::string b = "[";
        for (size_t i = 0; i < trains.size(); i++) b += (i ? "," : "") + trainJson(trains[i]);
        send(res, 200, b + "]");
    });

    svr.Get("/api/search", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lk(mtx);
        std::string s = trim(req.get_param_value("source")), d = trim(req.get_param_value("destination"));
        if (!isValidStation(s) || !isValidStation(d)) return fail(res, 400, "Invalid station name.");
        if (!isValidDate(trim(req.get_param_value("date")))) return fail(res, 400, "Invalid journey date (use DD-MM-YYYY).");
        std::string b = "[";
        bool first = true;
        for (const auto& t : trains)
            if (lower(t.source) == lower(s) && lower(t.destination) == lower(d)) {
                b += (first ? "" : ",") + trainJson(t);
                first = false;
            }
        send(res, 200, b + "]");
    });

    svr.Post("/api/book", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lk(mtx);
        const char* keys[] = {"trainId", "name", "age", "gender", "date", "seats"};
        std::string input;
        for (const char* k : keys) {
            std::string v = trim(req.get_param_value(k));
            if (v.find('\n') != std::string::npos) return fail(res, 400, "Invalid input.");
            input += v + "\n";
        }
        size_t before = reservations.size();
        std::string out;
        { IoCapture cap(input); bookReservation(trains, reservations); out = cap.out.str(); }
        if (reservations.size() > before) return send(res, 200, resJson(reservations.back()));
        for (const char* p : {"Enter train ID: ", "Passenger name: ", "Passenger age: ", "Passenger gender: ",
                              "Journey date (DD-MM-YYYY): ", "Number of seats: "}) {
            size_t pos;
            while ((pos = out.find(p)) != std::string::npos) out.erase(pos, std::string(p).size());
        }
        out = trim(out);
        fail(res, 400, out.empty() ? "Booking could not be completed." : out);
    });

    svr.Get("/api/reservation", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lk(mtx);
        Reservation r;
        switch (lookupReservation(trim(req.get_param_value("id")), reservations, r)) {
            case LOOKUP_SUCCESS: return send(res, 200, resJson(r));
            case LOOKUP_INVALID_ID: return fail(res, 400, "Invalid reservation ID format (e.g. RES001).");
            default: return fail(res, 404, "Reservation not found.");
        }
    });

    svr.Post("/api/cancel", [](const httplib::Request& req, httplib::Response& res) {
        std::lock_guard<std::mutex> lk(mtx);
        switch (processCancellation(trim(req.get_param_value("id")), reservations, trains)) {
            case CANCEL_SUCCESS: return send(res, 200, "{\"message\":\"Reservation cancelled. Seats restored.\"}");
            case CANCEL_INVALID_ID: return fail(res, 400, "Invalid reservation ID format (e.g. RES001).");
            case CANCEL_NOT_FOUND: return fail(res, 404, "Reservation not found.");
            case CANCEL_ALREADY_CANCELLED: return fail(res, 409, "This reservation has already been cancelled.");
            default: return fail(res, 500, "Cancellation could not be saved.");
        }
    });

    std::cout << "Railway Reservation UI running at http://127.0.0.1:8080  (Ctrl+C to stop)\n";
    svr.listen("127.0.0.1", 8080);
    return 0;
}
