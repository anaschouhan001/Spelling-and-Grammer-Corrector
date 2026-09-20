# Grammar & Spell Checker

A small Flask web app that cleans up text in two passes: spelling first with
[TextBlob](https://textblob.readthedocs.io/), then grammar with the
[`prithivida/grammar_error_correcter_v1`](https://huggingface.co/prithivida/grammar_error_correcter_v1)
seq2seq model from Hugging Face. You can paste text into the page or upload a
plain-text file, and both the spelling-corrected and grammar-corrected versions
are shown side by side.

## How it works

`SpellCheckerModule` in `Model.py` wraps the two stages:

- `correct_spell(text)` — splits the input on whitespace and runs
  `TextBlob(word).correct()` on each word.
- `correct_grammar(text)` — prefixes the input with `gec: `, encodes it with the
  model's tokenizer, and generates a correction with beam search
  (`num_beams=5`, `max_length=128`, `no_repeat_ngram_size=2`).

`app.py` exposes them over HTTP:

| Route | Method | Input | Renders |
| --- | --- | --- | --- |
| `/` | GET | — | the empty form |
| `/spell` | POST | form field `text` | `corrected_text`, `corrected_grammar_text` |
| `/grammar` | POST | file upload `file` | `corrected_file_text`, `corrected_file_grammar_text` |

Both POST routes run the spelling pass first and feed its output into the
grammar pass. `templates/index.html` is the single Bootstrap 5 page that holds
both forms and the result boxes.

## Requirements

- Python 3.10
- The packages pinned in `requirements.txt` (Flask, transformers, torch,
  textblob, and their dependencies)

## Running locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows; use: source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python -m textblob.download_corpora
python app.py
```

Then open http://127.0.0.1:5000.

The first run downloads the grammar model (a few hundred MB) from Hugging Face
and caches it locally, so expect a delay before the app is usable.

> `requirements.txt` is saved as UTF-16. If `pip install -r` fails to parse it,
> re-save the file as UTF-8 first.

## Running with Docker

```bash
docker build -t grammar-checker .
docker run -p 5000:5000 grammar-checker
```

The image installs the dependencies directly rather than from
`requirements.txt` and downloads the TextBlob corpora at build time. Note that
`app.py` starts Flask with `debug=True` and the default host, so the container
only serves `127.0.0.1` inside itself — change the `app.run(...)` call to
`app.run(host="0.0.0.0")` to reach it from the host.

## Trying the model without the web app

`Model.py` has a `__main__` block that runs a sample sentence through both
stages:

```bash
python Model.py
```

## Files

| Path | What it is |
| --- | --- |
| `app.py` | Flask routes |
| `Model.py` | spelling + grammar correction module |
| `templates/index.html` | the UI |
| `index.html` | a copy of the template at the project root |
| `example.txt` | sample messy text for the file-upload form |
| `Dockerfile` | container build for the app |
| `Dockerfile.test` | scratch image that only copies the template |
| `requirements.txt` | pinned dependencies (UTF-16 encoded) |

## Known limitations

- Spelling correction runs word-by-word, so TextBlob has no sentence context and
  will occasionally "correct" a correct but uncommon word.
- Grammar correction is capped at 128 tokens, so long uploads are truncated
  rather than processed paragraph by paragraph.
- File uploads are decoded as UTF-8 with `errors="ignore"`; binary files will
  produce garbage rather than an error.
