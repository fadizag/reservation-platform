# Reservation Platform UI/UX Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the Phase 1 reservation platform UI into a polished Arabic RTL Premium Minimal experience while preserving all reservation, delay, no-show, cancellation, notification, payment-ledger, and dispute business logic.

**Architecture:** Keep the existing Django feature-based modular monolith and server-rendered templates. Introduce a small shared visual system in the base template, then apply it consistently to passenger, driver, reservation, account, notification, and dashboard surfaces. Keep behavior and state transitions in existing services/views; template work should consume existing context and URLs rather than duplicate business rules.

**Tech Stack:** Django templates, Tailwind CSS via CDN, HTMX where already used, vanilla JavaScript only for presentation interactions, Tajawal web font, RTL CSS.

**Spec:** `docs/superpowers/specs/2026-09-13-reservation-platform-ui-ux-design.md`

## Global Constraints

- Premium Minimal visual direction.
- Light-first interface.
- Charcoal + Cream + quiet Terracotta palette.
- Tajawal typography.
- Soft cards with 12–16px radius and restrained shadows.
- Hybrid navigation: bottom navigation on mobile, sidebar/top navigation on larger screens.
- Rounded line icon language.
- Minimal map with smart information layer.
- Charcoal primary CTA; Terracotta reserved for important states/attention.
- Semantic but muted status colors; never communicate state by color alone.
- Arabic RTL is first-class.
- Responsive/mobile-first behavior.
- Do not change business logic or state-machine rules.

---

### Task 1: Establish shared design system

**Files:**
- Modify: `templates/base.html`
- Create: `templates/partials/navigation.html`
- Create: `templates/partials/flash_messages.html`
- Create: `templates/partials/status_badge.html`

**Interfaces:**
- Base template exposes shared CSS tokens, typography, spacing, buttons, cards, forms, badges, focus states, and responsive navigation.
- Partials consume ordinary Django template context only.

- [ ] Inspect existing base template and all template inheritance points.
- [ ] Add Cream page background, Charcoal text/surfaces, quiet Terracotta accent tokens, semantic status tokens, Tajawal, and RTL defaults.
- [ ] Add reusable button, card, input, focus, badge, divider, and responsive container classes.
- [ ] Add mobile bottom navigation and desktop navigation without changing destination URLs.
- [ ] Add consistent flash/alert presentation.
- [ ] Add reusable status badge partial that includes text/icon semantics.
- [ ] Run Django template checks and existing test suite.
- [ ] Commit shared design system.

### Task 2: Redesign passenger home

**Files:**
- Modify: `templates/reservations/passenger_dashboard.html`

**Interfaces:**
- Preserve existing view context, reservation URLs, and actions.
- Use smart presentation: upcoming trip first when present; otherwise quick booking; recent reservations below.

- [ ] Add failing/behavior-preservation checks for all existing passenger dashboard links/actions where practical.
- [ ] Build upcoming reservation hero card with date/time, route, status, and next action.
- [ ] Build empty-state quick booking card when no upcoming reservation exists.
- [ ] Add recent reservation cards with semantic status badges.
- [ ] Ensure mobile layout uses bottom navigation and comfortable touch targets.
- [ ] Verify no context variable or endpoint is renamed.
- [ ] Run tests.
- [ ] Commit passenger dashboard redesign.

### Task 3: Redesign driver home

**Files:**
- Modify: `templates/reservations/driver_dashboard.html`

**Interfaces:**
- Preserve existing driver actions and reservation URLs.
- Current trip is the visual priority.

- [ ] Add presentation checks around existing driver actions.
- [ ] Build current-trip card with passenger, pickup, destination, schedule, status, and next action.
- [ ] Add compact upcoming-trip section below the active trip.
- [ ] Keep map as supporting content rather than dominant content unless existing context provides map data.
- [ ] Ensure action hierarchy uses Charcoal primary CTA and quieter secondary actions.
- [ ] Run tests.
- [ ] Commit driver dashboard redesign.

### Task 4: Redesign reservation creation flow

**Files:**
- Modify: `templates/reservations/reservation_form.html`

**Interfaces:**
- Preserve the existing form fields, POST target, validation, and server-side reservation creation behavior.
- Do not implement new routing/map business logic in this task.

