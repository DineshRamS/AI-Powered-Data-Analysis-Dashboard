
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="AI-Powered Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Data Analysis Dashboard")
st.write("Interactive e-commerce sales analytics dashboard")

# File upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Load dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Convert date column if available
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(
            df['order_date'],
            errors='coerce'
        )

    st.success("Dataset uploaded successfully!")

# Sidebar Navigation
    st.sidebar.header("📌 Dashboard Navigation")

    section = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Visualizations",
            "AI Insights",
            "Anomaly Detection",
            "Business Recommendations",
            "Report"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.write("### Dataset Information")
    st.sidebar.write(f"Rows: {len(df):,}")
    st.sidebar.write(f"Columns: {len(df.columns):,}")

    if 'revenue' in df.columns:
        st.sidebar.write(
            f"Revenue: ₹{df['revenue'].sum():,.2f}"
        )

    st.sidebar.success("Dataset loaded successfully")

    # KPI calculations used by multiple dashboard sections
    total_revenue = df['revenue'].sum() if 'revenue' in df.columns else 0
    total_orders = df['order_id'].nunique() if 'order_id' in df.columns else len(df)
    average_revenue = df['revenue'].mean() if 'revenue' in df.columns else 0
    average_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 0
    total_quantity = df['quantity'].sum() if 'quantity' in df.columns else 0

    if section == "Overview":

    # Dataset overview
        st.subheader("Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Rows", f"{len(df):,}")

        with col2:
            st.metric("Total Columns", f"{len(df.columns):,}")

        with col3:
            st.metric(
                "Missing Values",
                f"{df.isnull().sum().sum():,}"
            )

        st.dataframe(df, use_container_width=True)

        # KPI calculations
        total_revenue = df['revenue'].sum() if 'revenue' in df.columns else 0
        total_orders = df['order_id'].nunique() if 'order_id' in df.columns else len(df)
        average_revenue = df['revenue'].mean() if 'revenue' in df.columns else 0
        average_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else 0
        total_quantity = df['quantity'].sum() if 'quantity' in df.columns else 0

        st.subheader("Key Performance Indicators")

        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        with kpi1:
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}")

        with kpi2:
            st.metric("Total Orders", f"{total_orders:,}")

        with kpi3:
            st.metric("Avg Order Revenue", f"₹{average_revenue:,.2f}")

        with kpi4:
            st.metric("Avg Customer Rating", f"{average_rating:.2f} / 5")

        with kpi5:
            st.metric("Total Quantity", f"{total_quantity:,}")
    # Data Quality & Preprocessing
        st.subheader("🧹 Data Quality & Preprocessing")

        duplicate_count = int(df.duplicated().sum())
        missing_count = int(df.isnull().sum().sum())

        quality_col1, quality_col2 = st.columns(2)

        with quality_col1:
            st.metric(
                "Duplicate Rows",
                f"{duplicate_count:,}"
            )

        with quality_col2:
            st.metric(
                "Missing Values",
                f"{missing_count:,}"
            )

        if duplicate_count == 0 and missing_count == 0:
            st.success(
                "✅ Dataset quality check passed. "
                "No duplicate rows or missing values detected."
            )
        else:
            st.warning(
                "⚠️ Dataset contains missing values or duplicate rows."
            )

        st.write("### Column Data Types")

        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(
            dtype_df,
            use_container_width=True
        )

        st.write("### Statistical Summary")

        numeric_summary = df.select_dtypes(include="number").describe().transpose()

        if not numeric_summary.empty:
            st.write("Numerical Columns")
            st.dataframe(
                numeric_summary,
                use_container_width=True
            )

        categorical_columns = df.select_dtypes(include="object").columns

        if len(categorical_columns) > 0:
            st.write("Categorical Columns")
            categorical_summary = pd.DataFrame({
                "Column": categorical_columns,
                "Unique Values": [
                    df[column].nunique()
                    for column in categorical_columns
                ],
                "Most Common Value": [
                    df[column].mode().iloc[0]
                    if not df[column].mode().empty
                    else "N/A"
                    for column in categorical_columns
                ]
            })

            st.dataframe(
                categorical_summary,
                use_container_width=True
            )

    elif section == "Visualizations":

    # Interactive Visualization
        st.subheader("Interactive Visualization")

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Pie Chart",
                "Histogram",
                "Scatter Plot"
            ]
        )

        # Prepare column lists for chart controls
        numeric_columns = [
            column
            for column in df.select_dtypes(include=np.number).columns
            if column not in ["order_id", "customer_id"]
        ]

        categorical_columns = [
            column
            for column in df.select_dtypes(
                include=["object", "category", "bool"]
            ).columns
            if column not in ["order_id", "customer_id"]
        ]

        all_columns = df.columns.tolist()

        if chart_type == "Bar Chart":

            if categorical_columns and numeric_columns:

                category_default = (
                    categorical_columns.index("product_category")
                    if "product_category" in categorical_columns
                    else 0
                )

                revenue_default = (
                    numeric_columns.index("revenue")
                    if "revenue" in numeric_columns
                    else 0
                )

                category_column = st.selectbox(
                    "Select Category Column",
                    categorical_columns,
                    index=category_default,
                    key="bar_category"
                )

                value_column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns,
                    index=revenue_default,
                    key="bar_value"
                )

                chart_data = (
                    df.groupby(
                        category_column,
                        dropna=False
                    )[value_column]
                    .sum()
                    .reset_index()
                    .sort_values(
                        value_column,
                        ascending=False
                    )
                )

                fig = px.bar(
                    chart_data,
                    x=category_column,
                    y=value_column,
                    title=f"{value_column} by {category_column}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning(
                    "The dataset needs at least one categorical column "
                    "and one numerical column for a bar chart."
                )

        elif chart_type == "Line Chart":

            date_columns = df.select_dtypes(
                include=["datetime64[ns]"]
            ).columns.tolist()

            if date_columns and numeric_columns:

                date_default = (
                    date_columns.index("order_date")
                    if "order_date" in date_columns
                    else 0
                )

                value_default = (
                    numeric_columns.index("revenue")
                    if "revenue" in numeric_columns
                    else 0
                )

                date_column = st.selectbox(
                    "Select Date Column",
                    date_columns,
                    index=date_default,
                    key="line_date"
                )

                value_column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns,
                    index=value_default,
                    key="line_value"
                )

                chart_data = (
                    df.dropna(subset=[date_column])
                    .groupby(
                        pd.Grouper(
                            key=date_column,
                            freq="ME"
                        )
                    )[value_column]
                    .sum()
                    .reset_index()
                )

                fig = px.line(
                    chart_data,
                    x=date_column,
                    y=value_column,
                    markers=True,
                    title=f"Monthly {value_column} Trend"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning(
                    "The dataset needs at least one date column "
                    "and one numerical column for the line chart."
                )

        elif chart_type == "Pie Chart":

            if categorical_columns and numeric_columns:

                category_default = (
                    categorical_columns.index("product_category")
                    if "product_category" in categorical_columns
                    else 0
                )

                value_default = (
                    numeric_columns.index("revenue")
                    if "revenue" in numeric_columns
                    else 0
                )

                category_column = st.selectbox(
                    "Select Category Column",
                    categorical_columns,
                    index=category_default,
                    key="pie_category"
                )

                value_column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns,
                    index=value_default,
                    key="pie_value"
                )

                chart_data = (
                    df.groupby(
                        category_column,
                        dropna=False
                    )[value_column]
                    .sum()
                    .reset_index()
                )

                fig = px.pie(
                    chart_data,
                    names=category_column,
                    values=value_column,
                    title=f"{value_column} Distribution"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning(
                    "The dataset needs at least one categorical column "
                    "and one numerical column for a pie chart."
                )

        elif chart_type == "Histogram":

            if numeric_columns:

                value_default = (
                    numeric_columns.index("revenue")
                    if "revenue" in numeric_columns
                    else 0
                )

                value_column = st.selectbox(
                    "Select Numerical Column",
                    numeric_columns,
                    index=value_default,
                    key="hist_value"
                )

                fig = px.histogram(
                    df,
                    x=value_column,
                    nbins=30,
                    title=f"Distribution of {value_column}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning(
                    "No numerical columns are available for the histogram."
                )

        elif chart_type == "Scatter Plot":

            if len(numeric_columns) >= 2:

                x_default = (
                    numeric_columns.index("unit_price")
                    if "unit_price" in numeric_columns
                    else 0
                )

                y_default = (
                    numeric_columns.index("revenue")
                    if "revenue" in numeric_columns
                    else 1
                )

                x_column = st.selectbox(
                    "Select X-Axis Column",
                    numeric_columns,
                    index=x_default,
                    key="scatter_x"
                )

                y_column = st.selectbox(
                    "Select Y-Axis Column",
                    numeric_columns,
                    index=y_default,
                    key="scatter_y"
                )

                fig = px.scatter(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} vs {x_column}"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.warning(
                    "At least two numerical columns are required "
                    "for a scatter plot."
                )

        # Correlation Heatmap
        st.subheader("Correlation Heatmap")

        numeric_columns = df.select_dtypes(include="number").columns

        if len(numeric_columns) >= 2:

            correlation_matrix = df[numeric_columns].corr()

            fig = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                aspect="auto",
                title="Numerical Feature Correlation"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Not enough numerical columns for a correlation heatmap.")

        # Dataset Filtering and Search
        st.subheader("🔎 Search & Filter Data")

        filter_column = st.selectbox(
            "Select Column to Filter",
            all_columns,
            key="filter_column"
        )

        if pd.api.types.is_datetime64_any_dtype(df[filter_column]):

            valid_dates = df[filter_column].dropna()

            if valid_dates.empty:
                filtered_df = df
            else:
                min_date = valid_dates.min().date()
                max_date = valid_dates.max().date()

                selected_dates = st.date_input(
                    f"Select {filter_column} range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="date_filter"
                )

                if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
                    start_date, end_date = selected_dates

                    filtered_df = df[
                        df[filter_column].dt.date.between(
                            start_date,
                            end_date
                        )
                    ]
                else:
                    filtered_df = df

        elif pd.api.types.is_numeric_dtype(df[filter_column]):

            valid_values = df[filter_column].dropna()

            if valid_values.empty:
                filtered_df = df
            else:
                min_value = float(valid_values.min())
                max_value = float(valid_values.max())

                if min_value == max_value:
                    st.info(
                        f"All values in {filter_column} are {min_value}."
                    )
                    filtered_df = df
                else:
                    filter_range = st.slider(
                        f"Select {filter_column} range",
                        min_value=min_value,
                        max_value=max_value,
                        value=(min_value, max_value),
                        key="filter_range"
                    )

                    filtered_df = df[
                        df[filter_column].between(
                            filter_range[0],
                            filter_range[1]
                        )
                    ]

        else:

            filter_value = st.text_input(
                f"Search {filter_column}",
                key="filter_value"
            )

            if filter_value:
                filtered_df = df[
                    df[filter_column]
                    .astype(str)
                    .str.contains(
                        filter_value,
                        case=False,
                        na=False
                    )
                ]
            else:
                filtered_df = df

        st.write(
            f"Showing **{len(filtered_df):,}** of **{len(df):,}** records"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

    elif section == "AI Insights":

    # AI-Powered Insights
        st.subheader("🤖 AI-Powered Insights")

        insights = []

        # Top product category
        if 'product_category' in df.columns and 'revenue' in df.columns:
            category_revenue = (
                df.groupby('product_category')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_category = category_revenue.index[0]
            top_category_revenue = category_revenue.iloc[0]

            insights.append(
                f"📦 **Top product category:** {top_category} "
                f"with revenue of ₹{top_category_revenue:,.2f}."
            )

        # Top region
        if 'region' in df.columns and 'revenue' in df.columns:
            region_revenue = (
                df.groupby('region')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_region = region_revenue.index[0]
            top_region_revenue = region_revenue.iloc[0]

            insights.append(
                f"🌍 **Top-performing region:** {top_region} "
                f"with revenue of ₹{top_region_revenue:,.2f}."
            )

        # Top payment method
        if 'payment_method' in df.columns and 'revenue' in df.columns:
            payment_revenue = (
                df.groupby('payment_method')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_payment = payment_revenue.index[0]
            top_payment_revenue = payment_revenue.iloc[0]

            insights.append(
                f"💳 **Most successful payment method:** {top_payment} "
                f"with revenue of ₹{top_payment_revenue:,.2f}."
            )

        # Strongest numerical relationship
        if 'revenue' in numeric_columns and len(numeric_columns) >= 2:

            correlations = (
                df[numeric_columns]
                .corr()['revenue']
                .drop('revenue')
            )

            strongest_factor = correlations.abs().idxmax()
            strongest_value = correlations[strongest_factor]

            insights.append(
                f"📈 **Strongest numerical relationship with revenue:** "
                f"{strongest_factor} "
                f"(correlation = {strongest_value:.2f})."
            )

        # Display insights
        for insight in insights:
            st.info(insight)

    elif section == "Anomaly Detection":

    # Anomaly / Outlier Detection
        st.subheader("🚨 Anomaly & Outlier Detection")

        if len(numeric_columns) > 0:

            anomaly_column = st.selectbox(
                "Select Numerical Column",
                numeric_columns,
                key="anomaly_column"
            )

            Q1 = df[anomaly_column].quantile(0.25)
            Q3 = df[anomaly_column].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_df = df[
                (df[anomaly_column] < lower_bound) |
                (df[anomaly_column] > upper_bound)
            ]

            outlier_count = len(outlier_df)
            outlier_percentage = (
                outlier_count / len(df) * 100
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Outliers Detected",
                    f"{outlier_count:,}"
                )

            with c2:
                st.metric(
                    "Outlier Percentage",
                    f"{outlier_percentage:.2f}%"
                )

            with c3:
                st.metric(
                    "Upper Bound",
                    f"{upper_bound:,.2f}"
                )

            if outlier_count > 0:
                st.write("Detected outlier records:")
                st.dataframe(
                    outlier_df,
                    use_container_width=True
                )
            else:
                st.success("No outliers detected.")

    elif section == "Business Recommendations":

    # Business Recommendations
        st.subheader("💼 Business Recommendations")

        recommendations = []

        if 'product_category' in df.columns and 'revenue' in df.columns:
            category_revenue = (
                df.groupby('product_category')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_category = category_revenue.index[0]

            recommendations.append(
                f"📦 Focus inventory and marketing efforts on "
                f"**{top_category}**, which generates the highest revenue."
            )

        if 'region' in df.columns and 'revenue' in df.columns:
            region_revenue = (
                df.groupby('region')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_region = region_revenue.index[0]

            recommendations.append(
                f"🌍 Consider increasing promotions and product "
                f"availability in the **{top_region}** region."
            )

        if 'payment_method' in df.columns and 'revenue' in df.columns:
            payment_revenue = (
                df.groupby('payment_method')['revenue']
                .sum()
                .sort_values(ascending=False)
            )

            top_payment = payment_revenue.index[0]

            recommendations.append(
                f"💳 Maintain a smooth **{top_payment}** payment experience "
                f"and consider payment-based offers."
            )

        if 'unit_price' in df.columns and 'revenue' in df.columns:
            correlation = df['unit_price'].corr(df['revenue'])

            recommendations.append(
                f"💰 Unit price has a correlation of **{correlation:.2f}** "
                f"with revenue. Review pricing and premium-product strategies."
            )

        for recommendation in recommendations:
            st.success(recommendation)

    elif section == "Report":

    # Automatic Summary Report
        st.subheader("📄 Summary Report")

        report_data = {
            "Metric": [
                "Total Rows",
                "Total Columns",
                "Missing Values",
                "Total Revenue",
                "Total Orders",
                "Average Order Revenue",
                "Average Customer Rating",
                "Total Quantity"
            ],
            "Value": [
                len(df),
                len(df.columns),
                int(df.isnull().sum().sum()),
                total_revenue,
                total_orders,
                average_revenue,
                average_rating,
                total_quantity
            ]
        }

        report_df = pd.DataFrame(report_data)

        st.dataframe(
            report_df,
            use_container_width=True
        )

        report_csv = report_df.to_csv(index=False)

        st.download_button(
            label="⬇️ Download Summary Report",
            data=report_csv,
            file_name="ecommerce_summary_report.csv",
            mime="text/csv"
        )
