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
    ('Date of Audit', '17 November 2026'),
    ('Git Baseline', 'main @ 08207b7 (Synced with railway-reservation-team12/SEMiniproject.git)'),
    ('Overall Audit Verdict', 'APPROVED FOR FINAL SUBMISSION (with documented quality observations)')
]
for i, (k, v) in enumerate(meta_data):
    t_meta.rows[i].cells[0].paragraphs[0].add_run(k).bold = True
    t_meta.rows[i].cells[1].paragraphs[0].add_run(v)

doc.add_paragraph()

# 1. Executive Summary & Mandate
doc.add_heading('1. Executive Summary & Reviewer Mandate', level=1)
doc.add_paragraph(
    'In accordance with IEEE Standard 1028-2008 (Standard for Software Reviews and Audits) and course instructions, '
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
    '  • Deliverable 5: Final Submission Readiness Checklist (25-point Verification Audit)'
)

# 2. Deliverable 1
doc.add_heading('2. Deliverable 1: Document Review Comments', level=1)

doc.add_heading('2.1 Review of SRS (v1.2)', level=2)
doc.add_paragraph(
    '• Finding: Functional Requirements (FR-001–FR-039), Security Requirements (SEC-001–005), and Non-Functional Requirements (NFR-001–010) are well-defined. '
    'However, Appendix C (Requirement Traceability Matrix) previously left Code File References and System Test IDs marked as TBD.\n'
    '• Reviewer Fix: Updated SRS to v1.2, fully populated all 15 RTM rows with verified C++ source files (src/booking.cpp, src/cancellation.cpp, etc.) '
    'and concrete test cases. Added Appendix D: Reviewer Assessment & Approval Record.'
)

doc.add_heading('2.2 Review of SAD (v1.2)', level=2)
doc.add_paragraph(
    '• Finding: Layered architecture pattern cleanly realized across Presentation, Application, Domain Validation, and Persistence layers. '
    'However, Section 4.6 still listed Part-1 planning tasks as open issues, and reviewer approval was pending.\n'
    '• Reviewer Fix: Updated SAD to v1.2, resolved all open issues (documenting delimited file store, C++17 modular implementation, 76 passed tests), '
    'verified module API signatures against src/*.h, and signed off Table 2.'
)

doc.add_heading('2.3 Review of Test Plan (v1.2)', level=2)
doc.add_paragraph(
    '• Finding: Follows IEEE 829 with Security Validation in Section 5.1 per faculty brief. However, Table 10 retained Partial/Pending statuses for cases completed in Part 3.\n'
    '• Reviewer Fix: Updated Test Plan to v1.2, updated test statuses to Passed based on 76 automated tests, Windows/Linux CI, and interactive CLI cancellation testing. '
    'Added Reviewer approval to Table 11.'
)

doc.add_heading('2.4 Review of Source Code & Tests', level=2)
doc.add_paragraph(
    '• Finding: Modular C++17 implementation with zero compilation warnings under -Wall -Wextra. 76/76 automated unit tests pass. '
    'Seat count and reservation status invariants are preserved. Discovered DEF-001 (mock test file side-effect) and documented mitigation.'
)

# 3. Deliverable 2
doc.add_heading('3. Deliverable 2: Requirement-to-Code/Test Consistency Check', level=1)
doc.add_paragraph('The table below summarizes the verified mapping across core requirements, modules, tests, and outcomes:')

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

# 4. Deliverable 3
doc.add_heading('4. Deliverable 3: Defect & Issue List', level=1)
t_def = doc.add_table(rows=1, cols=5)
t_def.style = 'Table Grid'
def_hdrs = ['Defect ID', 'Severity', 'Component', 'Description & Root Cause', 'Status / Verification']
for j, h in enumerate(def_hdrs):
    t_def.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

def_rows = [
    ('DEF-001', 'High', 'test_cancellation.cpp / cancellation.cpp', 'Mock unit tests calling processCancellation() overwrite production data/trains.dat with 2 mock trains.', 'Mitigated; restored data; recommend parameterizing train file path.'),
    ('DEF-002', 'Medium', 'src/booking.cpp', 'searchTrains() matches routes by source/destination stations without journey date filtering.', 'Accepted design scoping; date validated during passenger booking.'),
    ('DEF-003', 'Low', 'src/cancellation.cpp', 'Cancellation confirmation prompt handles standard English strings (Y/yes); non-standard inputs abort without re-prompting.', 'Accepted; fail-safe abort behavior is secure.'),
    ('DEF-004', 'Medium', 'SRS & Test Plan docs', 'Retained Part-1 TBD markers in RTM and Pending test statuses.', 'RESOLVED by Reviewer in SRS v1.2 and STP v1.2.'),
    ('DEF-005', 'Low', 'src/data_store.cpp', 'Hardcoded relative file paths require running from project root.', 'Documented in README.md and Makefile build instructions.')
]

for row_data in def_rows:
    r = t_def.add_row()
    for j, val in enumerate(row_data):
        r.cells[j].text = val

