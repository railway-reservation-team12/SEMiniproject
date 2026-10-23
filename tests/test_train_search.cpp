#include "booking.h"
#include "models.h"

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class CinRedirect {
private:
    std::istringstream input;
    std::streambuf* oldBuffer;

public:
    explicit CinRedirect(const std::string& text)
        : input(text),
          oldBuffer(std::cin.rdbuf(input.rdbuf())) {}

    ~CinRedirect() {
        std::cin.rdbuf(oldBuffer);
    }
};

int main() {
    int passed = 0;
    int failed = 0;

    auto check = [&](bool condition, const std::string& name) {
        if (condition) {
            std::cout << "[PASS] " << name << '\n';
            ++passed;
        } else {
            std::cout << "[FAIL] " << name << '\n';
            ++failed;
        }
    };

    std::vector<Train> trains = {
        {
            "T001",
            "Bangalore Express",
            "Bengaluru",
            "Chennai",
            "06:00",
            "12:00",
            100,
            80
        },
        {
            "T002",
            "Mysore Express",
            "Mysuru",
            "Bengaluru",
            "08:00",
            "10:00",
            80,
            50
        },
        {
            "T003",
            "Chennai Express",
            "Bengaluru",
            "Chennai",
            "14:00",
            "20:00",
            120,
            100
        }
    };

    std::cout << "\n--- Train Search Tests ---\n";

    {
        CinRedirect input("Bengaluru\nChennai\n");

        check(
            searchTrains(trains),
            "TS-01: Valid source and destination find matching trains"
        );
    }

    {
        CinRedirect input("bengaluru\nchennai\n");

        check(
            searchTrains(trains),
            "TS-02: Search is case-insensitive"
        );
    }

    {
        CinRedirect input("Bengaluru\nMumbai\n");

        check(
            !searchTrains(trains),
            "TS-03: Non-existent route returns false"
        );
    }

    {
        CinRedirect input("123Invalid\nChennai\n");

        check(
            !searchTrains(trains),
            "TS-04: Invalid station name is rejected"
        );
    }

    std::cout << "\n========================================\n";
    std::cout << "TRAIN SEARCH TEST SUMMARY\n";
    std::cout << "========================================\n";
    std::cout << "Total:  " << passed + failed << '\n';
    std::cout << "Passed: " << passed << '\n';
    std::cout << "Failed: " << failed << '\n';

    if (failed == 0) {
        std::cout << "RESULT: ALL TRAIN SEARCH TESTS PASSED\n";
        return 0;
    }

    std::cout << "RESULT: TRAIN SEARCH TESTS FAILED\n";
    return 1;
}
