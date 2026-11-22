# Pages that scroll (to fix in the layout pass)

David, 22 Nov 2026: get the content in place first; fix layout later. Each build records here which pages scroll,
at which iPhone sizes (Safari visible area, points) and by how much.

## 3.56
- Question 2 loses its warning line, so its explanation is shorter; the shared question position is still set by question 5, so positions are unchanged.

## 3.55
- Removing question 4's Try signing in box cut its explanation from 190px to 114px. The shared question position is now set by question 5 (Do your details match?, 179px, because of the example card), so all questions still sit low: at 375×637 the worst scroll with an answer is Q1 37, Q2 37, Q3 61, Q4 74, Q5 74, Q6 83px. Next step: make question 5's example card smaller (or let each question set its own position).

## 3.54
- All six questions share one question position, set by the tallest explanation: question 4 (NHS login access) 190px, question 5 179px, question 2 152px, question 1 140px (at 375×637). With an answer chosen, question 2 scrolls 44-58px on 375-wide phones. Fix: trim questions 4 and 5 (target about 145px).

## 3.49
No answers on questions 3-6 now carry a help link (three lines), so they scroll on smaller iPhones:
- Question 3 (ts2), No: 375×548 22px · 375×629 23px · 375×647 9px · 375×637 15px · 360×640 30px · 320×664 27px
- Question 4 (ts3), No: 375×548 35px · 375×629 36px · 390×664 5px · 393×659 10px · 402×681 2px · 375×647 22px · 375×637 28px · 360×640 43px · 320×664 40px
- Question 5 (ts4), No: 375×548 35px · 375×629 36px · 390×664 5px · 393×659 10px · 402×681 2px · 375×647 22px · 375×637 28px · 360×640 43px · 320×664 61px
- Question 6 (ts5), No: 375×548 43px · 375×629 45px · 390×664 14px · 393×659 19px · 375×647 31px · 375×637 37px · 360×640 52px · 320×664 49px
- Questions 1-2, GM Early Years App help, start page: as 3.48.

## 3.48
- Question 2 (ts1b): fits at every size except 360×640 (Yes 3px, No 6px).
- GM Early Years App help (s4-gm): as 3.46.
- Troubleshooter start page (ts): as 3.40.

## 3.46 (superseded)
- Question 2 (ts1b), No selected: 375×548 33px · 375×629 38px · 375×647 24px · 375×637 30px · 360×640 33px · 320×664 21px
- Question 2 (ts1b), Yes selected: 375×548 8px · 375×629 13px · 375×637 5px · 360×640 8px
- GM Early Years App help (s4-gm): 375×548 18px · 375×629 14px · 375×637 6px · 320×664 5px
- Troubleshooter start page (ts), from 3.40: 375×548 24px · 375×629 5px · 390×664 12px · 320×664 8px

## 3.44 (superseded)
- Question 2 (ts1b), No selected: 375×548 33px · 375×629 38px · 390×664 7px · 393×659 12px · 402×681 4px · 375×647 24px · 375×637 30px · 360×640 33px · 320×664 43px
- Question 2 (ts1b), Yes selected: 375×548 8px · 375×629 13px · 375×637 5px · 360×640 8px
- GM Early Years App help (s4-gm): 375×548 18px · 375×629 14px · 375×637 6px · 320×664 5px (the renamed card title wraps)
- Troubleshooter start page (ts), from 3.40: 375×548 24px · 375×629 5px · 390×664 12px · 320×664 8px