- [ ] Preserve all current form field names and validation output.
- [ ] Create a hybrid booking layout: location fields first, map/presentation area second where supported, then schedule/details.
- [ ] Add Smart Scheduling presentation for suggested date/time choices only when existing context supports them; otherwise preserve the current controls cleanly.
- [ ] Style validation and help text consistently.
- [ ] Add a prominent Charcoal confirmation CTA.
- [ ] Run tests.
- [ ] Commit booking UI redesign.

### Task 5: Redesign reservation details and state experience

**Files:**
- Modify: `templates/reservations/reservation_detail.html`
- Create: `templates/partials/reservation_status_timeline.html`
- Create: `templates/partials/delay_request_dialog.html`

**Interfaces:**
- Consume existing reservation status/events and existing action URLs.
- Delay dialog submits to existing delay workflow; no new state transition implementation belongs in templates.

- [ ] Verify existing state labels/actions before editing.
- [ ] Build hybrid detail layout: trip summary, current status card, compact timeline, map/supporting location information, details, actions.
- [ ] Build accessible timeline using text and icons, not color alone.
- [ ] Build delay request dialog with requested minutes, reason when present, countdown presentation, accept/reject actions, and clear status copy.
- [ ] Preserve existing no-show, cancellation, dispute, and delay endpoints.
- [ ] Ensure sensitive destructive actions use clear confirmation dialogs.
- [ ] Run reservation tests and template checks.
- [ ] Commit reservation detail redesign.

### Task 6: Redesign authentication and account surfaces

**Files:**
- Modify: `templates/accounts/*.html`
- Create/modify: account profile/settings template as dictated by actual repository tree.

**Interfaces:**
- Preserve login, signup, logout, and account URLs/forms.

- [ ] Inspect actual account templates and contexts.
- [ ] Apply Tajawal, Premium Minimal forms, validation states, and consistent authentication layout.
- [ ] Build profile card with essential stats when existing context supports them; otherwise show only real available data.
- [ ] Keep settings compact and uncluttered.
- [ ] Run tests.
- [ ] Commit account UI redesign.

### Task 7: Redesign notifications and admin/dashboard surfaces

**Files:**
- Modify: notification templates found in `templates/notifications/` if present.
- Modify: `templates/admin_dashboard/*.html`
- Modify: `templates/core/*.html` where applicable.

**Interfaces:**
- Preserve notification read/action URLs and real dashboard metrics.
- No fake metrics or invented business claims.

- [ ] Inspect actual notification/admin templates.
- [ ] Add smart notification presentation: attention-first items plus full history.
- [ ] Apply dashboard hierarchy, cards, tables, filters, and empty/error states.
- [ ] Use muted semantic status colors and accessible labels.
- [ ] Run tests.
- [ ] Commit notification/admin redesign.

### Task 8: Responsive/accessibility polish and regression verification

**Files:**
- Modify: `templates/base.html` and shared partials as needed.
- Modify: affected templates from Tasks 2–7.

**Interfaces:**
- No business-logic changes.

- [ ] Check mobile widths, tablet widths, and desktop widths.
- [ ] Verify RTL alignment, logical spacing, focus visibility, keyboard operation, and minimum touch target sizing.
- [ ] Verify status information remains understandable without color.
- [ ] Verify reduced-motion-friendly presentation for any animations.
- [ ] Run full Django test suite and `python manage.py check` in an environment with dependencies installed.
- [ ] Review changed templates for duplicated styling and consolidate shared rules.
- [ ] Commit final UI/UX polish.

### Task 9: Preview deployment and review

**Files:**
- Modify deployment configuration only if required by the preview environment.

- [ ] Push the completed UI branch.
- [ ] Deploy to the existing Render preview service without changing production behavior.
- [ ] Verify the preview URL across passenger, driver, reservation, authentication, notification, and admin flows.
- [ ] Compare desktop and mobile layouts against the approved spec.
- [ ] Record any visual regressions or functional regressions as follow-up fixes.
- [ ] Open a PR from `ui-ux-redesign` to `main` after verification.

## Verification checklist

- Existing reservation state machine behavior is unchanged.
- Delay acceptance/rejection and expiry behavior is unchanged.
- No-show gating remains server-side and unchanged.
- Cancellation/lock-period behavior is unchanged.
- Dispute and ledger workflows are unchanged.
- Existing URLs/forms/actions continue to work.
- `python manage.py check` passes.
- Existing tests pass.
- Preview is usable on mobile and desktop.
