import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import os

os.makedirs('generated_uml', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. UML USE CASE DIAGRAM (for SRS Figure 1)
# -----------------------------------------------------------------------------
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    ax.text(6, 7.65, "UML Use Case Diagram — Railway Reservation System", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#003366')

    # System Boundary Box
    system_box = FancyBboxPatch((3.2, 0.4), 8.4, 6.9, boxstyle="round,pad=0.1,rounding_size=0.15",
                                ec="#003366", fc="#F8FAFC", lw=2, zorder=1)
    ax.add_patch(system_box)
    ax.text(7.4, 7.05, "Railway Reservation System (System Boundary)", 
            fontsize=12, fontweight='bold', ha='center', va='center', color='#003366')

    # Actor: Passenger / User
    actor_x, actor_y = 1.6, 3.8
    head = Circle((actor_x, actor_y + 0.8), 0.28, ec='#1E293B', fc='#E2E8F0', lw=2, zorder=3)
    ax.add_patch(head)
    ax.plot([actor_x, actor_x], [actor_y + 0.52, actor_y - 0.2], color='#1E293B', lw=2.5, zorder=3)
    ax.plot([actor_x - 0.5, actor_x + 0.5], [actor_y + 0.25, actor_y + 0.25], color='#1E293B', lw=2.5, zorder=3)
    ax.plot([actor_x, actor_x - 0.4], [actor_y - 0.2, actor_y - 0.8], color='#1E293B', lw=2.5, zorder=3)
    ax.plot([actor_x, actor_x + 0.4], [actor_y - 0.2, actor_y - 0.8], color='#1E293B', lw=2.5, zorder=3)
    ax.text(actor_x, actor_y - 1.15, "Passenger / User\n(Primary Actor)", 
            fontsize=11, fontweight='bold', ha='center', va='top', color='#1E293B')

    # Use Cases
    use_cases = [
        ("Search Trains & Routes\n(FR-001 to FR-005)", 5.2, 6.2, 1.55, 0.45),
        ("View Train Schedules & Seats\n(FR-006 to FR-009)", 5.2, 4.9, 1.55, 0.45),
        ("Book Ticket\n(FR-010 to FR-018)", 5.2, 3.6, 1.55, 0.45),
        ("View Reservation\n(FR-019 to FR-023)", 5.2, 2.3, 1.55, 0.45),
        ("Cancel Ticket\n(FR-024 to FR-034)", 5.2, 1.0, 1.55, 0.45),
        ("Validate Input & Bounds\n(«include» / SEC-001)", 9.6, 4.2, 1.6, 0.48),
        ("Update Seat Inventory\n(«include» / NFR-006)", 9.6, 2.2, 1.6, 0.48)
    ]

    for label, cx, cy, rx, ry in use_cases:
        is_include = "include" in label
        fc_col = "#EFF6FF" if not is_include else "#FEF3C7"
        ec_col = "#2563EB" if not is_include else "#D97706"
        txt_col = "#1E3A8A" if not is_include else "#92400E"
        
        ellipse = patches.Ellipse((cx, cy), rx * 2, ry * 2, ec=ec_col, fc=fc_col, lw=1.8, zorder=2)
        ax.add_patch(ellipse)
        ax.text(cx, cy, label, fontsize=9.5, fontweight='bold', ha='center', va='center', color=txt_col, zorder=3)

    # Actor Associations
    primary_targets = [(5.2 - 1.55, 6.2), (5.2 - 1.55, 4.9), (5.2 - 1.55, 3.6), (5.2 - 1.55, 2.3), (5.2 - 1.55, 1.0)]
    for tx, ty in primary_targets:
        ax.annotate("", xy=(tx, ty), xytext=(actor_x + 0.5, actor_y + 0.25),
                    arrowprops=dict(arrowstyle="-", color="#334155", lw=1.6))

    # <<include>> dependencies
    includes = [
        ((5.2 + 1.55, 3.8), (9.6 - 1.6, 4.3)),
        ((5.2 + 1.55, 1.2), (9.6 - 1.6, 3.9)),
        ((5.2 + 1.55, 3.4), (9.6 - 1.6, 2.4)),
        ((5.2 + 1.55, 1.0), (9.6 - 1.6, 2.0))
    ]
    for start, end in includes:
        ax.annotate("", xy=end, xytext=start,
                    arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.4, ls="--"))

    ax.text(7.3, 4.35, "«include»", fontsize=8.5, fontstyle='italic', color='#B45309', ha='center', rotation=8)
    ax.text(7.3, 3.1, "«include»", fontsize=8.5, fontstyle='italic', color='#B45309', ha='center', rotation=-14)
    ax.text(7.3, 1.35, "«include»", fontsize=8.5, fontstyle='italic', color='#B45309', ha='center', rotation=18)

    plt.tight_layout()
    output_path = 'generated_uml/uml_use_case_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


# -----------------------------------------------------------------------------
# 2. UML 2.0 COMPONENT DIAGRAM (for SAD Figure 1)
# -----------------------------------------------------------------------------
def generate_component_diagram():
    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    ax.text(6.5, 9.15, "UML 2.0 Component Diagram — Railway Reservation System", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#003366')

    def draw_component(x, y, w, h, name, stereotype="«component»", subtext="", bg_col="#FFFFFF", border_col="#0284C7"):
        comp_box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.08",
                                 ec=border_col, fc=bg_col, lw=1.6, zorder=2)
        ax.add_patch(comp_box)
        ic_w, ic_h = 0.32, 0.22
        ic_x = x + w - ic_w - 0.1
        ic_y = y + h - ic_h - 0.1
        ax.add_patch(Rectangle((ic_x, ic_y), ic_w, ic_h, ec=border_col, fc="#F0F9FF", lw=1, zorder=3))
        ax.add_patch(Rectangle((ic_x - 0.08, ic_y + 0.13), 0.14, 0.06, ec=border_col, fc=border_col, lw=0.8, zorder=4))
        ax.add_patch(Rectangle((ic_x - 0.08, ic_y + 0.03), 0.14, 0.06, ec=border_col, fc=border_col, lw=0.8, zorder=4))
        
        ax.text(x + w/2, y + h - 0.22, stereotype, fontsize=8, fontstyle='italic', ha='center', va='center', color='#475569', zorder=5)
        ax.text(x + w/2, y + h/2 - 0.05, name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=5)
        if subtext:
            ax.text(x + w/2, y + 0.2, subtext, fontsize=8, color='#64748B', ha='center', va='center', zorder=5)

    layers = [
        ("Presentation Layer", 0.6, 7.1, 11.8, 1.7, "#F8FAFC", "#0284C7"),
        ("Application / Business Logic Layer", 0.6, 4.4, 11.8, 2.4, "#F8FAFC", "#2563EB"),
        ("Domain Validation Layer", 0.6, 2.5, 11.8, 1.6, "#F8FAFC", "#D97706"),
        ("Data Persistence Layer", 0.6, 0.45, 11.8, 1.75, "#F8FAFC", "#059669")
    ]
    for title, lx, ly, lw, lh, lfc, lec in layers:
        layer_box = FancyBboxPatch((lx, ly), lw, lh, boxstyle="round,pad=0.05,rounding_size=0.12",
                                   ec=lec, fc=lfc, lw=1.5, ls="--", zorder=1)
        ax.add_patch(layer_box)
        ax.text(lx + 0.25, ly + lh - 0.22, f"Package: {title}", fontsize=9.5, fontweight='bold', color=lec, zorder=2)

    # 1. Presentation
    draw_component(1.5, 7.35, 4.5, 1.15, "CLI Presentation\n(Interactive Menus)", subtext="src/main.cpp", bg_col="#F0F9FF")
    draw_component(7.0, 7.35, 4.5, 1.15, "Web Frontend Client\n(Browser UI)", subtext="web/app.js & web/index.html", bg_col="#F0F9FF")

    # 2. Application
    draw_component(1.0, 4.7, 3.4, 1.4, "Booking & Search\nModule", subtext="src/booking.cpp", bg_col="#EFF6FF")
    draw_component(4.8, 4.7, 3.4, 1.4, "Cancellation\nModule", subtext="src/cancellation.cpp", bg_col="#EFF6FF")
    draw_component(8.6, 4.7, 3.4, 1.4, "Reservation Lookup\nModule", subtext="src/reservation.cpp", bg_col="#EFF6FF")

    # 3. Domain Validation
    draw_component(3.5, 2.7, 6.0, 1.15, "Validation & Sanitization Engine", subtext="src/validation.cpp (Regex & Bounds)", bg_col="#FFFBEB", border_col="#D97706")

    # 4. Persistence Component & Data Artifacts
    draw_component(1.2, 0.65, 4.6, 1.25, "Data Store Engine\n(Flat File I/O)", subtext="src/data_store.cpp", bg_col="#ECFDF5", border_col="#059669")

    def draw_artifact(x, y, w, h, name):
        ax.add_patch(Rectangle((x, y), w, h, ec="#059669", fc="#F0FDF4", lw=1.4, zorder=2))
        ax.text(x + w/2, y + h - 0.2, "«artifact»", fontsize=7.5, fontstyle='italic', ha='center', color="#047857", zorder=3)
        ax.text(x + w/2, y + h/2 - 0.08, name, fontsize=8.5, fontweight='bold', ha='center', color="#065F46", zorder=3)

    draw_artifact(6.8, 0.75, 2.6, 1.05, "data/trains.dat\n(Train Records)")
    draw_artifact(9.7, 0.75, 2.6, 1.05, "data/reservations.dat\n(Booking Records)")

    # Connectors
    ax.annotate("", xy=(2.7, 6.1), xytext=(2.7, 7.35), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))
    ax.annotate("", xy=(6.5, 6.1), xytext=(6.5, 7.35), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))
    ax.annotate("", xy=(10.3, 6.1), xytext=(10.3, 7.35), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.5))

    ax.annotate("", xy=(4.8, 3.85), xytext=(2.7, 4.7), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    ax.annotate("", xy=(6.5, 3.85), xytext=(6.5, 4.7), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    ax.annotate("", xy=(8.2, 3.85), xytext=(10.3, 4.7), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    ax.text(6.5, 4.05, "validateInput()", fontsize=8.5, fontweight='bold', color="#1D4ED8", ha='center', va='center', zorder=6)

    ax.annotate("", xy=(3.5, 1.9), xytext=(3.5, 2.7), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5))
    ax.annotate("", xy=(2.7, 1.9), xytext=(2.7, 4.7), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5, ls="--"))
    
    # File I/O links
    ax.annotate("", xy=(6.8, 1.28), xytext=(5.8, 1.28), arrowprops=dict(arrowstyle="<->", color="#059669", lw=1.5))
    ax.annotate("", xy=(9.7, 1.28), xytext=(5.8, 1.28), arrowprops=dict(arrowstyle="<->", color="#059669", lw=1.5))

    plt.tight_layout()
    output_path = 'generated_uml/uml_component_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


# -----------------------------------------------------------------------------
# 3. UML CLASS DIAGRAM (for SAD Section 4.1)
# -----------------------------------------------------------------------------
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(14, 10.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10.5)
    ax.axis('off')

    ax.text(7, 10.15, "UML Class Diagram — System Architecture & Domain Model", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#003366')

    def draw_class(x, y, w, h, class_name, stereotype="", attributes=[], methods=[], bg_col="#FFFFFF", border_col="#1E3A8A"):
        box = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", ec=border_col, fc=bg_col, lw=1.5, zorder=2)
        ax.add_patch(box)
        th = 0.52 if not stereotype else 0.72
        ax.add_patch(Rectangle((x, y + h - th), w, th, ec=border_col, fc="#F1F5F9", lw=1.5, zorder=3))
        if stereotype:
            ax.text(x + w/2, y + h - 0.22, stereotype, fontsize=7.5, fontstyle='italic', ha='center', va='center', color='#475569', zorder=4)
            ax.text(x + w/2, y + h - 0.50, class_name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)
        else:
            ax.text(x + w/2, y + h - th/2, class_name, fontsize=9.5, fontweight='bold', ha='center', va='center', color='#0F172A', zorder=4)
        
        div_y1 = y + h - th
        ax.plot([x, x + w], [div_y1, div_y1], color=border_col, lw=1, zorder=4)

        # Draw attributes
        attr_y = div_y1 - 0.2
        for attr in attributes:
            ax.text(x + 0.12, attr_y, attr, fontsize=8, family='monospace', va='center', color='#1E293B', zorder=4)
            attr_y -= 0.23

        # Divider between attributes and methods
        if attributes and methods:
            div_y2 = div_y1 - len(attributes) * 0.23 - 0.12
            ax.plot([x, x + w], [div_y2, div_y2], color=border_col, lw=1, zorder=4)
            meth_y = div_y2 - 0.2
        else:
            meth_y = div_y1 - 0.2

        # Draw methods
        for m in methods:
            ax.text(x + 0.12, meth_y, m, fontsize=7.8, family='monospace', va='center', color='#0F172A', zorder=4)
            meth_y -= 0.23

    # 1. Models
    draw_class(0.6, 6.7, 4.0, 3.0, "Train", stereotype="«struct»",
               attributes=[
                   "- trainId: string",
                   "- trainName: string",
                   "- source: string",
                   "- destination: string",
                   "- departureTime: string",
                   "- arrivalTime: string",
                   "- totalSeats: int",
                   "- availableSeats: int"
               ],
               methods=[], bg_col="#F0FDF4", border_col="#16A34A")

    draw_class(5.0, 6.7, 4.4, 3.0, "Reservation", stereotype="«struct»",
               attributes=[
                   "- reservationId: string",
                   "- trainId: string",
                   "- passengerName: string",
                   "- age: int",
                   "- gender: char",
                   "- journeyDate: string",
                   "- seatsBooked: int",
                   "- status: ReservationStatus"
               ],
               methods=[], bg_col="#F0FDF4", border_col="#16A34A")

    draw_class(9.8, 7.7, 3.6, 2.0, "ReservationStatus", stereotype="«enumeration»",
               attributes=[
                   "+ STATUS_CONFIRMED = 1",
                   "+ STATUS_CANCELLED = 2"
               ],
               methods=[], bg_col="#FEF3C7", border_col="#D97706")

    # 2. Controllers
    draw_class(0.6, 3.3, 4.0, 2.7, "BookingController", stereotype="«module»",
               attributes=["- trainFile: string", "- resFile: string"],
               methods=[
                   "+ searchTrains(trains): bool",
                   "+ bookReservation(trains, res): bool",
                   "- getPassengerDetails(): Passenger"
               ], bg_col="#F0F9FF", border_col="#0284C7")

    draw_class(5.0, 3.3, 4.4, 2.7, "CancellationController", stereotype="«module»",
               attributes=[],
               methods=[
                   "+ processCancellation(id, res, tr): CancelResult",
                   "+ updateSeatAvailability(tr, id, seats): bool",
                   "+ cancelReservationFlow(res, tr): CancelResult"
               ], bg_col="#F0F9FF", border_col="#0284C7")

    draw_class(9.8, 3.3, 3.6, 2.7, "ReservationController", stereotype="«module»",
               attributes=[],
               methods=[
                   "+ lookupReservation(id, res, out): LookupResult",
                   "+ displayReservation(res, trains): void",
                   "+ getStatusString(status): string",
                   "+ viewReservationFlow(res, trains): bool"
               ], bg_col="#F0F9FF", border_col="#0284C7")

    # 3. Validation & Persistence
    draw_class(0.6, 0.2, 6.2, 2.6, "ValidationEngine", stereotype="«utility»",
               attributes=[],
               methods=[
                   "+ isValidReservationId(id: string): bool",
                   "+ isValidPassengerName(name: string): bool",
                   "+ isValidAge(age: int): bool",
                   "+ isValidDate(date: string): bool",
                   "+ isValidGender(gender: string): bool",
                   "+ sanitizeForDisplay(input, maxLen): string"
               ], bg_col="#FFFBEB", border_col="#D97706")

    draw_class(7.2, 0.2, 6.2, 2.6, "DataStoreManager", stereotype="«data access»",
               attributes=["- defaultTrainPath: string", "- defaultResPath: string"],
               methods=[
                   "+ loadTrains(filepath): vector<Train>",
                   "+ saveTrains(trains, filepath): bool",
                   "+ loadReservations(filepath): vector<Reservation>",
                   "+ saveReservations(res, filepath): bool",
                   "+ generateReservationId(res): string"
               ], bg_col="#ECFDF5", border_col="#059669")

    # Connectors
    ax.annotate("", xy=(5.0, 8.2), xytext=(4.6, 8.2), arrowprops=dict(arrowstyle="-", color="#334155", lw=1.5))
    ax.text(4.7, 8.4, "1", fontsize=8.5, fontweight='bold', color="#334155")
    ax.text(4.9, 8.4, "*", fontsize=9.5, fontweight='bold', color="#334155")

    ax.annotate("", xy=(9.8, 8.7), xytext=(9.4, 8.7), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5, ls="--"))

    ax.annotate("", xy=(2.6, 6.7), xytext=(2.6, 6.0), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.4, ls="--"))
    ax.annotate("", xy=(7.2, 6.7), xytext=(7.2, 6.0), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.4, ls="--"))
    ax.annotate("", xy=(11.6, 6.7), xytext=(11.6, 6.0), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.4, ls="--"))

    ax.annotate("", xy=(3.7, 2.6), xytext=(2.6, 3.3), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.4, ls="--"))
    ax.annotate("", xy=(10.3, 2.6), xytext=(10.3, 3.3), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.4, ls="--"))

    plt.tight_layout()
    output_path = 'generated_uml/uml_class_diagram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


