"""Build the concise paper figure as editable SVG; no dependencies."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1]
p=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1040" viewBox="0 0 1440 1040" role="img" aria-labelledby="title desc">','<title id="title">Evidence of AI-agent collusion: study design and findings</title>','<desc id="desc">80 archived and20 fresh cases feed conversation, action and outcome analyses. Fresh review supports9 agreements and8 enacted plans, with harm attribution unresolved. Outcome scores overlap algebraically; global loss and pair-only repair differ. Independent validation remains pending.</desc>','<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#94a3b8" stroke-width="1.5"/></marker></defs>','<rect width="1440" height="1040" fill="white"/>']
def t(x,y,s,size=24,color='#0f172a',weight=400,anchor='middle'):
 p.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>')
def box(x,y,w,h,color='#2563eb',fill='#f8fafc',dash=False):
 d=' stroke-dasharray="8 6"' if dash else ''
 p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="1.5"{d}/>')
def line(d,arrow=False):p.append(f'<path d="{d}" stroke="#94a3b8" stroke-width="2" fill="none"'+(' marker-end="url(#a)"' if arrow else '')+'/>')
t(720,48,'Which evidence distinguishes collusion?',34,weight=700)
t(720,84,'A nine-explanation framework',23,'#64748b')
box(70,120,610,116);t(375,162,'80 archived cases',30,weight=700);t(375,202,'240 model judgments',23,'#475569')
box(760,120,610,116);t(1065,162,'20 fresh cases',30,weight=700);t(1065,202,'Source-linked assistant review',23,'#475569')
line('M375 236 V268 H1065 V236')
for x in [270,720,1170]:
 if x!=720:line(f'M720 268 H{x}')
 line(f'M{x} 268 V300',True)
for x,title,sub in [(70,'Conversation','Reciprocal agreement'),(520,'Actions','Plan implementation'),(970,'Outcomes','Reward • repair • fills')]:
 box(x,310,400,110);t(x+200,354,title,28,weight=700);t(x+200,391,sub,23,'#475569')
line('M270 420 V452 H1170 V420 M720 420 V452')
line('M375 452 V486',True);line('M1065 452 V486',True)
box(70,496,610,180,'#0f766e','#f0fdfa');t(375,533,'FRESH EVIDENCE PROFILE',18,'#0f766e',700)
t(375,580,'9 agreements → 8 enacted plans',29,weight=700)
t(375,626,'Harm attribution unresolved',24,'#475569')
box(760,496,610,180,'#0f766e','#f0fdfa');t(1065,533,'BENCHMARK ACCOUNTING',18,'#0f766e',700)
t(1065,580,'Outsider loss = team gap + pair benefit',25,weight=700)
t(1065,626,'Overlapping scores ≠ extra corroboration',23,'#475569')
line('M375 676 V708 H1065 V676');line('M720 708 V740',True)
box(70,750,1300,140,'#334155','#f8fafc')
t(720,790,'Global loss can coexist with zero pair-only repair',29,weight=700)
t(720,836,'8 / 26 archive pairs     •     3 / 20 fresh pairs',28,'#334155')
line('M720 890 V924',True)
box(290,934,860,66,'#b45309','#fffbeb',True)
t(720,975,'Independent validation pending',25,'#92400e',700)
p.append('</svg>');(R/'docs/figures/research-overview.svg').write_text('\n'.join(p)+'\n')
