# Project Status

Status date: 2026-11-23. This is a code and documentation status snapshot, not an update to the historical course report or task board.

## Historical course records

The adjacent `Sprint Progress Report_А10.docx` records all nine Sprint 1 tasks and all five Sprint 2 tasks as Done in their final task boards. It also notes that the October 15 WIP burndown is an intermediate snapshot, not the final Sprint 1 status. The report says US3, US5, and US6 still require separate acceptance evidence and that additional account-management work does not alter A10 acceptance status. The original report was left untouched.

## Current code status

- **Sprint 3 T5.1 urgent filtering:** Implemented and covered by a backend test for today through day 3, sorting, and excluding expired products.
- **Sprint 3 T5.2 expiry statuses:** Inventory cards use separate colors for fresh, expiring soon, urgent, expired, and undated products. Expired items have a red treatment and muted image. Date boundaries are covered by a 20-date test. Browser screenshots remain outstanding.
- **Sprint 3 T5.3 reminder settings:** Account settings save the reminder time and enabled state. A daily email command, duplicate-delivery record, SMTP settings, Windows runner, and scheduling guide are implemented. Deployment still requires SMTP credentials and a scheduled task.
- **Sprint 3 T5.4 functional testing:** Backend tests pass (17), Angular tests pass (16), and the production build passes. SQLite backup unit tests pass (3). Manual screenshot and end-to-end browser evidence remain outstanding.
- **Sprint 3 T5.5 backup and restore:** A timestamped backup of the local project database passed integrity verification. It was restored to a separate copy and product/profile row counts matched. The working database was not replaced.
- **UI refresh:** Shared design tokens and responsive CSS updates cover authentication, navigation, inventory, dashboard, discounts, catalog, product details, cart, checkout, orders, and account pages. The customer Discover page now has a grocery-market layout with a promotional header, category chips, a live featured product, live discounted items, and a searchable product grid. No fabricated reviews or bestseller rankings were added. A production Angular build passes; browser-based visual QA remains outstanding.

## Final review readiness

The repository has installation, API, testing, and backup documentation. Remaining review work is manual UI/workflow verification, screenshot evidence, and review of unresolved A10 acceptance evidence. No CI/CD workflow, commit, or push was added.
