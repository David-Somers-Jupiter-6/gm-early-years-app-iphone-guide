# Changelog

Changes to the published website. The guide's own revision history is on its last page.

## Simple guide 1.4 – 26 November 2026 (live and trial)
Contacts and privacy (David).
- Contacts: "2 Choose your team" laid out the same way as "1 Choose your area", so it stays on one line in Safari (it was wrapped in a label element; the team box is now named by the heading instead).
- Contacts: the area note under the team box always keeps room for two lines, so the NHS login Support box no longer moves when switching between Bury, Rochdale (two lines) and Stockport (one line). Checked at 16 sizes: the box stays in exactly the same place. The Rochdale phone number no longer splits across lines.
- Accessibility and privacy: removed the line about GitHub keeping technical details (prototype). The page now fits without scrolling on iPhone 11 in Safari.
- Offline cache `ey-simple-v1.4`. Checked: 16 iPhone sizes plus Dark Mode (306 page states), no script errors, navigation tests pass.

## Simple guide 1.3 – 26 November 2026 (live and trial)
Every "Get help" opens the problem for that step (David).
- Steps 1, 3, 4, 5 and 6 already did. Step 2 and step 7 only opened the help page, as no problem covered them.
- New problems on Still not working?, in step order: "The link does not open the App" (step 2: check the App is installed, then tap the link again; GMDP Support) and "The App does not open after my code" (step 7: wait a few minutes, then email GMDP Support with the step and any error, never passwords or codes) – both from the full guide's own help.
- 7 problems; list rows slightly shorter on screens up to 700 px high. Only iPhone SE in Safari scrolls the closed list (56 px).
- Offline cache `ey-simple-v1.3`. Checked: 16 iPhone sizes plus Dark Mode (306 page states), each step's Get help opens its problem fully in view, no script errors, navigation tests pass.

