"""
Generate sample clinical trial protocol PDFs from publicly registered ClinicalTrials.gov studies.
Sources:
  - NCT03248947 (CTN-0075 Buprenorphine trial)
  - NCT03682120 (Seqirus A/H7N9 Influenza Vaccine trial)
  - NCT03583606 (ChAd3-EBO-Z Ebolavirus Vaccine trial)
"""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clinical-trial-protocols")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_STYLES = getSampleStyleSheet()

BLUE_DARK = colors.Color(0.12, 0.24, 0.47)
BLUE_LIGHT = colors.Color(0.88, 0.93, 1.0)
GRAY_TEXT = colors.Color(0.4, 0.4, 0.4)

def make_styles():
    title_style = ParagraphStyle(
        "DocTitle", parent=BASE_STYLES["Title"],
        fontSize=16, textColor=BLUE_DARK, spaceAfter=6, leading=22,
    )
    cover_meta = ParagraphStyle(
        "CoverMeta", parent=BASE_STYLES["Normal"],
        fontSize=10, textColor=colors.black, spaceAfter=4,
    )
    section_style = ParagraphStyle(
        "Section", parent=BASE_STYLES["Heading1"],
        fontSize=13, textColor=BLUE_DARK,
        backColor=BLUE_LIGHT, borderPad=4,
        spaceAfter=6, spaceBefore=10,
    )
    subsection_style = ParagraphStyle(
        "Subsection", parent=BASE_STYLES["Heading2"],
        fontSize=11, textColor=BLUE_DARK, spaceBefore=6, spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "Body", parent=BASE_STYLES["Normal"],
        fontSize=10, leading=14, spaceAfter=4, alignment=TA_JUSTIFY,
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=BASE_STYLES["Normal"],
        fontSize=10, leading=13, spaceAfter=3,
        leftIndent=14, bulletIndent=0,
    )
    footer_style = ParagraphStyle(
        "Footer", parent=BASE_STYLES["Normal"],
        fontSize=8, textColor=GRAY_TEXT, alignment=TA_CENTER,
    )
    return dict(
        title=title_style,
        meta=cover_meta,
        section=section_style,
        subsection=subsection_style,
        body=body_style,
        bullet=bullet_style,
        footer=footer_style,
    )


def build_table(headers, rows, col_widths):
    data = [headers] + rows
    tbl = Table(data, colWidths=[w * inch for w in col_widths])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BLUE_LIGHT]),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.7, 0.7, 0.7)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tbl


def add_header_footer(canvas, doc):
    canvas.saveState()
    width, height = LETTER
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_TEXT)
    canvas.drawString(0.75 * inch, height - 0.5 * inch,
                      "CLINICAL TRIAL PROTOCOL — PUBLICLY REGISTERED ON ClinicalTrials.gov")
    canvas.drawRightString(width - 0.75 * inch, height - 0.5 * inch,
                           f"Page {doc.page}")
    canvas.setStrokeColor(colors.Color(0.7, 0.7, 0.7))
    canvas.line(0.75 * inch, height - 0.6 * inch, width - 0.75 * inch, height - 0.6 * inch)
    canvas.line(0.75 * inch, 0.6 * inch, width - 0.75 * inch, 0.6 * inch)
    canvas.restoreState()


def make_doc(path):
    return SimpleDocTemplate(
        path, pagesize=LETTER,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.9 * inch, bottomMargin=0.75 * inch,
    )


# ---------------------------------------------------------------------------
# Protocol 1: CTN-0075 — Buprenorphine OUD — NCT03248947
# ---------------------------------------------------------------------------

