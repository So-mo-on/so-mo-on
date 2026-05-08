# 🧪 Your Flask Portfolio

A personal portfolio website built with Python + Flask.

## Project Structure

```
flask_portfolio/
│
├── app.py            ← Flask routes (don't need to edit often)
├── data.py           ← ⭐ YOUR CONTENT — edit this to update the site
├── analytics.py      ← ⭐ YOUR ANALYTICS FUNCTION — put your code here
├── requirements.txt  ← Python dependencies
│
└── templates/
    ├── base.html     ← Shared layout & navigation
    ├── index.html    ← CV / Home page
    ├── writing.html  ← Papers & Essays page
    └── analytics.html← Interactive analytics tool page
```

## Setup & Run

```bash
# 1. Install Flask (only needed once)
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open in browser
# http://127.0.0.1:5000
```

## How to Customize

### Update your personal info, CV, projects:
→ Edit `data.py` — it's just Python variables, no HTML needed.

### Add your analytics function:
→ Edit `analytics.py` — replace the body of `run()` with your code.

### Change colors or fonts:
→ Edit the `:root {}` CSS block in `templates/base.html`.

### Add a new page:
1. Add a route in `app.py`
2. Create a new template in `templates/`
3. Add a link in the `<nav>` in `base.html`
