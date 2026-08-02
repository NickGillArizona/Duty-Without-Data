---
layout: default
title: "Accessibility"
permalink: /accessibility/
description: "The accessibility commitment for the Duty Without Data site and repository: what is tested automatically, what is not yet tested, and how to report a barrier."
---

# Accessibility

What this site and repository do for accessibility, what is tested, what is not yet tested, and
how to report a barrier.

This archive is about disability rights, so its pages must stay usable with assistive technology.
Anything hard to use through a screen reader is a bug — report it and it will be treated as one.

## What the site does

- Semantic landmarks (`header`, `nav`, `main`, `footer`), a skip-to-content link, and visible
  keyboard focus on every interactive element.
- No JavaScript anywhere on the site; nothing requires a pointer, and no content moves or
  updates on its own.
- Light and dark presentation follow your system preference, with text contrast chosen for
  WCAG AA in both.
- Body text uses relative units and a capped line length; content reflows at 200% zoom without
  horizontal scrolling.
- Figures ship with substantive alternative text, and the repository carries written text
  equivalents and data alternatives alongside every diagram and chart.

## What is tested automatically

The repository's release gate includes a deterministic accessibility contract that runs on every
change. It requires substantive alt text on images, a written text equivalent after every
diagram, heading levels that descend one at a time, tables that open with an associated header
row, and link text that says where the link goes. What that contract does and does not establish
is documented in
[the release gate's description](https://github.com/NickGillArizona/Duty-Without-Data/blob/main/replication/GATES.md).

## What is not yet tested

Honesty about the boundary: the automated contract checks structure, not experience. As of this
site's redesign, no full manual screen-reader pass and no assistive-technology user testing have
been completed on the rendered site, and automated checks cannot certify WCAG conformance. A
manual keyboard and screen-reader review is the standing next step; this page will state the
result when it exists.

## Report a barrier

- [Open an issue](https://github.com/NickGillArizona/Duty-Without-Data/issues) describing the
  page and the barrier, or
- email [nickgill@arizona.edu](mailto:nickgill@arizona.edu).

Reports about access barriers are treated as defects, not requests.
