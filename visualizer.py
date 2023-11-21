from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from io import StringIO

# Initialize Data -- WILL BE ABSTRACTED INTO SEPARATE FUNCTION
operations_matrix = {0: "NULL", 1: "AVERAGE"}


def process(df_data):
    df_Iris = pd.read_csv("data/Iris.csv", delimiter=',')
    df_Setosa = df_Iris[df_Iris['Species'] == 'Iris-setosa']
    df_Versicolor = df_Iris[df_Iris['Species'] == 'Iris-versicolor']
    df_Virginica = df_Iris[df_Iris['Species'] == 'Iris-virginica']

    metrics_by_species = {'Iris-setosa': {"MeanSepalLengthCm": df_Setosa['SepalLengthCm'].mean(),
                                          "MeanSepalWidthCm": df_Setosa['SepalWidthCm'].mean(),
                                          "MeanPetalLengthCm": df_Setosa['PetalLengthCm'].mean(),
                                          "MeanPetalWidthCm": df_Setosa['PetalWidthCm'].mean()},
                          'Iris-versicolor': {"MeanSepalLengthCm": df_Versicolor['SepalLengthCm'].mean(),
                                              "MeanSepalWidthCm": df_Versicolor['SepalWidthCm'].mean(),
                                              "MeanPetalLengthCm": df_Versicolor['PetalLengthCm'].mean(),
                                              "MeanPetalWidthCm": df_Versicolor['PetalWidthCm'].mean()},
                          'Iris-virginica': {"MeanSepalLengthCm": df_Virginica['SepalLengthCm'].mean(),
                                             "MeanSepalWidthCm": df_Virginica['SepalWidthCm'].mean(),
                                             "MeanPetalLengthCm": df_Virginica['PetalLengthCm'].mean(),
                                             "MeanPetalWidthCm": df_Virginica['PetalWidthCm'].mean()}}
    # Organizes statistical information by species

    column_additions = {'SepalLengthCm': 'MeanSepalLengthCm',
                        'SepalWidthCm': 'MeanSepalWidthCm',
                        'PetalLengthCm': 'MeanPetalLengthCm',
                        'PetalWidthCm': 'MeanPetalWidthCm'}

    conditions = [df_Iris['Species'] == 'Iris-setosa',
                  df_Iris['Species'] == 'Iris-versicolor',
                  df_Iris['Species'] == 'Iris-virginica']

    for column in column_additions.keys():
        values = [df_Setosa[column].mean(),
                  df_Versicolor[column].mean(),
                  df_Virginica[column].mean()]
        df_Iris[column_additions[column]] = np.select(conditions, values)

    stratified_values = {"Iris-Versicolor": df_Versicolor, "Iris-Virginica": df_Virginica, "Iris-Setosa": df_Setosa}
    return stratified_values
    # Add titles and labels

    # names = df_Iris.Species
    # fig, ax = plt.subplots(1,4, figsize = (14,8))
    # ax[0].bar(x=names, height=df_Iris.MeanSepalLengthCm)
    # ax[1].bar(x=names, height=df_Iris.MeanSepalWidthCm)
    # ax[2].bar(x=names, height=df_Iris.MeanPetalLengthCm)
    # ax[3].bar(x=names, height=df_Iris.MeanPetalWidthCm)


def render_plot(stratified_values):
    # RENDER GRAPH --WILL BE ABSTRACTED INTO SEPARATE FUNCTION

    for flower in stratified_values:
        data = stratified_values[flower]['PetalWidthCm']
        min_val = data.min()
        max_val = data.max()
        mean_val = data.mean()
        med_val = data.median()
        mod_val = data.mode()[0]
        print('Minimum:{:.2f}\nMean:{:.2f}\nMedian:{:.2f}\nMode:{:.2f}\nMaximum:{:.2f}\n'.format(min_val,
                                                                                                 mean_val,
                                                                                                 med_val,
                                                                                                 mod_val, max_val))
        fig = plt.figure(figsize=(10, 4))
        data.plot.density()
        title = flower
        print(title)
        # Add titles and labels
        plt.title(flower)

        # Show the mean, median, and mode
        plt.axvline(x=data.mean(), color='cyan', linestyle='dashed', linewidth=2)
        plt.axvline(x=data.median(), color='red', linestyle='dashed', linewidth=2)
        plt.axvline(x=data.mode()[0], color='yellow', linestyle='dashed', linewidth=2)

        st.pyplot(fig)


def main():
    st.title('Dynamic Forms')
    dataframe = None
    print(st.session_state)
    if 'stage' not in st.session_state:
        st.session_state.stage = 0
        print(st.session_state)

    def set_stage(stage):
        st.session_state.stage = stage

    csv_form = st.form(key='my_form')
    file = csv_form.file_uploader(label="Input CSV", type=['csv'], help="tooltip", accept_multiple_files=False)
    # n_forms = st.number_input('Number of forms to create', 0, 10)
    csv_form.form_submit_button(label='Submit forms', on_click=set_stage, args=(2,))
    print(st.session_state.stage)
    if st.session_state.stage > 0:
        # forms_dict[i] = st.text_input(str(i))
        if not file and st.session_state['FormSubmitter:my_form-Submit forms']:
            set_stage(0)
            st.warning('Must Upload File Before Submission', icon="⚠️")

    if st.session_state.stage > 1:
        st.empty()
        bytes_data = file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        # st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(file)
        st.button('Cancel', on_click=set_stage, args=(0,))
        confirmation_form = st.form(key='validation_form')
        confirmation_form.success('Data has been successfully uploaded', icon="✅")
        confirmation_form.write(dataframe)
        confirmation_form.form_submit_button('Confirm', on_click=set_stage, args=(3,))

        # st.write(file)
    if st.session_state.stage > 2:
        processed_data_frame = process(dataframe)
        render_plot(processed_data_frame)
    # input_box = st.text_input("Input", "Type Here")


if __name__ == '__main__':
    main()
