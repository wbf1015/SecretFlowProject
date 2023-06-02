import secretflow as sf
import db
import logger
logger = logger.getLogger()

'''
init a sf with user,chrome and trusted third part, which 组成 a aby3 party
then init a spu device by this aby3 party and init pyu with TTP and chrome
'''
sf.shutdown()
sf.init(['user', 'chrome', 'TTP'], address='local')
aby3_config = sf.utils.testing.cluster_def(parties=['user', 'chrome', 'TTP'])
spu_device = sf.SPU(aby3_config)
pyu_TTP= sf.PYU('TTP')
pyu_chrome = sf.PYU('chrome')



