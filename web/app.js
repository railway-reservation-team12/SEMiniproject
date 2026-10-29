/**
 * VELOCITY · LUXURY RAILWAY RESERVATION SYSTEM
 * High-Precision Interaction Engine
 * Pure JS Lerp Scroll | 60FPS GPU Animations | View Transitions API
 * Team 12 | PES University Software Engineering
 */

(function () {
  "use strict";

  // ── Global State ───────────────────────────────────────────────────────────
  let state = {
    trains: [],
    reservations: [],
    schedules: [],
    showAllTrains: false,
    cancellationPendingIds: new Set(),
    undoPending: false,
    lastCancelledReservationId: null,
    undoTimer: null,
    isDarkMode: false,
    selectedCmdIndex: 0,
  };

  // Default seed fallback matching project's data/*.dat files
  const SEED_TRAINS = [
    {
      trainId: "T001",
      trainName: "Shatabdi Express",
      source: "Bangalore",
      destination: "Chennai",
      departureTime: "06:00",
      arrivalTime: "11:00",
      totalSeats: 120,
      availableSeats: 117,
    },
    {
      trainId: "T002",
      trainName: "Rajdhani Express",
      source: "Bangalore",
      destination: "Delhi",
      departureTime: "15:30",
      arrivalTime: "07:00",
      totalSeats: 200,
      availableSeats: 198,
    },
    {
      trainId: "T003",
      trainName: "Vande Bharat Express",
      source: "Bangalore",
      destination: "Mysuru",
      departureTime: "05:45",
      arrivalTime: "07:25",
      totalSeats: 160,
      availableSeats: 142,
    },
    {
      trainId: "T004",
      trainName: "Karnataka Express",
      source: "Bangalore",
      destination: "Delhi",
      departureTime: "19:20",
      arrivalTime: "10:30",
      totalSeats: 240,
      availableSeats: 210,
    },
    {
      trainId: "T005",
      trainName: "Kaveri Express",
      source: "Mysuru",
      destination: "Chennai",
      departureTime: "21:00",
      arrivalTime: "06:45",
      totalSeats: 180,
      availableSeats: 165,
    },
    {
      trainId: "T006",
      trainName: "Duronto Express",
      source: "Chennai",
      destination: "Delhi",
      departureTime: "06:50",
      arrivalTime: "10:35",
      totalSeats: 220,
      availableSeats: 185,
    },
    {
      trainId: "T007",
      trainName: "Coromandel Express",
      source: "Chennai",
      destination: "Kolkata",
      departureTime: "07:00",
      arrivalTime: "10:50",
      totalSeats: 250,
      availableSeats: 228,
    },
    {
      trainId: "T008",
      trainName: "Mumbai Rajdhani",
      source: "Mumbai",
      destination: "Delhi",
      departureTime: "16:55",
      arrivalTime: "08:35",
      totalSeats: 200,
      availableSeats: 176,
    },
    {
      trainId: "T009",
      trainName: "Deccan Queen",
      source: "Pune",
      destination: "Mumbai",
      departureTime: "07:15",
      arrivalTime: "10:25",
      totalSeats: 150,
      availableSeats: 130,
    },
    {
      trainId: "T010",
      trainName: "Howrah Mail",
      source: "Mumbai",
      destination: "Kolkata",
      departureTime: "21:30",
      arrivalTime: "12:15",
      totalSeats: 260,
      availableSeats: 240,
    },
    {
      trainId: "T011",
      trainName: "Tejas Express",
      source: "Bangalore",
      destination: "Goa",
      departureTime: "06:30",
      arrivalTime: "14:00",
      totalSeats: 140,
      availableSeats: 98,
    },
    {
      trainId: "T012",
      trainName: "Golden Chariot Luxury",
      source: "Bangalore",
      destination: "Hampi",
      departureTime: "20:00",
      arrivalTime: "06:30",
      totalSeats: 80,
      availableSeats: 54,
    },
    {
      trainId: "T013",
      trainName: "Prashanti Express",
      source: "Bangalore",
      destination: "Kolkata",
      departureTime: "14:00",
      arrivalTime: "01:30",
      totalSeats: 220,
      availableSeats: 208,
    },
    {
      trainId: "T014",
      trainName: "Udyan Superfast",
      source: "Bangalore",
      destination: "Mumbai",
      departureTime: "20:45",
      arrivalTime: "20:00",
      totalSeats: 200,
      availableSeats: 188,
    },
    {
      trainId: "T015",
      trainName: "Bangalore - Pune Superfast",
      source: "Bangalore",
      destination: "Pune",
      departureTime: "21:15",
      arrivalTime: "13:00",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T016",
      trainName: "Lalbagh Superfast",
      source: "Chennai",
      destination: "Bangalore",
      departureTime: "06:30",
      arrivalTime: "11:45",
      totalSeats: 160,
      availableSeats: 148,
    },
    {
      trainId: "T017",
      trainName: "Chennai - Goa Superfast",
      source: "Chennai",
      destination: "Goa",
      departureTime: "12:49",
      arrivalTime: "18:31",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T018",
      trainName: "Chennai - Hampi Superfast",
      source: "Chennai",
      destination: "Hampi",
      departureTime: "15:06",
      arrivalTime: "05:54",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T019",
      trainName: "Chennai - Mumbai Superfast",
      source: "Chennai",
      destination: "Mumbai",
      departureTime: "18:23",
      arrivalTime: "10:17",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T020",
      trainName: "Kaveri Express (Return)",
      source: "Chennai",
      destination: "Mysuru",
      departureTime: "21:15",
      arrivalTime: "07:00",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T021",
      trainName: "Chennai - Pune Superfast",
      source: "Chennai",
      destination: "Pune",
      departureTime: "09:57",
      arrivalTime: "20:03",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T022",
      trainName: "Karnataka Express (Return)",
      source: "Delhi",
      destination: "Bangalore",
      departureTime: "16:00",
      arrivalTime: "06:40",
      totalSeats: 240,
      availableSeats: 228,
    },
    {
      trainId: "T023",
      trainName: "Grand Trunk Express",
      source: "Delhi",
      destination: "Chennai",
      departureTime: "18:40",
      arrivalTime: "06:15",
      totalSeats: 220,
      availableSeats: 208,
    },
    {
      trainId: "T024",
      trainName: "Delhi - Goa Superfast",
      source: "Delhi",
      destination: "Goa",
      departureTime: "18:48",
      arrivalTime: "17:12",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T025",
      trainName: "Delhi - Hampi Superfast",
      source: "Delhi",
      destination: "Hampi",
      departureTime: "06:05",
      arrivalTime: "22:35",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T026",
      trainName: "Delhi - Kolkata Superfast",
      source: "Delhi",
      destination: "Kolkata",
      departureTime: "09:22",
      arrivalTime: "09:58",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T027",
      trainName: "August Kranti Rajdhani",
      source: "Delhi",
      destination: "Mumbai",
      departureTime: "16:50",
      arrivalTime: "09:45",
      totalSeats: 200,
      availableSeats: 188,
    },
    {
      trainId: "T028",
      trainName: "Delhi - Mysuru Superfast",
      source: "Delhi",
      destination: "Mysuru",
      departureTime: "15:56",
      arrivalTime: "19:44",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T029",
      trainName: "Delhi - Pune Superfast",
      source: "Delhi",
      destination: "Pune",
      departureTime: "18:13",
      arrivalTime: "06:07",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T030",
      trainName: "Goa Superfast",
      source: "Goa",
      destination: "Bangalore",
      departureTime: "15:00",
      arrivalTime: "04:30",
      totalSeats: 140,
      availableSeats: 128,
    },
    {
      trainId: "T031",
      trainName: "Goa - Chennai Superfast",
      source: "Goa",
      destination: "Chennai",
      departureTime: "09:47",
      arrivalTime: "16:53",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T032",
      trainName: "Goa - Delhi Superfast",
      source: "Goa",
      destination: "Delhi",
      departureTime: "12:04",
      arrivalTime: "21:16",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T033",
      trainName: "Goa - Hampi Superfast",
      source: "Goa",
      destination: "Hampi",
      departureTime: "15:21",
      arrivalTime: "08:39",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T034",
      trainName: "Goa - Kolkata Superfast",
      source: "Goa",
      destination: "Kolkata",
      departureTime: "18:38",
      arrivalTime: "13:02",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T035",
      trainName: "Mandovi Express",
      source: "Goa",
      destination: "Mumbai",
      departureTime: "09:15",
      arrivalTime: "19:40",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T036",
      trainName: "Goa - Mysuru Superfast",
      source: "Goa",
      destination: "Mysuru",
      departureTime: "09:12",
      arrivalTime: "05:48",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T037",
      trainName: "Goa - Pune Superfast",
      source: "Goa",
      destination: "Pune",
      departureTime: "12:29",
      arrivalTime: "10:11",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T038",
      trainName: "Hampi Heritage Express",
      source: "Hampi",
      destination: "Bangalore",
      departureTime: "19:30",
      arrivalTime: "06:00",
      totalSeats: 120,
      availableSeats: 108,
    },
    {
      trainId: "T039",
      trainName: "Hampi - Chennai Superfast",
      source: "Hampi",
      destination: "Chennai",
      departureTime: "18:03",
      arrivalTime: "20:57",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T040",
      trainName: "Hampi - Delhi Superfast",
      source: "Hampi",
      destination: "Delhi",
      departureTime: "06:20",
      arrivalTime: "07:20",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T041",
      trainName: "Hampi - Goa Superfast",
      source: "Hampi",
      destination: "Goa",
      departureTime: "09:37",
      arrivalTime: "12:43",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T042",
      trainName: "Hampi - Kolkata Superfast",
      source: "Hampi",
      destination: "Kolkata",
      departureTime: "12:54",
      arrivalTime: "17:06",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T043",
      trainName: "Hampi - Mumbai Superfast",
      source: "Hampi",
      destination: "Mumbai",
      departureTime: "15:11",
      arrivalTime: "22:29",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T044",
      trainName: "Hampi - Mysuru Superfast",
      source: "Hampi",
      destination: "Mysuru",
      departureTime: "18:28",
      arrivalTime: "09:52",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T045",
      trainName: "Hampi - Pune Superfast",
      source: "Hampi",
      destination: "Pune",
      departureTime: "06:45",
      arrivalTime: "14:15",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T046",
      trainName: "Howrah - Bangalore Express",
      source: "Kolkata",
      destination: "Bangalore",
      departureTime: "16:15",
      arrivalTime: "04:00",
      totalSeats: 220,
      availableSeats: 208,
    },
    {
      trainId: "T047",
      trainName: "Coromandel Express (Return)",
      source: "Kolkata",
      destination: "Chennai",
      departureTime: "14:50",
      arrivalTime: "16:40",
      totalSeats: 240,
      availableSeats: 228,
    },
    {
      trainId: "T048",
      trainName: "Kolkata - Delhi Superfast",
      source: "Kolkata",
      destination: "Delhi",
      departureTime: "15:36",
      arrivalTime: "11:24",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T049",
      trainName: "Kolkata - Goa Superfast",
      source: "Kolkata",
      destination: "Goa",
      departureTime: "18:53",
      arrivalTime: "16:47",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T050",
      trainName: "Kolkata - Hampi Superfast",
      source: "Kolkata",
      destination: "Hampi",
      departureTime: "06:10",
      arrivalTime: "21:10",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T051",
      trainName: "Gitanjali Express",
      source: "Kolkata",
      destination: "Mumbai",
      departureTime: "14:05",
      arrivalTime: "21:20",
      totalSeats: 240,
      availableSeats: 228,
    },
    {
      trainId: "T052",
      trainName: "Kolkata - Mysuru Superfast",
      source: "Kolkata",
      destination: "Mysuru",
      departureTime: "12:44",
      arrivalTime: "13:56",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T053",
      trainName: "Kolkata - Pune Superfast",
      source: "Kolkata",
      destination: "Pune",
      departureTime: "15:01",
      arrivalTime: "18:19",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T054",
      trainName: "Udyan Express",
      source: "Mumbai",
      destination: "Bangalore",
      departureTime: "08:15",
      arrivalTime: "09:00",
      totalSeats: 200,
      availableSeats: 188,
    },
    {
      trainId: "T055",
      trainName: "Mumbai - Chennai Superfast",
      source: "Mumbai",
      destination: "Chennai",
      departureTime: "06:35",
      arrivalTime: "10:05",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T056",
      trainName: "Konkan Kanya Express",
      source: "Mumbai",
      destination: "Goa",
      departureTime: "23:05",
      arrivalTime: "10:45",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T057",
      trainName: "Mumbai - Hampi Superfast",
      source: "Mumbai",
      destination: "Hampi",
      departureTime: "12:09",
      arrivalTime: "20:51",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T058",
      trainName: "Mumbai - Mysuru Superfast",
      source: "Mumbai",
      destination: "Mysuru",
      departureTime: "15:26",
      arrivalTime: "07:14",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T059",
      trainName: "Pragati Express",
      source: "Mumbai",
      destination: "Pune",
      departureTime: "16:25",
      arrivalTime: "19:35",
      totalSeats: 150,
      availableSeats: 138,
    },
    {
      trainId: "T060",
      trainName: "Chamundi Express",
      source: "Mysuru",
      destination: "Bangalore",
      departureTime: "06:45",
      arrivalTime: "09:30",
      totalSeats: 160,
      availableSeats: 148,
    },
    {
      trainId: "T061",
      trainName: "Mysuru - Delhi Superfast",
      source: "Mysuru",
      destination: "Delhi",
      departureTime: "09:17",
      arrivalTime: "22:23",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T062",
      trainName: "Mysuru - Goa Superfast",
      source: "Mysuru",
      destination: "Goa",
      departureTime: "12:34",
      arrivalTime: "09:46",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T063",
      trainName: "Mysuru - Hampi Superfast",
      source: "Mysuru",
      destination: "Hampi",
      departureTime: "15:51",
      arrivalTime: "14:09",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T064",
      trainName: "Mysuru - Kolkata Superfast",
      source: "Mysuru",
      destination: "Kolkata",
      departureTime: "18:08",
      arrivalTime: "19:32",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T065",
      trainName: "Mysuru - Mumbai Superfast",
      source: "Mysuru",
      destination: "Mumbai",
      departureTime: "06:25",
      arrivalTime: "06:55",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T066",
      trainName: "Mysuru - Pune Superfast",
      source: "Mysuru",
      destination: "Pune",
      departureTime: "09:42",
      arrivalTime: "11:18",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T067",
      trainName: "Pune - Bangalore Express",
      source: "Pune",
      destination: "Bangalore",
      departureTime: "17:30",
      arrivalTime: "09:15",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T068",
      trainName: "Pune - Chennai Superfast",
      source: "Pune",
      destination: "Chennai",
      departureTime: "15:16",
      arrivalTime: "21:04",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T069",
      trainName: "Pune - Delhi Superfast",
      source: "Pune",
      destination: "Delhi",
      departureTime: "18:33",
      arrivalTime: "08:27",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T070",
      trainName: "Pune - Goa Superfast",
      source: "Pune",
      destination: "Goa",
      departureTime: "06:50",
      arrivalTime: "13:50",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T071",
      trainName: "Pune - Hampi Superfast",
      source: "Pune",
      destination: "Hampi",
      departureTime: "09:07",
      arrivalTime: "18:13",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T072",
      trainName: "Pune - Kolkata Superfast",
      source: "Pune",
      destination: "Kolkata",
      departureTime: "12:24",
      arrivalTime: "05:36",
      totalSeats: 180,
      availableSeats: 168,
    },
    {
      trainId: "T073",
      trainName: "Pune - Mysuru Superfast",
      source: "Pune",
      destination: "Mysuru",
      departureTime: "15:41",
      arrivalTime: "10:59",
      totalSeats: 180,
      availableSeats: 168,
    },
  ];

  const SEED_RESERVATIONS = [
    {
      reservationId: "RES001",
      trainId: "T001",
      passengerName: "Rahul Sharma",
      passengerAge: 28,
      passengerGender: "M",
      journeyDate: "25-10-2026",
      seatsBooked: 2,
      status: 2, // Cancelled
    },
    {
      reservationId: "RES002",
      trainId: "T002",
      passengerName: "Priya Nair",
      passengerAge: 35,
      passengerGender: "F",
      journeyDate: "26-10-2026",
      seatsBooked: 1,
      status: 1, // Confirmed
    },
    {
      reservationId: "RES003",
      trainId: "T001",
      passengerName: "Vikram Singh",
      passengerAge: 30,
      passengerGender: "M",
      journeyDate: "25-10-2026",
      seatsBooked: 3,
      status: 2, // Cancelled
    },
  ];

  const SEED_SCHEDULES = (function () {
    const list = [];
    const dates = [];
    for (let d = 1; d <= 31; d++)
      dates.push(String(d).padStart(2, "0") + "-10-2026");
    for (let d = 1; d <= 30; d++)
      dates.push(String(d).padStart(2, "0") + "-11-2026");
    for (let d = 1; d <= 31; d++)
      dates.push(String(d).padStart(2, "0") + "-12-2026");
    for (let d = 1; d <= 31; d++)
      dates.push(String(d).padStart(2, "0") + "-01-2027");
    SEED_TRAINS.forEach((t) => {
      dates.forEach((dt) => list.push({ trainId: t.trainId, journeyDate: dt }));
    });
    return list;
  })();

  // ── DOM References ─────────────────────────────────────────────────────────
  const cursorGlow = document.getElementById("cursor-glow");
  const themeToggleBtn = document.getElementById("theme-toggle-btn");
  const trainsContainer = document.getElementById("trains-container");
  const emptyTrainsState = document.getElementById("empty-trains-state");
  const ticketDisplayContainer = document.getElementById(
    "ticket-display-container",
  );

  // Stats Counters
  const statTrainsCount = document.getElementById("stat-trains-count");
  const statSeatsCount = document.getElementById("stat-seats-count");
  const statReservationsCount = document.getElementById(
    "stat-reservations-count",
  );

  // Modals & Overlays
  const bookingModal = document.getElementById("booking-modal");
  const cmdPaletteModal = document.getElementById("cmd-palette-modal");
  const cmdInput = document.getElementById("cmd-input");
  const cmdResultsList = document.getElementById("cmd-results-list");
  const undoToast = document.getElementById("undo-toast");
  const undoBtn = document.getElementById("undo-btn");

  // Forms & Inputs
  const bookingForm = document.getElementById("booking-form");
  const bookTrainSelect = document.getElementById("book-train-select");
  const searchSource = document.getElementById("search-source");
  const searchDest = document.getElementById("search-dest");
  const searchDate = document.getElementById("search-date");
  const lookupIdInput = document.getElementById("lookup-id-input");
  const cancelIdInput = document.getElementById("cancel-id-input");

  // ── 1. Pure JS Lerp Scroll (No External CDN) ────────────────────────────────
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)",
  ).matches;

  let currentScrollY = window.scrollY;
  let targetScrollY = window.scrollY;
  let isScrolling = false;

  if (!prefersReducedMotion) {
    window.addEventListener(
      "wheel",
      (e) => {
        // Allow user smooth wheel interpolation
        targetScrollY += e.deltaY;
        targetScrollY = Math.max(
          0,
          Math.min(
            targetScrollY,
            document.documentElement.scrollHeight - window.innerHeight,
          ),
        );
        if (!isScrolling) {
          isScrolling = true;
          requestAnimationFrame(updateScroll);
        }
      },
      { passive: true },
    );

    function updateScroll() {
      const diff = targetScrollY - currentScrollY;
      currentScrollY += diff * 0.12; // 0.12 lerp factor for buttery smooth feel

      if (Math.abs(diff) > 0.5) {
        window.scrollTo(0, currentScrollY);
        requestAnimationFrame(updateScroll);
      } else {
        window.scrollTo(0, targetScrollY);
        currentScrollY = targetScrollY;
        isScrolling = false;
      }
    }
  }

  // Sync scroll target when user drags native scrollbar
  window.addEventListener(
    "scroll",
    () => {
      if (!isScrolling) {
        currentScrollY = window.scrollY;
        targetScrollY = window.scrollY;
      }
    },
    { passive: true },
  );

  // ── 2. Ambient Specular Cursor Glow & Magnetic CTA Buttons ─────────────────
  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let glowX = mouseX;
  let glowY = mouseY;

  window.addEventListener(
    "mousemove",
    (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    },
    { passive: true },
  );

  function renderCursorGlow() {
    glowX += (mouseX - glowX) * 0.15;
    glowY += (mouseY - glowY) * 0.15;
    if (cursorGlow) {
      cursorGlow.style.left = `${glowX}px`;
      cursorGlow.style.top = `${glowY}px`;
    }
    requestAnimationFrame(renderCursorGlow);
  }
  requestAnimationFrame(renderCursorGlow);

  // Magnetic CTAs (6px lerp following cursor, pure JS)
  function initMagneticButtons() {
    const magneticBtns = document.querySelectorAll(".magnetic-btn");
    magneticBtns.forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        if (prefersReducedMotion) return;
        const rect = btn.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const deltaX = (e.clientX - centerX) * 0.25;
        const deltaY = (e.clientY - centerY) * 0.25;
        const clampedX = Math.max(-6, Math.min(6, deltaX));
        const clampedY = Math.max(-6, Math.min(6, deltaY));
        btn.style.transform = `translate3d(${clampedX}px, ${clampedY}px, 0) scale(1.02)`;
      });

      btn.addEventListener("mouseleave", () => {
        btn.style.transform = `translate3d(0, 0, 0) scale(1)`;
      });
    });
  }

  // ── 3. Theme Toggle with View Transitions API Circular Reveal ──────────────
  function initTheme() {
    const savedTheme = localStorage.getItem("velocity_theme");
    if (savedTheme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
      state.isDarkMode = true;
    } else {
      document.documentElement.setAttribute("data-theme", "light");
      state.isDarkMode = false;
    }
  }

  function toggleTheme(event) {
    const willBeDark = !state.isDarkMode;

    const applyTheme = () => {
      if (willBeDark) {
        document.documentElement.setAttribute("data-theme", "dark");
        state.isDarkMode = true;
        localStorage.setItem("velocity_theme", "dark");
      } else {
        document.documentElement.setAttribute("data-theme", "light");
        state.isDarkMode = false;
        localStorage.setItem("velocity_theme", "light");
      }
    };

    if (!document.startViewTransition || prefersReducedMotion || !event) {
      applyTheme();
      return;
    }

    const x = event.clientX;
    const y = event.clientY;
    const endRadius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y),
    );

    const transition = document.startViewTransition(() => {
      applyTheme();
    });

    transition.ready.then(() => {
      document.documentElement.animate(
        {
          clipPath: [
            `circle(0px at ${x}px ${y}px)`,
            `circle(${endRadius}px at ${x}px ${y}px)`,
          ],
        },
        {
          duration: 450,
          easing: "cubic-bezier(0.16, 1, 0.3, 1)",
          pseudoElement: "::view-transition-new(root)",
        },
      );
    });
  }

  themeToggleBtn.addEventListener("click", toggleTheme);

  // ── 4. 60FPS Stagger Entrance Observer ──────────────────────────────────────
  function initEntranceObserver() {
    const elements = document.querySelectorAll(".stagger-in");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 },
    );

    elements.forEach((el, index) => {
      el.style.transitionDelay = `${index * 70}ms`;
      observer.observe(el);
    });
  }

  // ── 5. Data Layer (API / Seed Fallback) ─────────────────────────────────────
  async function loadData() {
    try {
      const [trainsRes, reservationsRes, schedulesRes] = await Promise.all([
        fetch("/api/trains")
          .then((r) => r.json())
          .catch(() => null),
        fetch("/api/reservations")
          .then((r) => r.json())
          .catch(() => null),
        fetch("/api/schedules")
          .then((r) => r.json())
          .catch(() => null),
      ]);

      if (
        trainsRes &&
        trainsRes.success &&
        trainsRes.data &&
        trainsRes.data.length > 0
      ) {
        state.trains = trainsRes.data;
      } else {
        state.trains = JSON.parse(JSON.stringify(SEED_TRAINS));
      }

      if (
        reservationsRes &&
        reservationsRes.success &&
        reservationsRes.data &&
        reservationsRes.data.length > 0
      ) {
        state.reservations = reservationsRes.data;
      } else {
        state.reservations = JSON.parse(JSON.stringify(SEED_RESERVATIONS));
      }

      if (schedulesRes && schedulesRes.success && schedulesRes.data) {
        state.schedules = schedulesRes.data;
      } else {
        state.schedules = JSON.parse(JSON.stringify(SEED_SCHEDULES));
      }
    } catch (err) {
      console.warn(
        "API unavailable, running with synchronized in-memory database:",
        err,
      );
      state.trains = JSON.parse(JSON.stringify(SEED_TRAINS));
      state.reservations = JSON.parse(JSON.stringify(SEED_RESERVATIONS));
      state.schedules = JSON.parse(JSON.stringify(SEED_SCHEDULES));
    }

    updateStats();
    populateStationSelects();
    populateTrainSelect();
    renderTrains(state.trains);
    renderInitialTicket();
  }

  function updateStats() {
    if (statTrainsCount) statTrainsCount.textContent = state.trains.length;

    const totalCapacity = state.trains.reduce(
      (sum, t) => sum + (t.totalSeats || 0),
      0,
    );
    if (statSeatsCount) statSeatsCount.textContent = totalCapacity;

    const confirmedCount = state.reservations.filter(
      (r) => r.status === 1,
    ).length;
    if (statReservationsCount)
      statReservationsCount.textContent = confirmedCount;
  }

  function populateTrainSelect() {
    bookTrainSelect.innerHTML = "";
    state.trains.forEach((train) => {
      const opt = document.createElement("option");
      opt.value = train.trainId;
      opt.textContent = `${train.trainId} — ${train.trainName} (${train.source} → ${train.destination} | ${train.totalSeats} seats per journey)`;
      bookTrainSelect.appendChild(opt);
    });
  }

  function populateStationSelects() {
    const selectedOrigin = searchSource.value;
    const selectedDestination = searchDest.value;
    const routes = state.trains.filter(
      (train) =>
        (!selectedOrigin || train.source === selectedOrigin) &&
        (!selectedDestination || train.destination === selectedDestination),
    );
    const validOrigin = routes.some((train) => train.source === selectedOrigin)
      ? selectedOrigin
      : "";
    const validDestination = routes.some(
      (train) => train.destination === selectedDestination,
    )
      ? selectedDestination
      : "";
    const origins = [
      ...new Set(
        state.trains
          .filter(
            (train) =>
              !validDestination || train.destination === validDestination,
          )
          .map((train) => train.source),
      ),
    ].sort((a, b) => a.localeCompare(b));
    const destinations = [
      ...new Set(
        state.trains
          .filter((train) => !validOrigin || train.source === validOrigin)
          .map((train) => train.destination),
      ),
    ].sort((a, b) => a.localeCompare(b));

    [
      [searchSource, "Choose origin", origins, validOrigin],
      [searchDest, "Choose destination", destinations, validDestination],
    ].forEach(([select, placeholder, stations, selected]) => {
      select.innerHTML = "";
      const placeholderOption = document.createElement("option");
      placeholderOption.value = "";
      placeholderOption.textContent = placeholder;
      placeholderOption.disabled = true;
      select.appendChild(placeholderOption);

      stations.forEach((station) => {
        const option = document.createElement("option");
        option.value = station;
        option.textContent = station;
        select.appendChild(option);
      });
      select.value = selected;
      if (!selected) placeholderOption.selected = true;
    });
  }

  function availableSeatsForDate(train, date) {
    if (!train || !date) return train ? train.totalSeats : 0;
    const confirmedSeats = state.reservations.reduce((sum, reservation) => {
      if (
        reservation.trainId === train.trainId &&
        reservation.journeyDate === date &&
        reservation.status === 1
      ) {
        return sum + reservation.seatsBooked;
      }
      return sum;
    }, 0);
    return Math.max(0, train.totalSeats - confirmedSeats);
  }

  function parseJourneyDate(dateStr) {
    const match = /^(\d{2})-(\d{2})-(\d{4})$/.exec(dateStr || "");
    if (!match) return null;
    const date = new Date(
      Number(match[3]),
      Number(match[2]) - 1,
      Number(match[1]),
    );
    if (
      date.getFullYear() !== Number(match[3]) ||
      date.getMonth() !== Number(match[2]) - 1 ||
      date.getDate() !== Number(match[1])
    )
      return null;
    date.setHours(0, 0, 0, 0);
    return date;
  }

  function isDepartureTimeUpcoming(train, dateStr) {
    const journeyDate = parseJourneyDate(dateStr);
    const now = new Date();
    if (!journeyDate) return false;

    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    if (journeyDate > today) return true;
    if (journeyDate < today) return false;

    const time = /^(\d{2}):(\d{2})$/.exec(train?.departureTime || "");
    if (!time) return false;
    const departureMinutes = Number(time[1]) * 60 + Number(time[2]);
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    return departureMinutes > currentMinutes;
  }

  // ── 6. Train Cards Rendering ───────────────────────────────────────────────
  function renderTrains(trains) {
    trainsContainer.innerHTML = "";

    if (!trains || trains.length === 0) {
      emptyTrainsState.style.display = "block";
      document.getElementById("reset-filters-btn").style.display = "none";
      return;
    }
    emptyTrainsState.style.display = "none";

    const visibleTrains = state.showAllTrains ? trains : trains.slice(0, 3);
    const viewAllButton = document.getElementById("reset-filters-btn");
    viewAllButton.style.display = trains.length > 3 ? "" : "none";
    viewAllButton.textContent = state.showAllTrains
      ? "Show Featured Lines"
      : "View All Lines";
    viewAllButton.setAttribute("aria-expanded", String(state.showAllTrains));

    // Accent colors cycle
    const accents = [
      "var(--c-marigold)",
      "var(--c-electric-lavender)",
      "var(--c-lemon)",
      "var(--c-pale-lavender)",
    ];

    visibleTrains.forEach((train, idx) => {
      const card = document.createElement("div");
      card.className = "train-card stagger-in";
      card.style.setProperty("--card-accent", accents[idx % accents.length]);

      const journeyDate = searchDate.value.trim();
      const availableSeats = availableSeatsForDate(train, journeyDate);
      const isLowSeats = availableSeats <= 20;

      card.innerHTML = `
        <div>
          <div class="train-card-top">
            <span class="train-badge-id">${escapeHtml(train.trainId)}</span>
            <span class="label-caps" style="color: ${accents[idx % accents.length]};">DAILY EXPRESS</span>
          </div>

          <h3 class="train-name">${escapeHtml(train.trainName)}</h3>

          <div class="route-indicator">
            <div class="station-node">
              <div class="station-name">${escapeHtml(train.source)}</div>
              <div class="station-time">${escapeHtml(train.departureTime)}</div>
            </div>

            <div class="route-track">
              <span class="label-caps" style="font-size: 9px;">DIRECT RUN</span>
              <div class="route-line"></div>
            </div>

            <div class="station-node destination">
              <div class="station-name">${escapeHtml(train.destination)}</div>
              <div class="station-time">${escapeHtml(train.arrivalTime)}</div>
            </div>
          </div>
        </div>

        <div class="train-meta-row">
          <div class="seats-badge ${isLowSeats ? "low" : ""}">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 18v3"></path><path d="M20 18v3"></path><path d="M19 10v7H5v-7"></path><path d="M15 4H9v6h6V4z"></path></svg>
            <span>${availableSeats} ${journeyDate ? "berths open" : "seats per journey"}</span>
          </div>

          <button class="btn-primary magnetic-btn book-line-btn" data-train-id="${train.trainId}">
            <span>Book Seat</span>
          </button>
        </div>
      `;

      trainsContainer.appendChild(card);
    });

    initMagneticButtons();
    initEntranceObserver();

    // Hook book buttons
    document.querySelectorAll(".book-line-btn").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        const trainId = e.currentTarget.getAttribute("data-train-id");
        openBookingModal(trainId);
      });
    });
  }

  // ── 7. Filtering & Shimmer Skeletons ────────────────────────────────────────
  function filterTrains() {
    const src = searchSource.value.trim().toLowerCase();
    const dest = searchDest.value.trim().toLowerCase();
    const date = searchDate.value.trim();

    // Render skeleton shimmer while filtering
    trainsContainer.innerHTML = `
      <div class="stat-card skeleton" style="height: 280px;"></div>
      <div class="stat-card skeleton" style="height: 280px;"></div>
    `;

    setTimeout(() => {
      const filtered = state.trains.filter((t) => {
        const matchSrc = !src || t.source.toLowerCase().includes(src);
        const matchDest = !dest || t.destination.toLowerCase().includes(dest);

        const matchDate =
          !date ||
          (state.schedules.some(
            (s) => s.trainId === t.trainId && s.journeyDate === date,
          ) &&
            isDepartureTimeUpcoming(t, date));

        return matchSrc && matchDest && matchDate;
      });

      renderTrains(filtered);
      document
        .getElementById("trains-section")
        .scrollIntoView({ behavior: "smooth", block: "start" });
    }, 180);
  }

  function handleSearchRouteChange() {
    populateStationSelects();
    if (searchDate.value && !datePicker.isDateSelectable(searchDate.value)) {
      searchDate.value = "";
    }
  }

  searchSource.addEventListener("change", handleSearchRouteChange);
  searchDest.addEventListener("change", handleSearchRouteChange);

  document
    .getElementById("filter-trains-btn")
    .addEventListener("click", filterTrains);
  document.getElementById("reset-filters-btn").addEventListener("click", () => {
    if (state.showAllTrains) {
      state.showAllTrains = false;
    } else {
      searchSource.value = "";
      searchDest.value = "";
      populateStationSelects();
      searchDate.value = "";
      state.showAllTrains = true;
    }
    renderTrains(state.trains);
  });
  document.getElementById("empty-reset-btn").addEventListener("click", () => {
    searchSource.value = "";
    searchDest.value = "";
    populateStationSelects();
    searchDate.value = "";
    state.showAllTrains = true;
    renderTrains(state.trains);
  });

  // ── 8. Digital Boarding Pass Ticket Rendering (Live Backend Integration) ──
  function renderInitialTicket() {
    ticketDisplayContainer.innerHTML = `
      <div style="text-align: center; padding: 48px 32px; background: var(--surface-card); border-radius: var(--radius-card); border: 1px dashed var(--border-card); max-width: 680px; width: 100%; margin: 0 auto; box-shadow: var(--shadow-resting);">
        <div class="stat-icon avatar-marigold" style="margin: 0 auto 16px; width: 52px; height: 52px; font-size: 20px;">🎟️</div>
        <span class="label-caps" style="color: var(--c-marigold);">OFFICIAL PASS VAULT</span>
        <h3 style="font-family: var(--font-serif); font-size: 26px; margin: 10px 0 8px; color: var(--text-primary);">Retrieve Digital Boarding Pass</h3>
        <p style="color: var(--text-secondary); max-width: 480px; margin: 0 auto; font-size: 14px; line-height: 1.6;">
          Enter your Reservation ID above and click <strong>Retrieve Pass</strong> to view, print, or manage your official journey pass.
        </p>
      </div>
    `;
  }

  async function fetchAndDisplayTicket(reservationId) {
    const query = (reservationId || "").trim().toUpperCase();
    if (!query) {
      alert("Please enter a valid Reservation ID (e.g. RES002).");
      return;
    }

    // Show luxury loading skeleton while querying backend
    ticketDisplayContainer.innerHTML = `
      <div class="stat-card skeleton" style="max-width: 680px; width: 100%; height: 380px; margin: 0 auto; border-radius: 32px;"></div>
    `;

    try {
      // Query backend API directly (reads fresh from data/reservations.dat and data/trains.dat)
      const res = await fetch(
        `/api/reservation?id=${encodeURIComponent(query)}`,
      );
      const data = await res.json();

      if (data && data.success && data.reservation) {
        displayTicketPass(data.reservation, data.train);
        ticketDisplayContainer.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      } else {
        throw new Error(
          data.error || `Reservation ${query} not found in database.`,
        );
      }
    } catch (err) {
      // Fallback: check in-memory cache if offline
      const local = state.reservations.find(
        (r) => r.reservationId.toUpperCase() === query,
      );
      if (local) {
        const train = state.trains.find((t) => t.trainId === local.trainId);
        displayTicketPass(local, train);
        ticketDisplayContainer.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      } else {
        ticketDisplayContainer.innerHTML = `
          <div style="text-align: center; padding: 48px 32px; background: var(--surface-card); border-radius: var(--radius-card); border: 1px solid var(--border-card); max-width: 600px; width: 100%; margin: 0 auto; box-shadow: var(--shadow-resting);">
            <div style="font-size: 40px; margin-bottom: 12px;">🔍</div>
            <span class="status-pill status-cancelled" style="margin-bottom: 12px;">BACKEND VERIFICATION: NOT FOUND</span>
            <h3 style="font-family: var(--font-serif); font-size: 24px; margin: 8px 0; color: var(--text-primary);">Reservation ${escapeHtml(query)} Not Found</h3>
            <p style="color: var(--text-secondary); font-size: 14px; line-height: 1.6; max-width: 440px; margin: 0 auto 20px;">
              No record matching reference "${escapeHtml(query)}" exists in <code>data/reservations.dat</code>. Please check your reservation ID or book a new journey.
            </p>
            <button type="button" class="btn-primary magnetic-btn" id="retry-search-btn">
              <span>Try Another ID</span>
            </button>
          </div>
        `;

        document
          .getElementById("retry-search-btn")
          ?.addEventListener("click", () => {
            lookupIdInput.value = "";
            lookupIdInput.focus();
            renderInitialTicket();
          });
      }
    }
  }

  function displayTicketPass(res, trainData) {
    const train = trainData ||
      state.trains.find((t) => t.trainId === res.trainId) || {
        trainName: "Express Service",
        source: "Origin",
        destination: "Destination",
        departureTime: "--:--",
        arrivalTime: "--:--",
      };

    const isConfirmed = res.status === 1;

    ticketDisplayContainer.innerHTML = `
      <div class="luxury-ticket">
        <div class="ticket-header-band">
          <div>
            <span class="label-caps" style="color: var(--c-lemon);">OFFICIAL BOARDING PASS · BACKEND VERIFIED</span>
            <div style="font-family: var(--font-serif); font-size: 24px; margin-top: 4px;">${escapeHtml(train.trainName)}</div>
          </div>
          <div style="text-align: right;">
            <span class="label-caps" style="color: var(--c-platinum); opacity: 0.8;">PASSENGER PASS ID</span>
            <div style="font-family: var(--font-mono); font-size: 18px; font-weight: 700; color: var(--c-marigold);">${escapeHtml(res.reservationId)}</div>
          </div>
        </div>

        <div class="ticket-body">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <div>
              <div class="label-caps">PASSENGER NAME</div>
              <div style="font-size: 22px; font-weight: 700; color: var(--text-primary); margin-top: 2px;">
                ${escapeHtml(res.passengerName)}
              </div>
            </div>

            <div class="status-pill ${isConfirmed ? "status-confirmed" : "status-cancelled"}">
              <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: currentColor;"></span>
              <span>${isConfirmed ? "CONFIRMED" : "CANCELLED"}</span>
            </div>
          </div>

          <div class="route-indicator" style="padding: 16px 0; margin-bottom: 24px;">
            <div class="station-node">
              <div class="label-caps">DEPARTURE</div>
              <div class="station-name">${escapeHtml(train.source)}</div>
              <div class="station-time">${escapeHtml(train.departureTime)}</div>
            </div>

            <div class="route-track">
              <span class="label-caps" style="font-size: 9px;">TRAIN ${escapeHtml(res.trainId)}</span>
              <div class="route-line"></div>
            </div>

            <div class="station-node destination">
              <div class="label-caps">ARRIVAL</div>
              <div class="station-name">${escapeHtml(train.destination)}</div>
              <div class="station-time">${escapeHtml(train.arrivalTime)}</div>
            </div>
          </div>

          <div class="ticket-perforation">
            <div class="perforation-circle-left"></div>
            <div class="perforation-line"></div>
            <div class="perforation-circle-right"></div>
          </div>

          <div class="ticket-grid">
            <div>
              <div class="label-caps">JOURNEY DATE</div>
              <div style="font-weight: 600; font-size: 16px; margin-top: 4px;">${escapeHtml(res.journeyDate)}</div>
            </div>
            <div>
              <div class="label-caps">PASSENGER AGE / GENDER</div>
              <div style="font-weight: 600; font-size: 16px; margin-top: 4px;">${res.passengerAge} yrs / ${escapeHtml(res.passengerGender)}</div>
            </div>
            <div>
              <div class="label-caps">RESERVED SEATS</div>
              <div style="font-weight: 600; font-size: 16px; margin-top: 4px; color: var(--c-marigold);">${res.seatsBooked} Seat(s)</div>
            </div>
          </div>
          <div>
  <div class="label-caps">AVAILABLE SEATS AFTER BOOKING</div>
  <div style="font-weight: 600; font-size: 16px; margin-top: 4px; color: var(--text-primary);">
    ${isConfirmed ? availableSeatsForDate(train, res.journeyDate) : "—"} Seat(s)
  </div>
</div>

          <div class="ticket-barcode-wrap">
            <div class="barcode-graphic" aria-hidden="true"></div>
            <div style="display: flex; gap: 12px;">
              <button type="button" class="btn-secondary" id="print-ticket-btn">
                <span>Print Pass</span>
              </button>
              ${
                isConfirmed
                  ? `
                <button type="button" class="btn-danger cancel-this-ticket-btn" data-res-id="${res.reservationId}">
                  <span>Cancel Ticket</span>
                </button>
              `
                  : ""
              }
            </div>
          </div>
        </div>
      </div>
    `;

    // Hook buttons inside ticket
    document
      .getElementById("print-ticket-btn")
      ?.addEventListener("click", () => {
        window.print();
      });

    const cancelBtn = ticketDisplayContainer.querySelector(
      ".cancel-this-ticket-btn",
    );
    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        executeCancellation(res.reservationId);
      });
    }
  }

  // Lookup button click & Enter key
  document.getElementById("lookup-btn").addEventListener("click", () => {
    fetchAndDisplayTicket(lookupIdInput.value);
  });

  lookupIdInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      fetchAndDisplayTicket(lookupIdInput.value);
    }
  });

  // ── 9. Booking Flow ────────────────────────────────────────────────────────
  function openBookingModal(trainId) {
    if (trainId) bookTrainSelect.value = trainId;
    document.getElementById("booking-error-msg").style.display = "none";
    bookingModal.classList.add("active");
    document.getElementById("book-passenger-name").focus();
  }

  function closeBookingModal() {
    bookingModal.classList.remove("active");
  }

  document
    .getElementById("hero-book-btn")
    .addEventListener("click", () => openBookingModal());
  document
    .getElementById("close-booking-modal")
    .addEventListener("click", closeBookingModal);
  document
    .getElementById("cancel-booking-btn")
    .addEventListener("click", closeBookingModal);

  bookingForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("booking-error-msg");
    errorEl.style.display = "none";

    const trainId = bookTrainSelect.value;
    const name = document.getElementById("book-passenger-name").value.trim();
    const age = parseInt(
      document.getElementById("book-passenger-age").value,
      10,
    );
    const gender = document.getElementById("book-passenger-gender").value;
    const date = document.getElementById("book-journey-date").value.trim();
    const seats = parseInt(
      document.getElementById("book-seat-count").value,
      10,
    );

    // Validation matching C++ rules
    if (!name || name.length > 60 || !/^[A-Za-z ]+$/.test(name)) {
      errorEl.textContent =
        "Please enter a valid passenger name containing only letters and spaces.";
      errorEl.style.display = "block";
      return;
    }

    if (isNaN(age) || age < 1 || age > 120) {
      errorEl.textContent = "Age must be between 1 and 120 years.";
      errorEl.style.display = "block";
      return;
    }

    if (!/^\d{2}-\d{2}-\d{4}$/.test(date)) {
      errorEl.textContent = "Date format must be DD-MM-YYYY (e.g. 25-10-2026).";
      errorEl.style.display = "block";
      return;
    }

    const train = state.trains.find((t) => t.trainId === trainId);
    const availableSeats = availableSeatsForDate(train, date);
    if (!isDepartureTimeUpcoming(train, date)) {
      errorEl.textContent =
        "Choose a journey date and departure time that have not passed.";
      errorEl.style.display = "block";
      return;
    }
    if (
      !train ||
      !state.schedules.some(
        (s) => s.trainId === trainId && s.journeyDate === date,
      )
    ) {
      errorEl.textContent =
        "This express line is not scheduled for the selected date.";
      errorEl.style.display = "block";
      return;
    }
    if (seats > availableSeats) {
      errorEl.textContent = `Not enough seats available. Berths remaining for this date: ${availableSeats}`;
      errorEl.style.display = "block";
      return;
    }

    // The API is authoritative for inventory and persists the reservation.
    try {
      const res = await fetch("/api/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ trainId, name, age, gender, date, seats }),
      });
      const data = await res.json();

      if (!res.ok || !data || !data.success || !data.reservation) {
        throw new Error(data?.error || "Booking failed.");
      }
      state.reservations.push(data.reservation);
      lookupIdInput.value = data.reservation.reservationId;
      displayTicketPass(data.reservation, data.train);
    } catch (err) {
      errorEl.textContent =
        err.message || "Booking could not be saved. Try again.";
      errorEl.style.display = "block";
      return;
    }

    updateStats();
    populateTrainSelect();
    renderTrains(state.trains);
    closeBookingModal();
    bookingForm.reset();

    // Scroll to ticket pass
    document
      .getElementById("lookup-section")
      .scrollIntoView({ behavior: "smooth" });
  });

  // ── 10. Cancellation Flow with 4-Second Undo Toast ───────────────────────────
  async function executeCancellation(reservationId) {
    if (state.cancellationPendingIds.has(reservationId)) return;
    const res = state.reservations.find(
      (r) => r.reservationId === reservationId,
    );
    if (!res) {
      alert(`Reservation ${reservationId} not found.`);
      return;
    }

    if (res.status === 2) {
      alert(`Reservation ${reservationId} is already cancelled.`);
      return;
    }

    const confirmCancel = confirm(
      `Are you sure you wish to cancel ticket ${reservationId} for ${res.passengerName}?`,
    );
    if (!confirmCancel) return;

    state.cancellationPendingIds.add(reservationId);
    try {
      const response = await fetch("/api/cancel", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reservationId }),
      });
      const data = await response.json();
      if (!response.ok || !data.success || !data.reservation) {
        throw new Error(data.error || "Cancellation could not be saved.");
      }

      Object.assign(res, data.reservation);
      state.lastCancelledReservationId = reservationId;
      updateStats();
      populateTrainSelect();
      renderTrains(state.trains);
      displayTicketPass(res);
      showUndoToast(reservationId, res.seatsBooked);
    } catch (err) {
      alert(err.message || "Cancellation could not be saved. Try again.");
    } finally {
      state.cancellationPendingIds.delete(reservationId);
    }
  }

  document
    .getElementById("cancel-trigger-btn")
    .addEventListener("click", () => {
      const id = cancelIdInput.value.trim().toUpperCase();
      if (!id) return;
      executeCancellation(id);
      cancelIdInput.value = "";
    });

  function showUndoToast(reservationId, seats) {
    clearTimeout(state.undoTimer);
    document.getElementById("undo-toast-text").textContent =
      `Pass ${reservationId} cancelled. ${seats} seat(s) restored.`;
    undoToast.classList.add("active");

    state.undoTimer = setTimeout(() => {
      undoToast.classList.remove("active");
      state.lastCancelledReservationId = null;
    }, 4000);
  }

  undoBtn.addEventListener("click", async () => {
    const resId = state.lastCancelledReservationId;
    if (!resId || state.undoPending) return;

    const res = state.reservations.find((r) => r.reservationId === resId);
    if (res) {
      state.undoPending = true;
      undoBtn.disabled = true;
      try {
        const response = await fetch("/api/undo_cancel", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ reservationId: resId }),
        });
        const data = await response.json();
        if (!response.ok || !data.success || !data.reservation) {
          throw new Error(data.error || "Reservation could not be restored.");
        }

        Object.assign(res, data.reservation);
        updateStats();
        populateTrainSelect();
        renderTrains(state.trains);
        displayTicketPass(res);
        clearTimeout(state.undoTimer);
        undoToast.classList.remove("active");
        state.lastCancelledReservationId = null;
      } catch (err) {
        alert(err.message || "Reservation could not be restored. Try again.");
      } finally {
        state.undoPending = false;
        undoBtn.disabled = false;
      }
    }
  });

  // ── 11. Command Palette (CMD+K / Ctrl+K) ────────────────────────────────────
  function openCmdPalette() {
    cmdPaletteModal.classList.add("active");
    cmdInput.value = "";
    renderCmdResults("");
    cmdInput.focus();
  }

  function closeCmdPalette() {
    cmdPaletteModal.classList.remove("active");
  }

  document
    .getElementById("open-cmd-btn")
    .addEventListener("click", openCmdPalette);

  function renderCmdResults(query) {
    const q = query.trim().toLowerCase();
    cmdResultsList.innerHTML = "";
    state.selectedCmdIndex = 0;

    const actions = [
      {
        id: "act-book",
        label: "Issue New Ticket",
        badge: "Key N",
        run: () => openBookingModal(),
      },
      {
        id: "act-theme",
        label: "Toggle Light / Dark Theme",
        badge: "Action",
        run: () => toggleTheme(),
      },
      {
        id: "act-routes",
        label: "Browse Express Lines",
        badge: "Route",
        run: () =>
          document
            .getElementById("trains-section")
            .scrollIntoView({ behavior: "smooth" }),
      },
      {
        id: "act-vault",
        label: "View Boarding Pass",
        badge: "Vault",
        run: () =>
          document
            .getElementById("lookup-section")
            .scrollIntoView({ behavior: "smooth" }),
      },
      {
        id: "act-cancel",
        label: "Open Cancellation Portal",
        badge: "Manage",
        run: () =>
          document
            .getElementById("cancellation-section")
            .scrollIntoView({ behavior: "smooth" }),
      },
    ];

    const matchedActions = actions.filter(
      (a) => !q || a.label.toLowerCase().includes(q),
    );

    // Matched trains
    const matchedTrains = state.trains
      .filter(
        (t) =>
          !q ||
          t.trainName.toLowerCase().includes(q) ||
          t.trainId.toLowerCase().includes(q) ||
          t.source.toLowerCase().includes(q) ||
          t.destination.toLowerCase().includes(q),
      )
      .map((t) => ({
        id: `train-${t.trainId}`,
        label: `${t.trainId} · ${t.trainName} (${t.source} → ${t.destination})`,
        badge: `${t.totalSeats} seats per journey`,
        run: () => openBookingModal(t.trainId),
      }));

    // Matched reservations
    const matchedRes = state.reservations
      .filter(
        (r) =>
          !q ||
          r.reservationId.toLowerCase().includes(q) ||
          r.passengerName.toLowerCase().includes(q),
      )
      .map((r) => ({
        id: `res-${r.reservationId}`,
        label: `Pass ${r.reservationId} · ${r.passengerName} (${r.status === 1 ? "Confirmed" : "Cancelled"})`,
        badge: r.journeyDate,
        run: () => {
          lookupIdInput.value = r.reservationId;
          fetchAndDisplayTicket(r.reservationId);
        },
      }));

    const allItems = [...matchedActions, ...matchedTrains, ...matchedRes];

    if (allItems.length === 0) {
      cmdResultsList.innerHTML = `<li style="padding: 24px; text-align: center; color: var(--text-secondary); font-size: 14px;">No matching results for "${escapeHtml(query)}"</li>`;
      return;
    }

    allItems.slice(0, 8).forEach((item, idx) => {
      const li = document.createElement("li");
      li.className = `cmd-item ${idx === 0 ? "selected" : ""}`;
      li.dataset.index = idx;
      li.innerHTML = `
        <div class="cmd-item-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
          <span>${escapeHtml(item.label)}</span>
        </div>
        <span class="kbd-badge">${escapeHtml(item.badge)}</span>
      `;

      li.addEventListener("click", () => {
        closeCmdPalette();
        item.run();
      });

      cmdResultsList.appendChild(li);
    });
  }

  cmdInput.addEventListener("input", (e) => {
    renderCmdResults(e.target.value);
  });

  // ── 12. Keyboard Navigation ────────────────────────────────────────────────
  window.addEventListener("keydown", (e) => {
    const isCmdOrCtrl = e.metaKey || e.ctrlKey;

    // Cmd+K / Ctrl+K
    if (isCmdOrCtrl && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (cmdPaletteModal.classList.contains("active")) {
        closeCmdPalette();
      } else {
        openCmdPalette();
      }
      return;
    }

    // ESC to close modals
    if (e.key === "Escape") {
      closeCmdPalette();
      closeBookingModal();
      return;
    }

    // If an input is focused, don't trigger hotkeys
    const activeTag = document.activeElement
      ? document.activeElement.tagName.toLowerCase()
      : "";
    if (
      activeTag === "input" ||
      activeTag === "select" ||
      activeTag === "textarea"
    ) {
      // Arrow keys in command palette
      if (cmdPaletteModal.classList.contains("active")) {
        const items = cmdResultsList.querySelectorAll(".cmd-item");
        if (items.length === 0) return;

        if (e.key === "ArrowDown") {
          e.preventDefault();
          state.selectedCmdIndex = (state.selectedCmdIndex + 1) % items.length;
          updateCmdSelection(items);
        } else if (e.key === "ArrowUp") {
          e.preventDefault();
          state.selectedCmdIndex =
            (state.selectedCmdIndex - 1 + items.length) % items.length;
          updateCmdSelection(items);
        } else if (e.key === "Enter") {
          e.preventDefault();
          items[state.selectedCmdIndex]?.click();
        }
      }
      return;
    }

    // Hotkey: '/' -> focus search
    if (e.key === "/") {
      e.preventDefault();
      searchSource.focus();
      return;
    }

    // Hotkey: 'N' -> new booking
    if (e.key.toLowerCase() === "n") {
      e.preventDefault();
      openBookingModal();
      return;
    }
  });

  function updateCmdSelection(items) {
    items.forEach((it, i) => {
      it.classList.toggle("selected", i === state.selectedCmdIndex);
      if (i === state.selectedCmdIndex) {
        it.scrollIntoView({ block: "nearest" });
      }
    });
  }

  // Close modals on overlay backdrop click
  [bookingModal, cmdPaletteModal].forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("active");
      }
    });
  });

  // ── Helper ─────────────────────────────────────────────────────────────────
  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // ── 13. Luxury Visual Calendar Popover (12-Color System) ───────────────────
  class LuxuryDatePicker {
    constructor() {
      this.popup = document.createElement("div");
      this.popup.className = "luxury-datepicker-popup";
      document.body.appendChild(this.popup);

      const today = new Date();
      this.currentViewYear = today.getFullYear();
      this.currentViewMonth = today.getMonth();
      this.targetInput = null;

      this.MONTH_NAMES = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];

      this.initGlobalEvents();
    }

    initGlobalEvents() {
      // Close on outside click
      document.addEventListener("click", (e) => {
        if (!this.popup.classList.contains("active")) return;
        if (
          !this.popup.contains(e.target) &&
          !e.target.closest(".datepicker-input-wrapper")
        ) {
          this.close();
        }
      });

      // Close on escape
      window.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && this.popup.classList.contains("active")) {
          this.close();
        }
      });
    }

    attach(inputElement) {
      if (!inputElement) return;
      const wrapper = inputElement.closest(".datepicker-input-wrapper");
      const triggerBtn = wrapper
        ? wrapper.querySelector(".datepicker-trigger-btn")
        : null;

      const openHandler = (e) => {
        e.stopPropagation();
        this.open(inputElement);
      };

      inputElement.addEventListener("click", openHandler);
      inputElement.addEventListener("focus", openHandler);
      if (triggerBtn) {
        triggerBtn.addEventListener("click", openHandler);
      }
    }

    open(inputElement) {
      this.targetInput = inputElement;

      // If input has a valid DD-MM-YYYY, parse it to show that month
      const val = (inputElement.value || "").trim();
      const selectedDate = parseJourneyDate(val);
      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      if (selectedDate && selectedDate >= today) {
        const parts = val.split("-");
        this.currentViewMonth = parseInt(parts[1], 10) - 1;
        this.currentViewYear = parseInt(parts[2], 10);
      } else {
        this.currentViewYear = today.getFullYear();
        this.currentViewMonth = today.getMonth();
      }

      this.render();
      this.positionPopup(inputElement);
      this.popup.classList.add("active");
    }

    close() {
      this.popup.classList.remove("active");
      this.targetInput = null;
    }

    positionPopup(inputElement) {
      const rect = inputElement.getBoundingClientRect();
      const popupWidth = 320;
      let left = rect.left + window.scrollX;
      let top = rect.bottom + window.scrollY + 8;

      // Prevent overflow off right edge of viewport
      if (left + popupWidth > window.innerWidth - 16) {
        left = window.innerWidth - popupWidth - 24;
      }

      this.popup.style.left = `${Math.max(16, left)}px`;
      this.popup.style.top = `${top}px`;
    }

    isDateSelectable(dateStr) {
      const journeyDate = parseJourneyDate(dateStr);
      if (!journeyDate) return false;

      const now = new Date();
      const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
      if (journeyDate < today) return false;

      // Search accepts any non-past date; availability is resolved after Search.
      if (this.targetInput?.id === "search-date") return true;

      let candidateTrains = state.trains;
      const trainId = bookTrainSelect.value;
      candidateTrains = candidateTrains.filter(
        (train) => train.trainId === trainId,
      );

      return candidateTrains.some(
        (train) =>
          state.schedules.some(
            (schedule) =>
              schedule.trainId === train.trainId &&
              schedule.journeyDate === dateStr,
          ) && isDepartureTimeUpcoming(train, dateStr),
      );
    }

    getQuickDates() {
      if (this.targetInput?.id === "search-date") {
        const today = new Date();
        return [0, 1, 2].map((offset) => {
          const date = new Date(
            today.getFullYear(),
            today.getMonth(),
            today.getDate() + offset,
          );
          return `${String(date.getDate()).padStart(2, "0")}-${String(date.getMonth() + 1).padStart(2, "0")}-${date.getFullYear()}`;
        });
      }

      return [
        ...new Set(state.schedules.map((schedule) => schedule.journeyDate)),
      ]
        .filter((dateStr) => this.isDateSelectable(dateStr))
        .sort((a, b) => parseJourneyDate(a) - parseJourneyDate(b))
        .slice(0, 3);
    }

    render() {
      const year = this.currentViewYear;
      const month = this.currentViewMonth;
      const monthName = this.MONTH_NAMES[month];

      // First day of month (0 = Sun, 1 = Mon...) -> align Monday as 0
      const firstDay = new Date(year, month, 1).getDay();
      const startCol = (firstDay + 6) % 7;
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const daysInPrevMonth = new Date(year, month, 0).getDate();

      // Current input selected day
      let selectedDay = null;
      let selectedMonth = null;
      let selectedYear = null;
      if (
        this.targetInput &&
        /^\d{2}-\d{2}-\d{4}$/.test(this.targetInput.value)
      ) {
        const p = this.targetInput.value.split("-");
        selectedDay = parseInt(p[0], 10);
        selectedMonth = parseInt(p[1], 10) - 1;
        selectedYear = parseInt(p[2], 10);
      }

      let daysHtml = "";

      // Prev month filler cells
      for (let i = startCol - 1; i >= 0; i--) {
        const d = daysInPrevMonth - i;
        daysHtml += `<button type="button" class="datepicker-day-cell other-month" disabled>${d}</button>`;
      }

      // Current month days
      for (let d = 1; d <= daysInMonth; d++) {
        const isSelected =
          selectedDay === d && selectedMonth === month && selectedYear === year;
        const dayStr = String(d).padStart(2, "0");
        const monthStr = String(month + 1).padStart(2, "0");
        const formattedDate = `${dayStr}-${monthStr}-${year}`;

        // Check if there are active timetable schedules for this date
        const isSelectable = this.isDateSelectable(formattedDate);

        daysHtml += `
          <button type="button"
                  class="datepicker-day-cell ${isSelected ? "selected" : ""} ${isSelectable ? "has-schedule" : ""}"
                  data-date="${formattedDate}" ${isSelectable ? "" : "disabled"}>
            ${d}
          </button>
        `;
      }

      // Remaining cells to complete grid
      const totalCells = startCol + daysInMonth;
      const remaining = (7 - (totalCells % 7)) % 7;
      for (let i = 1; i <= remaining; i++) {
        daysHtml += `<button type="button" class="datepicker-day-cell other-month" disabled>${i}</button>`;
      }

      const quickDates = this.getQuickDates();
      const quickDateButtons = quickDates
        .map((dateStr) => {
          const date = parseJourneyDate(dateStr);
          const label = date.toLocaleDateString(undefined, {
            day: "numeric",
            month: "short",
          });
          return `<button type="button" class="datepicker-preset-pill dp-preset" data-date="${dateStr}">${label}</button>`;
        })
        .join("");
      const today = new Date();
      const previousMonth =
        year < today.getFullYear() ||
        (year === today.getFullYear() && month <= today.getMonth());

      this.popup.innerHTML = `
        <div class="datepicker-header">
          <button type="button" class="datepicker-nav-btn" id="dp-prev-month" aria-label="Previous Month" ${previousMonth ? "disabled" : ""}>❮</button>
          <div class="datepicker-month-year">${monthName} ${year}</div>
          <button type="button" class="datepicker-nav-btn" id="dp-next-month" aria-label="Next Month">❯</button>
        </div>

        <div class="datepicker-weekdays">
          <div class="datepicker-weekday">Mo</div>
          <div class="datepicker-weekday">Tu</div>
          <div class="datepicker-weekday">We</div>
          <div class="datepicker-weekday">Th</div>
          <div class="datepicker-weekday">Fr</div>
          <div class="datepicker-weekday">Sa</div>
          <div class="datepicker-weekday">Su</div>
        </div>

        <div class="datepicker-days-grid">
          ${daysHtml}
        </div>

        <div class="datepicker-quick-presets">
          ${quickDateButtons}
          <button type="button" class="datepicker-preset-pill" id="dp-clear-btn" style="color: var(--c-crimson);">Clear</button>
        </div>
      `;

      // Event handlers inside popup
      this.popup
        .querySelector("#dp-prev-month")
        .addEventListener("click", (e) => {
          e.stopPropagation();
          this.currentViewMonth--;
          if (this.currentViewMonth < 0) {
            this.currentViewMonth = 11;
            this.currentViewYear--;
          }
          this.render();
        });

      this.popup
        .querySelector("#dp-next-month")
        .addEventListener("click", (e) => {
          e.stopPropagation();
          this.currentViewMonth++;
          if (this.currentViewMonth > 11) {
            this.currentViewMonth = 0;
            this.currentViewYear++;
          }
          this.render();
        });

      this.popup
        .querySelectorAll(".datepicker-day-cell:not(:disabled)")
        .forEach((btn) => {
          btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const chosenDate = btn.getAttribute("data-date");
            this.selectDate(chosenDate);
          });
        });

      this.popup.querySelectorAll(".dp-preset").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const chosenDate = btn.getAttribute("data-date");
          this.selectDate(chosenDate);
        });
      });

      this.popup
        .querySelector("#dp-clear-btn")
        .addEventListener("click", (e) => {
          e.stopPropagation();
          if (this.targetInput) {
            this.targetInput.value = "";
            this.targetInput.dispatchEvent(
              new Event("input", { bubbles: true }),
            );
            this.targetInput.dispatchEvent(
              new Event("change", { bubbles: true }),
            );
          }
          this.close();
        });
    }

    selectDate(dateStr) {
      if (this.targetInput && this.isDateSelectable(dateStr)) {
        this.targetInput.value = dateStr;
        this.targetInput.dispatchEvent(new Event("input", { bubbles: true }));
        this.targetInput.dispatchEvent(new Event("change", { bubbles: true }));
      }
      this.close();
    }
  }

  // ── Startup ────────────────────────────────────────────────────────────────
  initTheme();
  loadData();
  initMagneticButtons();
  initEntranceObserver();

  // Attach DatePickers
  const datePicker = new LuxuryDatePicker();
  const searchDateInput = document.getElementById("search-date");
  const bookDateInput = document.getElementById("book-journey-date");
  if (searchDateInput) datePicker.attach(searchDateInput);
  if (bookDateInput) datePicker.attach(bookDateInput);
})();
