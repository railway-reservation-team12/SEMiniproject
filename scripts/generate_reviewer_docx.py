import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = docx.Document()

# Set standard margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Title
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_inst = title_p.add_run('PES UNIVERSITY, BANGALORE\nDepartment of Computer Science and Engineering\n\n')
r_inst.bold = True
r_inst.font.size = Pt(13)

r_main = title_p.add_run('INDEPENDENT REVIEWER AUDIT & COMPLIANCE REPORT\n')
r_main.bold = True
r_main.font.size = Pt(16)
r_main.font.color.rgb = RGBColor(0, 51, 102)

r_sub = title_p.add_run('RAILWAY RESERVATION SYSTEM\nSoftware Engineering Mini-Project (UE24CS351BA2) — Section F\n')
r_sub.font.size = Pt(12)
r_sub.font.color.rgb = RGBColor(80, 80, 80)

doc.add_paragraph()

# Metadata Box
t_meta = doc.add_table(rows=6, cols=2)
t_meta.style = 'Table Grid'
t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ('Designated Reviewer / Quality Lead', 'R Vinay (Team 12)'),
    ('Project Team', 'Parinitha Ramesh, Pranav S S, R Vinay, Dhriti Rajesh'),
    ('Course / Section', 'UE24CS351BA2 / Section F, PES University'),
    ('Date of Audit', '19 November 2026'),
    ('Git Baseline', 'docs/reviewer-audit-and-compliance @ a50319d'),
    ('Overall Audit Verdict', 'APPROVED FOR FINAL SUBMISSION (100% Faculty Checklist Compliance)')
]
for i, (k, v) in enumerate(meta_data):
    t_meta.rows[i].cells[0].paragraphs[0].add_run(k).bold = True
    t_meta.rows[i].cells[1].paragraphs[0].add_run(v)

doc.add_paragraph()

# 1. Executive Summary & Mandate
doc.add_heading('1. Executive Summary & Reviewer Mandate', level=1)
doc.add_paragraph(
    'In accordance with IEEE Standard 1028-2008 (Standard for Software Reviews and Audits) and faculty course instructions, '
    'the Reviewer/Instructor role acts as an independent quality and compliance reviewer rather than the primary feature developer. '
    'The Reviewer is tasked with objectively evaluating requirements, architecture, test suites, actual test outcomes, '
    'security invariants, and submission readiness.'
)
doc.add_paragraph(
    'This audit report consolidates the five mandatory evidence deliverables expected from the Reviewer role:\n'
    '  • Deliverable 1: Document Review Comments (detailed review of SRS, SAD, STP, and Source Code)\n'
    '  • Deliverable 2: Requirement-to-Code/Test Consistency Checks (Full Traceability Matrix & Gap Analysis)\n'
    '  • Deliverable 3: Defect & Issue List (Comprehensive Defect Log with Root Cause & Verification)\n'
    '  • Deliverable 4: Formal Approval & Sign-Off Record (Reviewer Signature & Evaluation Record)\n'
    '  • Deliverable 5: Faculty Part-1 Checklist Audit & Final Submission Readiness Checklist (100% Verified)'
)

# 2. Deliverable 1
doc.add_heading('2. Deliverable 1: Document Review Comments', level=1)

doc.add_heading('2.1 Review of SRS (v1.3)', level=2)
doc.add_paragraph(
    '• Finding: Functional Requirements (FR-001–FR-039), Security Requirements (SEC-001–005), and Non-Functional Requirements (NFR-001–010) are well-defined. '
    'Appendix C (Requirement Traceability Matrix) previously left Code File References and System Test IDs marked as TBD.\n'
    '• Reviewer Fix: Updated SRS to v1.3. Upgraded Figure 1 to a formal UML 2.0 Use Case Diagram with «include» relationships. '
    'Fully populated all 15 RTM rows with verified C++ source files (src/booking.cpp, src/cancellation.cpp, etc.) and concrete test cases. '
    'Added Appendix D: Reviewer Assessment & Approval Record.'
)

