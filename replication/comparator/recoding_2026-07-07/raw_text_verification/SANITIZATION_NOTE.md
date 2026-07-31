# Sanitization Note - Companion Copies (2026-07-08)

Before publication, path references in this directory's files were made repo-relative so that no
local absolute path prefixes ship. Two files (adjudication_record.json, r1_panel_agreements.json)
carry the placeholder <WORKING_REPO> in their text_path fields in place of the working-repository
prefix. Two others (verification_inputs_r1.json, verification_inputs_r2.json) retain historical
`case_texts/` source locators. Those locators are not live repository paths; the underlying texts
are on file with the author.

VERIFICATION_MANIFEST.json records SHA-256 values for the pre-publication working-repository
originals, so a recompute against the published copies in this directory will not reproduce those
hashes. The opinion-text stores referenced by `text_path` are not redistributed here; they are on
file with the author. Where a CourtListener cluster ID is embedded in a `source_file` name, the
corresponding public opinion can also be retrieved from CourtListener.
