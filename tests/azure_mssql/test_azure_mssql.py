from toucan_connectors.azure_mssql.azure_mssql_connector import (
    AzureMSSQLConnector, AzureMSSQLDataSource
)


def test_connection_params():
    connector = AzureMSSQLConnector(host='my_host', user='my_user', password='', db='', name='')
    params = connector.connection_params
    assert params['server'] == 'my_host.database.windows.net'
    assert params['user'] == 'my_user@my_host'

    connector = AzureMSSQLConnector(host='my_host.database.windows.net', user='my_user',
                                    password='', db='', name='')
    params = connector.connection_params
    assert params['server'] == 'my_host.database.windows.net'
    assert params['user'] == 'my_user@my_host'

    connector = AzureMSSQLConnector(host='my_host.database.windows.net', user='my_user@my_host',
                                    password='', db='', name='')
    params = connector.connection_params
    assert params['server'] == 'my_host.database.windows.net'
    assert params['user'] == 'my_user@my_host'


def test_gcmysql_get_df(mocker):
    snock = mocker.patch('pymssql.connect')
    reasq = mocker.patch('pandas.read_sql')

    mssql_connector = AzureMSSQLConnector(
        name='test', host='localhost', db='mssql_db',
        user='ubuntu', password='ilovetoucan'
    )
    ds = AzureMSSQLDataSource(domain='test', name='test', query='my_query')
    mssql_connector.get_df(ds)

    snock.assert_called_once_with(
        server='localhost.database.windows.net',
        user='ubuntu@localhost',
        database='mssql_db',
        password='ilovetoucan',
        as_dict=True)
    reasq.assert_called_once_with('my_query', con=snock())