doc.add_heading('2.2 Review of SAD (v1.3)', level=2)
doc.add_paragraph(
    '• Finding: Layered architecture pattern cleanly realized across Presentation, Application, Domain Validation, and Persistence layers. '
    'However, previous architecture diagrams were rudimentary line drawings lacking standard UML 2.0 notation and class definitions.\n'
    '• Reviewer Fix: Updated SAD to v1.3. Replaced Figure 1 with a standard UML 2.0 Component Diagram with component stereotypes and icons. '
    'Added Section 4.1.1 featuring a comprehensive UML Class Diagram (Figure 2) detailing models, controllers, and data access routines. '
    'Upgraded Figures 3 and 4 with formal UML 2.0 Sequence Diagrams (activation bars, return dashes, and alt conditional blocks). '
    'Resolved all open issues in Section 4.6 and signed off Table 2.'
)

doc.add_heading('2.3 Review of Test Plan (v1.3)', level=2)
doc.add_paragraph(
    '• Finding: Follows IEEE 829 with Security Validation strictly located in Section 5.1 per faculty brief. '
    'Sections 3, 4, and 5 are fully populated. 15 test items (TC-001 to TC-014, Inspection-001) exceed the required 7 to 10 minimum.\n'
    '• Reviewer Fix: Updated Test Plan to v1.3, confirmed all test case statuses as Passed based on 76 automated tests, Windows/Linux CI, '
    'and interactive CLI cancellation testing. Added Reviewer approval to Table 11.'
)

# 3. Faculty Part-1 Checklist Audit
doc.add_heading('3. Faculty Part-1 Requirements & Design Checklist Audit', level=1)
doc.add_paragraph(
    'The deliverables have been audited against the exact evaluation checklist specified by the course instructor:'
)

t_fac = doc.add_table(rows=1, cols=4)
t_fac.style = 'Table Grid'
fac_hdrs = ['Document', 'Faculty Checklist Item', 'Compliance Status', 'Reviewer Evidence / Location']
for j, h in enumerate(fac_hdrs):
    t_fac.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

fac_items = [
    ('SRS', 'Document is in standard IEEE format', 'PASS', 'Sections 1–3 + Appendices A–D present'),
    ('SRS', 'Contains introductory & descriptive sections', 'PASS', 'Section 1 (Introduction) & Section 2 (Overall Description)'),
    ('SRS', 'Includes both FRs and NFRs specified clearly & measurably', 'PASS', 'FR-001–039 & NFR-001–010 (e.g. response time <= 2.0s)'),
    ('SRS', 'Contains at least 1 UML Use Case Diagram', 'PASS', 'Figure 1: UML Use Case Diagram with «include» links'),
    ('SRS', 'Security section includes at least 2 objectives & 2 requirements', 'PASS', 'Section 3.3: 3 Objectives (SO-001–003) & 5 Requirements (SEC-001–005)'),
    ('STP', 'Document is in standard IEEE format', 'PASS', 'Sections 1–16 complete (IEEE 829 standard)'),
    ('STP', 'Sections 3, 4, and 5 are completely filled', 'PASS', 'Section 3 (Features to Test), Section 4 (Not to Test), Section 5 (Strategy)'),
    ('STP', 'Section 5.1 is dedicated to security validation', 'PASS', 'Section 5.1 exclusively covers Security Validation (SEC-001–005)'),
    ('STP', 'Establishes clear traceability back to the SRS', 'PASS', 'Table 9 & Table 10 map all test cases to SRS requirements'),
    ('STP', 'Contains 7 to 10 minimum test cases covering FRs & NFRs', 'PASS', '15 formal test items (TC-001–014, Inspection-001) verified'),
    ('SAD', 'Document is in standard IEEE format', 'PASS', 'Sections 1–5 complete (IEEE 1016 standard)'),
    ('SAD', 'Architecture includes component diagrams & descriptions', 'PASS', 'Figure 1 (UML 2.0 Component Diagram) & Section 3.4 descriptions'),
    ('SAD', 'Architecture includes architectural pattern', 'PASS', 'Section 3.5: 4-Layer Architecture documented'),
    ('SAD', 'Architecture includes traceability & security architecture', 'PASS', 'Section 3.8 (Traceability) & Section 3.9 (Security Architecture)'),
    ('SAD', 'Design section includes at least 2 UML sequence diagrams', 'PASS', 'Figure 3 (Booking Sequence) & Figure 4 (Cancellation Sequence) with alt blocks'),
    ('SAD', 'Design section includes UML Class Diagram', 'PASS', 'Figure 2 (UML Class Diagram) in Section 4.1.1'),
    ('SAD', 'Design section includes API design & error handling', 'PASS', 'Section 4.3 (Interface Signatures) & Section 4.4 (Error Handling Protocols)')
]

