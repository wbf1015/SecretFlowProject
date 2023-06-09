import secretflow as sf
import spu
import db
from logger import *


def ABY3_shamir():
    # init the sf
    sf.shutdown()
    sf.init(['user', 'chrome', 'TTP', 'Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'], address='local')
    make_StartInfo_Logger('The system begin with node : user、chrome、TTP、Webserver1、Webserver2、Webserver3、Webserver4、Webserver5')
    # init the PYU unit
    pyu_user = sf.PYU('user')
    make_StartInfo_Logger('System init a PYU device user')
    pyu_TTP= sf.PYU('TTP')
    make_StartInfo_Logger('System init a PYU device TTP')
    pyu_chrome = sf.PYU('chrome')
    make_StartInfo_Logger('System init a PYU device chrome')
    # We use shamir to share the secret so we do not need spu,but we need spu to cal
    pyu_webserver1 = sf.PYU('Webserver1')
    make_StartInfo_Logger('System init a PYU device Webserver1')
    pyu_webserver2 = sf.PYU('Webserver2')
    make_StartInfo_Logger('System init a PYU device Webserver2')
    pyu_webserver3 = sf.PYU('Webserver3')
    make_StartInfo_Logger('System init a PYU device Webserver3')
    pyu_webserver4 = sf.PYU('Webserver4')
    make_StartInfo_Logger('System init a PYU device Webserver4')
    pyu_webserver5 = sf.PYU('Webserver5')
    make_StartInfo_Logger('System init a PYU device Webserver5')
    
    # the aby3 config
    aby3_config = sf.utils.testing.cluster_def(
        parties=['user', 'chrome', 'TTP'],
        runtime_config={
            'protocol': spu.spu_pb2.ABY3,
            'field': spu.spu_pb2.FM64,
        })
    make_StartInfo_Logger('System init a SPU device with user、chrome、TTP')
    
    ret_dic = {'pyu_user':pyu_user,'pyu_TTP':pyu_TTP,'pyu_chrome':pyu_chrome,'pyu_webserver1':pyu_webserver1\
            ,'pyu_webserver2':pyu_webserver2,'pyu_webserver3':pyu_webserver3,'pyu_webserver4':pyu_webserver4,\
            'pyu_webserver5':pyu_webserver5,'aby3_config':aby3_config}
    return ret_dic


def cheetah_semi2k():
    sf.shutdown()
    sf.init(['user', 'chrome', 'TTP', 'Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'], address='local')

    # init the PYU unit
    pyu_user = sf.PYU('user')
    pyu_TTP= sf.PYU('TTP')
    pyu_chrome = sf.PYU('chrome')
    pyu_webserver = sf.PYU('Webserver1')

    # the Cheetah config
    cheetah_config = sf.utils.testing.cluster_def(
        parties=['user', 'chrome'],
        runtime_config={
            'protocol': spu.spu_pb2.CHEETAH,
            'field': spu.spu_pb2.FM64,
        },
    )

    # the Semi2k config
    semi2k_config = sf.utils.testing.cluster_def(
        parties=['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'],
        runtime_config={
            'protocol': spu.spu_pb2.SEMI2K,
            'field': spu.spu_pb2.FM64,
        },
    )

    ret_dic = {'pyu_user':pyu_user,'pyu_YYP':pyu_TTP,'pyu_chrome':pyu_chrome,'pyu_webserver':pyu_webserver,'cheetah_config':cheetah_config,'semi2k_config':semi2k_config}
    return ret_dic



