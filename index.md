---
layout: default
title: Duty Without Data
description: "A law-review project on record-dependent disability fair-housing rights, the evidence behind the argument, and a bounded administrative response."
page_class: landing-page
---

<div class="landing">
  <section class="landing-hero" aria-labelledby="page-title">
    <div class="landing-shell">
      <p class="eyebrow">Forthcoming · Arizona Law Review · 2026</p>
      <h1 id="page-title">Duty Without Data</h1>
      <p class="hero-lead">A disability fair-housing right can exist in law and still become difficult to administer or prove when the facts that give it force do not travel from one decision to the next.</p>
      <div class="hero-lower">
        <div class="hero-meta">
          <p class="byline"><strong>Nicholas Gill</strong><br>J.D. candidate, Class of 2027<br>University of Arizona James E. Rogers College of Law</p>
          <div class="button-row" aria-label="Primary reading options">
            <a class="button button-primary" href="https://nickgillarizona.github.io/Duty-Without-Data/argument/">Read the argument</a>
            <a class="button" href="https://nickgillarizona.github.io/Duty-Without-Data/download-and-cite/">Read the manuscript</a>
          </div>
        </div>
        <p class="hero-deck">The evidence runs on three legs: doctrine, HUD’s own administrative record, and an original census of 606 decided cases. The response is a bounded rulemaking petition — preserve the records existing duties already presuppose, hand the tenant a copy, make HUD explain its choices.</p>
      </div>
    </div>
  </section>

  <!-- claim-block: census-headline -->
  <section class="headline-findings" aria-labelledby="headline-findings-title">
    <div class="landing-shell band-grid">
      <div class="band-intro">
        <p class="eyebrow">A descriptive census, not a causal estimate</p>
        <h2 id="headline-findings-title">Rare, counseled, and never pro se</h2>
        <p>Qualifying plaintiff-side judgments issued eighteen times in four and a half years.</p>
      </div>
      <div class="band-ledger">
        <div class="proof-grid">
          <div class="proof-card">
            <p class="proof-value">606 decided cases</p>
            <p>identified from 1,900 screened federal disability fair-housing opinion and order records, collapsed to one case-level unit.</p>
          </div>
          <div class="proof-card">
            <p class="proof-value">eighteen qualifying plaintiff-side judgments</p>
            <p>18/606 (3.0%) of decided cases.</p>
          </div>
          <div class="proof-card">
            <p class="proof-value">none of the 400 pro se cases</p>
            <p>produced a qualifying judgment. Across the same window, the pro se share of the decided docket rose from 59.6% to 76.1%.</p>
          </div>
        </div>
        <p class="finding-caveat">These figures describe the captured federal opinion-bearing docket. They do not establish causation, measure all fair-housing disputes, or show that missing records determined any individual result.</p>
      </div>
    </div>
  </section>
  <!-- /claim-block -->

  <section class="figure-band" aria-label="Figure 1">
    <div class="landing-shell">
      <figure class="figure-plate">
        <div class="exhibit">
          <picture>
            <source media="screen and (prefers-color-scheme: dark) and (max-width: 600px)" srcset="https://nickgillarizona.github.io/Duty-Without-Data/assets/figures/fig1_composition_mobile_dark.svg">
            <source media="screen and (max-width: 600px)" srcset="https://nickgillarizona.github.io/Duty-Without-Data/assets/figures/fig1_composition_mobile_light.svg">
            <source media="screen and (prefers-color-scheme: dark)" srcset="https://nickgillarizona.github.io/Duty-Without-Data/assets/figures/fig1_composition_dark.svg">
            <img src="https://nickgillarizona.github.io/Duty-Without-Data/assets/figures/fig1_composition_light.svg" width="980" height="627" alt="Line chart of the decided federal disability fair-housing docket across three periods: the pro se share rises from 59.6% to 76.1% while the qualifying-judgment rate stays low and flat — eighteen qualifying plaintiff-side judgments in all, none pro se, every one counseled.">
          </picture>
        </div>
        <figcaption class="figure-caption"><span class="figure-label">Figure 1.</span><span>Who files, and who wins: the top line is the pro se share of the decided docket; the bottom line is the qualifying-judgment rate. Every qualifying judgment sits on the counseled side of the gap. <a href="https://nickgillarizona.github.io/Duty-Without-Data/evidence-and-limits/">Examine the findings and their limits.</a></span></figcaption>
      </figure>
    </div>
  </section>

  {% if site.comment_window_active %}
  <aside class="current-note" aria-label="Dated public-comment material">
    <div class="landing-shell current-note-inner">
      <p><strong>Dated material.</strong> HUD’s Form HUD-27061 renewal is open for public comment; comments are due <time datetime="2026-08-11">August 11, 2026</time>. <a href="https://nickgillarizona.github.io/Duty-Without-Data/comment/">Read the comment guide and verify the live docket before filing.</a></p>
    </div>
  </aside>
  {% endif %}

  <section class="landing-section" aria-labelledby="ely-title">
    <div class="landing-shell narrative-grid">
      <div class="section-intro">
        <p class="eyebrow">A case that exposes the gap</p>
        <h2 id="ely-title">A right can fail between two decisions</h2>
      </div>
      <div class="reading-column">
        <p>In 2010, the Mobile Housing Board issued Donavette Ely a larger Section 8 voucher because her son’s asthma called for a bedroom with its own temperature controls — the Board’s own written explanation tied the voucher to his medical condition. When Ely could not find a qualifying unit in time and asked for more time to search, the Board refused, and later removed the family from the program.</p>
        <p>The Eleventh Circuit held the Board could not be liable, because Ely “never explained” that her extension request was connected to her son’s disability. <cite>Ely v. Mobile Housing Board</cite>, 605 F. App’x 846, 851–52 (11th Cir. 2015).</p>
        <p class="pull-quote">The record existed. The link did not.</p>
        <p><cite>Ely</cite> predates the census window; it is the illustration, not a data point. And it does not prove a different record system would have changed the outcome. It shows something narrower: an institution can hold the decisive fact at one stage and fail to carry it to the next — and the tenant pays for the gap.</p>
      </div>
    </div>
  </section>

  <section class="landing-section" aria-labelledby="method-title">
    <div class="landing-shell narrative-grid">
      <div class="section-intro">
        <p class="eyebrow">The research instrument</p>
        <h2 id="method-title">Built to be checked, not trusted</h2>
      </div>
      <div class="reading-column">
        <p>The dataset behind the census did not exist before this project. Several separately run AI models from different providers each read every opinion and answered the same fixed questions under frozen prompts; disagreements escalated to a designated adjudication model under rules set in advance, and the headline finding was re-examined by a separate ensemble from a different vendor, audited blind. The author designed the questions, set the rules, and made the legal and interpretive judgments; the models classified.</p>
        <p>The instrument ships with its calibration data:</p>
        <ul class="artifact-list">
          <li><strong>Frozen prompts</strong> — the questions, fixed before reading began.</li>
          <li><strong>Adjudication rules</strong> — set in advance, with every disagreement record published.</li>
          <li><strong>Claims ledger</strong> — every printed number tied to the script that produced it.</li>
          <li><strong>Release gate</strong> — numbers, links, figures, and the accessibility contract re-checked on every change, stating plainly what a green run does not establish.</li>
        </ul>
        <p><a href="https://nickgillarizona.github.io/Duty-Without-Data/methods-and-replication/">Inspect the method and replication materials.</a></p>
      </div>
    </div>
  </section>

  <section class="landing-section response-section" aria-labelledby="response-title">
    <div class="landing-shell response-grid">
      <div class="section-intro">
        <p class="eyebrow">The response</p>
        <h2 id="response-title">A bounded petition for the records existing duties already presuppose</h2>
        <p>Congress gave HUD express data-collection rulemaking authority in 1988, and HUD’s own regulation has named disability-related data categories since 1989 — yet no identified coordinated federal system reliably collects, links, or makes those records accessible. <a href="https://nickgillarizona.github.io/Duty-Without-Data/administrative-record/">Trace the statutes, notices, and forms.</a></p>
      </div>
      <div class="response-body">
        <div class="response-main">
          <p>The administrative record sharpens the ask. In 2022, HUD proposed collecting protected-class data; the 2023 approved form collected race and ethnicity only, with no explanation in the located public record; in June 2026, HUD proposed renewing the narrowed form unchanged.</p>
          <ul class="module-list">
            <li><strong>Transaction receipts.</strong> A minimally sufficient record of a disability-related request, response, timing, and disposition — with a contemporaneous copy to the requester.</li>
            <li><strong>Accessible-unit inventories.</strong> Source-, standard-, and date-specific asset records suited to the housing program in which the duty arises.</li>
            <li><strong>Aggregate visibility.</strong> Suppressed, diagnosis-free reporting fields tied to HUD’s separate statutory oversight authority.</li>
          </ul>
          <p>The vehicle is a modular petition under 5 U.S.C. § 553(e), which obligates HUD to answer and to state its grounds. If HUD denies it, the legal object is a reasoned agency decision, reviewable under <cite>Massachusetts v. EPA</cite>, 549 U.S. 497, 527–28 (2007).</p>
          <p>The remedy for an unreasoned denial is remand for explanation, not judicial database design.</p>
          <p><a href="https://nickgillarizona.github.io/Duty-Without-Data/argument/">Read the full doctrinal route and the principal objections.</a></p>
        </div>
        <aside class="response-rail" aria-label="Limiting principle">
          <div class="limiting-principle">
            <p class="panel-label">Limiting principle</p>
            <p><strong>Verification without substantive expansion.</strong> The proposal would not alter a liability standard, require a claimant to use prescribed language, create a diagnosis registry, publish tenant-to-unit matches, or ask a court to design a federal database.</p>
          </div>
        </aside>
      </div>
    </div>
  </section>

  <section class="landing-section route-section" aria-labelledby="routes-title">
    <div class="landing-shell">
      <div class="section-intro">
        <p class="eyebrow">Use the project at the depth you need</p>
        <h2 id="routes-title">Choose a route</h2>
      </div>
      <ul class="route-list">
        <li>
          <a href="https://nickgillarizona.github.io/Duty-Without-Data/argument/"><span class="route-kicker">Attorneys and judges</span><strong>Assess the legal theory</strong><span>Record-dependence, statutory authority, the petition vehicle, reviewability, and the limiting principles.</span></a>
        </li>
        <li>
          <a href="https://nickgillarizona.github.io/Duty-Without-Data/evidence-and-limits/"><span class="route-kicker">Skeptical readers</span><strong>Test the empirical claims</strong><span>What the census supports, what it does not, and where judgment rather than mechanical verification enters.</span></a>
        </li>
        <li>
          <a href="https://nickgillarizona.github.io/Duty-Without-Data/methods-and-replication/"><span class="route-kicker">Researchers</span><strong>Reproduce the analysis</strong><span>The study design, frozen prompts, adjudication rules, claim mappings, and runnable materials.</span></a>
        </li>
        <li>
          <a href="https://nickgillarizona.github.io/Duty-Without-Data/download-and-cite/"><span class="route-kicker">Editors and cite-checkers</span><strong>Read, cite, or reuse</strong><span>The manuscript, fixed releases, citation forms, licensing terms, and correction channels.</span></a>
        </li>
      </ul>
    </div>
  </section>

  <section class="landing-section about-section" aria-labelledby="about-title">
    <div class="landing-shell about-grid">
      <div class="section-intro">
        <h2 id="about-title">Authorship and access</h2>
      </div>
      <div class="reading-column">
        <p><strong>Nicholas Gill</strong> assembled the administrative record, designed the empirical study, and built the claim-to-source and reproduction materials accompanying the forthcoming Note. He reviewed and approved the public work and is responsible for it; the AI-use statement details the models’ roles and limits.</p>
        <p>The project argues that disability rights depend on records that reach people — and its own pages are built the same way: semantic HTML, no scripts, WCAG AA contrast targets, and an automated accessibility contract on every change, with the not-yet-tested parts stated rather than papered over. If any page is hard to use with assistive technology, that is a bug; report it.</p>
        <p><a href="https://github.com/NickGillArizona/Duty-Without-Data/blob/main/AI_USE.md">Read the AI-use statement</a> · <a href="https://nickgillarizona.github.io/Duty-Without-Data/accessibility/">Accessibility</a> · <a href="mailto:nickgill@arizona.edu">Contact Nicholas Gill</a></p>
      </div>
    </div>
  </section>
</div>
