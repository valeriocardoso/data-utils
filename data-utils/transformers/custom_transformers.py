# Leitura de base de dados de forma otimizada
def import_data(path, sep=',', optimized=True, n_lines=50):
    """
    Etapas:
        1. leitura de primeiras linhas do dataset
        2. retorno de

    Argumentos:
        path -- caminho onde o dataset está localizado [string]
        sep -- separador de colunas da base [string, default: ',']
        optimized -- indicador de leitura de arquivo de forma otimizada [bool, default: True]
        n_lines -- quantidade de linhas a serem lidas no processo de otimização [int, default: 50]

    Retorno:
    """

    # Verificando indicador de redução de memória RAM
    if optimized:
        # Lendo primeiras linhas do dataset
        df_raw = pd.read_csv(path, sep=sep, nrows=n_lines)
        start_mem = df_raw.memory_usage().sum() / 1024 ** 2

        # Retornando atributos elegíveis à otimização
        float64_cols = [col for col,
                        dtype in df_raw.dtypes.items() if dtype == 'float64']
        int64_cols = [col for col, dtype in df_raw.dtypes.items()
                      if dtype == 'int64']
        total_opt = len(float64_cols) + len(int64_cols)
        print(
            f'O dataset possui {df_raw.shape[1]} colunas, das quais {total_opt} são elegíveis a otimização.\n')

        # Otimizando tipos primitivos: float64 para float32
        for col in float64_cols:
            df_raw[col] = df_raw[col].astype('float32')

        # Otimizando tipos primitivos: int64 para int32
        for col in int64_cols:
            df_raw[col] = df_raw[col].astype('int32')

        # Verificando ganho de memória
        print('----------------------------------------------------')
        print(f'Memória RAM utilizada ({n_lines} linhas): {start_mem:.4f} MB')
        end_mem = df_raw.memory_usage().sum() / 1024 ** 2
        print(
            f'Memória RAM após otimização ({n_lines} linhas): {end_mem:.4f} MB')
        print('----------------------------------------------------')
        mem_reduction = 100 * (end_mem / start_mem)
        print(f'\nGanho de {mem_reduction:.2f}% em uso de memória!\n')

        # Criando objeto com os novos tipos primitivos
        dtypes = df_raw.dtypes
        col_names = dtypes.index
        types = [dtype.name for dtype in dtypes.values]
        column_types = dict(zip(col_names, types))

        # Lendo DataFrame completo com novos tipos
        return pd.read_csv(path, sep=sep, dtype=column_types)
    else:
        # Leitura de DataFrame sem otimização
        return pd.read_csv(path, sep=sep)
