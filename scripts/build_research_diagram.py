"""Render the research overview as an editable SVG; standard library only."""
from pathlib import Path
from html import escape
R=Path(__file__).resolve().parents[1]
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1420" viewBox="0 0 1440 1420" role="img" aria-labelledby="title desc">','<title id="title">Research overview: evidence of AI-agent collusion</title>','<desc id="desc">Nine-explanation evidence framework, an 80-case exploratory audit and 20 fresh cases, measured evidence and results, with future validation clearly separated.</desc>', '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#718096" stroke-width="1.5"/></marker></defs>','<rect width="1440" height="1420" fill="#f5f7fb"/>']
def text(x,y,t,size=19,color='#334155',weight='400'):
 parts.append(f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(t)}</text>')
def box(x,y,w,h,title,lines,accent='#2563eb',dashed=False):
 dash=' stroke-dasharray="8 6"' if dashed else ''
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="white" stroke="{accent}" stroke-width="1.5"{dash}/>')
 text(x+22,y+34,title,22,accent,'700')
 for n,line in enumerate(lines):text(x+22,y+65+n*27,line)
def arrow(x1,y1,x2,y2):parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#718096" stroke-width="2" fill="none" marker-end="url(#arrow)"/>')
text(52,49,'BEYOND COLLUSIVE TALK',15,'#2563eb','700')
text(52,91,'Which evidence distinguishes collusion from its alternatives?',31,'#0f172a','700')
text(52,124,'Completed analyses and their evidentiary limits • Apart Research Track 2.3',19)
box(52,155,1336,123,'1  PROPOSED FRAMEWORK · nine explanations',[
'Q: trustworthy records   A: reciprocal agreement   I: implemented plan   P: harmful purpose',
'H: adverse consequences linked to the conduct. Communication causality remains separate.'])
arrow(385,278,385,308);arrow(1055,278,1055,308)
box(52,315,646,158,'2A  ARCHIVE · exploratory',[
'80 Jira episodes · 40 matched baseline–treatment seeds',
'Fine-tuned Qwen variants · 6 agents; candidate pair of 2',
'Archive fully exposed; no pristine held-out claim.'])
box(742,315,646,158,'2B  FRESH APPLICATION · transfer setting',[
'20 generated episodes · 10 matched seed pairs',
'gpt-4o-mini · 6 agents; automatic filling disabled',
'Deterministic rule frozen; semantic review not frozen.'])
parts.append('<path d="M385 473 V491 M1055 473 V491 M263 491 H1177" stroke="#718096" stroke-width="2" fill="none"/>')
for x in [263,720,1177]:arrow(x,491,x,508)
box(52,515,422,151,'3  CONVERSATION',[
'Publication and eligible access',
'Specific reciprocal commitments',
'Latest accepted plan and revisions'])
box(509,515,422,151,'3  ACTIONS',[
'Successful assignments / skips',
'Plan–action matching per actor',
'Missing choices, errors and fills'])
box(966,515,422,151,'3  CONSEQUENCES',[
'Team gap and group reward ranges',
'Pair / single / joint repair scores',
'Fill effects; upstream regret gap'])
parts.append('<path d="M263 666 V687 H1177 V666 M720 666 V687" stroke="#718096" stroke-width="2" fill="none"/>')
arrow(385,687,385,703);arrow(1055,687,1055,703)
box(52,710,646,190,'4A  ARCHIVE AUDIT',[
'240 judge calls: conversation / actions / combined',
'26 pairs both act; 74 episodes contain fills',
'194 responses flagged by citation / policy checks',
'Flags are not independently validated error labels.'])
box(742,710,646,190,'4B  FRESH SOURCE-LINKED REVIEW',[
'9 specific bilateral agreements supported',
'8 implemented plans with adverse patterns',
'1 agreement with uncertain implementation; 11 uncertain',
'Harm attribution unresolved; no additional judge calls.'])
arrow(385,900,385,938);arrow(1055,900,1055,938)
box(52,945,1336,155,'5  SYNTHESIS · 100 cases and 50 matched seed comparisons',[
'Keep evidence dimensions separate: agreement ≠ implementation ≠ attributable harm.',
'Distributional advantage, repair opportunities and environment effects answer different questions.',
'No independent reference labels: no validated accuracy, precision, recall or communication-causal estimate.'],accent='#0f766e')
arrow(720,1100,720,1140)
box(52,1147,1336,165,'FUTURE VALIDATION · proposed, not completed',[
'Independent references for the nine explanations; allow overlapping and unresolved categories.',
'Compare nested evidence combinations on untouched cases after freezing the complete annotation pipeline.',
'Use independent-decision controls and communication interventions for stronger dependence / equivalence claims.'],accent='#b45309',dashed=True)
text(52,1360,'Scope: 100-case evidence audit and proposed operational framework; not a validated harmful-collusion detector.',18)
text(52,1388,'Public case files: 20 generated cases only. Hugging Face source cases excluded; judge outputs and scores retained.',17,'#64748b')
parts.append('</svg>');out=R/'docs/figures/research-overview.svg';out.write_text('\n'.join(parts)+'\n');print(out)
