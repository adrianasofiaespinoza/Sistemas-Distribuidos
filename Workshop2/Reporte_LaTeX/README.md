# Workshop 2 LaTeX Report

This directory contains the final academic report for **Workshop 2:
Communication (Messaging and Message Queuing)** in the Distributed Systems
course at Yachay Tech University.

## Contents

- `main.tex`: English academic report source.
- `main.pdf`: Compiled final report.
- `generate_figures.py`: Script used to regenerate architecture diagrams and
  execution-evidence screenshots.
- `figures/`: Report figures:
  - `arch_rmi.png`
  - `arch_pubsub.png`
  - `arch_pipeline.png`
  - `screenshot_activity1_rmi_example.png`
  - `screenshot_activity2_matrix_manager.png`
  - `screenshot_activity3_pubsub_example.png`
  - `screenshot_activity4_multi_pubsub.png`
  - `screenshot_activity5_pipeline_example.png`
  - `screenshot_activity6_broker_pipeline.png`

## Report Scope

The report explicitly covers:

- Activities 1, 3, and 5 as review and example-testing activities, each with
  its own section and screenshot.
- Activities 2, 4, and 6 as the implemented deliverables, each with code
  discussion, validation results, and screenshots.

## Rebuild

```bash
python generate_figures.py
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
