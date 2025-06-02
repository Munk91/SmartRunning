# Test and Debug the Route Generator

Check that:

- Invalid locations are handled gracefully
- No route found → user sees a friendly error
- Folium map is embedded correctly in Streamlit
- Surface filtering works (some edges may not have `surface` tags — handle that)
- Loop routes are approximately the right distance

Add logging or Streamlit `st.write()` for debugging if needed.
