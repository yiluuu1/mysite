from functools import partial
from influxdb import InfluxDBClient
import multiprocessing.dummy as mp


client = InfluxDBClient(host='210.17.199.226', port='8086', username='admin', password='ieph5Aqu', database='HotbitFuture')


def get_con(contract_list, _dic, key):
    con = 'select * from "btc_contract", "doge_contract", "dot_contract", "etc_contract", "eth_contract", ' \
          '"fil_contract", "ltc_contract", "trx_contract", "xrp_contract" where ' \
          '"type"=\'%s\' order by time desc limit 1;' % (key)
    result = client.query(con)
    for contract in contract_list:
        for point in result.get_points(measurement= contract):
            _dic[contract][point['type']] = round(point['value'], 3)
    return _dic
    
    
def hotbit_analysis(_dic, contract_list):
    key_list = ['ask1_price', 'bid1_price', 'hotbit_position','hotbit_profit','leverage','ask1_depth', 'bid1_depth',
                'binance_ask1', 'binance_bid1', 'binance_position', 'binance_profit','binance_mgnRatio',
                'ok_ask1', 'ok_bid1','okex_position', 'okex_profit', 'okx_mgnRatio']
    get_con_partial = partial(get_con, contract_list, _dic)
    p = mp.Pool(4)
    result = p.map(get_con_partial, key_list)[0]
    p.close()
    p.join()

    client.close()
    return list(result.values())
