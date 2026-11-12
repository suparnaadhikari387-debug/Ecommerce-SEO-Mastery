
import streamlit as st
import pandas as pd

from seo_analyzer import (
    audit_website,
    analyze_product,
    keyword_ideas
)

st.set_page_config(
    page_title="Ecommerce SEO Mastery",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Ecommerce SEO Mastery")
st.subheader("Your Ecommerce SEO Analysis Dashboard")

menu = st.sidebar.selectbox(
    "Choose a Tool",
    [
        "Dashboard",
        "Website SEO Audit",
        "Product SEO Analyzer",
        "Keyword Research",
        "About Project"
    ]
)

if menu == "Dashboard":

    st.header("Welcome to SEO Mastery")

    col1, col2, col3 = st.columns(3)

    col1.metric("SEO Tools", "3")
    col2.metric("Analysis Type", "On-Page SEO")
    col3.metric("Reports", "CSV")

    st.info(
        "Analyze websites, optimize product pages "
        "and discover keyword ideas."
    )

    st.write("### Available Features")

    st.write("1. Website SEO Audit")
    st.write("2. Product SEO Analyzer")
    st.write("3. Keyword Research")
    st.write("4. SEO Recommendations")

elif menu == "Website SEO Audit":

    st.header("Website SEO Audit")

    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com"
    )

    if st.button("Analyze Website"):

        if url:

            with st.spinner("Analyzing website..."):

                result = audit_website(url)

            if "error" in result:

                st.error(result["error"])

            else:

                st.metric(
                    "SEO Score",
                    f'{result["score"]}/100'
                )

                st.write("### Website Analysis")

                st.write("Title:", result["title"])
                st.write("Meta Description:", result["description"])
                st.write("H1 Headings:", result["h1"])
                st.write("H2 Headings:", result["h2"])
                st.write("Images Missing ALT:", result["missing_alt"])
                st.write("Word Count:", result["word_count"])

                st.write("### Recommendations")

                for item in result["recommendations"]:
                    st.warning(item)

                report = pd.DataFrame([result])

                st.download_button(
                    "Download SEO Report",
                    report.to_csv(index=False),
                    "seo_report.csv",
                    "text/csv"
                )

        else:
            st.warning("Please enter a website URL.")

elif menu == "Product SEO Analyzer":

    st.header("Product SEO Analyzer")

    title = st.text_input("Product SEO Title")

    description = st.text_area(
        "Meta Description"
    )

    keyword = st.text_input("Target Keyword")

    if st.button("Analyze Product"):

        score, suggestions = analyze_product(
            title,
            description,
            keyword
        )

        st.metric("Product SEO Score", f"{score}/100")

        st.write("### Suggestions")

        for item in suggestions:
            st.warning(item)

        if not suggestions:
            st.success("Your basic product SEO checks look good!")

elif menu == "Keyword Research":

    st.header("Keyword Research Tool")

    keyword = st.text_input("Enter Main Keyword")

    if st.button("Generate Keywords"):

        if keyword:

            ideas = keyword_ideas(keyword)

            df = pd.DataFrame(
                ideas,
                columns=["Keyword Ideas"]
            )

            st.dataframe(df, use_container_width=True)

            st.download_button(
                "Download Keywords",
                df.to_csv(index=False),
                "keyword_ideas.csv",
                "text/csv"
            )

        else:
            st.warning("Enter a keyword.")

else:

    st.header("About Ecommerce SEO Mastery")

    st.write("""
    Ecommerce SEO Mastery is a digital marketing project
    developed using Python and Streamlit.

    It helps users understand website optimization,
    product SEO and keyword research.

    Technologies:
    - Python
    - Streamlit
    - Pandas
    - BeautifulSoup
    - Requests
    """)
