# Changelog

Changes to the published website. The guide's own revision history is on its last page.

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
