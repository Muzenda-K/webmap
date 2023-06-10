import streamlit as st
import matplotlib.pyplot as plt
import io
import geopandas as gpd
from  matplotlib.colors import LinearSegmentedColormap
import numpy as np
import plotly.express as px
from Login import clear_all_but_first_page

# Title of the page
st.title('Yield Mapping')
st.subheader('Yield Graphs')

# side bar
with st.sidebar:
    # logout button
    logout_btn = st.button('Log out', on_click=clear_all_but_first_page())

    # Horizontal line
    st.markdown("---")

    # Naming the current page
    st.markdown("## Maps page")
    

# Upload yield file for analysis
global file
try: 
    file = st.file_uploader("Enter a geojson file", type='geojson')
except Exception as e:
    st.warning('Please upload a correct file')

# Reading file into a dataframe
global df
if file is not None:
    try:
        df = gpd.read_file(file)
    except Exception as e:
        st.warning(e)

# Display file in the form of interactive data frame
display_data = st.radio('Would you like to display your data?', options=['Yes', 'No'])

if display_data == 'Yes':
    try:
        st.write(df)
    except Exception as e:
        st.warning('Please upload your data file')

# Drawing Graphs
# Using Plotly
if file is not None:
    columns = df.columns.values.tolist()
    x_column = st.selectbox("select column for x-axis", columns, key='x_axis')
    y_column = st.selectbox("select column for y-axis", columns, key='y_axis')

    x_axis = df[x_column]
    y_axis = df[y_column]

    # User input for graphs
    col1, col2, col3 = st.columns(3)
    chart_name = col1.text_input('Give your graph a name')
    xlabel = col2.text_input('Label for x-axis')
    ylabel = col3.text_input('Label for y-axis')


    # Graphs panel
    st.subheader('Graphs Panel')

    # Draw different graphs
    tab1, tab2, tab3, tab4 = st.tabs(["Line Graph", "Bar Graph", "Histogram", "Box Plot"])
    with tab1:
        # Draw a line graph
        try: 
            fig = px.line(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
            
            # Save the figure as a pdf to the buffer
            fig.write_image(file=buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Graph",
                data=buffer,
                file_name="line.png",
                mime="image/png",
                    )
            
            
        except Exception as e:
            st.warning(e)
    
    with tab2:
        # Draw a bar graph
        try: 
            fig = px.bar(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
            
            # Save the figure as a pdf to the buffer
            fig.write_image(file=buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Graph",
                data=buffer,
                file_name="bar.png",
                mime="image/png",
                    )
        except Exception as e:
            st.warning('Something went wrong, make sure yu selected the right columns')

    with tab3:
        # Draw a histogram
        try:
            fig = px.histogram(df, x=y_column, labels={'value': ylabel, "variable": xlabel})
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
            
            # Save the figure as a pdf to the buffer
            fig.write_image(file=buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Graph",
                data=buffer,
                file_name="hist.png",
                mime="image/png",
                    )
        except Exception as e:
            st.warning('Something went wrong, make sure yu selected the right columns')

    with tab4:
        # Draw a box plot
        try:
            fig = px.box(y_axis, labels={'value': ylabel})
            st.plotly_chart(fig,  use_container_width=True)

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
            
            # Save the figure as a pdf to the buffer
            fig.write_image(file=buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Graph",
                data=buffer,
                file_name="boxplot.png",
                mime="image/png",
                    )
        except Exception as e:
            st.warning('Something went wrong, make sure yu selected the right columns')
        


# Maps section
st.set_option('deprecation.showPyplotGlobalUse', False)
# Graphs panel
st.markdown("---")
st.subheader('Maps Panel')

if file is not None:
    columns = df.columns.values.tolist()
    yield_values = st.sidebar.selectbox("Select Yield Column", columns, key='yield_column')
    tab1, tab2, tab3, tab4 = st.tabs(["Boundary Map", "Raw Map", "Normalised Map", "NullValues"])

    with tab1:
        try:
            st.markdown("## Boundary map")
            df.boundary.plot(linewidth=1, edgecolor='#222')
            plt.axis("off")

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
            
            # Save the figure as a pdf to the buffer
            plt.savefig(buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Map",
                data=buffer,
                file_name="Boundary.png",
                mime="image/png",
                    )
            # Display map
            st.pyplot()
        except Exception as e:
            st.warning(e)

    with tab2:
        try:
           st.markdown("## Raw yield map")
           # color map
           colors = ['#e2211a', '#f6ee05', '#DBFF33','#9df018', '#8bf017']
           cmap1 = LinearSegmentedColormap.from_list("n",colors)
           df.plot(
           column='maize_rf_lowN', 
           legend=True,
           legend_kwds={ "orientation": "vertical"},
           cmap=cmap1)
            
           # Download the graph
           # Create an in-memory buffer
           buffer = io.BytesIO()
            
           # Save the figure as a pdf to the buffer
           plt.savefig(buffer, format="png")

           # Download the pdf from the buffer
           st.download_button(
                label="Download Map",
                data=buffer,
                file_name="Raw.png",
                mime="image/png",
                    )
           # Display map
           st.pyplot() 
        except Exception as e:
            st.warning('Something went wrong')

    with tab3:
            try:
                st.markdown("## Nomarlised yield map")

                # Calculate mean value
                mean = df[yield_values].mean() # Correct

                # Normalise data
                data = df
                conditions = [
                    (data[yield_values] < mean),
                    (data[yield_values] == mean),
                    (data[yield_values] > mean)
                ]

                values = [-1, 0, 1]

                data[yield_values] = np.select(conditions, values)

                colors2 = ['#e2211a', '#f6ee05', '#8bf017']
                cmap2 = LinearSegmentedColormap.from_list("n",colors2)

                data.plot(
                    column=yield_values, 
                    legend=True,
                    legend_kwds={"label": "Grain yield", "orientation": "vertical"},
                    cmap=cmap2)

                # Download the graph
                # Create an in-memory buffer
                buffer = io.BytesIO()
                
                # Save the figure as a pdf to the buffer
                plt.savefig(buffer, format="png")

                # Download the pdf from the buffer
                st.download_button(
                    label="Download Map",
                    data=buffer,
                    file_name="Normalised.png",
                    mime="image/png",
                        )
                
                # Display Map
                st.pyplot()
            except Exception as e:
                st.warning(e)

    with tab4: 
        try:
            df.plot(
            column=yield_values,
            legend=True,
            scheme="quantiles",
            figsize=(15, 10),
            missing_kwds={
                "color": "lightgrey",
                "edgecolor": "red",
                "hatch": "///",
                "label": "Missing values",
            },
            )

            # Download the graph
            # Create an in-memory buffer
            buffer = io.BytesIO()
                
            # Save the figure as a pdf to the buffer
            plt.savefig(buffer, format="png")

            # Download the pdf from the buffer
            st.download_button(
                label="Download Map",
                data=buffer,
                file_name="Normalised.png",
                mime="image/png",
                    )
                
             
            # Display Map
            st.pyplot()
        except Exception as e:
            st.warning('Something went wrong')
