# Reservation Platform — UI/UX Redesign Specification

**Date:** 2026-09-13  
**Status:** Approved direction for implementation  
**Scope:** Visual system + UX redesign only; preserve existing reservation/business logic.

## 1. Product goal

Rebuild the Phase 1 reservation platform UI into a premium, minimal, Arabic-first experience that is easy to operate on mobile and remains polished on desktop. The redesign must make the user's current state and next action obvious without changing the existing reservation state machine, delay/no-show rules, financial ledger behavior, disputes, or authorization rules.

The existing product is a Django reservation platform for scheduled rides between passengers and drivers, with auth/roles, reservation state machine, symmetric delay workflow, no-show gating, lock period, notifications, financial ledger stub, disputes, and an Arabic RTL UI. fileciteturn17file0L2-L2

## 2. Approved visual direction

- **Style:** Premium Minimal.
- **Theme:** Light-first.
- **Palette:** Charcoal + Cream + quiet Terracotta.
- **Typography:** Tajawal.
- **Cards:** Soft cards, approximately 12–16px radius, very subtle shadow.
- **Navigation:** Hybrid — bottom navigation on mobile; sidebar/top navigation on larger screens.
- **Icons:** Rounded line icons.
- **Maps:** Minimal map with a smart information layer; map supports the task without dominating the UI.
- **Primary CTA:** Filled Charcoal. Terracotta is reserved for important statuses, alerts, and sensitive actions.
- **Status colors:** Quiet semantic colors: muted green for positive/completed states, sand/amber for waiting/action-required states, terracotta for destructive/problem states, and blue/gray for informational/transition states. Never communicate state by color alone; pair with text and iconography.
- **RTL:** Arabic-first and RTL by design, not as a final mirroring pass.
- **Responsive behavior:** Mobile-first, with intentional tablet/desktop layouts.

## 3. Passenger experience

### Home

Use a Smart Home layout:
- If a future/current reservation exists, make it the primary hero card.
- If no reservation exists, make quick booking the primary action.
- Show recent reservations below the primary content.
- Avoid dashboard clutter and decorative metrics that do not help the next action.

### Booking

Use a hybrid map booking flow:
1. Pickup field.
2. Destination field.
3. Interactive map for confirmation and adjustment.
4. Trip details and scheduling.
5. Review/confirm using a bottom sheet over the map.

Scheduling is Smart: present useful suggested times first, while allowing custom date/time selection.

### Upcoming reservation

Use a large, calm Upcoming Trip Card as the main element. It should expose date/time, route, reservation status, driver information when available, and exactly one dominant next action such as tracking or viewing details.

### Reservation details

Use the approved hybrid structure:
1. Trip summary.
2. Current status card.
3. Compact timeline of completed/upcoming states.
4. Map.
5. Details and available actions.

The current status and next permitted action must be visually stronger than historical details.

## 4. Driver experience

### Driver home

Use **Current Trip First**:
- Current reservation is the dominant content when one exists.
- Passenger information, pickup/destination, time, current state, and next action are immediately visible.
- Map is available when operationally useful but does not dominate the screen.
- When there is no current trip, present upcoming trips clearly.

## 5. Reservation state UX

Use a hybrid state experience:
- A prominent Status Card communicates the current state, meaning, and next action.
- A compact timeline provides orientation across the reservation lifecycle.
- Existing state transitions remain authoritative and must continue to go through the existing state-machine/service logic; the UI must never invent or directly mutate state.

For states such as confirmed, driver on way, arrived, waiting, in progress, completed, cancelled, passenger no-show, driver no-show, and disputed, use semantic visual treatment with text and icons.

## 6. Delay requests and sensitive actions

Delay requests use a clear dialog:
- Who requested the delay.
- Requested additional time.
- Countdown/deadline when relevant.
- Reason when available.
- Clear Accept / Reject actions.

Sensitive flows such as cancellation exceptions, no-show actions, and dispute-related confirmations should begin with a concise dialog. Escalate to a full page only when the existing business flow requires substantial information. Do not change authorization or eligibility rules.

The existing project already defines server-timestamp-based no-show eligibility, accepted-delay extensions, and auditable financial/dispute services; the redesign must surface those rules clearly without changing them. fileciteturn17file0L2-L2

## 7. Notifications

Use Smart Notifications:
- Surface only notifications requiring attention or action prominently.
- Keep a complete notification history in a dedicated notifications page.
- Prioritize delay requests, arrival, no-show eligibility, cancellation/dispute actions, and other operationally relevant events.
- Use semantic icons/status treatments and readable Arabic copy.

The existing notification row should remain the source of truth; push delivery is optional infrastructure and is not part of this visual redesign. fileciteturn17file0L2-L2

## 8. Profile

Use a Profile Card at the top, followed by a small set of useful stats and settings. Keep the screen calm and operational; do not turn it into a social profile.

## 9. Component system

Create a consistent component layer for:
- App shell and navigation.
- Page headers.
- Cards and list items.
- Primary/secondary/tertiary buttons.
- Form fields and validation messages.
- Status badges.
- Status cards and timelines.
- Bottom sheets.
- Dialogs.
- Notification items.
- Empty states.
- Loading/skeleton states.
- Error states.
- Confirmation/success states.
- Map overlays and location controls.

All components must use shared spacing, typography, radius, border, elevation, focus, hover, pressed, disabled, and accessibility rules rather than page-specific styling.

## 10. UX principles

1. **One dominant action:** each screen should have one obvious primary action.
2. **Current state first:** show what is happening now before history or secondary data.
3. **Next action explicit:** users should not have to infer what to do.
4. **Progressive disclosure:** advanced details appear only when useful.
5. **Low visual noise:** avoid excessive shadows, gradients, badges, and competing colors.
6. **Trust and safety:** destructive or financial actions require clear confirmation and consequence text.
7. **Accessibility:** adequate contrast, touch targets, keyboard/focus behavior, semantic labels, and non-color state indicators.
8. **RTL correctness:** layout direction, icon direction where appropriate, numbers/times, forms, maps, and mixed Arabic/Latin text must behave correctly.
9. **Responsive continuity:** information architecture stays consistent while layout adapts by viewport.
10. **Business logic is immutable during UI work:** no changes to reservation rules unless separately approved.

## 11. Out of scope for this redesign

- Real payment/deposit gateway.
- SMS integration.
- Native mobile application.
- New live-routing infrastructure or real-time location backend.
- New business rules.
- Changes to reservation authorization/state-machine behavior.

The current Phase 1 scope explicitly defers real payment processing, SMS, native mobile, live map click-to-pick-point/live driver location/real ETA infrastructure, and scheduled jobs. fileciteturn17file0L2-L2

## 12. Implementation acceptance criteria

- All passenger, driver, authentication, reservation, notification, delay, no-show, cancellation, financial-ledger, and dispute workflows continue to work as before.
- Every user-facing page follows the shared Premium Minimal design system.
- Mobile navigation uses bottom navigation; larger screens use the responsive desktop navigation pattern.
- Arabic RTL rendering is correct throughout.
- Booking uses the approved hybrid fields + map + bottom-sheet review interaction where the existing backend supports it.
- Reservation status uses the approved Status Card + Timeline pattern.
- Sensitive actions use clear dialogs.
- Empty/loading/error/success states are intentionally designed.
- UI does not expose fake metrics or claims.
- Production build/check/test commands are run before declaring the redesign complete.
- A deployed preview is reviewed visually on mobile and desktop before production rollout.