## Simple guide 1.2 – 26 November 2026 (live and trial)
Cover: Bury, Rochdale and Stockport back on one line (David).
- Cause: in 1.0–1.1 the area labels were 14 px (full guide 13 px), with wider spacing and an Accessibility link on the same line, so Stockport wrapped on narrower iPhones (and on David's iPhone 11 in Safari, where only 16 px was spare in testing).
- Labels now match the full guide (13 px, 6 px gaps; "For families in" kept together); cover side padding 16 px on 375–389 px wide screens. Spare room on the line: 22 px (iPhone SE/mini, same as the full guide) to 79 px; 53 px on iPhone 11.
- The Accessibility link moved to the cover's bottom bar, beside Start (icon and label, like Help on the step pages).
- Offline cache `ey-simple-v1.2`. Checked: 16 iPhone sizes plus Dark Mode (288 page states), no script errors, navigation tests pass.

## Simple guide 1.1 – 26 November 2026 (live and trial)
The App's sign-in screen now has its own step (David).
- Step 1 "Open your Activation Link" ends at tapping the link ("The App sign-in screen opens").
- New step 2 "Tap Continue to NHS login": screenshot of the App sign-in screen; under Parents and carers sign in below, tap Continue to NHS login; the buttons further down are for staff.
- 8 steps (13 pages); later steps renumbered. Offline cache `ey-simple-v1.1`.
- Checked: 16 iPhone sizes plus Dark Mode (288 page states): every step page still fits without scrolling; nothing too wide; no script errors; navigation tests pass.

## Simple guide 1.0 – 26 November 2026 (new: live and trial)
A new, much simpler version of the guide at its own address (the full guide is unchanged).
- Live: /simple/ · Trial: /simple/preview/. Its own Home Screen app ("EY App help"; trial "EY Simple") and offline copy (cache `ey-simple-v1.0`).
- 12 pages: cover (one Start button, a calm "You are not on your own" message), Before you start (3 things you need, plus the App Store tip), 7 sign-in steps (the full guide's 15 steps paired; "Restart your iPhone" dropped), Still not working? (5 common problems: tap one to see who can help, what to do and one button), Contacts (Health Visiting team finder for Bury, Rochdale and Stockport; NHS login Support), Accessibility and privacy.
- Each step has up to 3 numbered actions, one screenshot (tap to see full size) and a "Stuck here?" card that opens the matching problem. A Help button sits between Back and Next on every step.
- No Contents, Search or Sign-in check.
- Checked: every page and state at 16 iPhone sizes plus Dark Mode (270 page states): nothing too wide, no script errors; every step page fits without scrolling at all sizes. Scrolling only on Contacts once a team is chosen, Still not working? with a problem open on smaller phones, and Accessibility and privacy in Safari on smaller phones. Navigation, Back from help, Done and Get help links tested.

## 3.92 – 26 November 2026 (live and trial)
Sign-in check: the question box stays in the same place from question 4 to question 5 (David saw it move down on his iPhone).
- Cause: question 5's info area (card + 76 px "See an example" preview) was exactly the tallest of the six, with no spare room, so a small difference in how Safari draws it put question 5's box lower than the others.
- The preview is 56 px: the two account headings above the blue "See an example · Tap here" bar (fade removed); the whole box still opens the full example. Question 5 now has at least 19 px spare at all 16 sizes, so the box position is set by the other questions.
- The alignment also re-runs once the guide's fonts have loaded.
- Effect: on some sizes all six question boxes sit 7–21 px higher than in 3.91 (iPhone 11 in Safari unchanged); still identical on every question at 16 sizes.
- Checked: scripts/check_iphone_sizes.py (1,760 checks: nothing cut off or too wide; only the known team-picker names shortened); questions aligned at 16 sizes; no script errors; navigation tests the same as 3.91.
- Build: scripts/make392.py + scripts/review392/fixes.py.

## 3.91 – 26 November 2026
Sign-in check polish (David).
- Start page: the 6 questions are in pairs (1–2 your App account, 3–4 your NHS login, 5–6 both accounts). The dividers were inside each pair (between 1 and 2, 3 and 4, 5 and 6); now there is one divider below question 2 and one below question 4, in the gap between the pairs, and none inside a pair. Same line colour (adapts to Dark Mode).
- Questions 1–6 (screens up to 760 px high, where the "?" icon sits beside the question): the question's first line sat 5.5 px (1.5 px on screens up to 640 px high) below the middle of the icon. Now centred on it, as "i" and its label are above; the answers and reply move up 5 px on all six questions, which still line up with each other at all 16 sizes. Taller screens keep the "? Question" label row (already aligned).
- Checked: scripts/check_iphone_sizes.py (1,760 checks at 16 sizes: nothing cut off, nothing too wide; only the known team-picker names shortened); questions aligned at 16 sizes; no script errors; navigation tests the same as 3.90.
- Build: scripts/make391.py + scripts/review391/fixes.py.

## 3.90 – 25 November 2026
Points 3, 9, 11, 13, 14, 15, 16, 17 and 19 from the problems-and-solutions doc, as chosen by David.
- Sign-in check questions 1 and 2 ask something real: "Is the account for you?" (Are you the child's mother or primary carer? Yes, I am / No, I am not) and "Will you sign in yourself?" (Will you be the one signing in? Yes, I will / No, someone else will). The "Please tap an answer, then tap Next." strip is kept exactly as it was. Start page, results and Search use the new names; on the results a No to either is now a ✗ with Get help (counted), not a soft "i" with Read more.
- Sign-in check questions on iPhone SE in Safari: question 1 now lines up with 2–6 (it sat 27 px higher, already so in 3.89). Question 5 asks "Are your details the same in both accounts?", so on larger iPhones all six questions sit 23 px higher than in 3.89 (still identical on every question).
- Help pages: the main action in "What to do" is a full-width solid button (at least 44 px); "Still stuck?" is an outlined button (contrast 5.2:1 light, 9.1:1 Dark Mode).
- One set of example details: the step 5 and NHS login step 2 screenshots show c.somers@example.com (were a real email domain); the phone number in 8 screenshots ends 0123 / XXX-XXX-00123 to match the Question 5 example (07700 900123); the example NHS number is 123 456 7890 as in the step 7 screenshot.
- "Find your Health Visiting team" (was "Contact"), in Contents and Search too. Under the pickers: "You do not need to call them now. Keep their number handy in case the sign-in check finds a problem." – it gives way to the team's card once a team is chosen, so nothing above moves.
- Step 1: "Open Safari to come back to this guide." added as a fourth line; the filler sentence removed.
- "Check your NHS login details" (was "Signing in to NHS login"): the tips of steps 2–6 and Install step 4 are on their step pages; 6 tip pages removed (83 → 77 pages); Back/Next and page counts renumbered. Step 7's Note page and "Installation complete" stay.
- NHS login help says once, positively, who can help: the menu opens "NHS login is run by the NHS. Only its Support team can see or change your account."; under "Who can help · NHS login Support team" on 7 help pages: "Only they can see or change your NHS login account." (David's full sentence took 3 lines and pushed pages off an iPhone SE.) The GMDP line on NHS login step 1 removed.
- Wording: step 3, step 5, Question 5; curly apostrophes (Partner's, child's).
- Safari tab title "GM Early Years App – help signing in"; Home Screen name "EY App help"; "REVIEW DRAFT" removed from Document control and the page description.
- Checked: scripts/check_iphone_sizes.py (1,760 checks at 16 sizes: nothing cut off, nothing too wide; only the known team-picker names shortened); all 6 questions aligned at 16 sizes; no script errors; results, help and side-trip navigation tests the same as 3.89; NHS login check and install steps walked with Next and Back.
- Build: scripts/make390.py runs scripts/review390/fixes.py, fixes2.py and example_details_images.py.

## 3.89 – 25 November 2026
- Sign-in check start page: each of the 6 questions has a round "?" button on the right that opens the help page for that question – the same pages the results page uses (1 Who the account is for, 2 Who can sign in, 3 Set up NHS login, 4 Cannot sign in, 5 Common sign-in problems, 6 Activation Link issues). Back or Done on the help page returns to the start page. Its tap area is the full height of its row, so neighbouring buttons never overlap. "?" contrast 5.8:1 (light) and 7.9:1 (Dark Mode).
- Sign-in check start page: the 6 questions sit on the page background instead of white cards, so only real menus have white rows (fix 12 from the problems-and-fixes doc).
- Sign-in check questions: the "i" beside "Please tap an answer, then tap Next." is centred in its circle (it sat about 4 px high; now within 1 px, like the ✓ and ! icons).
- Checked: scripts/check_iphone_sizes.py (1,856 checks at 16 sizes: nothing cut off, nothing too wide; only the known team-picker names shortened); no script errors; results, help and side-trip navigation tests the same as 3.88; every "?" button tested by tapping at SE, iPhone 12–16 and Pro Max sizes.
- Build: scripts/make389.py runs scripts/review389/fixes.py.

## 3.88 – 25 November 2026
Fixes 4, 5, 6, 7, 9, 10 and 11 from the problems-and-fixes doc, as chosen by David.
- You are signed in (step 15): the right-hand button is Finish and goes back to the cover. The green box now says "You can close this guide now", and one line covers notifications and where to find help later. The screenshot keeps its 3.87 size on every iPhone.
- One set of counting words in the title boxes: Stage, Step and Question. How this guide works: "Before you start" (was "Section 1"); Sign-in check: "Stage 1 of 3 · What you need" (was "Section 3"); Signing in: "Step 5 of 15 · NHS login" (was "Part 2 of 3 · NHS login"). Contents, Search and the navigation are unchanged.
- Cannot get into your email: on iPhone SE in Safari the "Lost access to your email" button keeps its side padding (the icon touched the edge and the last letter was clipped).
- Your results: the "Sign-in check" label lines up with the right edge of the progress bar.
- Sign-in check questions: "Please tap an answer, then tap Next." shows in the space kept for the reply until an answer is tapped; the reply then takes its place, so nothing moves. Tapping Next without an answer still highlights it in blue. iPhone SE in Safari keeps the 3.87 behaviour (the reply space is under the bottom bar there).
- "No" replies: a round amber "!" icon in place of the red STOP sign.
- Set up NHS login and Cannot sign in: the main link is the same solid blue button inside "What to do" as on the other NHS login help pages.
- Checked: scripts/check_iphone_sizes.py (1,856 checks at 16 sizes: nothing cut off, nothing too wide; only the known team-picker names shortened); no script errors; results, help and side-trip navigation tests give the same results as 3.87; Finish goes to the cover; hint contrast 11.7:1 (light) and 12.2:1 (Dark Mode).
- Build: scripts/make388.py runs scripts/review388/fixes.py.

## Publishing setup – 24 November 2026 (evening)
- The deploy step now waits 15 seconds after the files are uploaded, and tries again up to twice (after 45 and 90 seconds) if GitHub has not registered the upload yet ("Found 0 artifact(s)" / "No artifacts named github-pages"). The guide itself is unchanged (3.87).

## 3.87 – 24 November 2026
- Sign-in check results: the bottom button is always Next and always goes to Section 4 Signing in, whatever the answers. Before, with anything red it said Done and went to Support, and Back from Support then went to "You are signed in" (step 15) because the trail had been reset.
- Get help / Answer / Read more on the results page: Next (or Done) keeps bringing you back to the results; Back too (unchanged, now tested).
- Side trips: the Health Visiting team and Contacts pages (hv, s5-hv, s5-2, s5-gmdp), when opened from a link on a Sign-in check, Signing in or Support page, now have a Done button back to where you were (as the GMDP help page already had). Before, Next from there carried on through Contacts and About this guide. Reached from Contents, Search or in page order they work as before.
- Checked: every results route (all Yes, one No, mixed, all No; every Get help link; every link inside each help page; every question reply link), Contacts in page order and from Contents; 16 iPhone sizes all fit; no script errors; contrast 2,436 text items at WCAG AA.
- Build: scripts/make387.py runs scripts/review387/nav_fix.py.

## 3.86 – 24 November 2026 (live and trial)
- Every page now fits on 16 iPhone sizes, from iPhone SE in Safari (375×548) to iPhone 16 Pro Max on the Home Screen (440×896), including Sign-in check questions after an answer, the results page (all Yes, all No, mixed) and the Health Visiting team finder (contact details and map).
- Sign-in check questions: after Yes or No, the reply was partly or fully hidden behind the bottom bar in Safari on every iPhone except the largest (since 3.78 or earlier). On screens 760 px high and under, the "?" icon now sits on the question's line and "Tap an answer, then tap Next." gives way; on 650 px and under the answer boxes are 44 px. Safety net: if a reply still opens below the bottom bar (iPhone SE in Safari), the page scrolls just enough to show it.
- Sign-in check start page: the compact list also on 701–730 px high screens (iPhone 11/XR in Safari, where question 6 was hidden).
- iPhone SE in Safari (600 px high and under): the location label sits above the title (3.85 drew it over the title); Contents leaves out the Cover/Introduction/Contents tiles and row subtitles; slightly shorter cover photo; NHS login account help, Sign-in check start page and Document control slightly tighter.
- Revision history: the 3.85 line now reads "calmer title boxes" (was "plain page titles").
- Checked: scripts/check_iphone_sizes.py (1,856 checks at 16 sizes: nothing cut off, nothing too wide); every page laid out as in 3.85 on screens 760 px and taller; no script errors; contrast of all 2,436 text items in light and Dark Mode at WCAG AA.
- Known: Health Visiting team picker shows "Ramsbottom, Tottington and North M…" and "Cheadle Hulme and Bram…" shortened (the full name shows in the card under it).
- Build: scripts/make386.py runs scripts/review386/fit_all_iphones.py.

## 3.85 – 24 November 2026 (live and trial)
- Design review, points 1–4 (as chosen in the mock-ups), plus tinted step numbers on How this guide works.
- Title box: calmer – no underline, fainter ABC blocks in the background, a location label in the box ("Section 3", "Your App account · Question 1 of 6", "Installing the App · Step 2 of 7"); the thin coloured strip at the top of the page stays on the cover only.
- One list style everywhere (Contents, Sign-in check start page, Contacts, Support, Your results): a white grouped panel, 44–52 px rows, 30 px icon tiles and grey chevrons.
- List icons as soft tints: pale pink with deep magenta, pale blue with NHS blue, grey for Accessibility.
- Buttons: Begin, Yes and "Stuck?" in one calm blue, with no pulse or glow (cover unchanged).
- Fewer capitals and less bold: in-page labels in sentence case at 15 px semibold; 36 bold words made regular ("child's mother or primary carer" stays bold).
- How this guide works: step numbers as tinted squares.
- Help icons (Who is it for, The issue, Who can help, What to do) stay solid for now.
- Checked: all 23 site checks pass; no script errors; nothing newly cut off (fits the same as or better than 3.84); contrast of all text in light and Dark Mode at WCAG AA.
- Build: scripts/make385.py runs the six scripts in scripts/review385. Not yet chosen: scripts/drafts/shape_spacing_draft.py (point 5) and tinted_help_icons_parked.py.

## Publishing setup – 24 November 2026
- GitHub Actions workflow moved off the deprecated Node.js 20 actions: actions/checkout v4 → v6, actions/configure-pages v5 → v6, actions/upload-pages-artifact v4 → v5, actions/deploy-pages v4 → v5. The guide itself is unchanged (still 3.84).

## 3.84 – 24 November 2026 (live and trial)
- "Troubleshooter" renamed "Sign-in check" everywhere carers see it (Contents, title boxes, section labels, Support menu, search, "Return to the sign-in check").
- Sign-in check start page (option B): "Who should answer" box with a person icon; the six questions as light, one-line rows grouped under Your App account, Your NHS login and Both accounts; "Answer Yes or No. It takes about 2 minutes." On short screens the headings and the time line give way.
- Questions 1 and 2: the No reply reads "Who can help · contact" with the "Your Health Visiting team" link on the next line (two lines, was three).
- Your results: shorter row titles (Who can sign in? · Do you have NHS login? · Can you sign in to NHS login? · Do your details match? · Has your link arrived?) so no row goes over two lines; on short screens all six answered rows now fit (the last was hidden behind the bottom bar).
- Next: a second tap within 450 ms is ignored (a quick double tap turned two pages). From the Home Screen on iPhones with a home indicator, the bottom bar sits higher, above the swipe-up area, so taps near the bottom edge are not lost.
- Checked: no broken links or script errors; every page lays out as in 3.83; nothing newly cut off; contrast of all 2,750 text items in light and Dark Mode at WCAG AA.
- Build: scripts/make384.py runs scripts/review384/changes.py and start_page.py (option B).

## 3.83 – 24 November 2026 (live and trial)
- Dark Mode: the Troubleshooter information box (all six questions) stayed light while its text turned light, so it was almost unreadable; it is now dark navy with light text. Links and the "Who can help" label in the Troubleshooter replies are now light blue.
- Both modes: small labels on the coloured title boxes (Part / Question / Stage / Installing the App) are white instead of pale blue; a Next button waiting for an answer has dark grey text on light grey in Light Mode so it can be read.
- Menus on Apple text sizes: cover (title 28, subtitle 17, labels 12, Start/For families 15, area labels 13), Contents tiles 15, Signing in overview 15, Support menu titles 17, GM Early Years App help 16/15, NHS login help list 17, stage labels 12, section badges 22. Short screens (Safari): GM Early Years App help 15/13 and Your results 15 so no row hides behind the bottom bar; the How this guide works note gives way.
- Wording: "go to Section 5 · Signing in" (wrong since 3.77) → "Signing in"; "(see Section 6 · Contacts)" → "(see Contacts)"; Contacts' team finder says Area.
- Checked: contrast of all 2,750 text items on every page (plus search results, team chosen, Troubleshooter replies) in light and Dark Mode – none below WCAG AA; every page lays out as in 3.82; nothing newly cut off at any test size.

## 3.82 – 24 November 2026 (live and trial)
- Search: the results list can no longer be dragged sideways off the page (it was 8px wider than its box, so iPhone let it scroll sideways); a sideways swipe no longer leaves Search (swipe right counted as Back); GM Early Years App icon in the title box; result snippets no longer start with title-box text ("NHS login Step 5 of 15:") and labels end with a full stop; topic "Contact your Health Visiting team"; greyed-out Next hidden.
- Contents: search button styled like the cover's Search row (green magnifier, Search, red microphone that starts voice search) on a white pill with a shadow; Cover page, Introduction and Contents as a row of tiles; sections grouped under Stage 1 · What you need (2, 3), Stage 2 · How to sign in (4), Stage 3 · Who can help (5, 6).
- Fix: 3.81 cut off the bottom of Contents by 10px on 375×635 screens. Contents now fits at every test size.
- Checked: no broken links or script errors; every page lays out as in 3.81 apart from the Search title; swipe still turns pages elsewhere; Contents links.
- Build: scripts/make382.py runs scripts/review382/search_contents.py (option B).

## 3.81 – 24 November 2026 (live and trial)
- 3.81 published to the live site (from 3.80), bringing 3.80's fixes live too. A text and UX review of every main page, for clearer, calmer wording for frustrated carers.
- Cover: subtitle "A guide to signing in on your iPhone"; Start the guide "One step at a time"; Bury, Rochdale and Stockport as soft labels (no border, not tappable) with a map pin before "For families in"; no greyed-out Back. Version kept.
- Introduction: example of the "one small detail" (a mobile number that does not match); "Tip: read this guide on another screen"; a line for carers with only their iPhone. Contents: short lines under Troubleshooter, Support and Contacts; How this guide works in its own card. How this guide works: the three stages use the same names as the Stage markers, plus a note that the stage is shown at the top of each page.
- Contact your Health Visiting team: title matches Contents; "Choose your area, then your team"; "Locality" → "Area"; every team says what to say when calling.
- Signing in (18 → 16 pages): "You will need" lists the Activation Link text; restart steps say how; help if the text cannot be found; clearer titles (Enter your email and password; Wait for / Enter the security code; Get / Wait for / Enter your App code); "Two different codes" box; don't tap the code message; TAP chips on steps 7 and 12; "Not your number?" links to the team finder; the two Helpful tip pages folded into steps 12 and 13 ("Stuck on this screen?" → Support, no section number).
- Support: "What do you need help with?"; the NHS login and App cards no longer overlap (App codes on the App card); NHS logo on the NHS login card. Contacts: team icon for Your Health Visiting team; plainer "For:" lines; GMDP email address breaks after the @.
- Accessibility: "Other formats" box; "you can ask for it in…"; email as a button; "Text too small?" tip. About this guide: "You do not need these pages to sign in." Accessibility statement: "Accessibility statement · N of 4" marker; GOV.UK compliance wording; clearer screenshots issue. Privacy: NHS login and the App have their own privacy notices; "GMDP Support Team".
- Page counters recomputed: 83 pages (Signing in 16). Checked: no broken links or script errors; every page's title box, progress lights, strip and navigation bar in the same place as 3.80; Signing in Back/Next 1–16; Dark Mode.
- Build: scripts/make381.py runs the review patches in scripts/review381.

## 3.80 – 23 November 2026 (trial)
- Fix: after 3.77 renumbered the sections, the Signing in pages lost their slim progress lights (numbered circles ran over "Part N of 3"), their screenshot sizing, the "Tap to enlarge" position and their title box height, while the Support NHS login step pages picked those styles up. 20 style rules picked out Signing in by its label 'Section 5'; they now use a permanent marker on the 18 Signing in pages (data-signin), so renumbering or renaming sections cannot break them again. Checked: all 85 pages lay out exactly as in 3.76 (3.79 differed on 30).
- Support menu order: NHS login account help, GM Early Years App help, Still need help?, Troubleshooter.

## 3.79 – 23 November 2026 (live)
- 3.79 published to the live site (from 3.78): Section 5 renamed Support, Section 6 renamed Contacts, and the Signing in step 13 tip fixed.

## 3.79 – 23 November 2026 (trial)
- Section 5 "Troubleshooting" renamed "Support" and Section 6 "Contact & support" renamed "Contacts": Contents, page titles, section labels and strips (82 + 12), aria labels, Done buttons ("Done – back to Support"), the search "no results" shortcut, the NHS login band on the NHS login Support team page, and the in-text mentions ("see Section 6 · Contacts", "Contact details for every team are in Section 6, Contacts").
- Fix: the Signing in step 13 tip still said "go to Section 6 · Troubleshooting" after the 3.77 renumbering; it now says "Section 5 · Support".

## 3.78 – 23 November 2026 (live)
- 3.78 published to the live site (from 3.76). Brings live the new structure from 3.77 (Troubleshooter as Section 3; About your account and the Checklist removed; Signing in 4, Troubleshooting 5, Contact & support 6) and the Contents fix below.

## 3.78 – 23 November 2026 (trial)
- Contents lists itself: Cover page, Introduction, Contents, How this guide works … (the Contents row uses the list icon and is marked as the current page).

## 3.77 – 23 November 2026 (trial)
- New structure. Contents: Cover page, Introduction, 1 How this guide works | 2 Contact your Health Visiting team (own band) | 3 Troubleshooter (own band) | 4 Signing in to the GM Early Years App | 5 Troubleshooting, 6 Contact & support | Accessibility, About this guide.
- Removed Section 3 About your account (acct, nhs) and Section 4 Checklist (s2, c1–c4, sum) – the Troubleshooter replaces them – and their script references (Checklist reset, summary count, answer dots, question alignment).
- The Troubleshooter (ts, ts1, ts1b, ts2–ts5, tsum) moved straight after Contact your Health Visiting team as Section 3 (labels, strip, aria label). Signing in is now Section 4, Troubleshooting 5, Contact & support 6 (labels, badges, aria labels, "see Section 6" mentions).
- Back / Next: Contact your HV team → Troubleshooter; Troubleshooter Back → Contact your HV team; Signing in Back → Troubleshooter results. Results Next goes to Signing in (all clear) or Troubleshooting (something to sort out) as before.
- Activation Link "When you have your link": "Return to the Troubleshooter – answer question 6, then follow the sign-in instructions."
- How this guide works: step 1 now "your Health Visiting team, then the Troubleshooter's 6 quick Yes or No questions".
- Page counters recomputed: 85 pages (Welcome 3, 1, 1, Troubleshooter 8, Signing in 18, Troubleshooting 41, Contact & support 5, About this guide 8).
- Checked: every internal link has a target; nothing refers to the removed pages; clicking Next from the cover runs cover → intro → contents → how → hv → Troubleshooter → results → Signing in; every Contents row opens the right page; Back links at every join; no script errors. validate_site.py now expects the Troubleshooter instead of the Checklist.

## 3.76 – 23 November 2026 (live)
- 3.76 published to the live site (from 3.51). Brings live all changes in 3.52–3.76: the Troubleshooter reworked into information boxes and Question windows (clearer titles, Does that make sense? on questions 1–2, Who can help / STOP replies lined up with the answers, same-size reply boxes, nothing moves when an answer is tapped, every question in the same place), who should answer at the top of the start page, question 5 version B (name, NHS number, mobile number and email address), Apple text sizes, shorter wording for 375-wide iPhones, and results rows showing the question title only.

## 3.76 – 23 November 2026 (trial)
- Troubleshooter results: each row shows only the question title (the second line, e.g. "Read who can access the account", "You need an NHS login account", "Not answered yet", is hidden), so every row is at most three lines. The icon and button (Get help / Read more / Answer) still show the result. The page now fits without scrolling on a 375-wide iPhone from the Home Screen even with all six answers needing help.

## 3.75 – 23 November 2026 (trial)
- Fix for iPhones that show the guide 375 points wide (iPhone 11 with Display Zoom, X/XS/11 Pro, 12/13 mini), opened from the Home Screen: question 5 now reads "Did you give your Health Visiting team these same details?" (two lines; it was three, which made every question reserve three lines) and question 2's Yes reply "Only the account holder can access the account." (two lines; it was three, which made every reply box three lines tall). Fit tests now subtract the status bar (Home Screen) as well as Safari's bars. 375-wide Home Screen: 37 pt over → 5 pt over.

## 3.74 – 23 November 2026 (trial)
- Troubleshooter titles (also start page list, results page and data-title): 1 "Who is the account for?", 2 "Who can sign in to the account?", 3 "Do you have an NHS login account?", 4 "Can you sign in to your NHS login account?", 5 "Are your details the same in both accounts?", 6 "Has your Activation Link arrived?". The title box is the same size for one- and two-line titles, so nothing moves.
- Information boxes have two short sections under a thin line: 1 Who it is for / If it is for the wrong person; 2 Who can access it / How they sign in; 3 What you need ("You need to have set up your own NHS login account. You use it to sign in to the GM Early Years App.") / Who must set it up (the account holder); 4 Signing in / Whose NHS login (the account holder's); 6 How it arrives / What it does. Everything still lines up on all six questions (375, 390, 430 wide); at 430 wide question 3's box sets the shared height (+6 px on every question).

## 3.73 – 23 November 2026 (trial)
- Troubleshooter questions 1–6: the ? QUESTION label, the question, "Tap an answer, then tap Next.", the Yes and No answer boxes and the reply boxes are in exactly the same place on every question (tsAlign now shares .ts-info, .ts-qa, .radios and .ts-replies; hint spacing the same on all six). Checked after Yes and after No at 375, 390 and 430 wide. Questions with a one-line question have a line's space before the hint. (3.72 did not deploy – GitHub Pages artifact error – and is included here.)

## 3.72 – 23 November 2026 (trial)
- Questions 1–2 No reply: the NHS logo is placed exactly like the green tick (absolute, 8 px in, centred top to bottom), so its centre lines up with the answer circles, and WHO CAN HELP / Contact Your Health Visiting team starts where the answer text starts. Replaces the negative-margin layout, which could render differently on iPhone.

## 3.71 – 23 November 2026 (trial)
- Troubleshooter start page: "Please answer as the child's mother or primary carer (the account holder)." now comes first; "Answer Yes or No. It takes a minute or two." stays at the end.
- Questions 1–6: the Question window starts at the same height on every page, and every Yes / No reply box is the same size (tsAlign shares .ts-info and .ts-replies heights across the six); nothing moves when an answer is tapped (checked at 375, 390 and 430 wide).
- Question 1: "In this guide, we call this person the account holder." joins the first sentence. Questions 1–2: "Does that make sense?" / "Yes, that makes sense" / "No, I'm not sure".
- Question 3: "NHS login confirms who you are." joins the first sentence; Who can help window removed; No answer "No, I do not have NHS login" (one line, like Yes); Yes reply "You will use it to sign in to the GM Early Years App."
- Question 4: new layout; Who can help removed; Signing in: "You need to be able to sign in to your own NHS login account before you can use the GM Early Years App."; Yes "You can use NHS login to sign in to the GM Early Years App."; No (STOP) "The NHS login Support team can help. See Cannot sign in."
- Question 5: new layout, version B – What must match: name, NHS number, mobile number and email address; question "Did you give your Health Visiting team the same details you use for NHS login?"; answers "Yes, they are the same" / "No, or I'm not sure"; Yes "Your details should match, so you can sign in."; No (STOP) "Your details must match to sign in. See Details do not match."
- Question 6: new layout; How it arrives; Yes "You have your Activation Link."; No (STOP) "You need it to sign in. See Activation Link not received."
- Apple text sizes: start page list and end line 17 (Body), list numbers 15 (Subheadline), results heading 17 (Headline). All Troubleshooter text is now on Apple's scale.

## 3.70 – 23 November 2026 (trial)
- Question 3 titled "Do you have NHS login?" (one line; "Do you have an NHS login?" took two), also in the start page list and on the results page. What you need: "You can only sign in to the GM Early Years App with your own NHS login account." Laid out like questions 1–2 (question window straight under the information, no gap under the question, reply slot kept so nothing moves). Yes: "You need your own NHS login to use the GM Early Years App." No (STOP): "You need one to use the GM Early Years App. See Set up NHS login." Both two lines on every iPhone. Who can help window kept for now.
- Questions 1–3: reply icons sit in the middle of their box; a chosen answer turning bold no longer changes its height.

## 3.69 – 23 November 2026 (trial)
- Question 2 (Who will be able to access the account?) laid out exactly like question 1: Who can help window removed; question window straight under the information; no space under the question; reply slot kept so nothing moves; Yes "Only the account holder can access the GM Early Years App account." (two lines on every iPhone); No is the NHS logo, WHO CAN HELP and "Contact Your Health Visiting team" (link); icons and text in line with the answers.

## 3.68 – 23 November 2026 (trial)
- Question 1 No reply: only the NHS logo, WHO CAN HELP and "Contact Your Health Visiting team" (link to Contact your Health Visiting team; Back returns to question 1).

## 3.67 – 23 November 2026 (trial)
- Question 1 replies: Yes (green tick) is "The account is set up for the child's mother or primary carer." on two lines, no heading; No (blue i) is the information, then WHO CAN HELP / Your Health Visiting team with the NHS logo, no heading. Reply icons, the NHS logo and the "Please tap an answer" reminder icon sit in line with the answer circles; all reply text starts where the answer text starts.

## 3.66 – 23 November 2026 (trial)
- Question 1 (About your account): the question window sits straight under "Who it is for" (question 1 no longer shares heights with questions 2–6); no space between the question and "Tap an answer, then tap Next."; the reply slot is kept from the start (Yes reply, No reply and "Please tap an answer" share it), so nothing moves when an answer is tapped.

## 3.65 – 23 November 2026 (trial)
- Question 1 (About your account): Who can help window removed (the question window keeps its place). The No reply (blue) now ends with "Who can help: Your Health Visiting team" in place of its link; the results page still links to the help page. Yes reply (green) unchanged.
- Questions 1–4: question windows slightly tighter (answer buttons 48 px, above Apple's 44) so both replies fit on a 390 × 844 iPhone.

## 3.64 – 23 November 2026 (trial)
- Troubleshooter questions: "Here is how it works." removed.

## 3.63 – 23 November 2026 (trial)
- Question 1 titled "About your account" (was "Who will be set up with an account?"), also in the start page list and on the results page.
- Questions 1–4: the question, hint, answers and the Yes / No reply sit together in their own "Question" card (slate edge, ? icon), styled like the information cards above it.

## 3.62 – 23 November 2026 (trial)
- Troubleshooting: "Who will be set up with an account" and "Partner's details used" lose their Still stuck? bar; "Only the account holder can access" opens with "Here is how it works."
- Troubleshooter questions 1–4 laid out like the help pages: "Here is how it works.", then an information card (what to know, then who can help), then the question. Replies after Yes / No now say what the answer means, keeping the existing help links.
- Question 4 titled "Can you sign in to NHS login?" (was "Do you have NHS login?"), also in the start page list and on the results page; its subheading removed.

## 3.61 – 22 November 2026 (trial)
- Question 3 titled "Do you have an NHS login?" (was "NHS login account"), also in the start page list and on the results page; subheading removed; body "You need your own NHS login account to use the GM Early Years App. NHS login confirms who you are."; answers "Yes, I have an NHS login account" / "No, I have not set up an NHS login account".

## 3.60 – 22 November 2026 (trial)
- Question 5 (Do your details match?): subheading removed; body "Your GM Early Years App account must use the same contact details as your NHS login account."; question "Do both accounts use the same contact details?". Example card unchanged.

## 3.59 – 22 November 2026 (trial)
- Question 2 titled "Who will be able to access the account?" (was "Who has access?"), also in the start page list and on the results page; subheading removed; body "Only the account holder (the child's mother or primary carer) can access the GM Early Years App account that has been set up for them."; question "Is it clear that only the account holder can access the GM Early Years App account?".

## 3.58 – 22 November 2026 (trial)
- Question 1 titled "Who will be set up with an account?" (was "About your account"), also in the start page list and on the results page; its subheading is removed, leaving the explanation as the body.

## 3.57 – 22 November 2026 (trial)
- Question 1 (About your account): subheading "Who will be set up with an account?"; explanation is one paragraph ("Your Health Visiting team sets up a GM Early Years App account for the child's mother or primary carer. In this guide, we call this person the account holder."); question "Is it clear who will be set up with a GM Early Years App account?".

## 3.56 – 22 November 2026 (trial)
- Question 2 (Who has access?): the warning "A partner or family member cannot access the account." is removed.

## 3.55 – 22 November 2026 (trial)
- Question 4 titled "Do you have NHS login?" (was "NHS login access"; "Do you have an NHS login?" took two lines on a 375-wide iPhone), also in the start page list. The "Not sure? Try it on the NHS website / Try signing in" box is removed.

## 3.54 – 22 November 2026 (trial)
- Question 2: warning reads "A partner or family member cannot access the account." (one line shorter). The question still sits lower because question 4's explanation is the tallest; see notes/overflow-to-fix.md.

## 3.53 – 22 November 2026 (trial)
- Question 2: subheading "Who will be able to access the account?"; text "Only the account holder can access the GM Early Years App account that has been set up for them."

## 3.52 – 22 November 2026 (trial)
- Who will be set up with an account: What to do reads "If an account has been set up for the wrong person, please contact your Health Visiting team.", followed by the Find your Health Visiting team button.

## 3.51 – 22 November 2026 (live)
- 3.51 published to the live site (from 3.32). Brings live all changes in 3.33–3.51: NHS login account help and GM Early Years App help (Common sign-in problems merged), the reworked Troubleshooter (6 questions, help links on every No, account names spelled out), renamed help pages, and the fix for "That is clear" on the No answers to questions 1 and 2.

## 3.51 – 22 November 2026 (trial)
- Question 1 titled "About your account" (start page list and Your results too). Subheading "Who will be set up with an account"; text "Your Health Visiting team sets up a GM Early Years App account for the child's mother or primary carer." then "In this guide, we call this person the account holder."; question "Is it clear who will be set up with an account?". No: "Please see Who will be set up with an account for more information."
- Help page renamed "Who will be set up with an account" (title, GM Early Years App help card, Your results link text).

## 3.50 – 22 November 2026 (trial)
- Troubleshooter always names the account: "the GM Early Years App account" or "your NHS login account" (start page, questions 1-6, question 5's label, question 6's No message). Question 1's title stays "Who is set up with an account?" to keep it short; its question already names the GM Early Years App account.

## 3.49 – 22 November 2026 (trial)
- Troubleshooter review fixes. Questions 3 and 4 use "you" ("Do you have an NHS login account?", "Can you sign in to NHS login?"). Question 4 explains: "You sign in to the App with the same email address and password as your NHS login."
- Every No on questions 3-6 says what it means and links straight to its help page: Set up NHS login, Cannot sign in, Details do not match, Activation Link not received. Done on those pages returns to the question.
- Your results (hidden summary lines): "All six checks are done"; Yes lines match the questions; "you" wording.

## 3.48 – 22 November 2026 (trial)
- Question 2: "In this guide, we call this person the account holder." replaced by a warning, "A partner or family member cannot sign in to the account." No reads "See Only the account holder can access for help." (two lines). Compact messages; fits at every size except 360×640.

## 3.47 – 22 November 2026 (trial)
- Troubleshooter: question 3 "Is this you?" removed. Six questions: after "Who has access?" comes "NHS login account". Start page list ("6 quick questions"), steppers, question numbers, Your results (the Account holder row) and the page code updated. Section 6 has 49 pages.
- The help page "Only the account holder can access" is still reached from question 2.

## 3.46 – 22 November 2026 (trial)
- Help page renamed "Only the account holder can access" (title, GM Early Years App help card, question 2's No link: "Please see Only the account holder can access for more information.").
- On that page, What to do ends "ask your Health Visiting team", followed by the Find your Health Visiting team button. The "Still stuck? Get help" bar is removed.

## 3.45 – 22 November 2026 (trial)
- GM Early Years App help, new order: Who is set up with an account; Only the child's mother or primary carer can access; Partner's details used; Details do not match; Activation Link issues; How to install the App; Add to Home Screen.

## 3.44 – 22 November 2026 (trial)
- Question 2: subheading "Who will be able to access the account?"; Yes "Yes, the child's mother or primary carer"; No "Please see Only the child's mother or primary carer can access for more information." with a link to that page.
- Help page "A partner is signing in" renamed "Only the child's mother or primary carer can access"; its card line reads "Not a partner or family member".
- No layout fitting in this build; pages that scroll are listed in notes/overflow-to-fix.md.

## 3.43 – 22 November 2026 (trial)
- Question 1: No shows "Please see Who is set up with an account for more information." The page name links to that help page; its Back and Done return to question 1 with the answer kept.
- The help page "Who the account is for" is renamed "Who is set up with an account" (title, GM Early Years App help card, Your results row).

## 3.42 – 22 November 2026 (trial)
- Question 1: Yes shows "Yes, the child's mother or primary carer" (was "That is clear").

## 3.41 – 22 November 2026 (trial)
- Question 1 is titled "Who is set up with an account?" (was "Who is the account for?"), also in the start page list. Its second line reads "In this guide, we call this person the account holder." On the iPhone SE the title is set slightly smaller so it stays on one line.

## 3.40 – 22 November 2026 (trial)
- Troubleshooter start page: after the list, "This troubleshooter should be answered by the child's mother or primary carer, not a partner or family member." "Answer Yes or No. It takes a minute or two." stays at the end. List rows a little tighter. Scrolls slightly on the smallest iPhones (agreed for now; the page will be cut down).

## 3.39 – 22 November 2026 (trial)
- Who the account is for: new line "In this guide, we call this person the account holder." What to do now reads "The account holder signs in with their own NHS login. Not sure? Ask the team." On the smallest screens "Still stuck?" gives way so the page does not scroll.

## 3.38 – 22 November 2026 (trial)
- Who the account is for: "Your Health Visiting team creates the GM Early Years App account for the child's mother or primary carer." (was "the App account").

## 3.37 – 22 November 2026 (trial)
- GM Early Years App help: all seven topic cards use the GM Early Years App colours (four were blue).

## 3.36 – 22 November 2026 (trial)
- Question 7: subheading "Your Activation Link", so it no longer repeats the question.

## 3.35 – 22 November 2026 (trial)
- Question 2 (Who has access?): Yes says "You are the account holder".
- Question 3 (Is this you?): No ("No, I am a partner or relative") says "Only the account holder can sign in to the account".
- Question 4 (NHS login account): subheading "An NHS login account is needed"; explanation "The account holder signs in to the GM Early Years App with their own NHS login account." Yes says "The account holder has an NHS login account"; No says "The account holder needs an NHS login account".
- Question 7: subheading "Have you received your Activation Link?" (was "Sent to you by text message").
- Your results wording matches.

## 3.34 – 22 November 2026 (trial)
- Question 1 asks "Is it clear who has been set up with a GM Early Years App account?" The explanation adds "This troubleshooter should be answered by the child's mother or primary carer, not a partner or family member."
- New page in GM Early Years App help: "Who the account is for", in the same style as "A partner is signing in". Question 1's Read more on Your results now opens it.
- Fix: since 3.31, the No answers on questions 1 and 2 said "That is clear". They now say "That is OK. We will help."
- Section 6 has 50 pages.

## 3.33 – 22 November 2026 (trial)
- Troubleshooting: "NHS login account issues" is now "NHS login account help" (menu, page title and the NHS login band).
- "GM Early Years App issues" is now "GM Early Years App help".
- "Common sign-in problems" is merged into GM Early Years App help. All six topics use cards with a title and a short explanation underneath. Details do not match, Partner's details used and A partner is signing in now go Back and Done to GM Early Years App help.
- Section 6 has 49 pages.

## 22 November 2026 – guide version 3.32 is live (Troubleshooter; Contents after the Introduction)

- **Troubleshooter live** (trials 3.23–3.31): Troubleshooting menu → Troubleshooter → seven questions → Your results, with Get help / Read more links that come back to the results.
- **Contents (with Search) back in the route**, straight after the Introduction: Cover → Introduction → Contents → How this guide works.
- **Questions 4 and 5 ask about the child's mother or primary carer**, like questions 1–3: "NHS login account" – "Does the child's mother or primary carer have an NHS login account?"; "NHS login access" – "Can the child's mother or primary carer sign in to NHS login?". Results say "They have NHS login", "They can sign in".
- Also live from the trials: section badges level with the title, pressed state on taps, results traffic-light badge, example card on Do your details match?, Checklist questions that stay in place.
- Checked at all sizes; no script errors. Offline copy renamed `ey-guide-v3.32`. Built by `scripts/make332.py`.

## 22 November 2026 – guide version 3.31 on the trial page only (/preview/)

- Troubleshooter focuses on who can **access** the account. Q1 asks "Is it clear who the GM Early Years App account is for?". Q2 "Who has access?" / "Account access" / "Only the child's mother or primary carer can access the account that has been set up for them." / "Is it clear only the child's mother or primary carer can access it?". Q5 "NHS login access" / "Used to sign in to the App" / "NHS login is used to access the GM Early Years App account." / "Can the mother or primary carer sign in to NHS login?" (Try signing in kept).
- Titles and questions worded to fit on one / two lines ("Who can access the account?" and "Can you access NHS login?" wrapped to two lines on most iPhones). Checked at 7 sizes: positions identical, everything fits. Built by `scripts/make331.py`.

## 22 November 2026 – guide version 3.30 on the trial page only (/preview/)

- **Troubleshooter: seven questions.** New question 3 "Is this you?" ("Are you the child's mother or primary carer?") so a partner is still found after the two "is it clear" questions.
- **Kinder "not sure"** on questions 1 and 2: blue "That is OK. We will help." message, amber light instead of red, and on the results a blue "i" with **Read more** (About your account / A partner is signing in).
- **Question 5 Can you use NHS login?**: "Can you access NHS login?" with a Tip box "Not sure? Try it on the NHS website." and a **Try signing in** button (opens www.nhs.uk/nhs-app/account/ in a new tab; the validator now allows that page).
- **Answer messages in one style**, one line each.
- **Checklist questions (c1–c4) line up** too: the question and answers sit in the same place on all four pages on every size (they moved on the iPhone SE). The alignment code handles both sets of questions.
- Checked at all 13 sizes: positions identical, everything fits, results and links correct; no script errors. 94 pages. Comparison page lists the new questions and the Checklist. Built by `scripts/make330.py`.

## 22 November 2026 – guide version 3.29 on the trial page only (/preview/)

- Troubleshooter questions 1–4 say exactly who and what: Q1 "Is it clear that the account is for the child's mother or primary carer?"; Q2 "Only the child's mother or primary carer" (a partner or relative cannot sign in for them; we call this person the account holder) and "Is it clear that only the child's mother or primary carer can sign in?"; Q3 "The GM Early Years App uses an NHS login account to sign you in."; Q4 "Can you access your NHS login account?" with email address and password, a Tip box, and "Can you sign in to your NHS login account?". Results rows 1–2 follow (Get help: About your account / A partner is signing in).
- Checked at 8 sizes: positions identical on all six questions; everything fits. Built by `scripts/make329.py`.

## 21 November 2026 – guide version 3.28 on the trial page only (/preview/)

- **Introduction**: back to the original (the conversation mock-up is withdrawn), with "You are not alone, and it is not your fault." on its own line in bold.
- **Troubleshooter: six questions**, short titles that fit on one line: Who is the account for? · Who can sign in? · Do you have NHS login? · Can you use NHS login? · Do your details match? · Has your link arrived? Which system each is about shows in colour under the title box (GM Early Years App / NHS login / NHS login and the App).
- **Clearer wording** on each question: a subheading that gives the answer, one or two short plain sentences, then the question. Results have six rows (Get help: A partner is signing in, Partner's details used, Set up NHS login, Cannot sign in, Details do not match, Activation Link issues).
- Comparison page list updated. Checked: positions identical on all six questions, fits at all sizes checked, results and Get help links correct; no script errors. 93 pages. Live stays at 3.26. Built by `scripts/make328.py`.

## 21 November 2026 – comparison page (/compare/)

- New page `compare/index.html` shows the live guide and the trial side by side at a chosen iPhone size. Pick a page (or use ‹ ›), or tap through either guide: the other follows when the page exists in both; pages only in the trial (the Troubleshooter) show "Not in this version" on the live side. Not linked from the guide; `noindex`.

## 21 November 2026 – guide version 3.27 on the trial page only (/preview/): mock-ups

- **Introduction as a conversation**: the reader's words on the right ("I'm having trouble signing in…", "I have tried before, and it did not work."), the guide's replies on the left with the App icon ("You are not alone, and it is not your fault.", "It usually comes down to one small detail. We will find it together, one step at a time."), appearing one after another. On shorter screens the second-screen tip becomes one line.
- **Section badges** a little smaller and lower so the number sits level with the title's last line (option C of three compared).
- **Troubleshooter questions**: a subheading states the answer first (e.g. "The child's mother or primary carer"), then each point on its own line. "Tap an answer, then tap Next" always shown (not on the iPhone SE in Safari). The explanation and question areas are the same height on all five pages, so the question and the Yes / No answers stay in exactly the same place. A checklist rule that gave every paragraph three lines' height is switched off here. Answer messages are one line; some answers and messages are shorter so they fit on one line.
- **Do your details match?**: the example is a clear "See an example · Tap here" card with a gentle glow.
- **Your results**: a traffic-light badge in the title box (green tick, amber "!", grey while unanswered); the title box keeps the guide's colours.
- **Quicker-feeling taps**: buttons, answers, cards and links show a pressed state the moment they are touched; pages fade in faster.
- Checked at all 13 sizes; no script errors. Live stays at 3.26. Built by `scripts/make327.py`.

## 21 November 2026 – guide version 3.26 is live (section badges; Contents in page order)

- **Section badges** (from trial 3.25): each section's opening page has its Contents icon in a white badge on the right of the title box; Signing in shows the App's ABC block icon. Hidden on the shortest and narrowest screens.
- **Contents in page order** (from trial 3.24): Contact & support, Accessibility, then About this guide (book icon instead of 8).
- Built from live 3.22 by `scripts/make326.py`. The Troubleshooter (trial 3.23) is not in the live version; the trial page stays at 3.25. Offline copy renamed `ey-guide-v3.26`.

## 21 November 2026 – guide version 3.25 on the trial page only (/preview/): section badges (mock-up)

- The title box of each section's opening page has a badge on the right with its Contents icon, so people can see where they are: Introduction (i), How this guide works (1), How to contact your HV team (2), About your account (3), Run through the Checklist (4), **Signing in (the App's ABC block icon)**, Troubleshooting (6), Contact & support (7), Accessibility (its icon), About this guide (book).
- Same white circle as the Troubleshooter and NHS login Support badges. Hidden on the shortest screens (600 px tall or less) and the narrowest (under 370 px wide), where titles need the room; no title gains an extra line anywhere.
- Includes 3.23 (Troubleshooter) and 3.24 (Contents order). Live stays at 3.22. Built by `scripts/make325.py`.

## 21 November 2026 – guide version 3.24 on the trial page only (/preview/)

- **Contents in page order**: 7 Contact & support, then **Accessibility**, then **About this guide**, which now has an open-book icon instead of the number 8 (the pages run Contact & support → Accessibility → About this guide).
- About this guide is no longer numbered elsewhere: page strips say "About this guide" (was "Section 8 · About this guide").
- Includes the 3.23 Troubleshooter. Checked: Contents and About this guide fit at the small, narrow and large sizes. Live stays at 3.22. Built by `scripts/make324.py`.

## 21 November 2026 – guide version 3.23 on the trial page only (/preview/): Troubleshooter

- **Troubleshooting** has a new first card, **Troubleshooter** ("Find out what is stopping you"), in the App colours.
- The Troubleshooter brings together About your account, Your account details and the Checklist, in the checklist format: one question per page, Yes or No, the progress LEDs, and a results page.
  1. Who has the account? (Are you the child's mother or primary carer?)
  2. Who can sign in? (Only the account holder, with their own NHS login. Do you have your own NHS login account?)
  3. Can you use NHS login?
  4. Do your details match? (with the account details example: a small preview; tap to see the whole example)
  5. Has your link arrived?
- **Your results**: a tick for each Yes, and a Get help button for each No (A partner is signing in, Set up NHS login, Cannot sign in, Details do not match, Activation Link issues). All Yes: Next goes to Signing in. Any No: Done goes back to Troubleshooting. Get help pages come back to the results.
- Begin starts with a clean set of answers; the Checklist keeps its own answers.
- On smaller iPhones the "Help from" lines on the Troubleshooting cards give way so the menu fits; on the results page the explanation under each problem gives way. Checked at all 13 sizes, light and dark; no script errors. 92 pages. Live stays at 3.22. Built by `scripts/make323.py`.

## 21 November 2026 – guide version 3.22 is live

- The trial versions 3.17, 3.18, 3.19 and 3.22 are now live: cover without "Help with a problem"; Search by speaking (cover microphone, search-box microphone always shown); "Step-by-step help to sign in" under Start the guide; Start opens the calmer Introduction; How this guide works says what will happen; Your roadmap removed (85 pages); Section 2 title "How to contact your HV team". Trials 3.20 and 3.21 were not used.
- Offline copy renamed `ey-guide-v3.22`.

## 21 November 2026 – guide version 3.22 on the trial page only (/preview/); replaces trials 3.20 and 3.21

- Contact your HV team finder put back as it was in 3.19 ("Find your team's contact details:", Locality and Health Visiting team side by side).
- Section 2 page title mock-up: **"How to contact your HV team"** (was "Contact your HV team"). It fits the title box on every iPhone, but on 375-wide screens and smaller (SE, mini, 12/13 Home Screen, 320/360) it goes onto two lines; one line on 390-wide and larger. Built from 3.19 by `scripts/make322.py`. Live stays at 3.16 until approved.

## 21 November 2026 – guide version 3.21 on the trial page only (/preview/); replaces trial 3.20

- 3.20's two steps one under the other made Contact your HV team too long with the **Map** chosen (the map shrank to about 100 px on small iPhones and the page still scrolled). 3.21 keeps the new lead line, "If you need to contact your Health Visiting team, you can find their contact details below.", and puts **1 Locality** and **2 Health Visiting team** back side by side. Same on Section 7 · Contact your HV team.
- The page re-fits when a choice changes; "Tap the contact number to call" gives way if the screen is too short.
- Checked: both pages at all 13 sizes with Contact details and with Map chosen; nothing scrolls. The map is about 20 px shorter than on the live version because the lead line is now two lines. Built from 3.19 by `scripts/make321.py`. Live stays at 3.16 until approved.

## 21 November 2026 – guide version 3.20 on the trial page only (/preview/)

- **Contact your HV team** (Section 2, and the same finder in Section 7): lead line now "If you need to contact your Health Visiting team, you can find their contact details below." The two choices are steps, one under the other: **1 Choose your area**, **2 Choose your Health Visiting team** (was Locality / Health Visiting team side by side). The team list says "Choose your area first" until an area is chosen.
- When a team is chosen, the page re-fits: on shorter screens the lead line and "Tap the contact number to call" give way so the contact card fits without scrolling.
- Checked: both pages at all 13 sizes, before and after choosing a team; no script errors. Live stays at 3.16 until approved. Built by `scripts/make320.py`.

## 21 November 2026 – guide version 3.19 on the trial page only (/preview/)

- **Cover**: Start the guide now has a second line, "Step-by-step help to sign in", so it matches Search ("Type or say what you need"). Checked: cover fits at all 13 sizes, light and dark. Includes 3.17 and 3.18. Live stays at 3.16 until approved. Built by `scripts/make319.py`.

## 21 November 2026 – guide version 3.18 on the trial page only (/preview/): a calmer start

- **Start opens the Introduction** (cover Start button and "Start the guide"), not Contents. Contents stays in the bottom bar.
- **Introduction**: "You are not alone, and it is not your fault." plus "If you have tried before and it did not work, it usually comes down to one small detail. This guide will help you find it, one step at a time." The "Need help now? Go to Troubleshooting" link is removed, so people are led through the questions.
- **How this guide works** now says what will happen: "You do not need to work out what is wrong. This guide does that with you." Then 3 parts: check what you need, sign in one step at a time, get the right help.
- **Your roadmap page removed** (How this guide works now does its job). Path: Cover → Introduction → How this guide works → Contact your HV team → About your account → Checklist. 85 pages.
- Includes 3.17 (cover without Help with a problem; Search by speaking). Checked: start path forwards and back, fit at all 13 sizes in light and dark, no script errors. Live stays at 3.16 until approved. Built by `scripts/make318.py`.

## 21 November 2026 – guide version 3.17 on the trial page only (/preview/)

- **Cover**: "Help with a problem" removed, so Start leads people through the questions instead of asking them to guess what is wrong. The Search row now says "Type or say what you need" and has a round microphone button. Tapping it opens Search and starts listening.
- **Search page**: the microphone in the search box is always shown. Where Safari cannot listen (for example from the Home Screen), tapping it opens the keyboard and says "Now tap the microphone at the bottom of your keyboard". A web page cannot switch on the keyboard microphone itself.
- Checked: cover and Search fit at all 13 sizes, light and dark; voice search tested with and without Safari speech; no script errors. Live stays at 3.16 until approved. Built by `scripts/make317.py`.

## 21 November 2026 – guide version 3.16 is live (GM Early Years App issues: Activation Link issues first)

- **Troubleshooting > GM Early Years App issues** now lists Activation Link issues first, How to install the App second and Add to Home Screen third. The two Activation Link issues pages moved to just after the menu, so the page numbers follow the same order (Troubleshooting pages 24–25; How to install the App now starts on page 26).
- Checked every Troubleshooting topic again: all 14 topics end with Done back to their menu, the four Troubleshooting choices end with Done back to Troubleshooting, and Troubleshooting's Next goes on to Section 7. No script errors. Offline copy renamed `ey-guide-v3.16`. Built by `scripts/make316.py`.

## 20 November 2026 – guide version 3.15 is live (Troubleshooting choices go back to the Troubleshooting menu)

- **NHS login account issues, GM Early Years App issues, Common sign-in problems**: Next now says **Done** and goes back to the Troubleshooting menu (in 3.14 it went sideways to the next menu).
- **Still need help?**: Next now says **Done** and goes back to Troubleshooting, or to the page whose Get help link you tapped (was: straight on to Section 7).
- **Troubleshooting menu**: Next goes on to Section 7 · Contact & support (was: NHS login account issues), so reading straight through still reaches the end and nothing loops. Back from Troubleshooting goes to where you were before it (for example the cover).
- Checked: 13 click-through routes (each choice, the NHS login walk-through, the install steps, Get help from a topic, from the cover, the Checklist summary, Search, opened directly, end of Signing in); no script errors. Offline copy renamed `ey-guide-v3.15`. Built by `scripts/make315.py`.

## 20 November 2026 – guide version 3.14 (sent for review, published with 3.15): all Troubleshooting topics go back to where you chose them

- Review of the other Troubleshooting pages found the same run-on in two more menus. **NHS login account issues**: its 8 topics ran into each other, and the last one ran into GM Early Years App issues. **Common sign-in problems**: its 3 topics ran into each other, and the last one ran into Still need help?. The last page of every topic now has **Done**.
- **Done goes back to where you chose the topic**: the menu, or the Checklist summary or Search if you came from there. If the page was opened directly, Done opens the topic's menu. This also fixes 3.13, where Back on the menu after Done stepped back into the topic you had just finished.
- **Menus no longer run into their first topic** (that made a loop now that topics return to the menu). Next on a menu goes to the next menu: Troubleshooting → NHS login account issues → GM Early Years App issues → Common sign-in problems → Still need help? → Section 7.
- Checked: clicked through 10 routes (each menu, the NHS login walk-through, the install steps, from the Checklist summary, from Search, opened directly, arrow keys); no script errors. Offline copy renamed `ey-guide-v3.14`. Built by `scripts/make314.py`.

## 20 November 2026 – guide version 3.13 is live (GM Early Years App issues: back to the menu)

- **Troubleshooting > GM Early Years App issues**: each choice is a separate topic, so finishing one now goes back to the GM Early Years App issues menu instead of running on into the next topic. On the last page of How to install the App, Add to Home Screen and Activation Link issues the Next button now says **Done** and opens the menu. Back on the first page of each topic also opens the menu.
- The GM Early Years App issues menu and Common sign-in problems now go Back to the Troubleshooting menu. Swipe and the arrow keys follow the same links.
- Checked: clicked through every topic at 3 iPhone sizes; the Done button fits. Offline copy renamed `ey-guide-v3.13`. Built by `scripts/make313.py`.

## 20 November 2026 – guide version 3.12 is live (trial improvements made live + new cover)

- **Everything from the trial is now live**: 3.10 (calmer design: gentler issue icon, reassuring first lines, grey pages with white cards, Part done / You're signed in, Still stuck?, Tap wording, shorter text, new Contents, Introduction and Checklist start) and 3.11 (accessibility statement, Your privacy, contrast fixes).
- **New cover "C3·6 All GMCA"** (David, from the cover mock-ups): solid GMCA slate logo band with the GMCA and Greater Manchester – Doing Digital Differently logos (nothing behind them); photo; white panel with a faint hexagon pattern and the large App icon; "For parents and carers · Version", title and "Help signing in to your account on an iPhone"; three choices with square icons in GMCA colours – Start the guide, Help with a problem, Search; "For families in Bury · Rochdale · Stockport"; Start button in GMCA slate. Dark Mode version. The old blue header is no longer shown.
- Checked: every page at 13 iPhone sizes (nothing needs scrolling), the cover in light and Dark Mode, accessibility check on the cover (no issues), the three choices open the right pages. Offline copy renamed `ey-guide-v3.12`. Built by `scripts/make312.py` (App icon in `scripts/assets/app-icon-cover.png`).

## 20 November 2026 – guide version 3.11 on the TRIAL link only (/preview/); live stays 3.09

- **Accessibility statement** (David): four pages in Section 8 · About this guide (Accessibility statement; Known issues; Feedback and contact; How it was tested), following the GOV.UK sample statement: what carers should be able to do, compliance status (partially compliant until a full independent audit), known limitations, other formats and reporting problems (GMDP Support), EHRC / EASS, and how and when it was checked. The Accessibility page in Section 7 links to it.
- **Your privacy** (David): one page – the guide collects nothing; what you type and choose stays on the iPhone; voice search uses Apple's speech service only when used; the host (GitHub) may keep technical details such as IP addresses.
- **Contrast fixes** from an axe-core check of every page in light and Dark Mode: cover quick links, green Start/Begin/Yes buttons (now #00703c), Dark Mode card headings and "Help from" names, link captions on Contact & support pages; the greyed-out Next is marked `aria-disabled`. Re-check: no failures.
- Checked at 200% zoom and in landscape (pages scroll, nothing cut off) and at 13 iPhone sizes. Guide is 86 pages; About this guide 8. Built by `scripts/make311.py`. `validate_site.py` allows the EASS link.

## 20 November 2026 – guide version 3.10 on the TRIAL link only (/preview/); live stays 3.09

- **Calmer design for frustrated carers** (David, from mock-ups): gentler blue-grey "i" for The issue; a reassuring first line on every Troubleshooting help page; light grey pages with white cards and soft shadows (light mode); "Part 1 done", "Part 2 done – nearly there" and a "You're signed in" finish in Signing in; a **Still stuck?** bar at the bottom of every help page (NHS login pages: Contact NHS login, replacing the duplicate contact button; HV pages: Get help → Still need help?); "Tap" wording everywhere (no "Select"); shorter text (GMDP note, Introduction, Checklist start, Activation Link page).
- **Front of the guide**: cover ("Help signing in to your account on an iPhone", a calm line, quick links Help with a problem / Search); Contents as white cards grouped by stage; Introduction ("You are not alone", second-screen tip as three icon rows, Need help now? link); Run through the Checklist lists the four questions up front.
- When a page would otherwise need scrolling (small iPhones), the extras (reassuring line, Part done line, tips) give way automatically (`fit()` adds `.tight`). Checked: all 82 pages at 13 sizes, nothing needs scrolling; Dark Mode; walk-through cover → checklist summary. Built by `scripts/make310.py`.

## 20 November 2026 – guide version 3.09 is live

- **Better Search** (David): everyday words find the guide's words (log in → sign in, text → message, lost/forgot → forgotten/reset, phone → mobile, download → install, shortcut/desktop → Home Screen, wife/husband → partner …), word endings (signed, changed, codes) and everyday filler words are handled; misspellings are matched to the closest word in the guide ("pasword" → "Showing results for password"); sentences with no page containing every word show the pages with most of them. **Popular topics** buttons under the box (Forgotten password, No Activation Link, Security code, Install the App, Add to Home Screen, Contact your HV team). No results: **Troubleshooting** and **Still need help?** buttons. Revision history and Document control are left out of results.
- **Voice search**: a microphone button in the search box on the website in Safari (Apple's speech service, with the iPhone's own permission prompts; listening shows a red pulsing button). Where voice search cannot run (Home Screen app, Claude app, permission refused) the button is hidden and carers are told to use the microphone on the iPhone keyboard.
- Tested with everyday questions, a simulated speech engine (results, refusal) and at every iPhone size. Offline copy renamed `ey-guide-v3.09`. Built by `scripts/make309.py`. `/preview/` updated to 3.09 too.

## 20 November 2026 – guide version 3.08 is live

- **Add to Home Screen helper** (David): new item **Add to Home Screen** in Troubleshooting > GM Early Years App issues, and a page with numbered steps and pictures of the Safari buttons. The guide shows the right steps for the iPhone: iOS 26 or later (More ••• > Share > Add to Home Screen > Add, with Open as Web App on), or older iPhones (Share > Add to Home Screen > Add). Opened from the Home Screen already, it just says so (green tick). Opened as a downloaded copy or in the Claude app, it asks the carer to open the guide website in Safari, with a button.
- Guide is now 81 pages; Troubleshooting 41. Checked at every iPhone size and in Dark Mode. Offline copy renamed `ey-guide-v3.08`. Built by `scripts/make308.py`. `/preview/` updated to 3.08 too.

## 20 November 2026 – faster updates on iPhones (website only, guide still 3.07)

- `sw.js`: when there is a signal, the guide is now always checked with the website (`cache: 'no-cache'`) instead of possibly using the browser's saved copy, which GitHub Pages lets phones keep for up to 10 minutes. New versions should show the next time the guide is opened (after this change has been picked up once). The offline copy for no signal is unchanged.

## 19 November 2026 – guide version 3.07 is live

- **Checklist progress bar colours** (David): the current question's segment now turns **green for Yes** and **red for No** as soon as an answer is chosen (no need to tap Next), and changes straight away if the answer is changed. Earlier questions stay green (Yes) or red (No), including on the summary. Unanswered: white for the current question, faint for questions to come. Segment size (3.03) and right-hand position (3.04) unchanged. Dark Mode checked.
- Offline copy renamed `ey-guide-v3.07`. Built by `scripts/make307.py`. `/preview/` updated to 3.07 too.

## 19 November 2026 – guide version 3.06 is live

- **How to install the App** (David): the A4 guide "GM Early Years App – How to install the App on a mobile phone (iOS) – Carer Role v1.04" is now inside Troubleshooting > GM Early Years App issues (first item, "How to install the App"), in the Signing in design: an introduction (You will need: Apple ID signed in, internet connection; GMDP Support Team for help), 7 step pages (progress bar, "Installing the App" label, instruction, Tap chip, screenshot 248 wide cropped to the highlighted part, Tap to enlarge), a helpful tip after Step 4 (the button says **Get** the first time, with Face ID / Touch ID / Apple ID password) and an "Installation complete" page linking to Section 5 · Signing in.
- Screenshots from the A4 guide, stored in `scripts/assets/install/`. All Signing in screenshot and step rules now also apply to install pages (`[data-inst]`); Signing in pages are unchanged (checked).
- Guide is now 80 pages; Troubleshooting 40. Checked at every iPhone size: every page fits, the same 10 px above the buttons as Signing in. Offline copy renamed `ey-guide-v3.06`. Built by `scripts/make306.py`. `/preview/` updated to 3.06 too.

## 19 November 2026 – guide version 3.05 is live

- **Troubleshooting: GM Early Years App issues** (David): the "Activation Link issues" card on the Troubleshooting menu is now **GM Early Years App issues** (user icon; tile and left highlight in the GM Early Years App colours; "For issues with access to the app"). It opens a new page, **GM Early Years App issues** (Section 6, page 23 of 30): app title box with a round white user icon, "For issues with access to the GM Early Years App.", and a list in the NHS login account issues style but in the app colours. The first item is **Activation Link issues** (the existing Activation Link pages). More items to follow from David.
- Guide is now 70 pages; Troubleshooting 30. Back/Next, page numbers and Contents counters updated. Checked at every size: no page needs scrolling, nothing else moved. Offline copy renamed `ey-guide-v3.05`. Built by `scripts/make305.py`. `/preview/` updated to 3.05 too.

## 19 November 2026 – guide version 3.04 is live

- **Checklist progress on the right** (David, from mock-up): on the four question pages and the checklist summary, the progress bar and "Question N of 4" now sit on the right-hand side of the title box, so they read differently from "Stage N of 3" on the left of a section's first page. Signing in and the NHS login steps are unchanged (left).
- Checked at 390, 320, 440 and 375×548. Offline copy renamed `ey-guide-v3.04`. Built by `scripts/make304.py`. `/preview/` updated to 3.04 too.

## 19 November 2026 – guide version 3.03 is live

- **Checklist progress bar** (David): now the same size and colours as the Signing in bar. Each of the four segments is the width of one Signing in step segment (so the bar is short, not full width). Colours as Signing in: green for questions answered (Yes or No – no red), white for the current question (it stays white after answering), faint for questions to come. Dark Mode matches Signing in too.
- Checked at 390, 320 and 375×548 in light and Dark Mode. Offline copy renamed `ey-guide-v3.03`. Built by `scripts/make303.py`. `/preview/` updated to 3.03 too.

## 19 November 2026 – guide version 3.02 is live

- **How this guide works** (David): "This guide is designed to help." now sits on its own line, in bold. On shorter screens (iPhone SE and similar) the gaps between paragraphs and the three cards are slightly tighter so the page still fits without scrolling.
- Checked at every iPhone size. Offline copy renamed `ey-guide-v3.02`. Built by `scripts/make302.py`. `/preview/` updated to 3.02 too.

## 19 November 2026 – guide version 3.01 is live

- **Contact your HV team** (Section 2): the title box is now the GM Early Years App title box (app colours with the faint ABC blocks) instead of the NHS-blue Health Visiting team band, with the usual "Stage 1 of 3 · What you need" marker, matching About your account. The Contact & support copy of the team finder is unchanged.
- Checked at every iPhone size with every team in both views: no scrolling needed; title in the same place. Offline copy renamed `ey-guide-v3.01`. Built by `scripts/make301.py`. `/preview/` updated to 3.01 too.

## 19 November 2026 – guide version 3.00 is live

- **Your account details is now part of About your account** (David): Section 3 · About your account has two pages – About your account (page 1 of 2) and Your account details (page 2 of 2). The separate "NHS login" section is gone, so the sections after it move up one: 4 Checklist · 5 Signing in · 6 Troubleshooting · 7 Contact & support · 8 About this guide. Contents, roadmap, section labels, title-box numbers and cross-references all follow. Your account details no longer shows a stage marker (that is only on a section's first page).
- **Contents: "Cover page" is the first row** (David), with a small page icon; it goes back to the front cover.
- **Still need help?** (Troubleshooting): the round headset icon in the title box, as on Contact & support > GMDP Support Team.
- **Title-box labels stay in one place** (David): "Question 1 of 4", "Part 1 of 3 · Get started" and the tip labels now sit at the top under the progress bar on every page, in the same place as "Stage N of 3" on a section's first page. Before, the label sat lower when the title was one line and higher when it wrapped to two, so it jumped between pages (for example Restart your iPhone → Open your Activation Link). Titles and underlines are unchanged.
- All pages checked at every iPhone size (no page needs scrolling; no label cut off). Offline copy renamed `ey-guide-v3.00`. Built by `scripts/make300.py`. `/preview/` updated to 3.00 too (still with the new Home Screen icon).

## 19 November 2026 – trial icon updated at /preview/

- **Home Screen icon (trial)** – David chose "New 2" from the mockups: the ABC blocks only, larger, on the magenta gradient (the yellow GUIDE label is gone). `scripts/make_icons.py` updated. On `/preview/` only; the live guide still has the old icon.

## 19 November 2026 – guide version 2.99 is live

- **Troubleshooting menus with icons, in the Contact & support style** (David, from mockup):
  - Troubleshooting start page: four cards with icon tiles, a short line and "Help from:" (NHS login Support team / your HV team); "Still need help?" has the GMDP tile. Descriptions shortened; lead now "What is the problem?". On the smallest screens the short lines are hidden (except "Contact the GMDP Support Team").
  - NHS login account issues: the eight options as one list with a small blue icon each.
  - Common sign-in problems: three cards with icons.
- All pages checked at every iPhone size. `/preview/` updated to 2.99 too (still with the new Home Screen icon).

## 19 November 2026 – guide version 2.98 is live

- **Removed "Confirm your details"** (Section 2 · Your Health Visiting team, page 2 of 2) – David: that is being done somewhere else. Section 2 is now one page (Contact your HV team), which goes straight on to Section 3 · About your account. The guide has 69 pages.
- The trial at `/preview/` is updated to 2.98 too, still with the new Home Screen icon. The live guide keeps the old icon until David approves the new one.

## 19 November 2026 – trial: guide version 2.97 at /preview/

- **New Home Screen icon (trial)** – David chose "B+F 1" from the icon mockups: the ABC blocks from the guide's title boxes with a yellow GUIDE label, on the guide's magenta gradient. Icons (180, 192, 512 and maskable 512) made by `scripts/make_icons.py` with the guide's own Archivo font. On the trial at `/preview/` only; the live guide still has the old icon.

## 19 November 2026 – guide version 2.96 is live

- GMDP Support Team page: round white headset icon in the title box, matching the NHS login Support team page (in the GM Early Years colour).
- Contact & support > Your Health Visiting team: the instruction line now always stays, so the page no longer moves when a locality and team are chosen. On shorter screens (iPhone SE, mini, 12–16 in Safari) the lead line "Your team can check your account and link." is left out to make room — the Contact & support card already says what the team is for.
- All pages checked at every iPhone size; all 23 teams checked in both views.

## 19 November 2026 – guide version 2.95 is live

- **Troubleshooting help pages as three blocks** (David, from mockup) – all 12 help pages: **The issue** (amber card) · **Who can help** (blue card with the team's logo – NHS for NHS login Support and Health Visiting teams, ABC for GMDP Support) · **What to do** (green card, with the help buttons inside it as blue pills). Icons sit beside the small headings so the text uses the full card width. Spacing tightens on shorter screens so every page still fits.
- **Signing in overview** (David, from mockup): the three parts as a connected strip of tiles – Get started (Steps 1–3) → NHS login (Steps 4–9) → GM Early Years App (Steps 10–15) – and "You will need" as three icon rows (email address, password, iPhone for text messages).
- **Stage marker** (David, from mockup): on each section's first page, three bars and "Stage N of 3 · What you need / How to sign in / Who can help" sit inside the title box above the title (no extra height; titles stay in place). On the Health Visiting team page the NHS band says "Stage 1 of 3". Hidden on iPhone SE in Safari, where title boxes are compact. (Built inside the title box rather than below it, as two pages had no room below.)
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.95`. Built by `scripts/make295.py`.

## 19 November 2026 – guide version 2.94 is live

- **Contact & support – who to contact for what** (David, from mockup): "Who to contact depends on the problem:" then three cards with logos – **Your Health Visiting team** (For: your App account – your details and Activation Link) · **NHS login Support team** (For: your NHS login – setting up, signing in, security codes) · **GMDP Support Team** (For: problems with the App itself, once NHS login works). Accessibility is a quieter line underneath ("Large print, easy-read and other formats"). Logos are embedded once in the styles.
- **Checklist summary** (David, from mockup): a headline banner at the top – amber "**2 things to sort out first**" (the number follows the answers), grey "**Not quite finished**", or green "**You are ready to sign in**" with a **Go to Signing in** button. Problems are red cards with a solid **Get help** button; ticked items are one quiet line. On screens up to 700 px tall the banner's second line is hidden so even four problems fit. Still works without JavaScript (the banner then says "Some things").
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; five answer combinations on the summary; every card link. Offline copy renamed `ey-guide-v2.94`. Built by `scripts/make294.py`.

## 19 November 2026 – guide version 2.93 is live

- **Team finder** (David – the instruction changed after a team was chosen, which looked like the page jumping): one layout that never changes – "Find your team's contact details:" then numbered labels over the two menus, **① Locality** and **② Health Visiting team** (② "HV team" on 320 px wide screens). The labels now show on every screen; the Locality menu says "Choose". Section 2 and the Section 8 copy (Section 8 still hides its one-line instruction once a team is chosen, as before).
- **About your account – headings** (David): **Who will be set up with an account?** · **Who will be able to access the account?** · **Who will not be able to access the account?** (the last answered by the yellow note). New reusable in-page heading style for information pages.
- **Section 4 page retitled "Your account details"** with a GM Early Years App title box (was "Before you sign in" in an NHS login box).
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; every team on both finder pages. Offline copy renamed `ey-guide-v2.93`. Built by `scripts/make293.py`.

## 19 November 2026 – guide version 2.92 is live

- **New order** (David): 1 How this guide works · **2 Contact your Health Visiting team** · 3 About your account · 4 NHS login · 5 Checklist · 6 Signing in · 7 Troubleshooting · 8 Contact & support · 9 About this guide. Contents, roadmap, page order, section labels and cross-references all follow.
- **Signing in to NHS login moves to Troubleshooting** (David): NHS login Steps 1–7 and their tips now follow "NHS login account issues" and are option **1 Signing in to NHS login** on that list. Section 4 NHS login keeps "Before you sign in", whose Next now goes to the Checklist. Step 1 now says "Cannot sign in? See the other NHS login account issues"; the Step 7 note now ends "If any of these details are different from your GM Early Years App account, contact your Health Visiting team".
- **Roadmap options listed vertically** (David), one per row in each stage; the "Tap a section" line dropped for room.
- **Team finder wording** (David), Section 2 and the Section 8 copy: "If you need to contact your Health Visiting team, you can find their contact details by: • selecting your **Locality** • then selecting your **Health Visiting team**". On Section 2, once a team is chosen, the same instruction shows on one line ("Select your Locality, then your Health Visiting team.") so the team card fits.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; every team on both finder pages; every roadmap and Contents link; Next route. Offline copy renamed `ey-guide-v2.92`. Built by `scripts/make292.py`.

## 19 November 2026 – guide version 2.91 is live

- **How this guide works** (David): now David's description – "Sometimes connecting to things online does not go the way we hope, and that can be frustrating. **This guide is designed to help.** Working through the steps in this guide will: 1 Show you **what you need** to access the app · 2 Show you **examples** of how to access the app · 3 Show you **who can help**, and what to do, when there are problems."
- **Your roadmap** (new, Section 1 page 2): what happens next, in the same three stages, each section one tap away – **1 What you need**: About your account, NHS login, Contact your HV team, Checklist · **2 How to sign in**: Signing in to the GM Early Years App · **3 Who can help**: Troubleshooting, Contact & support. (The section list moved here from page 1.) The guide is 70 pages.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; every roadmap link tested. Offline copy renamed `ey-guide-v2.91`. Built by `scripts/make291.py`.

## 18 November 2026 – guide version 2.90 is live

- **Step 1 title** (David): **Signing in to NHS login** (was "Go to NHS login").
- **Section 3 pages 3 and 4 deleted** (David): Step 2 "Sign-in page opens" and its note ("If you already have an NHS login account … do not tap Create NHS account"). Step 1 now leads straight to Email and password.
- The NHS login steps are now **1 to 7**: band labels, progress bars, hidden step text, Search titles and the Step 3 note's "continue at Step 6" all renumbered. Section 3 is 14 pages; the guide is 69 pages.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.90`. Built by `scripts/make290.py`.

## 18 November 2026 – guide version 2.89 is live

- **Before you sign in (Section 3 page 1) is now the worked example** (David – the diagram was confusing). The words come first: "Your details must be **exactly the same** in **NHS login** and the **GM Early Years App**." Then, with more space: "✓ **Same details:** you can sign in." / "✗ **Different details:** ask your HV team." Then "For example:" and two quiet example account cards – NHS login = GM Early Years App – with made-up details (Charlotte Somers, 485 777 3456, 07700 900123, c.somers@example.com). The cards have tinted headers and a thin coloured top edge so the text leads. Screen readers hear the example as one sentence.
- The "Sign in to check your details" button is removed; Next leads to Step 1. The 2.87 diagram styles are removed.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.89`. Built by `scripts/make289.py`.

## 18 November 2026 – guide version 2.88 is live

- **NHS login pages 2 and 3 combined** (David): "Signing in to NHS login" and "Step 1 · Go to NHS login" are now one Step 1 page that flows top to bottom – why ("Sign in to your own NHS login account to check your details. You use the same email address and password for the GM Early Years App."), what to do ("Open this website in Safari on your iPhone, or on any computer:"), the full-width **settings.login.nhs.uk** button, then below a divider "**Cannot sign in?** See NHS login account issues in Section 7. (The GMDP Support team cannot assist …)".
- "Sign in to check your details" and Next on page 1 go straight to Step 1; Back on Step 1 returns to page 1. Section 3 is 16 pages; the guide is 71 pages.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.88`. Built by `scripts/make288.py`.

## 18 November 2026 – guide version 2.87 is live

- **Section 3 · NHS login now opens with the key message** (David): the start page is **Before you sign in** (band "NHS login | Start here"). A diagram – NHS login | must match | GM Early Years App – puts a tick on both sides of each detail: Given name, Surname, NHS number, Mobile phone number ("Gets your security codes"), Email address ("Used to sign in to NHS login"). Then **Same? You can sign in** / **Different? Ask your HV team** (links to Section 4), and a button **Sign in to check your details →** that leads into the NHS login sign-in steps. Chosen from four mockups (checklist, side-by-side diagram, worked example, Yes/No diagram): the diagram with the Yes/No ending.
- The "This section has two parts" list and the separate Part a page are gone; the sign-in start page band is "NHS login | Signing in" again. Section 3 is 17 pages; the guide is 72 pages.
- **Fix:** 2.85 left a style block open, so the print styles and the Contact details / Map fade on screens taller than 700 px were not applying. Corrected, and every build now checks that the stylesheet is balanced.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; Health Visiting team finder rechecked. Offline copy renamed `ey-guide-v2.87`. Built by `scripts/make287.py`.

## 18 November 2026 – guide version 2.86 is live

- **Section 4 page 1 title** (David): **Contact your HV team** (was "Contact your team"). One line on every iPhone, same position as every other title.
- **Team cards** (Section 4 and Section 8): "Tap the **contact number** to **call**." – the key words in bold.
- Every team checked in both views on both pages at the tightest sizes; nothing moved. Offline copy renamed `ey-guide-v2.86`. Built by `scripts/make286.py`.

## 18 November 2026 – guide version 2.85 is live

- **Health Visiting team finder** (David) – Section 4 Contact your team, and the same finder in Section 8:
  - The instruction "To see your team's contact details, select your Locality, then your Health Visiting team" now stays on screen after a team is chosen (Section 4), so a carer who picked the wrong team can see what to do.
  - More space between the instruction and the menus, and between the menus and the team card.
  - The **Contact details / Map** switch is always shown on the card. A newly chosen team always opens on Contact details. Switching fades smoothly (no motion if the iPhone's Reduce Motion is on).
  - **"Tap the contact number to call."** is now inside the card, under the opening hours, above a thin divider. The separate note under the card has gone (the switch now shows the map).
  - **One phone number per team**: Cheadle Hulme and Bramhall (0161 835 6552) and Heatons (0161 835 6490) keep their first number only.
  - Card polish: rounded corners with a soft shadow, a clock icon on the hours line to match the address pin, more room under the team name.
  - On shorter screens (iPhone in Safari) the small "Locality" and "Health Visiting team" labels above the menus are hidden from view, as the instruction just above names both; screen readers still hear them. The first menu now shows "Locality" rather than "Choose". The smallest map height is 100 px (was 130 px) so the map view fits on iPhone SE.
- Every team (23) checked in both views on both pages at every iPhone size, plus every page of the guide. Offline copy renamed `ey-guide-v2.85`. Built by `scripts/make285.py`.

## 18 November 2026 – guide version 2.84 is live

- **Section 4 · Your Health Visiting team title boxes** (David): same design as NHS login – a dark blue strip at the top with the NHS logo and **Health Visiting team**, then the title and underline on the NHS login blue. The NHS logo in the corner and the faint ABC blocks are gone. Both Section 4 pages.
- Titles shortened to one line, as the strip already says Health Visiting team: **Contact your team** and **Confirm your details** (Contents and Search keep the full names). The title and underline sit in the same place as on every other page.
- **About your account** (David): one highlight only. "In this guide, we call this person the account holder" is now plain text after the opening sentence; then the two points; then the yellow note "A partner or another family member **cannot** sign in to the account".
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.84`. Built by `scripts/make284.py`.

## 18 November 2026 – guide version 2.83 is live

- **Section 3 · NHS login titles on one line** (David): Step 1 Go to NHS login · 2 Sign-in page opens · 3 Email and password · 4 Security code page · 5 Get your security code · 6 Enter the security code · 7 Checking your details · 8 Your NHS account page (tips use their step's title). Part a is now titled **Information needed**; the band on the two part pages reads "NHS login | Part a" and "Part b". All fit on one line at 375 px wide and above; at 320 px (Display Zoom) a few wrap, as some Signing in titles do.
- **Title boxes match Section 6 Signing in**: the NHS login step boxes are now 110 px (were 128 px) with the title and underline in exactly the same place; the NHS login band stays on top with the progress bar under it. On iPhone SE in Safari they match the Signing in boxes too. Every title box in the guide is now the same size at 375 px and above.
- **Wording**: the Signing in to NHS login page no longer sends people back to the checklist (it now comes later); it says the same email address and password are used for the GM Early Years App, links to NHS login account issues, and adds the GMDP Support team note. Step 4 no longer repeats its tip. Step 6 and 7 tips both say "(see Section 8 · Contact & support)". Step 8's note now ends "Tap Next to go to Section 4 · Contact your Health Visiting team". "NHS login Support team" is spelled one way throughout.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664. Offline copy renamed `ey-guide-v2.83`. Built by `scripts/make283.py`.

## 17 November 2026 – guide version 2.82 is live

- **Skeleton of the new structure** (David), so each section can be worked on step by step: I Introduction · 1 How this guide works · 2 About your account · 3 NHS login (a Information needed from NHS login, b Signing in to NHS login) · 4 Contact your Health Visiting team · 5 Run through the Checklist · 6 Signing in to the GM Early Years App · 7 Troubleshooting · 8 Contact & support · 9 About this guide · Accessibility.
- **About your account** (new Section 2): checklist Information 1 and 2 combined into one page. The checklist now starts straight at question 1, its start page says it has 4 questions, and its progress bar has 4 segments.
- **NHS login** (Section 3): new start page listing parts a and b; new placeholder page **Information needed from NHS login** (content to follow); the existing NHS login sign-in pages are part b.
- **Contact your Health Visiting team** (Section 4): the team finder is retitled; new placeholder page **Confirm your NHS login contact details** (content to follow), in NHS blue.
- Section numbers 2 to 8 became 3 to 9 everywhere (labels, Contents, How this guide works, cross-references, styling). Back and Next follow the new order (73 pages).
- To fit the extra rows on shorter screens: Contents rows 40 px (34 px on iPhone SE in Safari) and How this guide works rows 41 px (37 px).
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 375×637, 360×640 and 320×664; checklist answers and the Next route checked. Offline copy renamed `ey-guide-v2.82`. Built by `scripts/make282.py`.

## 17 November 2026 – guide version 2.81 is live

- **New section order** (David): 1 How this guide works · 2 Signing in to NHS login · 3 Your Health Visiting team · 4 Checklist · 5 Signing in to the GM Early Years App · 6 Troubleshooting · 7 Contact & support · 8 About this guide. Cover, Contents and Introduction stay first.
- How this guide works moved out of About this guide to become Section 1; its list now shows the new route (sections 2 to 8).
- The NHS login sign-in pages (start page plus Steps 1 to 8 and tips) moved out of Troubleshooting into their own Section 2, **Signing in to NHS login**; they are no longer on the NHS login account issues list (now 7 items).
- Section numbers updated everywhere: page labels, Contents, cross-references ("see Section 7", "go to Section 6 · Troubleshooting") and the styling for the Signing in screenshots. Back and Next follow the new order.
- To fit the extra rows: Contents no longer lists the Cover page (Back from Contents still goes there) or shows the "Select Next below" tip; How this guide works no longer shows the grey descriptions or the "Tap a section" line; on iPhone SE in Safari the Contents rows are 37 px.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, including every checklist answer. Offline copy renamed `ey-guide-v2.81`. Built by `scripts/make281.py`.

## 17 November 2026 – guide version 2.80 is live

- **NHS login sign-in steps are numbered 1 to 8** instead of A to H (band "Step 3 of 8", page names, screen reader text, tip pages and the "continue at Step 7" link).
- **Progress bar** on Steps 1 to 8 and their tip pages, like Section 3 Signing in: eight slim segments under the NHS login band (done green, current white). These title boxes are 128 px so a two-line title fits; titles stay in the same position as on every other page.
- Step 8 renamed **Your NHS account page**, so it no longer shares the title "Check your NHS account details" with the list item.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, light and Dark Mode. Offline copy renamed `ey-guide-v2.80`. Built by `scripts/make280.py`.

## 17 November 2026 – guide version 2.79 is live

- NHS login account issues list: "How to sign in to NHS login" is now item 2, renamed **Check your NHS account details** (list and page title). The page and its Steps A to H now follow Set up NHS login, so Next and Back follow the list order.
- Steps B to H screenshots now match Section 3 Signing in: 248 points wide and centred, cropped to the part of the screen that matters and the highlighted area, with "Tap to enlarge" underneath. The title boxes keep the NHS login blue band.
- Checked NHS login's help: signing in is still email address and password, then a security code sent to your phone (or a passkey).
- Checked on eight iPhone sizes in Safari and as a Home Screen app; every title box now the same size at every width. Offline copy renamed `ey-guide-v2.79`. Built by `scripts/make279.py`.

## 17 November 2026 – guide version 2.78 is live

- **Cannot get into your email** now follows NHS login's own advice. NHS login only lets you change your email in your settings after signing in; if you cannot get into your email, you need to create a new NHS login. What to do: "Set up a new NHS login with an email you can open." then "Ask your Health Visiting team to update your App account." The first button is renamed "Lost access to your email" and opens NHS login's page on it.
- On iPhone SE in Safari the bracketed note and the two buttons on this page are slightly smaller so it fits.
- Checked on eight iPhone sizes in Safari and as a Home Screen app. Offline copy renamed `ey-guide-v2.78`. Built by `scripts/make278.py`.

## 17 November 2026 – guide version 2.77 is live

- Troubleshooting page "When you can sign in to NHS login" removed (David).
- "Change your password" removed from the NHS login account issues list and the guide: NHS login's help says you change your password in your NHS login settings, after signing in, by entering your current password — so it is not a sign-in problem. Forgotten passwords are still covered by "Forgotten your password", and both pages linked to the same NHS login passwords page.
- "How to sign in to NHS login" is now item 8 on the NHS login account issues list, with the "NHS login | Account issues" band like the other pages on the list. The list stays at eight items and fits every iPhone.
- Page numbers updated: Troubleshooting is now 32 pages; the guide is 71 pages (plus Search).
- Checked on eight iPhone sizes in Safari and as a Home Screen app. Offline copy renamed `ey-guide-v2.77`. Built by `scripts/make277.py`.

## 17 November 2026 – guide version 2.76 is live

- **Titles and underlines sit in exactly the same place on every page**, so nothing shifts when you move between pages. The seven section start pages (Introduction, Your Health Visiting team, Checklist, Signing in, Troubleshooting, Contact & support, About this guide) use a different kind of title box, which had slightly different settings: title 2 px further right and 2 px lower, tighter line spacing, and the underline 2 px right and 2 px higher. They now match every other page.
- The Contact & support "Your Health Visiting team" title sat 16 px higher than the others to leave room for the NHS logo underneath; the logo now sits bottom right beside the title, as on the Section 1 team page.
- Measured on all 72 title boxes at 375 × 637, 375 × 548, 320 × 664 and 430 × 876: one position everywhere. Offline copy renamed `ey-guide-v2.76`. Built by `scripts/make276.py`.

## 17 November 2026 – guide version 2.75 is live

- **Back to clear title boxes** (David: lighter, less busy). The 2.73–2.74 design is now called "the banded version".
- Every title box is in the GM Early Years App colours (plum to crimson) with the white ABC blocks from the app logo faintly behind the right-hand side. No band or page icon; the small label above the title ("Question 1 of 4", "Part 2 of 3 · NHS login") is back.
- The Your Health Visiting team pages are NHS blue, with the ABC blocks and the NHS logo. The Section 1 title no longer runs under the NHS logo.
- NHS login pages keep the banded look: NHS blue with the "NHS login | …" band, NHS mark and page icon (the NHS login account issues pages, When you can sign in to NHS login, How to sign in to NHS login, Steps A to H and their tips, NHS login Support Team).
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 360 × 640 and 320 × 664, light and Dark Mode, including every checklist answer. Offline copy renamed `ey-guide-v2.75`. Built by `scripts/make275.py`.

## 17 November 2026 – guide version 2.74 is live

- Same look as 2.73, smaller file: the app icon in the title box bands was stored 45 times, which grew the guide from 1.9 MB to 3.6 MB. It is now stored once, so the guide is back to 1.9 MB and opens faster on a weak signal. Offline copy renamed `ey-guide-v2.74`. Built by `scripts/make274.py`.

## 17 November 2026 – guide version 2.73 is live

- **New title boxes across the guide**, chosen from the "App band + icon" mockups. Every title box is in the GM Early Years App colours (plum to crimson, from the ABC app logo) with a dark band reading "GM Early Years App | section" and the ABC app icon.
- **NHS login pages are not in the app colours.** They are NHS blue with an "NHS login" band and the NHS mark, matching the NHS login account issues pages: When you can sign in to NHS login, How to sign in to NHS login, Steps A to H and their tips, and NHS login Support Team.
- Question, step and tip pages: the band shows the section and position (for example "Checklist | Question 1 of 4"), with the progress bar under it. Other pages have a page icon in a white circle. The large faded page numbers and the small NHS logo in title boxes are no longer shown. The NHS logo no longer overlaps the Section 1 title.
- Narrow and short screens: on iPhones narrower than 370 px the band shows the app icon without the app name; on iPhone SE in Safari the band is slimmer, page icons are hidden and pages with a progress bar keep their previous header, so every page still fits.
- Trials 2.71 (section colours with faded ABC blocks) and 2.72 (app colour with faded blocks) were reviewed at `/preview/` and are not used; the trial copy is removed.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, plus 360 × 640 and 320 × 664, light and Dark Mode, including every checklist answer. Offline copy renamed `ey-guide-v2.73`. Built by `scripts/make273.py`.

## 17 November 2026 – guide version 2.70 is live

- **NHS login account issues pages** (the section page and its eight pages) have a new title box, option 6c: a dark NHS blue band reading "NHS login | Account issues", an NHS blue title box, and a white circle with an icon for the page (person, add person, padlock, key, phone with message, envelope, change arrows, mobile phone, ID card).
- On very short screens (iPhone SE in Safari) the band is slimmer and the icon is hidden so every page still fits.
- Checked on eight iPhone sizes in Safari and as a Home Screen app, light and Dark Mode. Offline copy renamed `ey-guide-v2.70`. Built by `scripts/make270.py` (uses `scripts/nhsmark_white.png`).

## 17 November 2026 – guide version 2.69 is live

- **Every page now fits on every iPhone.** After the cover fix, every page was checked on eight iPhone sizes (SE to 16 Pro Max), in Safari and as a Home Screen app.
- Activation Link not received was 4 px too long on a 12/13 mini in Safari: rows tightened slightly.
- iPhone SE in Safari (about 548 px tall): 20 pages and three checklist answers did not fit. On screens this short, title boxes now size to their content (at least 72 px) instead of a fixed 110 px, spacing is tighter, and two hint lines are hidden (Contents "Select Next…" and How this guide works "Tap a section…"). Text sizes are unchanged and nothing changes on taller screens.
- Offline copy renamed `ey-guide-v2.69`. Built by `scripts/make269.py`.

## 17 November 2026 – guide version 2.68 is live

- **Cover fills the screen on every iPhone.** Since 2.31 the cover photo was capped at 240 px, so taller screens showed a white gap above Back / Contents / Start, worst as a Home Screen app (132 px on a 12/13 mini, 264 px on a 16 Pro Max). The photo now takes the free space first, up to 85% of the screen width; the blue panel takes anything left, with its text centred; the photo framing moved left so the child's face stays in view.
- Checked with no gap on iPhone SE, 12/13 mini, 12/13/14, 14 Pro/15/16, 16 Pro, XR/11, Plus/Pro Max and 16 Pro Max, in Safari and as a Home Screen app. Offline copy renamed `ey-guide-v2.68`. Built by `scripts/make268.py`.

## 17 November 2026 – guide version 2.67 is live

- NHS login account issues pages 3 to 8 (Forgotten your password, Security code not arriving, Cannot get into your email, Change your password, Mobile number problems, My name has changed) now show **The issue**, **Who can help** (NHS login Support team, with the bracketed GMDP note) and **What to do**, with help links as buttons. The email, mobile number and name pages add a second step: ask your Health Visiting team to update your App account.
- "Common reasons for sign-in problems" is now a contents page, **Common sign-in problems**, leading to three pages: Details do not match, Partner's details used, A partner is signing in. These replace the "What stopped you signing in?" pages (Troubleshooting pages 31 to 33). The Troubleshooting contents row is renamed to match.
- **Still need help?** shows the GMDP Support team, what to include in the email, "Never send passwords or security codes.", and the email address on the button.
- Everything fits at 375 × 637, 360 × 640 and 320 × 664. Offline copy renamed `ey-guide-v2.67`. Built by `scripts/make267.py`.

## 17 November 2026 – guide version 2.66 is live

- Troubleshooting pages "Set up NHS login", "Cannot sign in" and "Activation Link not received" now show three parts: **The issue**, **Who can help** and **What to do**, with the help links as buttons under What to do.
- Who can help on the two NHS login pages is the NHS login Support team, with "(The GMDP Support team cannot assist with NHS login account issues, as they do not have access to NHS login accounts.)" underneath.
- "I have not received an Activation Link" is retitled "Activation Link not received" (both pages), with three short checks and a "What to ask" box.
- All three pages fit at 375 × 637, 360 × 640 and 320 × 664, light and Dark Mode. Offline copy renamed `ey-guide-v2.66`. Built by `scripts/make266.py`.

## 17 November 2026 – guide version 2.65 is live

- The live guide is now 2.65 (it was 2.57). This brings in all the changes in 2.58 to 2.65 below. The offline copy (`sw.js`) is renamed `ey-guide-v2.65`, so phones that saved an older version get 2.65 next time they have a signal. The trial copy at /preview/ is removed.

## 17 November 2026 – guide version 2.65 (trial copy at /preview/; the live guide stays 2.57)

- **Checklist questions line up:** on all four question pages the section line, the first line of the explanation, the first line of the question, and the tops of the Yes and No boxes are at the same height (the explanation always takes three lines of space, the question two).
- Q3 question: "Do both accounts use the same email address and mobile number?"
- Q4 message after No: "Select **Next** to see your checklist summary."
- Fits at all eight sizes, except Q4 with No chosen at 360 × 640 (19 px). At 320 wide the Yes answers on Q1 and Q2 take two lines, so their No boxes sit lower.

## 17 November 2026 – guide version 2.64 (trial copy at /preview/; the live guide stays 2.57)

- **Checklist questions:** each page gives the reason, then asks the question on its own line in bold, then "Select one option, then select Next." and the two answers.
  - Q1 "Do you have an NHS login account?" – "Yes, I have an NHS login account" / "No, I have not set up an NHS login account".
  - Q2 "You will sign in to the App with your NHS login email address and password." "Can you sign in to your NHS login account?" – "Yes, I can sign in to my NHS login" / "No, I cannot sign in to my NHS login".
  - Q3 "…the same email address and mobile number as your NHS login account." "Does your GM Early Years App account use the same email address and mobile number as your NHS login account?" – "Yes, my account details match" / "No, my account details do not match, or I'm not sure".
  - Q4 "Have you received an Activation Link?" – "Yes, I have my Activation Link" / "No, I have not received an Activation Link".
  - Stop message after No on Q1–Q3: "Select **Next** to complete the checklist."
- **Checklist summary:** "If any item below has a red cross, tap **Get help** next to it to find out what to do." under the section line; the amber box at the bottom is removed.
- Fits at all eight sizes, except Q3 with No chosen at 320 × 664 (12 px).

## 17 November 2026 – guide version 2.63 (trial copy at /preview/; the live guide stays 2.57)

- **Checklist summary:** Next always goes to Section 3, Signing in to the GM Early Years App. It is green when all four answers are Yes; when there are crosses it stays blue but still goes to Signing in (it used to go to Troubleshooting).
- NHS login account cross: **Get help** opens the new "Set up NHS login" page.
- Amber message with crosses: "Select **Get help** next to each cross." ("or Next for more help" removed). The summary now fits at all eight sizes in all 81 answer combinations.
- No pages deleted; the "What stopped you signing in?" pages stay for now.

## 16 November 2026 – guide version 2.62 (trial copy at /preview/; the live guide stays 2.57)

- **New Troubleshooting page, "Set up NHS login"** (page 3 of 34): what the NHS login set-up help covers (What is NHS login?, Where you can use NHS login, What you need to set up an NHS login, How to set up an NHS login), the link help.login.nhs.uk/setupnhslogin, and "GMDP Support cannot access NHS login accounts." at the bottom.
- **NHS login account issues:** "Set up NHS login" is item 1 (the others are now 2 to 8). "GMDP Support cannot assist with NHS login account issues." is now under the section line, above the list, in place of "Choose your problem to find NHS login help:"; the line at the bottom is removed. Fits at all eight sizes.
- Page numbers updated: Troubleshooting has 34 pages; the guide has 73 pages (plus Search).

## 16 November 2026 – guide version 2.61 (trial copy at /preview/; the live guide stays 2.57)

- **Section 3 Signing in, new titles:** page 6, Step 5 "Enter your credentials" (was "Enter your email and password"); page 7, Step 6 "Enter the security code" (was "Get your NHS login security code"); page 8, Step 7 "Enter security code" (was "Enter your NHS login security code"); pages 12, 13 and 14, Step 11, its Helpful tip and Step 12 "App verification code" (were "Get your App verification code" and "Enter your App verification code").
- Troubleshooting Step C and its Helpful tip keep "Enter your email and password".

## 16 November 2026 – guide version 2.60 (trial copy at /preview/; the live guide stays 2.57)

- **Section 1 › Your Health Visiting team:** removed the first line, "Your team can check your account and link." The Contact & support team page keeps it.

## 16 November 2026 – guide version 2.59 (trial copy at /preview/; the live guide stays 2.57)

- **Contact & support › Your Health Visiting team:** removed the two lines under the team card ("To view on a map, tap the address." / "To call, tap the contact number."). Every card now fits on a 375 × 637 screen (the Stockport "Cheadle Hulme and Bramhall" card was 9 px over in 2.58). Section 1's team page keeps the two lines.
- Still over on the smallest screen (320 × 664): the map view of three cards on this page (Bury 5th, Rochdale 4th and 5th, 5 px); Checklist summary with all four answers No (15 px); How this guide works (31 px) and Mobile number problems (15 px), left as they are; "I have not received an Activation Link" (also 10 px at 360 wide), to be reworked later.

## 16 November 2026 – guide version 2.58 (trial copy at /preview/; the live guide stays 2.57)

- **Every title box the same height (Option B, 110 px).** The title sits at the bottom of the box; the progress bar stays at the top. **Contents** is the one exception: it keeps its shorter title box and the "Select Next" tip.
- **Shorter titles so they fit:** Step H and its Note page "Check your NHS account details" (was "Check your name, date of birth and NHS number"); Step C and its Helpful tip page "Enter your email and password" (was "Enter your email address and password"); Step D Good to know page "Security code page" (was "The security code page opens"; Step D itself unchanged).
- **Left as they are (need a short scroll on the smallest screen, 320 × 664):** How this guide works (31 px), Mobile number problems (15 px). "I have not received an Activation Link" (10 px at 360 and 320 wide) is to be reworked later.
- **Still to decide:** Contact & support › Your Health Visiting team, one Stockport card is 9 px too long on a 375 × 637 screen (and three cards' map views 5 px at 320 wide); Checklist summary with all four answers No is 15 px too long at 320 wide.

## 16 November 2026 – guide version 2.57 is live

- The live guide is now 2.57 (it was 2.54). This brings in all the changes in 2.55, 2.56 and 2.57 below. The offline copy (`sw.js`) is renamed `ey-guide-v2.57`, so phones that saved 2.54 get the new version next time they have a signal. The trial copy at /preview/ is removed.

## 16 November 2026 – guide version 2.57 (trial copy at /preview/)

- **NHS login Support Team, NHS login help:** shorter link titles. "What is NHS login / Set up an NHS login account" is now "Set up an NHS login account"; "Contact the NHS login Support Team" is now "Contact NHS login support"; "Change your email, mobile number or password" is now "Change contact details". "NHS login Help Centre" and the web addresses are unchanged.
- **I have not received an Activation Link, What should I check?:** the third point is now "If you cannot find the link, contact your Health Visiting team." (removed "or it does not open").
- "Forgotten your password" and "Common reasons for sign-in problems" are unchanged (to be reworked later).
- **Fit:** every page now fits at all eight sizes, including "NHS login Support Team" and "I have not received an Activation Link" at 320 × 664.

## 16 November 2026 – guide version 2.56 (trial copy at /preview/; the live guide stays 2.54)

- **Checklist summary:** the title box shows one title, "Checklist summary" (the label "Checklist summary" and the title "Your checklist results" repeated each other). The stop messages on Questions 1 to 4 now say "checklist summary" to match.
- **Your Health Visiting team (both pages):** team cards show only the team name, address, phone number(s) and opening hours. Removed: "Referral only, through your Health Visitor or midwife." (Enhanced and SEND, Bury) and "For young first-time parents, referred by the midwife. Number: Health Visiting Advice Line." (Family Nurse Partnership, Stockport).
- **NHS logo** in the title box of both Health Visiting team pages (the NHS part of the guide's NHS login badge, same size and place).
- Numbered circles on three Troubleshooting pages are 15, the same as the other lists.
- **Fit:** the checklist summary (all 81 answer combinations) and every team card now fit at all eight sizes. Still over, only at 320 × 664: "NHS login Support Team" (3 px, text visible) and "I have not received an Activation Link" (4 px, to be reworked later).

## 16 November 2026 – guide version 2.55 (trial copy at /preview/; the live guide stays 2.54)

- **All text on Apple's recommended iPhone sizes:** reading text, links, messages, search results, buttons and controls are Body 17 everywhere (some had been reduced to 15 or 16 to make pages fit); page titles are Title 2 22 (were 21.5 or 23); the cover title is Large Title 34 (was 36); headings inside pages are Headline 17 (were 16 or 18). Labels (11 to 13), the cover's subtitle lines and the icons in circles are unchanged.
- **Pages that no longer fit** (only on the two narrowest test screens): Checklist results at 320 × 664 when three or four answers are No (4 px; 27 px with four Nos, where the last line goes under the Back/Next bar); "I have not received an Activation Link" and "NHS login Support Team" at 320 × 664 (4 px and 3 px); the Family Nurse Partnership card at 320 × 664 and 360 × 640 (2 to 5 px). Every other page and state fits at all eight sizes.

## 16 November 2026 – guide version 2.54

- **Checklist questions 1 to 4:** choosing "No, or I'm not sure" now shows the same short message on every question: "You will not be able to access a GM Early Years App account", then "Select Next to complete the checklist. Your checklist results will then explain what to do next." (Question 4: "Select Next to see your checklist results and what to do next."). The links and longer help that were in these messages are removed; the specific help is given once, on the checklist results page.
- **Checklist results:** Get help for "NHS login account" now opens "What stopped you signing in?" in Troubleshooting (which has the NHS login set-up guidance), in place of Question 1.
- The message text is 17 (the old messages had been reduced to 15 to fit).
- Tested: every question in both answer states, in Light and Dark Mode, fits at all eight iPhone sizes.

## 16 November 2026 – guide version 2.53

- **Home Screen app:** the website now has an app icon (an open book with a yellow question mark, different from the GM Early Years App's own icon) and the name "EY App Guide". In Safari, Share → Add to Home Screen puts it on the iPhone; it then opens full screen like an app. New files: `manifest.webmanifest`, `icons/`, `sw.js`; the deploy workflow now publishes them.
- **Works offline:** after one visit, the website keeps a copy of the guide on the phone (`sw.js`), so it opens with no signal. With a signal it always fetches the latest version. Maps still need a signal. A downloaded copy of the file is unchanged.
- **Search:** a Search button in the Contents title box opens a new Search page. It searches the titles and words of every page (including team names and addresses), highlights the matching words and opens a page when tapped. Results scroll inside the page; the page itself still fits one screen.
- **Dark Mode:** the guide follows the iPhone's Light/Dark setting. Printing stays light.
- `validate_site.py` checks the Home Screen files and that the offline copy is named for the current version.
- Tested: every page fits at all eight iPhone sizes in both Light and Dark Mode; all team cards fit; search tested with sample words; the guide opened offline after one visit (local test).

## 16 November 2026 – guide version 2.52

- New page in Section 6: **How this guide works**. It shows the six sections in order as a route; each one can be tapped to go straight to it. Under Checklist, two markers show the branch: all Yes goes to Signing in, any No goes to Troubleshooting.
- Section 6 is now 4 pages (About this guide, How this guide works, Document control, Revision history); the guide has 72 pages.
- Tested: every page fits at all eight iPhone test sizes; Next and Back walk correctly through Sections 5 and 6.

## 16 November 2026 – guide version 2.51

- New **Section 6 · About this guide**, with its own title page, Document control and Revision history (moved from Contact & support).
- **Section 5 · Contact & support** now holds only the help pages: Your Health Visiting team, NHS login Support Team, GMDP Support Team and Accessibility (5 pages). Its list shows "Accessibility – Large print, easy-read and other formats" in place of "About this guide".
- **Accessibility** wording: "If this guide is hard to read or use, it is available in large print, easy-read and other formats or languages. To ask for one, please contact the GMDP Support Team at …".
- **Contents** has two new rows: 6 About this guide, and Accessibility at the end (with an accessibility symbol). Spacing tightened so it still fits one screen.
- The guide now has 71 pages; page positions, section lines and Back/Next links updated.
- Tested: every page fits at 375×637, 390×664, 393×659, 430×739, 375×715, 360×640, 414×715 and 320×664; Next and Back walk correctly through Sections 5 and 6.

## 16 November 2026 – guide version 2.50

- Your Health Visiting team (Section 1 and the Contact & support copy): every team address (23 on each page) is now a tappable link. Tapping it opens a map of that address inside the team card, with a Contact details / Map switch to go back. The map fills the space left on the screen and loads only when it is first opened. "Open in Maps" under the map opens the address in the Maps app.
- Under the team card: "To view on a map, tap the address." and "To call, tap the contact number." (hidden while the map is showing).
- Choosing another team starts on contact details again. Printing shows contact details only.
- Checklist, Information 2 of 2 (Who can sign in?): new wording; "A partner or another family member cannot sign in to the account." is now in a yellow box.
- Tested: all 46 team cards, in both views, fit at 375×637, 390×664, 393×659, 430×739, 375×715, 360×640, 414×715 and 320×664; every page fits at all eight sizes.

## 16 November 2026 – guide version 2.49

- NHS login logo sits at the bottom right of the title box on "How to sign in to your NHS login account" and "NHS login Support Team", so the titles use the full width (the first now fits on two lines instead of three).

## 16 November 2026 – guide version 2.48

New page layout ("C"):
- The blue header (logo, GM Early Years App, GMCA) shows on the cover only.
- Every other page opens with a blue title box. Title pages keep their existing box. On checklist, Signing in and NHS login step pages the box holds the progress bar, the small label (for example "Question 1 of 4") and the title, with the step number or letter as a large faint number. Other pages have the title in the box; the NHS login logo sits inside the box on the two pages that have it.
- The section line ("SECTION 2 · CHECKLIST … PAGE 4 OF 8") sits under the box as plain text; the thin progress line under it is removed.
- The "8 / 70" counter under Contents is removed.
- The numbered circles beside step and question titles are removed (the number is in the box).
- Signing in screenshots get more room because the header no longer takes space.
- Printing: boxes print as plain headings.
- Tested: every page, all 81 summary answer combinations and all 23 team cards fit at 375×637, 390×664, 393×659, 430×739 and 375×715; at 360×640, 414×715 and 320×664 fewer pages scroll than in 2.47. Downloaded-copy mode (no scripts) hides the header after the cover too.

## 16 November 2026 – guide version 2.47

- Reading text is now 17 (Apple's default size) everywhere a carer reads: Health Visiting team pages, Checklist summary, Signing in page 1 and step 1, Troubleshooting topic lines, notes and web addresses, and Contact & support. Labels are unchanged. The GMDP email button stays 15 so the address fits.
- Long web addresses break after a slash, never at a hyphen.
- So that pages still fit one screen at 375 × 637 and the other iPhone test sizes:
  - Your Health Visiting team (both copies): opening line now "Your team can check your account and link."; the Contact & support copy also hides the "To see your team" line once a team is chosen.
  - NHS login Support Team: description now "For NHS login problems. GMDP Support cannot access NHS login accounts."
  - Troubleshooting NHS login pages: bottom note now "GMDP Support cannot access NHS login accounts."
  - Checklist summary: "Select Answer next to any item with a dash." and "Select Get help next to each cross, or Next for more help."; rows slightly tighter.
  - Signing in step 1: the screenshot is slightly smaller. No Activation Link: spacing tightened.
- Tested: every page, all 81 summary answer combinations and all 23 team cards at 375×637, 390×664, 393×659, 430×739 and 375×715.

## 16 November 2026 – guide version 2.46

- Checklist Information 1 (Section 2, page 2): "Your Health Visiting team sets up a GM Early Years App account for:" followed by a bullet, "the **child's mother** or **primary carer**." (bold as before).

## 16 November 2026 – guide version 2.45

- "Select Next to continue." is now "Tap Next to continue." on Checklist Information 1 and Information 2 (the only two places it appeared).

## 16 November 2026 – guide version 2.44

- Checklist (Section 2, page 1): the information box now reads "If you answer No, a summary at the end of the checklist will explain what to do next or where to get help." (replaces the two earlier sentences).

## 16 November 2026 – guide version 2.43

- Introduction: "Contact & support" in the last line is now a link that opens Section 5, Contact & support. Back returns to the Introduction.

## 15 November 2026 – guide version 2.42

- Checklist (Section 2, page 1): "If you answer No, the guide will explain what to do next" and "A summary at the end shows what to do next or where to get help" are now in an information box, in the same style as "In this guide, this person is called the account holder" on the next page.
- Spacing in the box is slightly tighter so that the page still fits one screen at 375 × 637.

## 15 November 2026 – guide version 2.41

- Section 1, Your Health Visiting team: the title is now in the blue title box with a large "1", like the Introduction and the Checklist. The title stays on one line.
- To make room, the "To see your team's contact details…" line hides once a team is chosen, and the team card sits a little closer to the choices. Every team still fits one screen at 375 × 637 and above.
- The copy in Contact & support is unchanged.

## 15 November 2026 – guide version 2.40

- Revision history: the 2.37 entry now correctly says "New Section 1, Your Health Visiting team".

## 15 November 2026 – guide version 2.39

- Checklist (Section 2, page 1) reworded: "Before you sign in, please run the checklist to ensure that everything is ready." The 2 information pages and 4 questions are now bullet points, with a space between paragraphs. The summary line now reads "A summary at the end shows what to do next or where to get help."

## 15 November 2026 – guide version 2.38

- Checklist (Section 2, page 1): title shortened to "Checklist", also in Contents and in the three "return to the checklist" links in Troubleshooting.
- The large "Begin the checklist" button is removed; the Begin button at the bottom is green and pulses, like Signing in.
- Wording: "Tap Begin to start the checklist."

## 15 November 2026 – guide version 2.37

- New Section 1, "Your Health Visiting team", is its own page between the Introduction and the Checklist (Introduction → Next → Section 1 → Next → Section 2 Checklist). It is a copy of the team finder page, with its own Locality and team choices.
- The original "Your Health Visiting team" page stays in Contact & support.
- Sections renumbered: Checklist 2, Signing in 3, Troubleshooting 4, Contact & support 5. Contents shows the new numbers and its "Your Health Visiting team" row opens Section 1.
- The guide now has 70 pages; page counts and progress bars updated.
- Printing: the Section 1 copy shows a pointer to Contact & support instead of repeating all 23 teams.

## 15 November 2026 – guide version 2.36

- Contents: "Cover page" added as the first entry and "Your Health Visiting team" after Introduction (it opens the existing page in Contact & support). The "Select Next" prompt now uses the standard information box, on Contents and Introduction. The Contents title box is shorter so that seven entries fit.
- Signing in, page 1: the large "Begin signing in" button is removed; the bottom Begin button is green.
- Step 1, Restart your iPhone: three short steps, with how to turn the iPhone off and on in an information box.
- Step 6: the "Not asked for a code?" box is removed.
- Step 9: title changed to "Checking your details".

## 15 November 2026 – guide version 2.35

- Text sizes now follow Apple's recommendations for iPhone: main text, answer options, boxes and buttons 17; supporting text 15; labels 12 to 13; nothing under 11 except the lettering in the GMCA logo.
- A few tight pages use 15 for detail text so that every page still fits one screen.
- Downloaded copies (no scripts) re-tuned for the larger text.
- The `/preview/` trial has been removed now that it is the live guide.

## 15 November 2026 – preview: Apple text sizes

- A trial version is published at `/preview/` with text sizes following Apple's iOS text styles (body 17, secondary 15, labels 12 to 13, nothing under 11). The live guide is unchanged at v2.34.

## 15 November 2026 – guide version 2.34

- Page height: pages are now sized to the visible part of the screen (100dvh) instead of the screen with the browser toolbars hidden (100vh). On an iPhone in Chrome this was 736 against a visible 637, so the bottom 99 px of some pages sat behind Back, Contents and Next.
- Small links: in-text links keep their look but respond to taps across a 44 px-high area (55 of 69 links; the 14 left are in Troubleshooting).

## 15 November 2026 – guide version 2.33

- Introduction: the "GM Early Years App Account Support" section is replaced by one line pointing to Contact & support, where the support details already are.
- Testing aid: adding `?debug` to the website address shows a small read-out of the screen sizes the browser reports on each page. It is not shown otherwise.

## 15 November 2026 – guide version 2.32

- Signing in pages: the guide now measures the visible screen more cautiously (smallest of the window, dynamic viewport and visual viewport) and re-measures after the browser toolbars settle, so the bottom of the page is not cut off.
- Downloaded copies (no scripts): more room is kept below each Signing in screenshot.

## 15 November 2026 – guide version 2.31

- Printing now gives the whole guide (about 42 A4 pages) instead of only the page on screen. Both answers to each checklist question and every Health Visiting team are printed.
- Cover: new full photo; the "Greater Manchester – Doing Digital Differently" wording is a separate layer and is no longer cropped.
- Cover start button now reads "Start".
- NHS login Support Team page: larger NHS login logo.
- "NHS Login" corrected to "NHS login" in 14 places.
- Menu titles for checklist questions 2 and 4 now match the short titles on the pages.

## 15 November 2026 – guide version 2.30

- Signing in (steps 1 to 15): every screenshot is now the same width and starts the same distance below the text. On a short screen the picture shows less of the phone screen instead of shrinking.
- "Tap to enlarge" now sits under each Signing in screenshot, so it no longer covers a highlighted button.
- Pages now fit without scrolling on a 375 × 637 screen (iPhone with the browser toolbars showing).

## 15 November 2026 – website created

- Guide version 2.29 (review draft, iPhone edition) published as `index.html`, unchanged from the delivered file.
- Added the 404 page, validation scripts and the GitHub Pages deployment workflow.