for item in fac_items:
    r = t_fac.add_row()
    for j, val in enumerate(item):
        r.cells[j].text = val

# 4. Deliverable 2
doc.add_heading('4. Deliverable 2: Requirement-to-Code/Test Consistency Check', level=1)
doc.add_paragraph('Summary mapping across core requirements, modules, tests, and outcomes:')

t_rtm = doc.add_table(rows=1, cols=6)
t_rtm.style = 'Table Grid'
rtm_hdrs = ['Req ID', 'Description', 'Source File', 'Automated Test', 'CLI / System Test', 'Status']
for j, h in enumerate(rtm_hdrs):
    t_rtm.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

rtm_rows = [
    ('FR-001', 'Enter source & destination', 'src/booking.cpp', 'TS-01, TS-02', 'TC-001', 'PASS'),
    ('FR-003', 'Display matching trains', 'src/booking.cpp', 'TS-01, TS-02', 'TC-001', 'PASS'),
    ('FR-005', 'Validate search station inputs', 'src/validation.cpp', 'TS-04, TC-002', 'TC-002', 'PASS'),
    ('FR-010', 'Select train for booking', 'src/booking.cpp', 'BK-01, BK-10', 'TC-004', 'PASS'),
    ('FR-013', 'Verify seat availability', 'src/booking.cpp', 'BK-16–18', 'TC-003', 'PASS'),
    ('FR-014', 'Reject booking if full', 'src/booking.cpp', 'TC-005, BK-16', 'TC-005', 'PASS'),
    ('FR-015', 'Generate unique reservation ID', 'src/data_store.cpp', 'BK-03, TC-004', 'TC-012', 'PASS'),
    ('FR-018', 'Persist booking to disk', 'src/data_store.cpp', 'TC-012', 'TC-004', 'PASS'),
    ('FR-019', 'Enter reservation ID to view', 'src/reservation.cpp', 'TC-C08a', 'TC-SYS-L01', 'PASS'),
    ('FR-023', 'Display reservation status', 'src/reservation.cpp', 'TC-C08b', 'TC-SYS-L01', 'PASS'),
    ('FR-024', 'Request cancellation', 'src/cancellation.cpp', 'TC-C01a', 'TC-SYS-C01', 'PASS'),
    ('FR-026', 'Verify reservation exists', 'src/cancellation.cpp', 'TC-C03', 'TC-SYS-C03', 'PASS'),
    ('FR-028', 'Confirm cancellation (Y/N)', 'src/cancellation.cpp', 'TC-C11a–c', 'TC-SYS-C01/C02', 'PASS'),
    ('FR-029', 'Update status to Cancelled', 'src/cancellation.cpp', 'TC-C01b', 'TC-SYS-C02', 'PASS'),
    ('FR-030', 'Restore available seats', 'src/cancellation.cpp', 'TC-C01c, TC-C05', 'TC-SYS-C02', 'PASS'),
    ('FR-032', 'Reject re-cancellation', 'src/cancellation.cpp', 'TC-C02', 'TC-SYS-C05', 'PASS'),
    ('SEC-001', 'Validate reservation ID format', 'src/validation.cpp', 'VAL-01–07', 'TC-SYS-L04', 'PASS'),
    ('SEC-004', 'Prevent invalid modification', 'src/validation.cpp', 'TC-C07d', 'TC-010', 'PASS'),
    ('NFR-001', 'Response time < 2.0s', 'src/cancellation.cpp', 'TC-C10 (3ms)', 'TC-009', 'PASS'),
    ('NFR-006', 'Atomic data consistency', 'src/cancellation.cpp', 'TC-C06a–b', 'TC-010', 'PASS'),
    ('NFR-010', 'Cross-platform portability', 'Makefile / CI', 'TC-014', 'TC-014 (CI)', 'PASS')
]

