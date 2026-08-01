# assets/

## `prospur-logo.png` (not included in this scaffold)

Per PLAYBOOK.md §1: the Prospur wordmark, 880×168 PNG with alpha. Drop the
real asset here before rendering any composition — `templates/*/assemble.py`
reference it by this exact filename for the sticky brand mark.

White-on-dark treatment is done in CSS, not a second file:

```css
.brand-mark--on-dark {
  filter: brightness(0) invert(1);
}
```

## `fonts/`

Inter (body) + Source Serif 4 (editorial). See `fonts/README.md`.
