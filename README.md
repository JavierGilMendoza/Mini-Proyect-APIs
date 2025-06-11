# La Quiniela Results API

This project provides a RESTful API for querying historical results from La Quiniela, covering seasons from 1993/1994 to the present.

## Goals

- Clean and unify raw historical football data
- Develop a REST API (using FastAPI) to expose this data
- Prepare the dataset for training a future AI prediction model

## Project Structure

- `/data`: contains raw, cleaned, and unified CSV files
- `/scripts`: data preprocessing and transformation scripts
- `/api`: source code of the REST API
- `/notebooks`: exploratory notebooks and initial analysis

## Setup

Install dependencies with:

```bash
pip install -r requirements.txt
