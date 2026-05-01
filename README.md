# CAMPERappPLUS — prototipo

Gestione del proprio camper: scadenze + libretto digitale.

## Avvio rapido

```bash
cd CamperApp
.venv\Scripts\activate
streamlit run app.py
```

L'app si apre nel browser su http://localhost:8501

## Struttura

- `app.py` — UI Streamlit (3 pagine: camper, scadenze, libretto)
- `storage.py` — persistenza su `data/camper.json`
- `data/` — dati locali (creata automaticamente)

## Stop

Ctrl+C nel terminale che esegue Streamlit.
