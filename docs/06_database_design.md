# 06 - Database Design

## Overview

The Clinic CRM database is designed based on real-world clinic workflows rather than a simple appointment booking system.

The database must support:

- Multiple clinics (future SaaS support)
- Multiple staff roles
- Multiple operator skills
- Different service durations
- Shared rooms
- Shared devices
- Telegram reservations
- Website reservations
- Phone reservations
- Medical records
- Payments
- Future expansion without redesign

---

# Core Entities

## Clinic

Represents a clinic.

Examples:

- Taj Beauty Slim

---

## Staff

Represents every employee.

Examples

- Manager
- Secretary
- Doctor
- Operator
- Tattoo Artist
- Podiatrist
- Massage Therapist

A staff member may have multiple roles.

---

## Role

Examples

- Manager
- Secretary
- Doctor
- Operator

Relationship

Staff ↔ Role

Many-to-Many

---

## Skill

Represents professional abilities.

Examples

- Laser
- Cryolipolysis
- HIFU
- RF
- Carbon Peel
- Facial
- Podology

One staff member may have multiple skills.

One skill may belong to multiple staff members.

---

## Patient

Stores patient information.

Each patient has

- Main file number
- Multiple sub-file numbers
- Contact information
- Medical history

---

## Medical Record

Stores medical forms and treatment history.

One patient may have multiple medical records.

---

## Service

Represents clinic services.

Examples

- Laser Hair Removal
- Cryolipolysis
- HIFU
- Facial
- Carbon Peel
- PRP
- Botox

Each service contains

- Duration
- Base price
- Description
- Required skills
- Required room
- Required devices

---

## Room

Represents physical rooms.

Examples

- Laser Room
- Facial Room
- Cryo Room
- Doctor Room
- Massage Room

Rooms are resources.

Only one appointment may occupy the same room at the same time.

---

## Device

Represents clinic devices.

Examples

- HIFU
- Cryolipolysis
- RF
- Carbon
- Cavitation

Each device belongs to one room.

Devices may require cooldown time between appointments.

Devices may become unavailable due to maintenance.

---

## Appointment

Central entity of the system.

Appointment references

- Patient
- Service
- Staff
- Room
- Date
- Start Time
- End Time
- Status

Appointment status

- Requested
- Pending
- Confirmed
- Cancelled
- Completed
- No Show

Reservation sources

- Telegram Bot
- Website
- Phone
- Reception

---

## Schedule

Stores working schedules.

Supports

- Morning shift
- Evening shift
- Vacation
- Exceptions
- Holidays

---

## Payment

Supports

- Deposit
- Full payment
- Cash
- Card
- Online payment

Payment status

- Pending
- Paid
- Refunded

---

## Notification

Supports

- Telegram
- SMS
- Internal notification

---

# Booking Constraints

The booking engine must validate:

- Staff availability
- Room availability
- Device availability
- Required skills
- Appointment duration
- Cleaning interval
- Device cooldown interval

---

# Future Integrations

The database is designed to integrate with:

- Django REST Framework
- React
- Telegram Bot
- WordPress
- SMS Gateway
- Payment Gateway

---

# Design Principles

- Normalize database structure
- Avoid duplicated information
- Keep business logic outside models
- Support future expansion
- Suitable for production environments