# -----------------------------------------------------------------------------
# 4. UML SEQUENCE DIAGRAM 1: TICKET BOOKING (for SAD Figure 2)
# -----------------------------------------------------------------------------
def generate_sequence_booking():
    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    ax.text(6.5, 9.15, "UML Sequence Diagram — Ticket Booking Workflow", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#003366')

    lifelines = [
        ("Passenger\n:User", 1.2),
        ("UserInterface\n:CLI/Web", 3.8),
        ("ValidationEngine\n:Validator", 6.4),
        ("BookingModule\n:Controller", 9.0),
        ("DataStore\n:Persistence", 11.6)
    ]

    for label, lx in lifelines:
        ax.add_patch(Rectangle((lx - 0.9, 8.2), 1.8, 0.65, ec="#0284C7", fc="#EFF6FF", lw=1.5, zorder=3))
        ax.text(lx, 8.52, label, fontsize=9, fontweight='bold', ha='center', va='center', color="#0F172A", zorder=4)
        ax.plot([lx, lx], [8.2, 0.6], color="#94A3B8", lw=1.2, ls="--", zorder=1)

    def activation_bar(x, y_top, y_bot, col="#BAE6FD"):
        ax.add_patch(Rectangle((x - 0.12, y_bot), 0.24, y_top - y_bot, ec="#0284C7", fc=col, lw=1.2, zorder=2))

    activation_bar(1.2, 8.0, 0.8)
    activation_bar(3.8, 7.8, 1.0)
    activation_bar(6.4, 7.1, 5.8)
    activation_bar(9.0, 5.4, 1.4)
    activation_bar(11.6, 4.4, 2.0)

    # Messages
    ax.annotate("", xy=(3.8, 7.7), xytext=(1.2, 7.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(2.5, 7.85, "1: selectBookOption()", fontsize=8.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(1.2, 7.4), xytext=(3.8, 7.4), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2, ls="--"))
    ax.text(2.5, 7.55, "2: promptPassengerDetails()", fontsize=8.5, ha='center', color="#475569")

    ax.annotate("", xy=(3.8, 7.0), xytext=(1.2, 7.0), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(2.5, 7.15, "3: submitDetails(trainId, name, age, date, seats)", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(6.4, 6.7), xytext=(3.8, 6.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(5.1, 6.85, "4: validateInputs(name, age, gender, date)", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(3.8, 6.1), xytext=(6.4, 6.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--"))
    ax.text(5.1, 6.25, "5: return validationOk (true)", fontsize=8.5, ha='center', color="#047857")

    ax.annotate("", xy=(9.0, 5.5), xytext=(3.8, 5.5), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(6.4, 5.65, "6: bookReservation(trainId, passenger, seats)", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(11.6, 4.8), xytext=(9.0, 4.8), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 4.95, "7: findTrainById(trainId)", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(9.0, 4.2), xytext=(11.6, 4.2), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.2, ls="--"))
    ax.text(10.3, 4.35, "8: return trainRecord (available >= seats)", fontsize=7.8, ha='center', color="#0369A1")

    ax.annotate("", xy=(11.6, 3.4), xytext=(9.0, 3.4), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 3.55, "9: generateReservationId() & saveReservations()", fontsize=7.8, ha='center', color="#0F172A")

    ax.annotate("", xy=(11.6, 2.7), xytext=(9.0, 2.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 2.85, "10: updateTrainSeats(-seats) & saveTrains()", fontsize=7.8, ha='center', color="#0F172A")

    ax.annotate("", xy=(9.0, 2.1), xytext=(11.6, 2.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--"))
    ax.text(10.3, 2.25, "11: return persistSuccess (true)", fontsize=8, ha='center', color="#047857")

    ax.annotate("", xy=(3.8, 1.6), xytext=(9.0, 1.6), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.4, ls="--"))
    ax.text(6.4, 1.75, "12: return bookingResult(RES003, Confirmed)", fontsize=8, ha='center', color="#0369A1")

    ax.annotate("", xy=(1.2, 1.1), xytext=(3.8, 1.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
    ax.text(2.5, 1.25, "13: displayBookingConfirmationBanner()", fontsize=8, ha='center', color="#047857")

    # Alt Frame
    ax.add_patch(Rectangle((0.7, 0.95), 11.6, 4.9, ec="#94A3B8", fc="none", lw=1.2, ls=":", zorder=1))
    ax.add_patch(Rectangle((0.7, 5.55), 2.2, 0.3, ec="#94A3B8", fc="#F1F5F9", lw=1.2, zorder=2))
    ax.text(1.8, 5.7, "alt [Seats Available]", fontsize=8, fontweight='bold', ha='center', va='center', color="#334155", zorder=3)

    plt.tight_layout()
    output_path = 'generated_uml/uml_sequence_booking.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")


# -----------------------------------------------------------------------------
# 5. UML SEQUENCE DIAGRAM 2: TICKET CANCELLATION (for SAD Figure 3)
# -----------------------------------------------------------------------------
def generate_sequence_cancellation():
    fig, ax = plt.subplots(figsize=(13, 9.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    ax.text(6.5, 9.15, "UML Sequence Diagram — Ticket Cancellation & Seat Restoration", 
            fontsize=15, fontweight='bold', ha='center', va='center', color='#003366')

    lifelines = [
        ("Passenger\n:User", 1.2),
        ("UserInterface\n:CLI/Web", 3.8),
        ("ValidationEngine\n:Validator", 6.4),
        ("CancellationModule\n:Controller", 9.0),
        ("DataStore\n:Persistence", 11.6)
    ]

    for label, lx in lifelines:
        ax.add_patch(Rectangle((lx - 0.9, 8.2), 1.8, 0.65, ec="#D97706", fc="#FEF3C7", lw=1.5, zorder=3))
        ax.text(lx, 8.52, label, fontsize=9, fontweight='bold', ha='center', va='center', color="#0F172A", zorder=4)
        ax.plot([lx, lx], [8.2, 0.6], color="#94A3B8", lw=1.2, ls="--", zorder=1)

    def activation_bar(x, y_top, y_bot, col="#FED7AA"):
        ax.add_patch(Rectangle((x - 0.12, y_bot), 0.24, y_top - y_bot, ec="#D97706", fc=col, lw=1.2, zorder=2))

    activation_bar(1.2, 8.0, 0.8)
    activation_bar(3.8, 7.8, 1.0)
    activation_bar(6.4, 7.1, 5.8)
    activation_bar(9.0, 5.5, 1.4)
    activation_bar(11.6, 4.8, 2.0)

    # Messages
    ax.annotate("", xy=(3.8, 7.7), xytext=(1.2, 7.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(2.5, 7.85, "1: selectCancelOption()", fontsize=8.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(1.2, 7.35), xytext=(3.8, 7.35), arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2, ls="--"))
    ax.text(2.5, 7.5, "2: promptReservationId()", fontsize=8.5, ha='center', color="#475569")

    ax.annotate("", xy=(3.8, 6.95), xytext=(1.2, 6.95), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(2.5, 7.1, "3: submitReservationId(\"RES002\")", fontsize=8.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(6.4, 6.6), xytext=(3.8, 6.6), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(5.1, 6.75, "4: isValidReservationId(\"RES002\")", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(3.8, 6.0), xytext=(6.4, 6.0), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--"))
    ax.text(5.1, 6.15, "5: return formatValid (true)", fontsize=8.5, ha='center', color="#047857")

    ax.annotate("", xy=(9.0, 5.5), xytext=(3.8, 5.5), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(6.4, 5.65, "6: cancelReservationFlow(reservations, trains)", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(11.6, 4.9), xytext=(9.0, 4.9), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 5.05, "7: findReservationById(\"RES002\")", fontsize=8, ha='center', color="#0F172A")

    ax.annotate("", xy=(9.0, 4.3), xytext=(11.6, 4.3), arrowprops=dict(arrowstyle="->", color="#0284C7", lw=1.2, ls="--"))
    ax.text(10.3, 4.45, "8: return record (Status = Confirmed)", fontsize=7.8, ha='center', color="#0369A1")

    ax.annotate("", xy=(1.2, 3.8), xytext=(9.0, 3.8), arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.4))
    ax.text(5.1, 3.95, "9: displayReservationCard() & promptConfirmation(\"Are you sure? (Y/N)\")", fontsize=7.8, ha='center', color="#B45309")

    ax.annotate("", xy=(9.0, 3.3), xytext=(1.2, 3.3), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(5.1, 3.45, "10: userConfirmAnswer(\"Y\")", fontsize=8.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(11.6, 2.7), xytext=(9.0, 2.7), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 2.85, "11: setStatus(STATUS_CANCELLED) & saveReservations()", fontsize=7.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(11.6, 2.0), xytext=(9.0, 2.0), arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.4))
    ax.text(10.3, 2.15, "12: updateSeatAvailability(T002, +1) & saveTrains()", fontsize=7.5, ha='center', color="#0F172A")

    ax.annotate("", xy=(3.8, 1.5), xytext=(9.0, 1.5), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.2, ls="--"))
    ax.text(6.4, 1.65, "13: return CANCEL_SUCCESS", fontsize=8.5, ha='center', color="#047857")

    ax.annotate("", xy=(1.2, 1.1), xytext=(3.8, 1.1), arrowprops=dict(arrowstyle="->", color="#059669", lw=1.5))
    ax.text(2.5, 1.25, "14: displayCancellationBanner(1 seat restored to T002)", fontsize=7.8, ha='center', color="#047857")

    # Alt Frame
    ax.add_patch(Rectangle((0.7, 0.95), 11.6, 3.2, ec="#94A3B8", fc="none", lw=1.2, ls=":", zorder=1))
    ax.add_patch(Rectangle((0.7, 3.85), 2.2, 0.3, ec="#94A3B8", fc="#F1F5F9", lw=1.2, zorder=2))
    ax.text(1.8, 4.0, "alt [User Confirmed ('Y')]", fontsize=7.8, fontweight='bold', ha='center', va='center', color="#334155", zorder=3)

    plt.tight_layout()
    output_path = 'generated_uml/uml_sequence_cancellation.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {output_path}")

generate_use_case_diagram()
generate_component_diagram()
generate_class_diagram()
generate_sequence_booking()
generate_sequence_cancellation()
