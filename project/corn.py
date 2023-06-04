import secretflow as sf
import spu
import db
import logger
logger = logger.getLogger()


def ABY3_semi2k():
    # init the sf
    sf.shutdown()
    sf.init(['user', 'chrome', 'TTP', 'Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'], address='local')
    logger.info('The system begin with node : user、chrome、TTP、Webserver1、Webserver2、Webserver3、Webserver4、Webserver5')
    # init the PYU unit
    pyu_user = sf.PYU('user')
    logger.info('System init a PYU device user')
    pyu_TTP= sf.PYU('TTP')
    logger.info('System init a PYU device TTP')
    pyu_chrome = sf.PYU('chrome')
    logger.info('System init a PYU device chrome')
    pyu_webserver = sf.PYU('Webserver1')
    logger.info('System init a PYU device Webserver1')
    
    # the aby3 config
    aby3_config = sf.utils.testing.cluster_def(
        parties=['user', 'chrome', 'TTP'],
        runtime_config={
            'protocol': spu.spu_pb2.ABY3,
            'field': spu.spu_pb2.FM64,
        })
    logger.info('System init a SPU device with user、chrome、TTP')
    
    # the Semi2k config
    semi2k_config = sf.utils.testing.cluster_def(
        parties=['Webserver1', 'Webserver2', 'Webserver3', 'Webserver4', 'Webserver5'],
        runtime_config={
            'protocol': spu.spu_pb2.SEMI2K,
            'field': spu.spu_pb2.FM64,
        },
    )
    logger.info('System init a SPU device with all webserver')
    
    ret_dic = {'pyu_user':pyu_user,'pyu_TTP':pyu_TTP,'pyu_chrome':pyu_chrome,'pyu_webserver':pyu_webserver,'aby3_config':aby3_config,'semi2k_config':semi2k_config}
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



