def data_overview(df, corr=False, label_name=None, sort_by='qtd_null', thresh_percent_null=0, thresh_corr_label=0):
    """
    Etapas:
        1. levantamento de atributos com dados nulos no conjunto
        2. análise do tipo primitivo de cada atributo
        3. análise da quantidade de entradas em caso de atributos categóricos
        4. extração da correlação pearson com o target para cada atributo
        5. aplicação de regras definidas nos argumentos
        6. retorno do dataset de overview criado

    Argumentos:
        df -- DataFrame a ser analisado [pandas.DataFrame]
        label_name -- nome da variável target [string]
        sort_by -- coluna de ordenação do dataset de overview [string - default: 'qtd_null']
        thresh_percent_null -- filtro de dados nulos [int - default: 0]
        threh_corr_label -- filtro de correlação com o target [int - default: 0]

    Retorno
        df_overview -- dataet consolidado contendo análise das colunas [pandas.DataFrame]
    """

    # Criando DataFrame com informações de dados nulos
    df_null = pd.DataFrame(df.isnull().sum()).reset_index()
    df_null.columns = ['feature', 'qtd_null']
    df_null['percent_null'] = df_null['qtd_null'] / len(df)

    # Retornando tipo primitivo e qtd de entradas para os categóricos
    df_null['dtype'] = df_null['feature'].apply(lambda x: df[x].dtype)
    df_null['qtd_cat'] = [len(df[col].value_counts()) if df[col].dtype == 'object' else 0 for col in
                          df_null['feature'].values]

    if corr:
        # Extraindo informação de correlação com o target
        label_corr = pd.DataFrame(df.corr()[label_name])
        label_corr = label_corr.reset_index()
        label_corr.columns = ['feature', 'target_pearson_corr']

        # Unindo informações
        df_null_overview = df_null.merge(label_corr, how='left', on='feature')
        df_null_overview.query('target_pearson_corr > @thresh_corr_label')
    else:
        df_null_overview = df_null

    # Filtrando dados nulos de acordo com limiares
    df_null_overview.query('percent_null > @thresh_percent_null')

    # Ordenando DataFrame
    df_null_overview = df_null_overview.sort_values(
        by=sort_by, ascending=False)
    df_null_overview = df_null_overview.reset_index(drop=True)

    return df_null_overview