# 5. Deliverable 4
doc.add_heading('5. Deliverable 4: Formal Approval & Sign-Off Record', level=1)
doc.add_paragraph(
    'I have conducted an independent, comprehensive audit of the Team 12 Railway Reservation System deliverables, '
    'including the Software Requirements Specification (SRS v1.2), Software Architecture and Design Specification (SAD v1.2), '
    'Software Test Plan (STP v1.2), C++17 source code, and automated/system test suites. '
    'The project demonstrates exemplary architectural modularity, robust input validation, and exact state consistency during booking and cancellation workflows. '
    'All 76 automated unit tests pass without failure, and live interactive CLI testing confirms proper seat count restoration and error handling. '
    'With the remediation of documentation TBDs and recording of defect DEF-001, the project fulfills all academic and institutional requirements.'
)

t_sign = doc.add_table(rows=1, cols=4)
t_sign.style = 'Table Grid'
sign_hdrs = ['Role', 'Name', 'Date', 'Signature / Verdict']
for j, h in enumerate(sign_hdrs):
    t_sign.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

sign_rows = [
    ('Independent Reviewer / Quality Lead', 'R Vinay', '17/11/2026', 'R. Vinay (APPROVED)'),
    ('QA / Test Lead', 'Pranav S S', '17/11/2026', 'Pranav.S.S (VERIFIED)'),
    ('Development Lead', 'Parinitha Ramesh', '17/11/2026', 'Parinitha (VERIFIED)'),
    ('Project Instructor / Evaluator', 'Ashok Kumar Patil', 'Pending Eval', 'Accepted for Academic Review')
]
for row_data in sign_rows:
    r = t_sign.add_row()
    for j, val in enumerate(row_data):
        r.cells[j].text = val

# 6. Deliverable 5
doc.add_heading('6. Deliverable 5: Final Submission Readiness Checklist', level=1)
t_chk = doc.add_table(rows=1, cols=4)
t_chk.style = 'Table Grid'
chk_hdrs = ['Sl.', 'Verification Item', 'Standard / Target', 'Reviewer Verdict']
for j, h in enumerate(chk_hdrs):
    t_chk.rows[0].cells[j].paragraphs[0].add_run(h).bold = True

chk_items = [
    ('01', 'SRS IEEE-format structure', 'IEEE 830 / 29148 structure', 'PASS'),
    ('02', 'Functional Requirements completeness', 'FR-001 to FR-039 addressed', 'PASS'),
    ('03', 'Security Requirements & Objectives', 'SO-001–003, SEC-001–005 verified', 'PASS'),
    ('04', 'Non-Functional Requirements', 'NFR-001 to NFR-010 verified', 'PASS'),
    ('05', 'Requirements Traceability Matrix', 'Zero TBD entries (all linked)', 'PASS'),
    ('06', 'SAD Layered Architecture', 'Presentation/App/Validation/Data', 'PASS'),
    ('07', 'SAD Component & Sequence Diagrams', 'Layer-consistent diagrams present', 'PASS'),
    ('08', 'API / Module Interface alignment', 'Interfaces match src/*.h headers', 'PASS'),
    ('09', 'SAD Open Issues resolution', 'All Part-1 next steps closed', 'PASS'),
    ('10', 'STP IEEE-format structure', 'IEEE 829 standard structure', 'PASS'),
    ('11', 'STP Security Validation location', 'Section 5.1 (Faculty brief)', 'PASS'),
    ('12', 'Test Case Coverage', '15 formal test items (TC-001–014, Insp)', 'PASS'),
    ('13', 'Automated Unit Test Execution', '76/76 unit tests passed (0 failures)', 'PASS'),
    ('14', 'Code & Branch Coverage Reports', 'docs/Code-Coverage-Report.md', 'PASS'),
    ('15', 'Interactive CLI System Testing', 'TC-SYS-L01–04, TC-SYS-C01–05 verified', 'PASS'),
    ('16', 'Data Consistency Verification', 'Seats increment 198->199 on cancel', 'PASS'),
    ('17', 'Performance Benchmark', 'TC-C10 completes in 3ms (< 2.0s)', 'PASS'),
    ('18', 'Input Sanitization & Security', 'Tag stripping & regex boundary checks', 'PASS'),
    ('19', 'Error Handling & Robustness', 'Graceful errors without crashes', 'PASS'),
    ('20', 'Cross-Platform Build & Portability', 'Windows & Linux CI passing', 'PASS'),
    ('21', 'Code Cleanliness & Warnings', 'Compiles with -Wall -Wextra cleanly', 'PASS'),
    ('22', 'Defect & Limitation Logging', 'Honest reporting (DEF-001 to 005)', 'PASS'),
    ('23', 'Sign-Off & Approvals Table', 'Documented approvals across docs', 'PASS'),
    ('24', 'Git Repository Hygiene', 'Synced with upstream @ 08207b7', 'PASS'),
    ('25', 'Final Deliverables Packaging', 'DOCX and Markdown synchronized', 'PASS')
]
for item in chk_items:
    r = t_chk.add_row()
    for j, val in enumerate(item):
        r.cells[j].text = val

output_path = 'Reviewer_Audit_and_Compliance_Report_Team12.docx'
doc.save(output_path)
print(f'Successfully generated {output_path}')
