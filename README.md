# منصة حجز الرحلات — Phase 1 MVP

A Django reservation platform for scheduled rides between passengers and drivers. This is Phase 1 as scoped: auth + roles, the reservation state machine, the symmetric delay workflow, no-show gating, the lock period, notifications, a financial ledger stub, disputes, and a minimal Arabic-RTL UI. No real payment gateway or SMS integration yet — those are intentionally deferred.

## ⚠️ Important: this was written without being able to run it

The sandbox I built this in has no internet access and no Django installed, so I could not run `pip install`, `manage.py migrate`, `manage.py test`, or `manage.py check`. Every file here was hand-written and carefully cross-checked, but **you should run the checks below before trusting it in anything real** — there is a real chance of a typo, a missing import, or a template tag mistake surfacing on first run. Please run these and send me anything that fails and I'll fix it immediately:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py test apps.reservations
python manage.py runserver
```

By default it runs on SQLite with zero config. To use PostgreSQL, set:

```bash
export DJANGO_DB_ENGINE=postgresql
export DJANGO_DB_NAME=reservation_platform
export DJANGO_DB_USER=postgres
export DJANGO_DB_PASSWORD=yourpassword
export DJANGO_DB_HOST=localhost
export DJANGO_DB_PORT=5432
```

To create a driver or admin account: sign up as a passenger via the UI, then in `/django-admin/` edit the user's `role` field (or `is_superuser` for full admin access — the dashboard treats superusers as admins too).

## Project structure

```
config/                 settings, root urls, wsgi/asgi
apps/
  core/                 PlatformSettings (admin-tunable business rules), home routing
  accounts/              custom User (role: passenger/driver/admin), signup/login
  locations/             Location, DriverPosition, MapService abstraction (osm/google/mapbox)
  reservations/          Reservation, ReservationEvent (timeline), DelayRequest,
                         CancellationExceptionRequest + services/ (state_machine,
                         delay, no_show, cancellation) + tests/
  notifications/         Notification, WebPushSubscription, notify() service
  payments/               Transaction ledger + service functions (stubbed, auditable)
  disputes/               Dispute, DisputeAttachment + service
  admin_dashboard/        views-only app reading real counts (no fake metrics)
templates/                RTL Arabic templates, Tailwind + HTMX via CDN
```

## Design decisions / assumptions made without asking

- **Status changes only happen through `state_machine.transition()`.** Every view calls this (or a service that calls it) rather than setting `.status` directly, so the timeline can never drift from reality.
- **Waiting timer**: when a driver marks arrival, the waiting period is set to `PlatformSettings.max_waiting_minutes` from that moment. An accepted delay request extends `waiting_deadline` by the requested minutes rather than replacing it.
- **No-show gating** implements the exact checklists from your brief as `check_passenger_no_show_eligible` / `check_driver_no_show_eligible` — both return the list of failed conditions, which the UI shows instead of a bare "not allowed."
- **Passenger connectivity**: nothing in the no-show or state-machine logic depends on the passenger's browser being connected — eligibility is computed from server-recorded timestamps only, so a passenger who reconnects later still has an accurate picture waiting for them. There is no live WebSocket/polling layer yet in this phase; the passenger simply reloads the reservation page to see current state.
- **Reservation creation form** takes pickup/destination as a label + manually-entered lat/lng for this phase, since wiring an actual interactive map click-to-pick-point widget is a frontend task better done once you confirm the map provider (OSM/Google/Mapbox) via `MAP_PROVIDER`.
- **Financial logic** (apps/payments) is fully separated from reservation status — no view moves money directly. Functions exist for authorize/release/penalize/credit/refund/dispute-adjustment; they create real, auditable `Transaction` rows now, but no gateway call happens yet (per "do not implement real payment processing yet").
- **Web Push** is wired as a no-op until `WEBPUSH_VAPID_PUBLIC_KEY` / `WEBPUSH_VAPID_PRIVATE_KEY` are set and `pywebpush` is installed — the in-app `Notification` row is always created regardless, so nothing is lost by push not being configured yet.
- **Delay request expiry** (`delay.expire_stale_delay_requests()`) is written but not yet scheduled — call it from a periodic task (management command + cron, or Celery beat) once you pick a task runner; not added automatically to avoid guessing your infra.

## What's deliberately not built yet (per your Phase 1 scope)

- Real payment/deposit processor integration
- Real SMS
- Native mobile app
- Live map click-to-pick-point UI, live driver location updates, ETA via a real routing engine (the `MapService.estimate_route` is a great-circle placeholder until a routing engine is wired in)
- Scheduled/periodic jobs (delay expiry sweep, no-show reminder pings)

## Test coverage

`apps/reservations/tests/test_reservation_flow.py` covers: reservation creation, driver acceptance, valid/invalid/duplicate transitions, arrival + waiting timer start, passenger delay request + driver acceptance, driver delay request + passenger rejection, delay-response authorization, delay amount validation, passenger no-show (happy path + blocked before waiting elapses + blocked with an active accepted delay), driver no-show (happy path + blocked if already arrived), lock-period cancellation vs. free cancellation, unauthorized cancellation, financial transaction recording, notification creation, and dispute creation + authorization.
