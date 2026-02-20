def opcion_1():
    df_ind = None
    dates = ["2023-01-31", "2023-02-28", "2023-03-31", "2023-04-30", "2023-05-31", 
            "2023-06-30", "2023-07-31", "2023-08-31", "2023-09-30", "2023-10-31", 
            "2023-11-30", "2023-12-31", "2024-01-31", "2024-02-29", "2024-03-31", 
            "2024-04-30", "2024-05-31", "2024-06-30", "2024-07-31", "2024-08-31",
            "2024-09-30", "2024-10-31", "2024-11-30"]
    frequencies = [2, 3, 5, 6, 7]
    
    progress_bar = st.progress(0)
    total_iterations = len(dates) * len(frequencies)
    current_iteration = 0

    for ff in dates:
        for f in frequencies:
            current_iteration += 1
            progress_bar.progress(current_iteration / total_iterations)
            
            npage = 1
            while True:
                response_data = fetch_data(ff, f, npage, 
                                        {'Content-type': 'application/json', 
                                         'Authorization': st.session_state.token})
                if response_data is None:
                    break

                if 'message' not in response_data or 'data' not in response_data['message']:
                    break
                
                df_nested_list = pd.json_normalize(response_data["message"], 
                                                 record_path=['data'])
                df_nested_list['frecuencia'] = f
                if df_nested_list.empty:
                    break
                
                if df_ind is None:
                    df_ind = df_nested_list
                else:
                    df_ind = pd.concat([df_ind, df_nested_list])
                npage += 1

    if df_ind is not None:
        st.dataframe(df_ind)
        
        # Generar Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_ind.to_excel(writer, index=False, sheet_name="Indicadores")
        
        # Ofrecer botón de descarga
        st.download_button(
            label="📥 Descargar Excel de Indicadores",
            data=output.getvalue(),
            file_name="Indicadores_Kawak.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return True
    return False

def opcion_2():
    headers2 = {
        'Authorization': st.session_state.token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    SalidasNoConformes = Api_Kawak(headers2, 
                                 url='https://api.kawak.com.co/api/v1/salidasNoConformes/pool')
    if SalidasNoConformes:
        data = SalidasNoConformes['message']['data']
        df = pd.json_normalize(data)
        st.dataframe(df)
        
        # Generar Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Salidas No Conformes")
        
        # Ofrecer botón de descarga
        st.download_button(
            label="📥 Descargar Excel de Salidas No Conformes",
            data=output.getvalue(),
            file_name="Salidas_No_Conformes_Kawak.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return True
    return False

def opcion_3():
    headers2 = {
        'Authorization': st.session_state.token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    accionesMejora = Api_Kawak(headers2, 
                              url='https://api.kawak.com.co/api/v1/accionesMejora')
    if accionesMejora:
        dataMejora = accionesMejora['message']['data']
        df = pd.json_normalize(dataMejora)
        st.dataframe(df)
        
        # Generar Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Acciones Mejora")
        
        # Ofrecer botón de descarga
        st.download_button(
            label="📥 Descargar Excel de Acciones Mejora",
            data=output.getvalue(),
            file_name="Acciones_Mejora_Kawak.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return True
    return False

def opcion_4():
    headers2 = {
        'Authorization': st.session_state.token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    Documental = Api_Kawak(headers2, url='https://api.kawak.com.co/api/v1/docs')
    if Documental and Documental.get("status") != "error":
        dataDoc = Documental['message']['data']
        df = pd.json_normalize(dataDoc)
        st.dataframe(df)
        
        # Generar Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Documentos")
        
        # Ofrecer botón de descarga
        st.download_button(
            label="📥 Descargar Excel de Documentos",
            data=output.getvalue(),
            file_name="Documentos_Kawak.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return True
    return False

def opcion_5():
    headers2 = {
        'Authorization': st.session_state.token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    codigos = [6, 8, 9, 10, 11, 12, 13]
    dataframes = []
    
    progress_bar = st.progress(0)
    for i, codigo in enumerate(codigos):
        progress_bar.progress((i + 1) / len(codigos))
        ControlRiesgos = Api_Kawak(
            headers2,
            url=f'https://api.kawak.com.co/api/v1/controlesRiesgo?id_del_sistema_de_gestion_de_riesgos=135'
        )
        if ControlRiesgos:
            data = ControlRiesgos['message']['data']
            df = pd.json_normalize(data)
            df['codigo'] = codigo
            dataframes.append(df)

    if dataframes:
        df_combined = pd.concat(dataframes, ignore_index=True)
        st.dataframe(df_combined)
        
        # Generar Excel para descarga
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_combined.to_excel(writer, index=False, sheet_name="Riesgos")
        
        # Ofrecer botón de descarga
        st.download_button(
            label="📥 Descargar Excel de Riesgos",
            data=output.getvalue(),
            file_name="Riesgos_Kawak.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return True
    return False