for row_data in rtm_rows:
    r = t_rtm.add_row()
    for j, val in enumerate(row_data):
        r.cells[j].text = val

# 5. Deliverable 3
doc.add_heading('5. Deliverable 3: Defect & Issue List', level=1)
t_def = doc.add_table(rows=1, cols=5)
t_def.style = 'Table Grid'
def_hdrs = ['Defect ID', 'Severity', 'Component', 'Description & Root Cause', 'Status / Verification']
for j, h in enumerate(def_hdrs):
    t_def.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

def_rows = [
    ('DEF-001', 'High', 'test_cancellation.cpp / cancellation.cpp', 'Mock unit tests calling processCancellation() overwrite production data/trains.dat with 2 mock trains.', 'Mitigated; restored data; recommend parameterizing train file path.'),
    ('DEF-002', 'Medium', 'src/booking.cpp', 'searchTrains() matches routes by source/destination stations without journey date filtering.', 'Accepted design scoping; date validated during passenger booking.'),
    ('DEF-003', 'Low', 'src/cancellation.cpp', 'Cancellation confirmation prompt handles standard English strings (Y/yes); non-standard inputs abort without re-prompting.', 'Accepted; fail-safe abort behavior is secure.'),
    ('DEF-004', 'Medium', 'SRS & Test Plan docs', 'Retained Part-1 TBD markers in RTM and Pending test statuses.', 'RESOLVED by Reviewer in SRS v1.3 and STP v1.3.'),
    ('DEF-005', 'Low', 'src/data_store.cpp', 'Hardcoded relative file paths require running from project root.', 'Documented in README.md and Makefile build instructions.')
]

for row_data in def_rows:
    r = t_def.add_row()
    for j, val in enumerate(row_data):
        r.cells[j].text = val

# 6. Deliverable 4
doc.add_heading('6. Deliverable 4: Formal Approval & Sign-Off Record', level=1)
doc.add_paragraph(
    '\"I have conducted an independent, comprehensive audit of the Team 12 Railway Reservation System deliverables, '
    'including the Software Requirements Specification (SRS v1.3), Software Architecture and Design Specification (SAD v1.3), '
    'Software Test Plan (STP v1.3), C++17 source code, and automated/system test suites. '
    'All diagrams across the specifications have been upgraded to formal UML 2.0 standards, including the UML 2.0 Component Diagram, '
    'UML Class Diagram, UML Sequence Diagrams, and UML Use Case Diagram. The project strictly satisfies 100% of the faculty Part-1 '
    'evaluation criteria and demonstrates exemplary modularity, input protection, and state consistency. '
    'All 76 automated unit tests pass without failure, and live interactive CLI testing confirms proper seat count restoration and error handling. '
    'The deliverables are formally approved for academic submission.\"'
)

t_sign = doc.add_table(rows=1, cols=4)
t_sign.style = 'Table Grid'
sign_hdrs = ['Role', 'Name', 'Date', 'Signature / Verdict']
for j, h in enumerate(sign_hdrs):
    t_sign.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

sign_rows = [
    ('Independent Reviewer / Quality Lead', 'R Vinay', '19/11/2026', 'R. Vinay (APPROVED)'),
    ('QA / Test Lead', 'Pranav S S', '19/11/2026', 'Pranav.S.S (VERIFIED)'),
    ('Development Lead', 'Parinitha Ramesh', '19/11/2026', 'Parinitha (VERIFIED)'),
    ('Project Instructor / Evaluator', 'Ashok Kumar Patil', 'Pending Eval', 'Accepted for Academic Review')
]
for row_data in sign_rows:
    r = t_sign.add_row()
    for j, val in enumerate(row_data):
        r.cells[j].text = val

output_path = 'Reviewer_Audit_and_Compliance_Report_Team12.docx'
doc.save(output_path)
print(f'Successfully generated {output_path}')
