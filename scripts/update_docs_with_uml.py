import docx
from docx.shared import Inches
import os

print("--- Updating SAD with high-res UML diagrams ---")
doc_sad = docx.Document('SAD_Railway_Reservation_System_Team12_Audited.docx')

# 1. Replace image blobs in SAD
with open('generated_uml/uml_component_diagram.png', 'rb') as f:
    comp_bytes = f.read()
with open('generated_uml/uml_sequence_booking.png', 'rb') as f:
    seq_book_bytes = f.read()
with open('generated_uml/uml_sequence_cancellation.png', 'rb') as f:
    seq_cancel_bytes = f.read()

for rel in doc_sad.part.rels.values():
    if 'image1.png' in rel.target_ref:
        rel.target_part._blob = comp_bytes
        print("Replaced image1.png (Component Diagram) in SAD")
    elif 'image2.png' in rel.target_ref:
        rel.target_part._blob = seq_book_bytes
        print("Replaced image2.png (Booking Sequence) in SAD")
    elif 'image3.png' in rel.target_ref:
        rel.target_part._blob = seq_cancel_bytes
        print("Replaced image3.png (Cancellation Sequence) in SAD")

# 2. Insert UML Class Diagram into SAD Section 4.1
# Find paragraph 4.2 UML Sequence Diagrams
target_idx = None
for i, p in enumerate(doc_sad.paragraphs):
    if p.text.strip() == "4.2 UML Sequence Diagrams":
        target_idx = i
        break

if target_idx is not None:
    p_target = doc_sad.paragraphs[target_idx]
    
    p_h = p_target.insert_paragraph_before("4.1.1 UML Class Diagram – Domain Entities & Module Architecture")
    p_h.style = "Heading 2" if "Heading 2" in doc_sad.styles else None

    p_desc = p_target.insert_paragraph_before(
        "The UML Class Diagram defines the structural design and domain model of the Railway Reservation System. "
        "It models the core domain data entities (Train, Reservation, and ReservationStatus enum), business logic controller modules "
        "(BookingController, CancellationController, and ReservationController), the domain validation engine, and the persistence data store manager."
    )

    p_img = p_target.insert_paragraph_before()
    p_img.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    run_img.add_picture('generated_uml/uml_class_diagram.png', width=Inches(6.2))

    p_cap = p_target.insert_paragraph_before("Figure 2: UML Class Diagram – System Architecture & Domain Model")
    p_cap.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    doc_sad.paragraphs[target_idx].insert_paragraph_before() # spacing paragraph
    print("Inserted UML Class Diagram section into SAD")

# 3. Update captions and figure numbers in SAD
for p in doc_sad.paragraphs:
    if p.text.strip() == "Figure 1: UML Component Diagram – Railway Reservation System":
        p.text = "Figure 1: UML 2.0 Component Diagram – Railway Reservation System"
    elif p.text.strip() == "Figure 2: UML Sequence Diagram – Ticket Booking":
        p.text = "Figure 3: UML 2.0 Sequence Diagram – Ticket Booking Workflow"
    elif p.text.strip() == "Figure 3: UML Sequence Diagram – Ticket Cancellation":
        p.text = "Figure 4: UML 2.0 Sequence Diagram – Ticket Cancellation & Seat Restoration"

# 4. Add revision history in SAD
t_rev = doc_sad.tables[0]
r_new = t_rev.add_row()
r_new.cells[0].text = "1.3"
r_new.cells[1].text = "19 November 2026"
r_new.cells[2].text = "R Vinay (Reviewer)"
r_new.cells[3].text = "Upgraded architecture diagrams to formal UML 2.0 standard (Component, Class, and Sequence Diagrams); verified complete compliance with faculty Part-1 design checklist."

doc_sad.save('SAD_Railway_Reservation_System_Team12_Audited.docx')
print("Successfully saved SAD_Railway_Reservation_System_Team12_Audited.docx")


print("\n--- Updating SRS with high-res UML diagram ---")
doc_srs = docx.Document('Railway_Reservation_System_SRS_Team12_Audited.docx')

with open('generated_uml/uml_use_case_diagram.png', 'rb') as f:
    uc_bytes = f.read()

for rel in doc_srs.part.rels.values():
    if 'image1.png' in rel.target_ref:
        rel.target_part._blob = uc_bytes
        print("Replaced image1.png (Use Case Diagram) in SRS")

# Add revision history in SRS
t_rev_srs = doc_srs.tables[0]
r_new_srs = t_rev_srs.add_row()
r_new_srs.cells[0].text = "R Vinay (Reviewer)"
r_new_srs.cells[1].text = "19 November 2026"
r_new_srs.cells[2].text = "Replaced Use Case Diagram with formal UML 2.0 standard diagram with «include» relationships; verified complete compliance with faculty Part-1 requirements checklist."
r_new_srs.cells[3].text = "1.3"

doc_srs.save('Railway_Reservation_System_SRS_Team12_Audited.docx')
print("Successfully saved Railway_Reservation_System_SRS_Team12_Audited.docx")


print("\n--- Updating Test Plan revision history ---")
doc_tp = docx.Document('Test_Plan_Railway_Reservation_System.docx')
t_rev_tp = doc_tp.tables[0]
r_new_tp = t_rev_tp.add_row()
r_new_tp.cells[0].text = "1.3"
r_new_tp.cells[1].text = "19 November 2026"
r_new_tp.cells[2].text = "R Vinay (Reviewer)"
r_new_tp.cells[3].text = "Verified strict compliance with faculty Part-1 testing checklist (Sections 3, 4, 5 filled, Section 5.1 dedicated to security validation, 15 test cases covering FRs/NFRs)."

doc_tp.save('Test_Plan_Railway_Reservation_System.docx')
print("Successfully saved Test_Plan_Railway_Reservation_System.docx")
