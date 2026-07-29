# Notebooks

This directory contains exploratory assets preserved from the original repository.

## Purpose

The notebook remains part of the project for:

- historical provenance
- exploratory analysis
- reproducibility of the original proof of concept

It is not the production application.

## Contents

- `exploratory-job-market-analysis.ipynb`: original exploratory analysis, retained separately from the application runtime
- `helpers/exploratory_jobs.py`: reusable support functions extracted from notebook logic without introducing the full production package yet
- `requirements-exploration.txt`: minimal dependency list for rerunning the notebook flow

## Reproducibility Notes

- The notebook was originally executed with Python `3.7.6`.
- Install a Chrome browser and compatible ChromeDriver through the operating system, container image, or an automated driver manager before running the scraping cells.
- The notebook reflects the original exploratory workflow and historical source assumptions; it is not exercised by CI.
- Do not run the historical GeekHunter scraper without prior written authorization.
  [GeekHunter's current terms](https://www.geekhunter.com.br/pt/termos-de-uso) prohibit automated
  scraping or crawler tools without that authorization.
- The historical selectors and Selenium APIs are unvalidated and may no longer work.

## Boundary With Production Code

- exploratory helpers in this directory are not imported by the application
- production ingestion, normalization, enrichment, analytics, and API code lives under `src/`
- the production GeekHunter parser is retained for provenance and fixture-based parsing only; live
  GeekHunter retrieval is unsupported
