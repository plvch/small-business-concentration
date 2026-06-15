# It's rational to ignore small business

A short data note on why Germany's fiscal neglect of small businesses is — by the
numbers — rational, and where a fix might actually come from.

**Read it:** https://plvch.github.io/small-business-concentration/

Built in the same design language as [open-indexing](https://github.com/plvch/open-indexing)
and [indexes_cost](https://github.com/plvch/indexes_cost) (shared `assets/plvch-tokens.css`,
light/dark themes).

## What's here

- `index.html` — the published post (static, no dependencies). Generated.
- `build_site.py` — rebuilds `index.html`: reuses the shared CSS + theme toggle,
  drops in the prose, and renders the two charts as inline SVG / tables from the
  data in `data/`.
- `assets/plvch-tokens.css` — the shared plvch design tokens.
- `data/` — the derived tables behind the figures (from the underlying Destatis /
  Eurostat / CompNet analysis).

## Regenerate

```sh
python3 build_site.py        # -> index.html
```

## Figures & sources

- **Figure 1 — concentration.** Lorenz curves of corporate turnover vs personal
  income. Destatis Umsatzsteuerstatistik (73321-0004, 2021) and Lohn- u.
  Einkommensteuerstatistik (73111-0005, 2022). Turnover Gini ≈ 0.96 (grouped
  estimate); personal income Gini ≈ 0.49 (Gesamtbetrag der Einkünfte, pre-tax).
- **Figure 2 — Germany vs Europe.** Aggregate HHI by country from IWH/CompNet
  (2021); cross-country turnover Gini computed from Eurostat SBS (`sbs_sc_ovw`, 2023).

Numbers span 2021–2023 source years. The personal disposable-income Gini cited in
discussion (~0.28) is Eurostat SILC `ilc_di12`, a different concept from the
taxpayer-gross Gini shown here.
