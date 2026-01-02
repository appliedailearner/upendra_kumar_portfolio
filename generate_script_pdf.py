from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        # w=0 means utilize available width within margins
        self.cell(0, 10, 'Value-Selling Discovery Script', 0, 1, 'C')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 5, 'For Cloud Architects & Technical Leads', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(240, 240, 250)
        # Reset X to left margin to ensure full width usage is correct
        self.set_x(self.l_margin)
        self.cell(0, 8, label, 0, 1, 'L', True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.set_x(self.l_margin)
        self.multi_cell(0, 6, body)
        self.ln()

    def bullet_points(self, points):
        self.set_font('Helvetica', '', 11)
        for point in points:
            self.set_x(self.l_margin)
            # Indent slightly using string padding or separate cell? 
            # Safest is just text with dash.
            self.multi_cell(0, 6, f"- {point}")
        self.ln()

# Create PDF with explicit A4 format and margins
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.set_margins(15, 15, 15)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Introduction
pdf.chapter_title('Introduction')
pdf.chapter_body('This script is designed to help Cloud Architects move beyond "solution designing" to "deal shaping." Use this framework in your first customer interactions to uncover business triggers, quantify impact, and align technical solutions to executive outcomes.')

# Section 1
pdf.chapter_title('1. The Business Trigger (Opening)')
pdf.chapter_body('Do not accept generic statements like "we want to modernize." Dig for the compelling event.')
pdf.bullet_points([
    'Script: "I understand the goal is [Project Name], but I want to make sure we hit the timeline that matters most to you. What specifically triggered this conversation right now?"',
    'Follow-up: "What happens if you do nothing for the next 6 months?"',
    'Reality Check: "Is there a hard deadline driving this (e.g., data center exit, regulatory audit, license renewal)?"'
])

# Section 2
pdf.chapter_title('2. Clarify Pain in Business Terms')
pdf.chapter_body('Technical pain (latency) must be translated to business pain (revenue loss, reputation).')
pdf.bullet_points([
    'Script: "Where is the business feeling the most friction today because of the current state?"',
    'Quantify: "How does that impact your team - are we talking about lost hours, delayed releases, or actual downtime cost?"',
    'Constraints: "What are the non-negotiables we need to design around (budget caps, residency, compliance)?"'
])

# Section 3
pdf.chapter_title('3. Define Success Metrics')
pdf.chapter_body('If you cannot measure it, you cannot defend it.')
pdf.bullet_points([
    'Script: "If we come back in 90 days and say this project was a massive success, what number on your dashboard changed?"',
    'Examples: "Are we looking to reduce deployment lead time, cut incident volume by X%, or flatten the cost curve?"',
    'Commitment: "Great. So our design goal is to improve [Metric] by [Amount]."'
])

# Section 4
pdf.chapter_title('4. The Value Hypothesis (The Pivot)')
pdf.chapter_body('Connect your architecture to their metrics.')
pdf.bullet_points([
    'Script: "Based on what you said, here is how we will approach the architecture:"',
    '- "To solve [Pain Point 1], we will implement [Solution A] (e.g., Landing Zone automation) to drive [Metric B] (e.g., faster onboarding)."'
])

# Section 5
pdf.chapter_title('5. The Close: 90-Day Proof Plan')
pdf.chapter_body('Move to a tangible next step.')
pdf.bullet_points([
    'Script: "I know a full transformation is a big commitment. I propose we start with a 90-day value proof."',
    'Offer: "In the first 90 days, we will deliver: 1) A validated landing zone, 2) Migration of [Pilot App], and 3) A baseline of [Success Metric]."',
    'Ask: "Does that align with your priority for this quarter?"'
])

pdf.output("C:/MyResumePortfolio/assets/pdf/Value_Selling_Discovery_Script.pdf")
print("PDF generated successfully.")