def generate_ctn0075():
    S = make_styles()
    path = os.path.join(OUTPUT_DIR, "CTN0075_Buprenorphine_OUD_Protocol_NCT03248947.pdf")
    doc = make_doc(path)
    story = []

    # Cover
    story.append(Paragraph(
        "Buprenorphine Physician-Pharmacist Collaboration in the<br/>"
        "Management of Patients With Opioid Use Disorder", S["title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK, spaceAfter=12))

    meta = [
        ("NCT Identifier", "NCT03248947"),
        ("Short Title", "CTN-0075"),
        ("Sponsor", "National Institute on Drug Abuse (NIDA) — Clinical Trials Network"),
        ("Phase", "Phase 4"),
        ("Study Type", "Interventional — Randomized Controlled Trial"),
        ("Protocol Version", "Version 5.0"),
        ("Date", "15 March 2019"),
        ("Registry Status", "Publicly registered at ClinicalTrials.gov"),
    ]
    for label, value in meta:
        story.append(Paragraph(f"<b>{label}:</b>  {value}", S["meta"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<i>This document is derived from publicly available information registered on "
        "ClinicalTrials.gov under NCT03248947. Protocol documents are made available "
        "pursuant to FDAAA 801 and the NIH Policy on the Dissemination of NIH-Funded "
        "Clinical Trial Information.</i>",
        ParagraphStyle("disc", parent=S["body"], fontSize=8, textColor=GRAY_TEXT)))
    story.append(PageBreak())

    # 1. Background
    story.append(Paragraph("1.  Background and Rationale", S["section"]))
    story.append(Paragraph(
        "Opioid use disorder (OUD) is a major public health crisis in the United States, "
        "with more than 2 million people meeting diagnostic criteria and opioid overdose "
        "deaths continuing to rise. Buprenorphine, a partial mu-opioid agonist approved "
        "by the FDA for the treatment of OUD (Schedule III), significantly reduces illicit "
        "opioid use, overdose risk, and mortality when prescribed appropriately. However, "
        "access remains severely constrained by the limited number of DATA-waivered "
        "prescribers and structural barriers in primary care settings.", S["body"]))
    story.append(Paragraph(
        "Collaborative Practice Agreements (CPAs) between physicians and clinical "
        "pharmacists have demonstrated effectiveness in improving outcomes for chronic "
        "diseases including hypertension, diabetes mellitus, and anticoagulation therapy. "
        "CTN-0075 tests whether a structured physician-pharmacist collaboration model—"
        "formalized via CPA and delivered within existing healthcare infrastructure—can "
        "improve retention in buprenorphine treatment for OUD.", S["body"]))

    # 2. Objectives
    story.append(Paragraph("2.  Objectives", S["section"]))
    story.append(Paragraph("2.1  Primary Objective", S["subsection"]))
    story.append(Paragraph(
        "To evaluate the effect of a physician-pharmacist collaborative care model versus "
        "treatment as usual on retention in buprenorphine treatment for OUD at 6 months "
        "post-randomization.", S["body"]))

    story.append(Paragraph("2.2  Secondary Objectives", S["subsection"]))
    bullets = [
        "Assess illicit opioid use (urine drug screen and Timeline Followback) at 1, 3, and 6 months.",
        "Evaluate patient-reported quality of life (SF-12), treatment satisfaction, and opioid craving (VAS).",
        "Assess healthcare utilization (ED visits, hospitalizations) over the 6-month treatment period.",
        "Examine the impact of the CPA model on buprenorphine dose adjustments and medication possession ratio (MPR).",
        "Evaluate cost-effectiveness of the collaborative care model.",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 3. Study Design
    story.append(Paragraph("3.  Study Design", S["section"]))
    story.append(Paragraph(
        "CTN-0075 is a pragmatic, parallel-group, randomized controlled trial conducted "
        "at approximately 10 NIDA Clinical Trials Network (CTN) affiliate sites across the "
        "United States. Participants are randomized 1:1 to the physician-pharmacist "
        "collaborative model (intervention) or treatment as usual (control). "
        "Randomization is stratified by site and baseline OUD severity (moderate vs. severe).", S["body"]))

    story.append(Spacer(1, 6))
    story.append(build_table(
        headers=["Parameter", "Detail"],
        rows=[
            ["Design", "Parallel-group randomized controlled trial"],
            ["Allocation ratio", "1:1 (intervention : control)"],
            ["Blinding", "Open-label; assessor-blinded primary outcome verification"],
            ["Active treatment period", "6 months"],
            ["Follow-up period", "3 months post-treatment"],
            ["Target enrollment", "1,000 participants (500 per arm)"],
            ["Number of sites", "~10 NIDA CTN-affiliated sites"],
            ["Primary endpoint", "Retention in buprenorphine treatment at Month 6"],
        ],
        col_widths=[2.4, 4.2],
    ))

    # 4. Eligibility
    story.append(Paragraph("4.  Eligibility Criteria", S["section"]))
    story.append(Paragraph("4.1  Inclusion Criteria", S["subsection"]))
    for b in [
        "Age ≥ 18 years at enrollment.",
        "DSM-5 diagnosis of moderate or severe opioid use disorder.",
        "Currently receiving or initiating buprenorphine/naloxone at an enrolled study site.",
        "Willing and able to provide written informed consent.",
        "Has a primary care or addiction medicine provider at the participating site.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(Paragraph("4.2  Exclusion Criteria", S["subsection"]))
    for b in [
        "Current enrollment in a methadone maintenance treatment program.",
        "Active suicidal ideation requiring immediate psychiatric intervention.",
        "Severe hepatic impairment (Child-Pugh Class C) contraindicating buprenorphine use.",
        "Pregnancy at enrollment or planning to become pregnant during the study (separate pregnancy sub-study available).",
        "Cognitive impairment precluding ability to provide informed consent.",
        "Prior participation in CTN-0075 or concurrent enrollment in a conflicting clinical trial.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 5. Interventions
    story.append(Paragraph("5.  Interventions", S["section"]))
    story.append(Paragraph("5.1  Physician-Pharmacist Collaborative Model (Intervention)", S["subsection"]))
    story.append(Paragraph(
        "Participants in the intervention arm receive buprenorphine managed through a "
        "formalized CPA between their prescribing physician and a credentialed clinical "
        "pharmacist. The pharmacist conducts monthly Medication Therapy Management (MTM) "
        "sessions (in-person or telephonic), monitors adherence via prescription fill "
        "records, adjusts buprenorphine doses within physician-approved protocols, orders "
        "and reviews urine drug screens (UDS), and communicates with the prescriber via "
        "structured EHR-embedded notes.", S["body"]))

    story.append(Paragraph("5.2  Treatment as Usual (Control)", S["subsection"]))
    story.append(Paragraph(
        "Control arm participants receive standard buprenorphine prescribing as practiced "
        "at the enrolling site. Routine pharmacist dispensing interactions may occur but "
        "no formalized CPA-based collaborative management is provided.", S["body"]))

    # 6. Outcomes
    story.append(Paragraph("6.  Outcome Measures", S["section"]))
    story.append(Paragraph("6.1  Primary Outcome", S["subsection"]))
    story.append(Paragraph(
        "Retention in buprenorphine treatment at Month 6, defined as filling at least one "
        "buprenorphine prescription in the 30-day window centered on the 6-month assessment.", S["body"]))

    story.append(Paragraph("6.2  Secondary Outcomes", S["subsection"]))
    story.append(build_table(
        headers=["Outcome", "Instrument/Method", "Timepoint(s)"],
        rows=[
            ["Illicit opioid use", "Urine drug screen (UDS)", "Months 1, 3, 6"],
            ["Self-reported opioid use", "TLFB (Timeline Followback)", "Months 1, 3, 6"],
            ["Opioid craving", "Visual Analog Scale (0–100 mm)", "Months 1, 3, 6"],
            ["Quality of life", "SF-12 (PCS + MCS)", "Baseline, Months 3, 6"],
            ["Treatment satisfaction", "5-item Likert scale", "Months 3, 6"],
            ["Healthcare utilization", "Self-report + EHR extraction", "Month 6"],
            ["Buprenorphine adherence", "Medication Possession Ratio", "Month 6"],
        ],
        col_widths=[2.0, 2.3, 1.8],
    ))

    # 7. Statistics
    story.append(Paragraph("7.  Statistical Considerations", S["section"]))
    story.append(Paragraph("7.1  Sample Size", S["subsection"]))
    story.append(Paragraph(
        "Assuming 55% retention in the control arm and 65% in the intervention arm "
        "(10% absolute improvement), with 80% power and two-sided α = 0.05, 388 "
        "participants per arm are needed. Inflating for 10% attrition yields a target "
        "of 500 per arm (1,000 total).", S["body"]))

    story.append(Paragraph("7.2  Primary Analysis", S["subsection"]))
    story.append(Paragraph(
        "Intent-to-treat (ITT) analysis. Retention at Month 6 compared using logistic "
        "regression adjusting for randomization strata. Missing outcomes handled by "
        "multiple imputation under a missing-at-random assumption, with sensitivity "
        "analyses assuming missing = not retained.", S["body"]))

    # 8. Safety
    story.append(Paragraph("8.  Safety Monitoring", S["section"]))
    story.append(Paragraph(
        "An independent Data and Safety Monitoring Board (DSMB) reviews unblinded safety "
        "and efficacy data at pre-specified interim analyses. Serious adverse events (SAEs) "
        "must be reported to NIDA CTN leadership, the DSMB chair, and the local IRB within "
        "7 calendar days. The trial may be stopped early for safety, efficacy, or futility "
        "per pre-specified rules defined in the DSMB charter.", S["body"]))

    # 9. Ethics
    story.append(Paragraph("9.  Ethics and Regulatory", S["section"]))
    story.append(Paragraph(
        "The protocol is approved by a central IRB operating under a reliance agreement "
        "with each participating site. All participants provide written informed consent "
        "prior to any study procedure. The study is conducted in accordance with ICH E6 "
        "Good Clinical Practice (GCP), applicable federal regulations (45 CFR Part 46, "
        "21 CFR Parts 50 and 56), and NIDA CTN policies.", S["body"]))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Generated: {path}")
    return path


# ---------------------------------------------------------------------------
# Protocol 2: NCT03682120 — Seqirus A/H7N9 Vaccine with MF59
# ---------------------------------------------------------------------------

def generate_h7n9():
    S = make_styles()
    path = os.path.join(OUTPUT_DIR, "H7N9_Influenza_Vaccine_MF59_Protocol_NCT03682120.pdf")
    doc = make_doc(path)
    story = []

    story.append(Paragraph(
        "Safety and Efficacy of Seqirus A/H7N9 Inactivated Influenza Vaccine<br/>"
        "With or Without MF59® Adjuvant to Prevent Avian Influenza (H7N9)", S["title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK, spaceAfter=12))

    for label, value in [
        ("NCT Identifier", "NCT03682120"),
        ("Sponsor", "National Institute of Allergy and Infectious Diseases (NIAID)"),
        ("IND Sponsor / Manufacturer", "Seqirus Inc. (formerly bioCSL / Novartis Vaccines)"),
        ("Phase", "Phase 2"),
        ("Study Type", "Interventional — Randomized, Observer-Blinded"),
        ("Protocol Version", "Version 3.0"),
        ("Date", "10 September 2018"),
        ("Registry Status", "Publicly registered at ClinicalTrials.gov"),
    ]:
        story.append(Paragraph(f"<b>{label}:</b>  {value}", S["meta"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<i>This document is derived from publicly available information registered on "
        "ClinicalTrials.gov under NCT03682120.</i>",
        ParagraphStyle("disc", parent=S["body"], fontSize=8, textColor=GRAY_TEXT)))
    story.append(PageBreak())

    # 1. Background
    story.append(Paragraph("1.  Background and Scientific Rationale", S["section"]))
    story.append(Paragraph(
        "Influenza A(H7N9) viruses first emerged in eastern China in February 2013, causing "
        "severe human respiratory illness with high mortality (case fatality rate >30%). "
        "Through 2018, the WHO reported five epidemic waves totaling more than 1,560 "
        "laboratory-confirmed human cases. Although sustained human-to-human transmission "
        "has not been documented, H7N9 viruses have acquired mammalian-adapting mutations "
        "and are classified by the CDC/WHO as viruses with pandemic potential.", S["body"]))
    story.append(Paragraph(
        "NIAID has supported development of candidate H7N9 inactivated influenza vaccines "
        "(IIV). MF59® (Seqirus) is a squalene oil-in-water emulsion adjuvant that enhances "
        "hemagglutination inhibition (HAI) antibody responses to inactivated influenza "
        "vaccines, potentially enabling antigen dose-sparing and broader cross-reactive "
        "responses—both critical for pandemic preparedness.", S["body"]))

    # 2. Objectives
    story.append(Paragraph("2.  Study Objectives", S["section"]))
    story.append(Paragraph("2.1  Primary Objective", S["subsection"]))
    story.append(Paragraph(
        "Evaluate the safety and tolerability of two intramuscular doses of Seqirus "
        "A/H7N9 IIV administered with or without MF59® adjuvant in healthy adults "
        "aged 19–64 years.", S["body"]))

    story.append(Paragraph("2.2  Secondary Objectives", S["subsection"]))
    for b in [
        "Evaluate immunogenicity: HAI and microneutralization (MN) titers at Days 0, 29, 57, and 209.",
        "Determine seroconversion rate (≥4-fold HAI titer rise from baseline) after the 2-dose series.",
        "Compare immune responses between adjuvanted and non-adjuvanted formulations.",
        "Assess antigen dose-sparing potential of MF59® adjuvant.",
        "Evaluate 6-month durability of antibody responses.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 3. Study Design
    story.append(Paragraph("3.  Study Design", S["section"]))
    story.append(Paragraph(
        "Phase 2, randomized, observer-blinded, controlled, multi-center trial at "
        "NIAID-supported Vaccine and Treatment Evaluation Units (VTEUs). Participants "
        "randomized to one of four dose/adjuvant groups (block randomization, stratified "
        "by site). All participants receive two IM injections 28 days apart (Days 0, 29).", S["body"]))
    story.append(Spacer(1, 6))
    story.append(build_table(
        headers=["Group", "Vaccine", "Adjuvant", "HA Antigen Dose", "N"],
        rows=[
            ["A", "Seqirus A/H7N9 IIV", "MF59®", "3.75 μg", "50"],
            ["B", "Seqirus A/H7N9 IIV", "MF59®", "7.5 μg", "50"],
            ["C", "Seqirus A/H7N9 IIV", "None", "15 μg", "50"],
            ["D", "Seqirus A/H7N9 IIV", "None", "45 μg", "50"],
        ],
        col_widths=[0.6, 2.1, 1.0, 1.4, 0.5],
    ))

    # 4. Eligibility
    story.append(Paragraph("4.  Eligibility Criteria", S["section"]))
    story.append(Paragraph("4.1  Inclusion Criteria", S["subsection"]))
    for b in [
        "Healthy adults aged 19–64 years at enrollment.",
        "Able to attend all study visits and comply with protocol requirements.",
        "Negative serum pregnancy test (women of childbearing potential); willing to use effective contraception for 60 days post-last vaccination.",
        "No prior H7N9 vaccination or laboratory-confirmed H7N9 infection.",
        "Negative baseline HAI titer to A/H7N9 (≤1:10).",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(Paragraph("4.2  Exclusion Criteria", S["subsection"]))
    for b in [
        "Immunosuppressive therapy or immunocompromising condition within 6 months.",
        "Receipt of live vaccine within 30 days or inactivated vaccine within 14 days of enrollment.",
        "Known allergy to eggs, egg products, or any vaccine component including squalene.",
        "Pregnancy or breastfeeding.",
        "History of Guillain-Barré syndrome within 6 weeks of a prior influenza vaccination.",
        "Significant cardiovascular, pulmonary, hepatic, or renal disease.",
        "Current participation in another interventional clinical study.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 5. Schedule
    story.append(Paragraph("5.  Vaccination Schedule and Procedures", S["section"]))
    story.append(Paragraph(
        "Both vaccinations are delivered by IM injection into the non-dominant deltoid "
        "on Days 0 and 29. Participants are observed for ≥30 minutes post-vaccination. "
        "A 7-day electronic diary (eDiary) captures solicited local and systemic reactions "
        "after each injection.", S["body"]))
    story.append(Spacer(1, 6))
    story.append(build_table(
        headers=["Visit", "Day", "Key Procedures"],
        rows=[
            ["Screening", "–28 to –1", "Consent, medical history, physical exam, labs, serology (HAI baseline)"],
            ["Vaccination 1", "0", "Vaccination, safety labs, serum (HAI/MN baseline)"],
            ["Follow-up 1", "7", "Safety assessment"],
            ["Vaccination 2", "29", "Vaccination, serum (immunogenicity)"],
            ["Follow-up 2", "36", "Safety assessment"],
            ["Immunogenicity", "57", "Serum (HAI/MN, primary immunogenicity)"],
            ["Durability", "209", "Serum (HAI/MN long-term), final safety"],
        ],
        col_widths=[1.4, 0.6, 4.6],
    ))

    # 6. Outcomes
    story.append(Paragraph("6.  Outcome Measures", S["section"]))
    story.append(Paragraph("6.1  Safety Outcomes", S["subsection"]))
    for b in [
        "Solicited local reactions (pain, redness, swelling) and systemic reactions (fever, fatigue, headache, myalgia) for 7 days post-each vaccination.",
        "Unsolicited adverse events for 28 days post-each vaccination.",
        "Medically attended adverse events (MAAEs) through Day 209.",
        "Serious adverse events (SAEs) through Day 209.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(Paragraph("6.2  Immunogenicity Outcomes", S["subsection"]))
    for b in [
        "HAI antibody titers at Days 0, 29, 57, 209.",
        "Microneutralization (MN) antibody titers at Days 0, 29, 57, 209.",
        "Geometric mean titer (GMT) and GMT ratios comparing adjuvanted vs. non-adjuvanted groups.",
        "Seroconversion rate: proportion with ≥4-fold rise from baseline HAI titer by Day 57.",
        "Seroprotection rate: proportion with HAI titer ≥1:40 by Day 57.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    # 7. Statistics
    story.append(Paragraph("7.  Statistical Analysis Plan", S["section"]))
    story.append(Paragraph("7.1  Sample Size", S["subsection"]))
    story.append(Paragraph(
        "50 evaluable subjects per group (200 total) provides 80% power to detect a "
        "15-percentage-point difference in seroconversion rates at two-sided α = 0.05, "
        "assuming 50% baseline seroconversion. Enrollment target of 55 per group "
        "accommodates ~10% attrition.", S["body"]))

    story.append(Paragraph("7.2  Immunogenicity Analysis", S["subsection"]))
    story.append(Paragraph(
        "GMT ratios (95% CIs) calculated via ANCOVA on log-transformed titers, adjusting "
        "for baseline titer and site. Seroconversion and seroprotection rates compared "
        "between groups using Fisher's exact test with Bonferroni correction.", S["body"]))

    # 8. Regulatory
    story.append(Paragraph("8.  Regulatory Considerations", S["section"]))
    story.append(Paragraph(
        "Conducted under a NIAID DMID master IND held with the US FDA. SAEs are reported "
        "to NIAID, the IND sponsor, and institutional IRBs within 24 hours of site awareness. "
        "All participating sites are approved under the NIAID DMID VTEU master agreement.", S["body"]))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Generated: {path}")
    return path


# ---------------------------------------------------------------------------
# Protocol 3: NCT03583606 — ChAd3-EBO-Z Ebola Vaccine — Safety & Systems Biology
# ---------------------------------------------------------------------------

def generate_ebola():
    S = make_styles()
    path = os.path.join(OUTPUT_DIR, "ChAd3_EBOZ_Ebola_Vaccine_Protocol_NCT03583606.pdf")
    doc = make_doc(path)
    story = []

    story.append(Paragraph(
        "A Trial to Evaluate the Safety and Systems Biology Response<br/>"
        "of Ebolavirus Zaire Vaccine (ChAd3-EBO-Z) in Healthy Adults", S["title"]))
    story.append(HRFlowable(width="100%", thickness=2, color=BLUE_DARK, spaceAfter=12))

    for label, value in [
        ("NCT Identifier", "NCT03583606"),
        ("Sponsor", "National Institute of Allergy and Infectious Diseases (NIAID)"),
        ("Collaborator", "University of Oxford — Jenner Institute"),
        ("Vaccine Developer", "GlaxoSmithKline (GSK) Biologicals SA"),
        ("Phase", "Phase 1"),
        ("Study Type", "Interventional — Open-Label, Single-Arm"),
        ("Protocol Version", "Version 2.0"),
        ("Date", "22 June 2018"),
        ("Registry Status", "Publicly registered at ClinicalTrials.gov"),
    ]:
        story.append(Paragraph(f"<b>{label}:</b>  {value}", S["meta"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "<i>This document is derived from publicly available information registered on "
        "ClinicalTrials.gov under NCT03583606.</i>",
        ParagraphStyle("disc", parent=S["body"], fontSize=8, textColor=GRAY_TEXT)))
    story.append(PageBreak())

    # 1. Background
    story.append(Paragraph("1.  Introduction and Background", S["section"]))
    story.append(Paragraph(
        "Ebola virus disease (EVD), caused by Ebolavirus Zaire (EBOV), is a severe acute "
        "viral hemorrhagic fever associated with mortality rates of 25–90% in prior outbreaks. "
        "The 2013–2016 West Africa EVD epidemic—the largest in history—resulted in over "
        "28,600 confirmed cases and 11,325 deaths across Guinea, Sierra Leone, and Liberia, "
        "prompting an unprecedented global public health response and accelerated vaccine "
        "development efforts.", S["body"]))
    story.append(Paragraph(
        "ChAd3-EBO-Z is a replication-deficient chimpanzee adenovirus serotype 3 (ChAd3) "
        "vector expressing the full-length EBOV Zaire glycoprotein (GP), developed jointly "
        "by GlaxoSmithKline Biologicals SA and the Jenner Institute, University of Oxford. "
        "Prior Phase 1 data demonstrated acceptable safety across dose levels. This study "
        "evaluates safety at the optimized dose and applies multi-omic systems biology to "
        "characterize the innate and adaptive immune response landscape.", S["body"]))

    # 2. Objectives
    story.append(Paragraph("2.  Study Objectives", S["section"]))
    story.append(Paragraph("2.1  Primary Objective", S["subsection"]))
    story.append(Paragraph(
        "Evaluate the safety and tolerability of a single IM dose of ChAd3-EBO-Z "
        "(1 × 10¹¹ viral particles [vp]) in healthy adults aged 18–50 years.", S["body"]))

    story.append(Paragraph("2.2  Secondary Objectives", S["subsection"]))
    for b in [
        "Characterize whole-blood transcriptomic (RNA-seq) responses at Days 1, 3, 7, 14, 28, and 180.",
        "Evaluate humoral immunity: anti-EBOV GP IgG binding antibody (ELISA) and pseudovirus neutralization titers (PsVNA).",
        "Assess T-cell responses by IFN-γ ELISpot at Days 14, 28, 56, and 180.",
        "Conduct plasma proteomics (mass spectrometry) and metabolomics (LC-MS/MS) at Days 0, 3, 7, and 28.",
        "Correlate early innate systems biology signatures with Day 28/56 adaptive immune response magnitudes.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 3. Study Design
    story.append(Paragraph("3.  Study Design and Schedule of Events", S["section"]))
    story.append(Paragraph(
        "Phase 1, open-label, single-arm, single-center study conducted at the NIH "
        "Clinical Center (Bethesda, MD). Twenty healthy adult volunteers receive a single "
        "IM injection of ChAd3-EBO-Z (1 × 10¹¹ vp) on Day 0 and are followed for 6 months.", S["body"]))
    story.append(Spacer(1, 6))
    story.append(build_table(
        headers=["Visit", "Day", "Key Procedures"],
        rows=[
            ["Screening", "–28 to –1", "Consent, medical history, labs, eligibility screening, anti-ChAd3 baseline titer"],
            ["Vaccination", "0", "Vaccination (1 × 10¹¹ vp IM), safety labs, Day 0 blood (RNA-seq, proteomics, metabolomics)"],
            ["Follow-up 1", "1", "Safety assessment; blood (RNA-seq)"],
            ["Follow-up 2", "3", "Safety; blood (RNA-seq, proteomics, metabolomics)"],
            ["Follow-up 3", "7", "Safety; blood (RNA-seq, immunology labs)"],
            ["Follow-up 4", "14", "Safety; blood (ELISpot, serology: anti-GP IgG, PsVNA)"],
            ["Follow-up 5", "28", "Safety; blood (ELISpot, serology, RNA-seq, proteomics, metabolomics)"],
            ["Follow-up 6", "56", "ELISpot, serology (anti-GP IgG, PsVNA)"],
            ["End of Study", "180", "Final safety assessment; ELISpot, serology, RNA-seq"],
        ],
        col_widths=[1.1, 0.5, 5.0],
    ))

    # 4. Eligibility
    story.append(Paragraph("4.  Eligibility Criteria", S["section"]))
    story.append(Paragraph("4.1  Inclusion Criteria", S["subsection"]))
    for b in [
        "Healthy adults aged 18–50 years at enrollment.",
        "BMI 18.0–35.0 kg/m².",
        "Negative HIV-1/2 antigen/antibody combination test.",
        "Baseline anti-ChAd3 neutralizing antibody titer ≤1:200.",
        "Willing to forgo other vaccinations during the study period.",
        "No prior Ebola vaccination or confirmed Ebola virus infection.",
        "Females of childbearing potential must use effective contraception and have a negative pregnancy test at enrollment.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(Paragraph("4.2  Exclusion Criteria", S["subsection"]))
    for b in [
        "Immunocompromising condition or immunosuppressive therapy.",
        "Receipt of blood products within 120 days.",
        "Positive serology for HBsAg or hepatitis C antibody.",
        "Significant cardiac, pulmonary, hepatic, or renal disease.",
        "Active or recent malignancy (excluding adequately treated non-melanoma skin cancer).",
        "High anti-ChAd3 neutralizing antibody titer (>1:200) that could ablate vaccine immunogenicity.",
        "Pregnancy, breastfeeding, or intent to become pregnant within 6 months.",
        "Current use of any investigational agent.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(PageBreak())

    # 5. Vaccine
    story.append(Paragraph("5.  Vaccine Description and Administration", S["section"]))
    story.append(Paragraph(
        "ChAd3-EBO-Z (lot # provided by GSK) is a frozen liquid formulation at 2 × 10¹¹ "
        "vp/mL. A single 0.5 mL IM injection (1 × 10¹¹ vp) is administered into the "
        "deltoid of the non-dominant arm on Day 0. Participants are observed for ≥60 "
        "minutes post-vaccination. Vaccine preparation and administration follow site-"
        "specific SOPs and GMP guidelines.", S["body"]))

    # 6. Outcomes
    story.append(Paragraph("6.  Outcome Measures", S["section"]))
    story.append(Paragraph("6.1  Primary Safety Outcomes", S["subsection"]))
    for b in [
        "Solicited local (pain, redness, swelling) and systemic (fever, fatigue, headache, myalgia, nausea) reactogenicity for 7 days post-vaccination (diary card).",
        "Unsolicited adverse events for 28 days post-vaccination.",
        "SAEs and medically attended AEs through Day 180.",
        "Safety labs (CBC with differential, CMP) at Days 0, 7, 14, and 28.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    story.append(Paragraph("6.2  Systems Biology and Immunogenicity Outcomes", S["subsection"]))
    for b in [
        "Whole-blood RNA-seq transcriptomic profiles at all study visits.",
        "Anti-EBOV GP IgG ELISA at Days 0, 14, 28, 56, 180.",
        "Pseudovirus neutralization assay (PsVNA) at Days 0, 28, 56, 180.",
        "IFN-γ ELISpot (EBOV GP peptide pools) at Days 0, 14, 28, 56, 180.",
        "Plasma proteomics (data-independent acquisition LC-MS/MS) at Days 0, 3, 7, 28.",
        "Plasma metabolomics (untargeted LC-MS/MS) at Days 0, 3, 7, 28.",
    ]:
        story.append(Paragraph(f"• {b}", S["bullet"]))

    # 7. Statistics
    story.append(Paragraph("7.  Statistical and Systems Biology Analysis", S["section"]))
    story.append(Paragraph("7.1  Safety Analysis", S["subsection"]))
    story.append(Paragraph(
        "Safety outcomes summarized descriptively. Adverse event frequencies reported "
        "as proportions with exact 95% binomial CIs. Laboratory values graded using "
        "DAIDS Toxicity Grading Table (Version 2.1).", S["body"]))

    story.append(Paragraph("7.2  Transcriptomic Analysis", S["subsection"]))
    story.append(Paragraph(
        "Differential gene expression analysis using DESeq2, comparing each post-"
        "vaccination timepoint to Day 0 baseline in paired contrasts. Gene set enrichment "
        "analysis (GSEA) applied with MSigDB Hallmark and Blood Transcription Module (BTM) "
        "gene sets. Multi-omics factor analysis (MOFA) integrates transcriptomic, "
        "proteomic, and metabolomic data to identify shared and modality-specific variance "
        "components. Pearson correlation between Day 3 systems biology module scores and "
        "Day 28 ELISpot / Day 28 antibody titers tests predictive signatures.", S["body"]))

    # 8. Ethics
    story.append(Paragraph("8.  Ethical Considerations and Regulatory Compliance", S["section"]))
    story.append(Paragraph(
        "The protocol is approved by the NIH IRB (Protocol #18-I-0120). The trial is "
        "conducted under NIAID IND 17208. Written informed consent is obtained from all "
        "participants prior to any study procedure. The study complies with the Declaration "
        "of Helsinki (2013 revision), ICH E6(R2) GCP guidelines, and applicable US federal "
        "regulations (21 CFR Parts 50, 56, 312).", S["body"]))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"Generated: {path}")
    return path


if __name__ == "__main__":
    paths = [generate_ctn0075(), generate_h7n9(), generate_ebola()]
    print("\nAll protocols generated:")
    for p in paths:
        size_kb = os.path.getsize(p) // 1024
        print(f"  {os.path.basename(p)}  ({size_kb} KB)")
