# app.py
import streamlit as st
import pandas as pd

# Import helper modules (must be in the same folder)
# If you haven't created them yet, ask me and I'll send them.
try:
    from rubric_loader import load_rubric_from_excel
    from scorer import Scorer
except Exception as e:
    load_rubric_from_excel = None
    Scorer = None
    _IMPORT_ERROR = e

# Path to rubric file (change only if your Excel is at a different path)
RUBRIC_PATH = "Case study for interns.xlsx"   # keep the Excel in same folder as app.py

st.set_page_config(page_title="Nirmaan – Intro Scorer", layout="wide")
st.title("Nirmaan – Student Introduction Scoring Tool")

st.write(
    "Upload or paste a transcript to automatically evaluate it using the rubric from the Excel file. "
    "The system gives: Final Score, Per-criterion scoring, Feedback and raw JSON output."
)

# Layout: transcript input on left, options on right
col1, col2 = st.columns([3, 1])

with col1:
    transcript = st.text_area("Paste transcript here", height=300)
    uploaded = st.file_uploader("Or upload a .txt transcript", type=["txt"])
    if uploaded is not None:
        try:
            transcript = uploaded.read().decode("utf-8")
        except Exception:
            # fallback: try default decode
            transcript = uploaded.read().decode(errors="ignore")

with col2:
    audio_duration = st.number_input("Audio duration (seconds) — Optional", min_value=0, value=0, step=1)
    alpha = st.slider("Weight between rule vs semantic scoring (α)", 0.0, 1.0, 0.6, 0.05)
    st.markdown("**Notes:**\n- Ensure `Case study for interns.xlsx` is in same folder as this file.\n- If helper modules aren't present, scoring won't run.")

# Button action
if st.button("Score Transcript"):
    if not transcript or not transcript.strip():
        st.error("⚠ Please paste or upload a transcript first.")
    else:
        if load_rubric_from_excel is None or Scorer is None:
            st.error(
                "Required helper modules not found. "
                "Make sure `rubric_loader.py` and `scorer.py` are in the same folder as this file.\n\n"
                f"Import error: {_IMPORT_ERROR}"
            )
        else:
            # Try loading the rubric and scoring; handle errors so UI stays responsive
            try:
                with st.spinner("Loading rubric..."):
                    rubric = load_rubric_from_excel(RUBRIC_PATH)
                st.success(f"Loaded rubric with {len(rubric.get('criteria', []))} criteria.")
            except FileNotFoundError:
                st.error(f"Rubric Excel not found at `{RUBRIC_PATH}`. Please place the Excel file in the app folder or update RUBRIC_PATH.")
            except Exception as e:
                st.error(f"Error loading rubric: {e}")
            else:
                try:
                    scorer = Scorer(rubric=rubric, alpha=alpha,
                                    audio_duration_sec=audio_duration if audio_duration > 0 else None)
                    result = scorer.score_transcript(transcript)
                except Exception as e:
                    st.error(f"Error while scoring transcript: {e}")
                else:
                    st.success("Scoring complete")
                    st.header(f" Final Score: {result.get('final_score', 0):.1f} / 100")
                    st.write(
                        f"**Word Count:** {result.get('word_count', 0)}  |  "
                        f"**Unique Words:** {result.get('distinct_words', 0)}  |  "
                        f"**TTR:** {result.get('ttr', 0):.3f}"
                    )

                    st.subheader("🔹 Per-Criterion Breakdown")
                    try:
                        df = pd.DataFrame(result.get("per_criterion", []))
                        display_cols = [c for c in ["criterion", "weight", "score_out_of", "score_obtained",
                                                    "rule_score", "semantic_score", "feedback"] if c in df.columns]
                        st.dataframe(df[display_cols], use_container_width=True)
                    except Exception:
                        st.write("Could not display per-criterion table (unexpected format).")
                        st.json(result.get("per_criterion", []))

                    st.subheader("Feedback Summary")
                    for c in result.get("per_criterion", []):
                        crit_name = c.get("criterion", "Unnamed")
                        obtained = c.get("score_obtained", 0)
                        out_of = c.get("score_out_of", c.get("weight", 0))
                        st.markdown(f"**{crit_name} — {obtained:.1f}/{out_of:.1f}**")
                        st.write(c.get("feedback", ""))

                    st.subheader("Raw JSON Output")
                    st.json(result)
