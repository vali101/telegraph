# This is an example how the code could be used
from scraper.scraper import Scraper
from scraper.client import Client

Client(api_id=123456,
       api_hash="***********",
       phone="+49***********")

scraper = Scraper(num_messages=None,
                  step_size=200,
                  maximum_iterations=1)

seed_channels = ['querdenken241', 'querdenken351_aktiv', 'querdenken_6051', 'querdenken621_aktiv', 'ImpfGenozidKinder',
                 'querdenken215', 'querdenken381', 'querdenken_7171', 'querdenken8331', 'Maskenverbot',
                 'querdenken_911', 'querdenken511', 'corona', 'querdenken231', 'querdenken235', 'querdenken_791',
                 'querdenken_201', 'querdenken341_aktiv', 'MASKENFREI_ME', 'querdenken30', 'querdenken_775',
                 'querdenken215_aktiv', 'corona_infokanal_bmg', 'querdenken_334', 'querdenken911_aktiv',
                 'querdenken361', 'querdenken7141_aktiv', 'querdenken831', 'querdenken751', 'Pandemie1',
                 'querdenken6051_aktiv', 'querdenken238_aktiv', 'querdenken53', 'impfenchippenbargeldlos',
                 'QuerdenkenTV', 'querdenken7192_aktiv', 'querdenken_241', 'querdenken_231', 'querdenken453_aktiv',
                 'querdenken7451', 'querdenken5221', 'querdenken762_aktiv', 'querdenken_8341', 'querdenken615_aktiv',
                 'querdenken_571pw', 'querdenken_773', 'querdenken_235', 'querdenken203', 'querdenken228',
                 'querdenken201_aktiv', 'QUERDENKEN', 'querdenken242', 'querdenken242_aktiv', 'querdenken410',
                 'querdenken743', 'querdenken763', 'querdenken773_aktiv', 'querdenken351', 'querdenken_8331',
                 'querdenken_228', 'querdenken_861', 'querdenken8341', 'querdenken761', 'querdenken831_aktiv',
                 'querdenken7261', 'FakePandemie', 'querdenken615', 'Maske', 'QUERDENKEN_711', 'querdenken201',
                 'querdenken241_aktiv', 'querdenken_681', 'querdenken_793', 'coronavirus2020_kz', 'querdenken866_aktiv',
                 'GemeinsamMaskenfreiEinkaufen', 'querdenken_751', 'querdenken762', 'querdenken_242',
                 'impfenmussfreiwilligbleiben', 'querdenken_763', 'querdenken761_aktiv', 'querdenken763_aktiv',
                 'PandemieProdukte', 'querdenken234_aktiv', 'querdenken751_aktiv', 'querdenken_721', 'querdenken_615',
                 'querdenken_831', 'querdenken_571', 'querdenken791', 'querdenken453', 'MaskenfreiEinkaufenKanal',
                 'querdenken_351', 'querdenken6051', 'querdenken621', 'querdenken211_aktiv', 'querdenken381_aktiv',
                 'querdenken40_aktiv', 'querdenken7261_aktiv', 'querdenken8341_aktiv', 'querdenken_6201',
                 'querdenken_711', 'querdenken_794', 'cama_2Q2Q', 'querdenken361_aktiv', 'querdenken284_aktiv',
                 'querdenken211', 'impfenst', 'coronau', 'querdenken718', 'UKcoronavirusnews', 'querdenken7171',
                 'querdenken793_aktiv', 'querdenken841_aktiv', 'querdenken7192', 'querdenken_841', 'querdenken_713',
                 'querdenken_7261', 'querdenken_743', 'querdenken7551', 'querdenken571_aktiv', 'querdenken775_aktiv',
                 'querdenken702', 'querdenken_702', 'querdenken203_aktiv', 'querdenken5221_aktiv', 'querdenken2932',
                 'querdenken911', 'querdenken_441', 'querdenken30_aktiv', 'querdenken711', 'Nicht_impfenlassen',
                 'querdenken7171_aktiv', 'querdenken_761', 'querdenken775', 'querdenken234', 'querdenken841',
                 'querdenken238', 'querdenken_511', 'querdenken_5221', 'querdenken794_aktiv', 'querdenken228_aktiv',
                 'querdenken_284', 'querdenken_381', 'querdenken341', 'querdenken_453', 'querdenken69_aktiv',
                 'querdenken_238', 'querdenken861', 'querdenken_30', 'querdenken_621', 'querdenken791_aktiv',
                 'impfenhh', 'querdenken713', 'querdenken713_aktiv', 'querdenken_7141', 'Individuelle_Impfentscheidung',
                 'CoronaG', 'querdenken_866', 'fakepandemie1', 'Masken', 'querdenken711_aktiv', 'querdenken441_aktiv',
                 'querdenken_69', 'querdenken40', 'Impfen', 'querdenken69', 'querdenken_215', 'querdenken_341',
                 'querdenken793', 'querdenken_203', 'querdenken_718', 'wir_lassen_uns_nicht_impfen', 'querdenken_361',
                 'corona0', 'querdenken_2932', 'querdenken7551_aktiv', 'querdenken773', 'querdenken410_aktiv',
                 'querdenken6201', 'oliverjanich', 'querdenken334_aktiv', 'querdenken721', 'querdenken794',
                 'querdenken_40', 'querdenken681', 'querdenken_410', 'MyGovCoronaNewsdesk', 'CoronaOberlausitz',
                 'spcoronavirus', 'querdenken2932_aktiv', 'querdenken_7451', 'impfen_nein_danke', 'querdenken7141',
                 'querdenken_762', 'querdenken235_aktiv', 'querdenken6201_aktiv', 'fortschrittliche_corona_infos',
                 'querdenken441', 'querdenken571pw', 'querdenken866', 'querdenken718_aktiv', 'querdenken_53',
                 'querdenken53_aktiv', 'maskel', 'querdenken743_aktiv', 'WirStehenAuf', 'Corona_Fakten',
                 'querdenken_7551', 'querdenken861_aktiv', 'querdenken_234', 'querdenken702_aktiv',
                 'querdenken231_aktiv', 'querdenken721_aktiv', 'querdenken511_aktiv', 'querdenken8331_aktiv',
                 'maskenfreie_kids', 'querdenken334', 'querdenken284', 'querdenken681_aktiv', 'querdenken7451_aktiv',
                 'querdenken_7192', 'querdenken571pw_aktiv', 'Pandemie', 'querdenken571', 'querdenken_211',
                 'reitschusterde']

scraper.scrape(seed_channels)
