"""Data profile for Post 30: buy, or rent and invest the difference.

Every file in data/ is frozen by its SHA-256 (the step-3 reports record where each comes from); a file that does not
match stops the script. Run on its own, this prints the coverage of each series the build reads and the cross-checks
the design names, and stops at the end if a cross-check lacks a pinned value. Run from the post folder:
python3 -I profile_data.py
"""
import csv
import datetime
import hashlib
import io
import os
import re
import warnings
import zipfile

import openpyxl

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

# Every file under data/, by its path inside data/. The AHS and cost source documents are not read by the build (their
# values sit in ahs_values.csv and cost_values.csv), but each CSV row names one of them, and they are pinned too.
FILES = {
    "acs/20061us0130000.zip": "b2abf6e8c4034530b0c85f8fa136023030c2b50ee0388c6865c501810708e112",
    "acs/20061us0131000.zip": "be2e87784dd23dc9335393d4b6e7afa7303b7c004436d8eca656f8da2c4c62de",
    "acs/20071us0135000.zip": "315ffe752f8f2d1769924a3d50556bccddfcc982360665200d8143a2f5ce5b96",
    "acs/20071us0136000.zip": "79a1c945f67390d9c77d62f255cd49d9306111270b910aa6f304f73b30c13105",
    "acs/20081us0139000.zip": "81e6eabd821ab564daffc1d5967e2485178a3f51219bb9daabe8f7a0ae197d61",
    "acs/20081us0140000.zip": "620d1ada604d712e02a564694738e6268232dd6a89577daab0bf1bcb8becb5cc",
    "acs/20091us0150000.zip": "b1a434da8bfcaad9141cf4fe030f14c7bba35c32aed5c51ea0bf5f221922b95b",
    "acs/20091us0151000.zip": "af4d1ed4e0c89758aabd473e5de9f24ea42e09098e9305c62f177f2419920106",
    "acs/20101us0150000.zip": "83f7c3296fab5298e6b2d01547e2f0b9af38a93097e8fcc74b379b0da13563c2",
    "acs/20101us0151000.zip": "cacefb40b20545dec4a1e643ebdf05f36d5208a703242c07806835be9e2f076c",
    "acs/20111us0156000.zip": "09ffcd907b358561e9e49339045c143b6d2ca4ea583ad2268825a9b179a8ed85",
    "acs/20111us0158000.zip": "725aad4877332153011a101df4721404c0a07a893a33c1c243e686345da63552",
    "acs/20121us0156000.zip": "ad004a2a781e091bc52f6e1aba48708ad42727c037c7908f8e908e376967736c",
    "acs/20121us0158000.zip": "219b9f798a5b51704c552d8dad4ab6bd1bfabd6c23bd8fbcbe2da644125e80cc",
    "acs/20131us0147000.zip": "6cfb4cddb45f7d66274a1c4f428233043c2f216d2fb50d0bbebc60fce89f161d",
    "acs/20131us0148000.zip": "cb496701d7a356726cd03ffaacb104532f0bd26efd5570ae597c96803ad5979f",
    "acs/20131us0149000.zip": "0de206de2028ae1faaa19812d82dead69aaaa17bb9dbcf19113a3c1dfbc71b1e",
    "acs/20141us0142000.zip": "d07a2433845a3d77cdcfc3ac0a4f4e25f05fc5546eace082528b7dfb928d40bb",
    "acs/20141us0144000.zip": "cb516aa038db9e411067f715ca8f0eb85d450f5c3c20bed41f97a7d8b64a0b21",
    "acs/20151us0142000.zip": "6a1a37f7cd281f2605d7546eae62d0b0ce51cae723f19b727c6c094dd330e497",
    "acs/20151us0144000.zip": "d24a0abb3bfb2b0023212fe6f056283e2418ebef535fa4ec5493e15e847e49b7",
    "acs/20161us0143000.zip": "eac638abfa4d6cdd604108b52d015f714329124fc0dcc250f2b5b00d01db6b22",
    "acs/20161us0145000.zip": "ccf69d66d113b99f83a61b750fbbe3ab084cbb1919d71af0bfdaf5de185629ba",
    "acs/20171us0143000.zip": "48acf6545a2dcdf280abcc84bb3a7285a8f4c505fdc1e7445277c611a310462b",
    "acs/20171us0145000.zip": "d731127fb98bb05c1b7e49efa96d908b3f53d52a481265d1a6957fa5b3262586",
    "acs/20181us0152000.zip": "34572a5d5979222c9bba567f57bf913ad5abcaf663b243b7c11c0653311e2b6b",
    "acs/20181us0154000.zip": "89965287fa62b2e62d01061b2bf92ff0d909dd7fc5cc988c1662e0b3a5fd0f6c",
    "acs/20191us0151000.zip": "9b5836dc0b1dbd725ca6c46e8568ac3dff1e14842459ed7b2f62729308c27b18",
    "acs/20191us0153000.zip": "b000aa74d49ceac807e1faace6f4d8154c1d8e115485d1a34fd0716869faa466",
    "acs/Geos20211YR.txt": "f24e9ac0d255cf38d20c0c23ebed6b6874b181f462f417b522304047a03286ea",
    "acs/Geos20221YR.txt": "f29667153e72ac95a5a76b87725cf1e509b53bd5611802432a04f06806e8b63f",
    "acs/Geos20231YR.txt": "d0e8ca5b28243016f89cb20588675ff6ace83cac503cf0273ec3f2ee7f9fcb62",
    "acs/Geos20241YR.txt": "2155acb3c81672eee9b0bd971cca60cd77d8b66222b34973928f57c087ea4afe",
    "acs/Geos20251YR.txt": "c8e9250ae8d2632bff4c9e800e5880722ea2cbd899a81c3ef071165fea13e387",
    "acs/acs_positions.csv": "03d07a97de59164c51c1aa76f1b737c9fc4c2841d365f019d74b0e434bf8242a",
    "acs/acsdt1y2021-b25077.dat": "0bc6d61db91997024c5cdfa07b43c692ffbe8f417dcdf9853db83f1ad21d5e40",
    "acs/acsdt1y2021-b25082.dat": "997448ed26bcc1741c5cfcc86a66433df6482865087ce46330679800c76deb93",
    "acs/acsdt1y2021-b25090.dat": "f56d8908d9743a75de1d657e4b044824a01c6ff303c6edfdc7dbcb82b16d7737",
    "acs/acsdt1y2022-b25077.dat": "2ce7a81314c8290186972e1675f3fbea3bfd19dab53cd8f206c2964130a40eb5",
    "acs/acsdt1y2022-b25082.dat": "28a4407f22248834a64d624d0786775eaa6d18bd62502f862f6894a9334f8bc6",
    "acs/acsdt1y2022-b25090.dat": "8327d702e247c98d705174d07eb9d39ebe289c13121c3f15bb9394e72bc518e7",
    "acs/acsdt1y2023-b25077.dat": "c39987ce683bc4ac8d5831ac9fb67cbcdfaa9bbb81193bc3af4582ad97353723",
    "acs/acsdt1y2023-b25082.dat": "302624aa5a8374f126a686ba948bca4b508b13e17efeeb882f175275d123303c",
    "acs/acsdt1y2023-b25090.dat": "4cf509db1f0379673ed44c666b842211523504bf9a2bc76d6ff6b77ca7c2c433",
    "acs/acsdt1y2024-b25082.dat": "7b35e18067f951a57338d88bb31a16f59f4a1d607f632a9a11e39b1462950b2f",
    "acs/acsdt1y2024-b25090.dat": "60f95c0745c34d9bd9d4dfca86d09947f463ef61c76d0e525b0b4b80a018810b",
    "acs/acsdt1y2025-b25077.dat": "7ab895b182348af2e79cb31e45717be5fdcc38ab1e1ad959cb4e0e7e9393b772",
    "acs/acsdt1y2025-b25082.dat": "4db69c6f29eee4d7fe117c5c9dc054be8c1bf7f64cfb6ab29c8a6065b0b9a3c7",
    "acs/acsdt1y2025-b25090.dat": "de416cf2b861cfe14e30ce1278a87d813fa30693450d7f6415e8e1b555a5ecd0",
    "acs/acsdt1y2025-b25103.dat": "4f3ee59fbf3149db9a06cb1f5a4e3170dc19668d6c69f33f5123127e63c068b3",
    "acs/e20061us0130000.txt": "e6d7c16c7a80ff4657383e9926d03498baa696dc473cc41aabcd5ede115fa519",
    "acs/e20061us0131000.txt": "88114192d147aa8553e696717fb2ed9fa452cb44547ae4174cc97286b265b907",
    "acs/e20071us0135000.txt": "6c635a50710b0c36ce623cac9bd01c7265ea2d81dd2ad11e5f9ec59cdbd598a6",
    "acs/e20071us0136000.txt": "00549c1f8a72736ad463018cd41529526886a1df9470b9a7b47a07c596bbd281",
    "acs/e20081us0139000.txt": "639a6a60b8067e99424d6b54356f80cfbad99a9b016b4331ef78b09386d7b352",
    "acs/e20081us0140000.txt": "13eaeacd3e1fd77c76ede695a6493817c7b2ec3c16d2b1a61a9a87dfc6059d00",
    "acs/e20091us0150000.txt": "4662d04733325728e21704570c21c46387c8e7a7a0e338df45c89682816dd573",
    "acs/e20091us0151000.txt": "f58b1aacdc398b42f899f36f32f058a3d31c7b65c01dff590fd09aaa3422977a",
    "acs/e20101us0150000.txt": "7d8f4ab67c41f527488a3795f7e1b1e966ae6eaac021357ad5a436bdf9514b25",
    "acs/e20101us0151000.txt": "f53205c5efb1ec10c4a803e0678ef1525b8dff89d1571376ab846808d3f9c05a",
    "acs/e20111us0156000.txt": "50bf52bd064307d940d2b4f7ec44971371de92c1cbd9eac87c4460fe2988c49d",
    "acs/e20111us0158000.txt": "73879742f9bc6137f7db076f08fa4e369c051ab965ae6e2d432cd6be424500af",
    "acs/e20121us0156000.txt": "fb52e05f835faa69639bc3b77a81de43f57d16c6db253de2d100c60137c90790",
    "acs/e20121us0158000.txt": "912df931e195c60aa65e6a50e2e65e35ecdd2198b99aead8d5875b10035d04bb",
    "acs/e20131us0147000.txt": "28cfe09295507016b5293eef51cd8441b5e8c3ccc3c881ae12213468f922bd31",
    "acs/e20131us0148000.txt": "2738c276973199440e7e044b54e8dbcf37aafe74d2cb8825c46888eed63e875b",
    "acs/e20131us0149000.txt": "6c6a170125c9364c6503c1222f9c095bcdd5552c306c1767e66ab67cf7103156",
    "acs/e20141us0142000.txt": "a5bb4d346f17b471258edf521d3c4aa6f36e60c42c1e223c7c05711573450b53",
    "acs/e20141us0144000.txt": "73e5d351a39588f0a6a1c0fecfc15abb4254fbd96ae3310ce186bee19c0ac3ce",
    "acs/e20151us0142000.txt": "31b17e35a546887c98acbc8dbac1f24a11e798a097cebf5a20ae018dcea9e1b6",
    "acs/e20151us0144000.txt": "1aba27110677e45b19454ca3679d876aa9dace8e05f93e75b07add18923a9492",
    "acs/e20161us0143000.txt": "74b5d1e575b4fd0c370ac4052f1f7bc0b77ef35b661c0fa1e90f78bc943daed1",
    "acs/e20161us0145000.txt": "f3257a271f9a266cefa028e78e3352e13edbe94e36e78ca43afd63b1d6d41664",
    "acs/e20171us0143000.txt": "d1f21c574e54f7bc2a8af2675c9a4c0e21a8a1bb80e2afc98fe1e4d44282ba9d",
    "acs/e20171us0145000.txt": "7321f29445167f1ba3f936e34acd0c34658f7149d3d4d3ab48c422dcf2e969fc",
    "acs/e20181us0152000.txt": "cf27883c0fd5eb47bcc4f7c8735ba00941d4d638ec96a348d4636cafcb10f929",
    "acs/e20181us0154000.txt": "b48d93a94d86425b6a3f8dbe0cbe917d119f97ee0bf8de482fd0579de5adc1e3",
    "acs/e20191us0151000.txt": "27f8d7f196e17ffe6e2ca04928b65a59c6c1093f797703a22c1112ef4bb13382",
    "acs/e20191us0153000.txt": "0c94948f7cd7898aaecd029ec334e8971022a09f90e010b65832d795dca05e86",
    "acs/g20061us.txt": "f1c042bbbfa9ec5b2d5092908807ed619c182cc71107a93c3cdd46c44d952054",
    "acs/g20071us.txt": "aaf411a7d3b8dce3199cb888d8b0825f8fcacbd0ae4fbdf597f002bf0b1efdbc",
    "acs/g20081us.txt": "a3c98376dee89be5c550e79320bfbef0b464e69f233c3385a40488b85159e7c3",
    "acs/g20091us.txt": "a9ff9999965571f4b3bdf0beab7517ac3325601acbba902984ce7773203fbb0c",
    "acs/g20101us.csv": "ff65f55adc0ee315f47b46f52dde4f2ebb43bdc640d9df2671562dafc64eb070",
    "acs/g20111us.csv": "d8d030ca15ccf0c9cc70af5ff6790a8fc075dde9d21fc81af1c8a98bbc5a04f4",
    "acs/g20121us.csv": "223a2b16ba94e530cf1ce40bb69f8eff6835acf4f39e37d92aec2eee5c08736f",
    "acs/g20131us.csv": "43437cbe1a45c8267557c249810583ea8e7fd4e01c7f2fed754d7d800dd791b5",
    "acs/g20141us.csv": "dc53d7e85e4498a9a2fa9dc7d4c2539ac53e7d5a21d1e675f0d48a31535bc846",
    "acs/g20151us.csv": "6639a6c9e28ae3bedd3afd6011c1e657519fac07b9a7d3d2b051d6fcf8726f45",
    "acs/g20161us.csv": "40d2be3d5f62daf1c2884a0cc02cc91df7f20e582ae8c1c90820744b50438b97",
    "acs/g20171us.csv": "0a6123de31cb6f16ee3c07ea5b3c9688f3cec63526e903018b4a2928e7666a65",
    "acs/g20181us.csv": "b1fc6c533d3845290dace40990081a19c1dfa6927d6b95c7129b5965bc4ebde2",
    "acs/g20191us.csv": "50a9f92f62fc816741f2a6b83b7660385442aa952da392e6bea6134b96a27af2",
    "acs/us0000131.2005-1yr.zip": "e54d1b1665fba6adb09f63437f515539df2d59842a525a9f487acbadf193e857",
    "acs/us0000131e.2005-1yr": "3f7330b8b6510c72db25cac7c2c5deacac53fc5057c7c1ed4e3bfadce663edeb",
    "acs/us0000132.2005-1yr.zip": "54bd413d0376865cd1fe1b106c560918276af58df5857300f6b27c5e1dde9b57",
    "acs/us0000132e.2005-1yr": "1c887775b63b2995cc832f7ebdb7cef5a227a6ee64728858a989f9e5abf3786b",
    "acs/usgeo.2005-1yr": "b31eb15ca45a56eda05b76a52d7e54b79e2c468c4dab63ca336f2cca53560513",
    "aei_dlm_rent_price_ratio_2018q2.xlsx": "eba71363889d5207a140c1600c3395fc847b2f04bbc148bb45978190207efb9e",
    "ahs/ahs2005_tab3-13.xls": "c01b2c412da2bb532ee296661249c3311fff1610384b618a97bc8e566f0e988e",
    "ahs/ahs_values.csv": "bd053dbc9ed39abee158f94fb97871515af66f2b6e92f0ecd3808ffa53d987c3",
    "ahs/h150-01.pdf": "3acb2a1f3256312388ae0a6a1e6832e0ae1a608a0e74e4e475d1d80a71777e4b",
    "ahs/h150-03.pdf": "7290bc7aa4ac7cc50ff6681fd44400142a3a14edcf080c29abd47abb3bb54952",
    "ahs/h150-05.pdf": "0d650398c6f27bef6bee719fd0f0211e275fcae5b035ba46d3fd43ebff9ba6d4",
    "ahs/h150-73C.pdf": "3b09ae95f37928c8902f02e248793f8e04bcd09cc7e442e610dfdb9881b6ea58",
    "ahs/h150-74C.pdf": "5b5ca1889104e9b5c80b48b3512e70deaaf3185853b43db9623e554c8d615c96",
    "ahs/h150-75c.pdf": "4a78e44e102e4ba0dbb9ee4fd13becc7368616d92c22b0e7c5084bb0982d93df",
    "ahs/h150-76c.pdf": "70821d0e3dfb36cc0e34b2436a8b2da9d1ed86be15c2a5d9a19dd844aa37d0a8",
    "ahs/h150-77c.pdf": "67fa042e80b7cc8efcd18a906bd7ac61de722a46ac1f05473e51d41449e47683",
    "ahs/h150-78c.pdf": "de5df29505654408a3a434a4f2f286eae2f442a453910d66156554ffcd377cc2",
    "ahs/h150-79c.pdf": "9c0b86f639ed575d01511373dc22f70b885088316f11a2b80e961acf112a12bc",
    "ahs/h150-80c.pdf": "edee8daca928aad50bb23fac6da138ddb2a12b679d49163f650f047ea85d9e2b",
    "ahs/h150-81c.pdf": "a8de836a79740dc2f63f1336108b03988cdeee7821eca9466eee67840ab04f7e",
    "ahs/h150-83c.pdf": "e812976483cfccc9cb1deb0b1138f4eff3ef361c7bf2275d21f2ac9c483ec474",
    "ahs/h150-85.pdf": "ce594322f219f8c25ec7545d0d744e7d8cc4022937c80c2fcf107a07efcfaa26",
    "ahs/h150-87.pdf": "4aa9a964223b2f5433d8be483f8451f656f727f9f163281bb86b1cc4fb601202",
    "ahs/h150-89.pdf": "f5ae55204c086dfa148b90ac1ea602400c5ea959b1ce1c895c47a8ed172bc34f",
    "ahs/h150-91.pdf": "a4e901e877bbd86838aeae3b157ae177c69e8acdda6dd5fb040de5c8d245d360",
    "ahs/h150-97.pdf": "db3f5afeffaa6fa78388985f7548f25b444f3ae2a1110d5c31c713af7393284a",
    "ahs/h150-99-rv.pdf": "c2ed3215a035ff58a344bee30c84595e1565cd5011c378fbeb5d60e3e56fa4d1",
    "ahs/h150_93.pdf": "cc886645197b8bfdd25a51a7ef477d0ae742454f7579078647a586451c4d7d7d",
    "ahs/h150_95rv.pdf": "f7e74b356a35b500b7e9df09005e213793bf5129f8b9c8382a638f4faa7d7e45",
    "bea/bea_fa_section5all_ia20250202204948.xlsx": "afb5988f9cebac83bfc0bd30ca5c0921c5c024363d92231711815058b785844d",
    "bea/bea_fa_seriesregister_ia20250207173438.txt": "fc902fc813dfeea585df24435b4a3ea689429d28c366bef6e97925a215b89d4a",
    "bea/bea_fixedassets_ia20250202204946.txt": "d880b8dfb5eb92e541f066ba8445a85d0df568bd1e7642a1c9790772ca5721fe",
    "bea_nipadataa_ia20261020095433.txt": "9f8e96bb72181d14d7b555f3e1b09c71e900fb8de4c305dc9217424de4757f27",
    "bls_cu_data_12_ushousing_ia20261029154324.txt": "b2ecc4021ea612ee9acf3629f2cbcfc7e1b063338ee5ede5ae10d74512019704",
    "bls_rcpiurs_allitems_ia20260819.xlsx": "355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8",
    "census_coh_values_unadj.txt": "5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6",
    "census_nrs_price_sold_cust.xlsx": "9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3",
    "costs/census_ahs2023_table_specs_puf_estimates.xlsx": "f94af71db86b11562252823f64ffad919e88ec0f6802a9d91dd8c8732b9b9b0e",
    "costs/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf":
        "7aaeadcd06a98abfff9c6c5f957493d2783f19a85752f618efea562867271c58",
    "costs/cost_values.csv": "9b5767862bad96824aa0d608867a8f2e42bc9a04a43831c0ba728c97d267974e",
    "costs/naic_homeowners_report_dy2021_ia20240217020958.pdf":
        "b1c98f9c1753730593a0c9329f23d6e44168aa0459ba2c020867a94b5d57c638",
    "costs/naic_homeowners_report_dy2022_ia20250706013631.pdf":
        "369718e3f64767077c1639902d8a053c42b3110a2dd0c3cf802ca4658ca69858",
    "costs/naic_homeowners_report_dy2023_ia20261011104807.pdf":
        "b157866e6656e17041416665557867f4effe77b7b124656a747d2833ea9f4739",
    "fhfa_hpi_at_us_and_census.csv": "580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba",
    "fhfa_hpi_po_us_and_census.txt": "4776cd3261d1a5ba71701d2fd7c934184d86494b7b2332ba6b20afa63fae1fea",
    "frb_z1_csv_2026-09-11.zip": "83b8eded0bc7f9b74c0269ef503a863cee88312460fd7eef076284b98fc28c06",
    "freddiemac_pmms_historicalweeklydata.xlsx": "3066c422d5b7ec93038a60078871d4b43c51c9df268afa9a0ac363b18c7e292a",
    "french_ff_factors_csv_2026-09-update.zip": "593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66",
    "ici_per32_01_data.xlsx": "d6fd8052b5621288194a79665d8e2d74cb977922a6628f03b849c64a3f5c2d70",
    "z1_owner_occupied_extract.csv": "6148186b68d2d404e32ac425689eca0c130fa3282c989616f9bec225ae1efab2",
}

PMMS = "freddiemac_pmms_historicalweeklydata.xlsx"       # mortgage rate and points (R4, R5, R9)
DLM = "aei_dlm_rent_price_ratio_2018q2.xlsx"             # level A to 2018Q2 (R3)
FHFA_AT = "fhfa_hpi_at_us_and_census.csv"                # the value from 1975Q1 (R2), R14's price
FHFA_PO = "fhfa_hpi_po_us_and_census.txt"                # level A's extension (SA, R3) and R15.3 (NSA)
NEW_HOUSE = "census_nrs_price_sold_cust.xlsx"            # the 1972 to 1974 bridge (R2)
Z1 = "z1_owner_occupied_extract.csv"                     # value bases (R2, R3, R7c)
Z1_PACKAGE = "frb_z1_csv_2026-09-11.zip"                 # the extract's source (extract_z1.py)
NIPA = "bea_nipadataa_ia20261020095433.txt"              # DOSTRC (R3), upkeep and depreciation (R2, R7c)
FA = "bea/bea_fixedassets_ia20250202204946.txt"          # owner-occupied share (R7c)
FA_REGISTER = "bea/bea_fa_seriesregister_ia20250207173438.txt"
FA_BOOK = "bea/bea_fa_section5all_ia20250202204948.xlsx"
CPI = "bls_cu_data_12_ushousing_ia20261029154324.txt"   # OER for level A (R3), the CPI rent path (R15.1)
FRENCH = "french_ff_factors_csv_2026-09-update.zip"      # market return (R8)
ICI = "ici_per32_01_data.xlsx"                           # fund fee (R8)
RCPIURS = "bls_rcpiurs_allitems_ia20260819.xlsx"         # 2025 dollars (R14)
COH = "census_coh_values_unadj.txt"                      # R14's price base
ACS_POSITIONS = "acs/acs_positions.csv"                  # property tax (R7a), insurance (R7b), R15.5 and R15.6
AHS_VALUES = "ahs/ahs_values.csv"                        # property tax (R7a), insurance (R7b)
COST_VALUES = "costs/cost_values.csv"                    # insurance (R7b), loan costs (R5), R15.5, R15.6

NIPA_SERIES = ("DOSTRC", "DOWNRC", "B1300C", "W307RC", "W316RC", "B2607C", "A946RC")
FA_SERIES = {"k1r53101esoo": "FAAt501:11", "k1r53101es00": "FAAt501:2"}   # R7c (A2): owner-occupied over private
Z1_SERIES = ("LM155035015", "FL155035013")
CPI_SERIES = ("CUSR0000SEHC01", "CUUR0000SEHA", "CUUR0000SEHC01")
QUARTER_END = {3: 1, 6: 2, 9: 3, 12: 4}


def path(rel: str) -> str:
    """The absolute path of a pinned data file, after checking its SHA-256; a mismatch stops the script."""
    if rel not in FILES:
        raise SystemExit(f"{rel}: not a pinned data file")
    p = os.path.join(DATA, rel)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    if h.hexdigest() != FILES[rel]:
        raise SystemExit(f"{rel}: sha256 {h.hexdigest()} is not the pinned {FILES[rel]}")
    return p


def check_hashes() -> None:
    for rel in FILES:
        path(rel)


def _rows(rel: str, sheet: str) -> list[tuple]:
    """All rows of one worksheet, values only (openpyxl's warning about unparsed page headers silenced)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        wb = openpyxl.load_workbook(path(rel), data_only=True, read_only=True)
        try:
            return list(wb[sheet].iter_rows(values_only=True))
        finally:
            wb.close()


def _num(text: str) -> float:
    return float(str(text).replace(",", "").replace("$", "").strip())


# --- mortgage (Freddie Mac PMMS) ----------------------------------------------------------------------------------------

def read_pmms() -> list[tuple[tuple[int, int, int], float, float | None]]:
    """PMMS weekly file, sheet 'Full History': (week date, U.S. 30-year fixed rate in percent, 30-year fees and points,
    or None where the cell is blank)."""
    rows = _rows(PMMS, "Full History")
    if rows[4][1:3] != ("U.S.", "30 yr") or rows[5][1:3] != ("30 yr", "fees &") or rows[6][:3] != ("Week", "FRM", "points"):
        raise SystemExit(f"{PMMS}: unexpected header {rows[4][:3]} {rows[5][:3]} {rows[6][:3]}")
    out = []
    for r in rows[7:]:
        if not isinstance(r[0], datetime.datetime):
            continue
        if not isinstance(r[1], (int, float)):
            raise SystemExit(f"{PMMS}: no rate on {r[0]:%Y-%m-%d}")
        if isinstance(r[2], (int, float)):
            points = float(r[2])
        elif r[2] is None or str(r[2]).strip() == "":
            points = None
        else:
            raise SystemExit(f"{PMMS}: points cell {r[2]!r} on {r[0]:%Y-%m-%d}")
        out.append(((r[0].year, r[0].month, r[0].day), float(r[1]), points))
    return out


# --- rent-to-price ratios ---------------------------------------------------------------------------------------------

def read_dlm() -> dict[tuple[int, int], float]:
    """Davis, Lehnert and Martin, sheet 'rent-price data', column F (FHFA purchase-only after 2000):
    {(year, quarter): ratio}. Dates are stored as year + quarter / 10 with float drift (2018.1999999999866)."""
    rows = _rows(DLM, "rent-price data")
    if rows[0][4] != "FHFA purchase only after 2000" or rows[1][0] != "Date" or rows[1][5] != "rent-price ratio":
        raise SystemExit(f"{DLM}: unexpected header {rows[0][:6]} {rows[1][:6]}")
    out = {}
    for r in rows[2:]:
        if r[0] is None:
            continue
        y, q = divmod(round(r[0] * 10), 10)
        if not 1 <= q <= 4 or abs(r[0] - (y + q / 10)) > 1e-6 or (y, q) in out:
            raise SystemExit(f"{DLM}: unexpected date {r[0]!r}")
        out[(y, q)] = float(r[5])
    keys = sorted(out)
    expected = [(y, q) for y in range(keys[0][0], keys[-1][0] + 1) for q in (1, 2, 3, 4)]
    if keys != [k for k in expected if k <= keys[-1]]:
        raise SystemExit(f"{DLM}: quarters are not contiguous")
    return out


def read_fhfa_at() -> dict[tuple[int, int], float]:
    """FHFA all-transactions index, USA, not seasonally adjusted, quarterly: {(year, quarter): index}."""
    out = {}
    with open(path(FHFA_AT), encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) != 4:
                raise SystemExit(f"{FHFA_AT}: row {row}")
            if row[0] == "USA":
                out[(int(row[1]), int(row[2]))] = float(row[3])
    return out


def read_fhfa_po() -> dict[tuple[int, int], tuple[float, float]]:
    """FHFA purchase-only index, USA: {(year, quarter): (not seasonally adjusted, seasonally adjusted)}."""
    with open(path(FHFA_PO), encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    head = lines[0].split("\t")
    if head != ["division", "year", "qtr", "index_po_not_seasonally_adjusted", "index_po_seasonally_adjusted"]:
        raise SystemExit(f"{FHFA_PO}: unexpected header {head}")
    out = {}
    for line in lines[1:]:
        p = line.split("\t")
        if p[0] == "USA":
            out[(int(p[1]), int(p[2]))] = (float(p[3]), float(p[4]))
    return out


def read_new_house_index() -> dict[int, float]:
    """Census constant-quality (Laspeyres) price index of new single-family houses sold, United States, annual index
    (2005 = 100), for every year with one."""
    rows = _rows(NEW_HOUSE, "Price Index")
    hdr = next(i for i, r in enumerate(rows) if r[0] == "Year")
    if rows[hdr][1] != "Annual index" or rows[hdr - 1][1] != "United States":
        raise SystemExit(f"{NEW_HOUSE}: column B is {rows[hdr - 1][1]!r} / {rows[hdr][1]!r}")
    out = {}
    for r in rows[hdr + 1:]:
        if not isinstance(r[0], int):
            break
        if isinstance(r[1], (int, float)):
            out[r[0]] = float(r[1])
    return out


def read_z1() -> dict[str, dict[tuple[int, int], float]]:
    """Federal Reserve Z.1 extract: {series: {(year, quarter): millions of dollars}} for LM155035015 and
    FL155035013, quarter-end levels."""
    out = {s: {} for s in Z1_SERIES}
    with open(path(Z1), encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            code = r["series"].removesuffix(".Q")
            if code not in out or r["unit_mult"] != "Millions":
                raise SystemExit(f"{Z1}: unexpected row {r}")
            y, m, _ = (int(x) for x in r["date"].split("-"))
            out[code][(y, QUARTER_END[m])] = float(r["value"])
    return out


# --- BEA national accounts and fixed assets ----------------------------------------------------------------------------

def _flat(rel: str, codes) -> dict[str, dict[int, float]]:
    """A BEA flat file ('%SeriesCode,Period,Value', annual periods): {code: {year: value}} for the codes asked."""
    out = {c: {} for c in codes}
    with open(path(rel), encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        if next(reader) != ["%SeriesCode", "Period", "Value"]:
            raise SystemExit(f"{rel}: unexpected header")
        for code, period, value in reader:
            if code in out:
                if not re.fullmatch(r"\d{4}", period):
                    raise SystemExit(f"{rel}: {code} period {period}")
                out[code][int(period)] = _num(value)
    return out


def read_nipa() -> dict[str, dict[int, float]]:
    """NIPA annual flat file (2026 vintage), millions of dollars: DOSTRC (R3), DOWNRC, B1300C, W307RC (published
    negative), W316RC, A946RC (R7c) and B2607C (R2)."""
    return _flat(NIPA, NIPA_SERIES)


def read_fa() -> dict[str, dict[int, float]]:
    """BEA Fixed Assets flat file (2024 vintage), Table 5.1 current-cost net stock, year-end, millions of dollars:
    line 11 (owner-occupied) and line 2 (private), after checking the series register names those lines."""
    lines = {}
    with open(path(FA_REGISTER), encoding="utf-8", newline="") as fh:
        for r in csv.reader(fh):
            if r and r[0] in FA_SERIES:
                lines[r[0]] = r[5]
    for code, line in FA_SERIES.items():
        if line not in lines.get(code, "").split("|"):
            raise SystemExit(f"{FA_REGISTER}: {code} is {lines.get(code)!r}, not {line}")
    return _flat(FA, FA_SERIES)


def read_fa_book() -> dict[str, dict[int, float]]:
    """The same two lines of Table 5.1 as printed in the Section 5 workbook, for the cross-check."""
    rows = _rows(FA_BOOK, "FAAt501-A")
    hdr = next(r for r in rows if r[0] == "Line")
    out = {}
    for r in rows:
        if r[2] in FA_SERIES:
            out[r[2]] = {int(y): float(v) for y, v in zip(hdr[3:], r[3:]) if y is not None and v is not None}
    return out


# --- stocks and fees ---------------------------------------------------------------------------------------------------

_FRENCH_ROW = re.compile(r"^\s*(\d{6}),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\s*$")


def read_french() -> tuple[dict[tuple[int, int], tuple[float, float]], str]:
    """Fama/French 3 Factors, monthly section: ({(year, month): (Mkt-RF, RF)} in percent, the file's copyright line)."""
    with zipfile.ZipFile(path(FRENCH)) as z:
        if z.namelist() != ["F-F_Research_Data_Factors.csv"]:
            raise SystemExit(f"{FRENCH}: members {z.namelist()}")
        lines = z.read("F-F_Research_Data_Factors.csv").decode("latin-1").splitlines()
    if lines[4].replace(" ", "") != ",Mkt-RF,SMB,HML,RF":
        raise SystemExit(f"{FRENCH}: unexpected header {lines[4]!r}")
    out = {}
    for line in lines[5:]:
        m = _FRENCH_ROW.match(line)
        if not m:
            break
        out[(int(m.group(1)[:4]), int(m.group(1)[4:]))] = (float(m.group(2)), float(m.group(5)))
    rights = [l.strip() for l in lines if l.strip().startswith("Copyright")]
    if len(rights) != 1:
        raise SystemExit(f"{FRENCH}: copyright lines {rights}")
    return out, rights[0]


def read_ici() -> dict[int, float]:
    """ICI Figure S3: index equity mutual funds, asset-weighted average expense ratio, percent: {year: value}."""
    rows = _rows(ICI, "S3")
    if rows[4][4] != "Index equity" or rows[5][0] != "Year" or rows[5][4] != "Asset-weighted average":
        raise SystemExit(f"{ICI}: column E is {rows[4][4]!r} / {rows[5][4]!r}")
    return {r[0]: float(r[4]) for r in rows[6:] if isinstance(r[0], int) and isinstance(r[4], (int, float))}


# --- prices: CPI, R-CPI-U-RS, Census 2000 --------------------------------------------------------------------------------

def read_cpi() -> dict[str, dict[tuple[int, int], float | None]]:
    """BLS LABSTAT cu.data.12.USHousing: {series: {(year, month): index, or None where BLS published '-'}}, months
    M01 to M12 only."""
    out = {s: {} for s in CPI_SERIES}
    with open(path(CPI), encoding="latin-1") as fh:
        head = [h.strip() for h in next(fh).split("\t")]
        if head[:4] != ["series_id", "year", "period", "value"]:
            raise SystemExit(f"{CPI}: unexpected header {head}")
        for line in fh:
            p = [x.strip() for x in line.rstrip("\n").split("\t")]
            if p[0] in out and re.fullmatch(r"M(0[1-9]|1[0-2])", p[2]):
                out[p[0]][(int(p[1]), int(p[2][1:]))] = None if p[3] == "-" else float(p[3])
    return out


def read_rcpiurs() -> dict[int, dict]:
    """BLS R-CPI-U-RS, all items: {year: {'avg': the AVG column as stored, 'months': the twelve monthly cells}}."""
    rows = _rows(RCPIURS, "All items")
    hdr = next(r for r in rows if r[0] == "YEAR")
    if list(hdr[1:]) != ["JAN", "FEB", "MAR", "APR", "MAY", "JUNE", "JULY", "AUG", "SEP", "OCT", "NOV", "DEC", "AVG"]:
        raise SystemExit(f"{RCPIURS}: unexpected header {hdr}")
    return {r[0]: {"avg": float(r[13]), "months": list(r[1:13])} for r in rows
            if isinstance(r[0], int) and isinstance(r[13], (int, float))}


def read_census_value() -> tuple[int, int]:
    """Census of Housing, median value of specified owner-occupied units, United States, unadjusted:
    (the year of the first column, 2000, and its value), from the header line and line 5."""
    with open(path(COH), encoding="latin-1") as fh:
        lines = fh.read().splitlines()
    years = lines[2].split()
    if not lines[4].startswith("United States") or years[0] != "2000":
        raise SystemExit(f"{COH}: unexpected layout {lines[2]!r} {lines[4][:30]!r}")
    return int(years[0]), int(_num(re.findall(r"\$[\d,]+", lines[4])[0]))


# --- ACS, AHS, cost values ------------------------------------------------------------------------------------------------

_FIELD = re.compile(r"value: field (\d+)")
_COLUMN = re.compile(r"value: column (B\d+_E\d+)")
_SEQUENCE = re.compile(r"sequence (\d{4}); comma-separated, no header, (\d+) fields per record")
_GEO = re.compile(r"United States: (\S+) line (\d+)")


def _us_line(rel: str, line_no: int) -> None:
    """The geography file's line for the record read must be the United States."""
    with open(path(rel), encoding="latin-1") as fh:
        line = fh.read().splitlines()[line_no - 1]
    if "United States" not in line or not ("01000US" in line or "0100000US" in line):
        raise SystemExit(f"{rel} line {line_no} is not the United States: {line[:80]!r}")


def _sequence_cell(rel: str, field: int, sequence: str, n_fields: int) -> float:
    with open(path(rel), encoding="latin-1") as fh:
        rows = [r for r in csv.reader(fh) if len(r) > 5 and r[5] == "0000001"]
    if len(rows) != 1 or rows[0][4] != sequence or len(rows[0]) != n_fields:
        raise SystemExit(f"{rel}: LOGRECNO 0000001 record not as described (sequence {sequence}, {n_fields} fields)")
    return float(rows[0][field - 1])


def _table_cell(rel: str, column: str) -> float:
    with open(path(rel), encoding="latin-1") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="|") if r["GEO_ID"] == "0100000US"]
    if len(rows) != 1:
        raise SystemExit(f"{rel}: {len(rows)} United States rows")
    return float(rows[0][column])


def read_acs() -> dict[tuple[int, str], float]:
    """Every cell in acs/acs_positions.csv, read as its how_to_find column says: {(year, cell): value}."""
    with open(path(ACS_POSITIONS), encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = {}
    for r in rows:
        rel, how = r["file"].removeprefix("data/"), r["how_to_find"]
        geo = _GEO.search(how)
        if not geo:
            raise SystemExit(f"{ACS_POSITIONS}: no United States line named for {r['year']} {r['cell']}")
        _us_line("acs/" + geo.group(1), int(geo.group(2)))
        if (field := _FIELD.search(how)) is not None:
            seq = _SEQUENCE.search(how)
            if seq is None:
                raise SystemExit(f"{ACS_POSITIONS}: no sequence for {r['year']} {r['cell']}")
            value = _sequence_cell(rel, int(field.group(1)), seq.group(1), int(seq.group(2)))
        elif (column := _COLUMN.search(how)) is not None:
            value = _table_cell(rel, column.group(1))
        else:
            raise SystemExit(f"{ACS_POSITIONS}: no position for {r['year']} {r['cell']}")
        key = (int(r["year"]), r["cell"])
        if key in out:
            raise SystemExit(f"{ACS_POSITIONS}: {key} listed twice")
        out[key] = value
    return out


def _value_rows(rel: str, prefix: str) -> dict[tuple[str, int], float]:
    """A step-3 value table: {(name, year): value as printed}; every row's source document must be a pinned file."""
    with open(path(rel), encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = {}
    for r in rows:
        doc = prefix + r["file"].removeprefix("data/").removeprefix(prefix)
        if doc not in FILES:
            raise SystemExit(f"{rel}: {r['name']} {r['year']} cites {r['file']}, which is not pinned")
        key = (r["name"], int(r["year"]))
        if key in out:
            raise SystemExit(f"{rel}: {key} listed twice")
        out[key] = _num(r["value_as_printed"])
    return out


def read_ahs_values() -> dict[tuple[str, int], float]:
    """AHS values read from the H150 volumes by two readers (data/ahs/ahs_values.csv): {(name, year): value}."""
    return _value_rows(AHS_VALUES, "ahs/")


def read_cost_values() -> dict[tuple[str, int], float]:
    """NAIC, AHS 2023 and CFPB values read by two readers (data/costs/cost_values.csv): {(name, year): value}."""
    return _value_rows(COST_VALUES, "costs/")


# --- profile ----------------------------------------------------------------------------------------------------------------

def span(keys) -> str:
    ks = sorted(keys)
    return f"{ks[0]} to {ks[-1]}, {len(ks)} entries"


def main() -> None:
    check_hashes()
    print(f"all {len(FILES)} files under data/ match their pinned sha256")

    weeks = read_pmms()
    years = range(1972, 2026)
    rate_weeks = {y: sum(1 for d, _, _ in weeks if d[0] == y) for y in years}
    point_weeks = {y: sum(1 for d, _, p in weeks if d[0] == y and p is not None) for y in years}
    months_without = [(y, m) for y in years for m in range(1, 13)
                      if not any(d[:2] == (y, m) and p is not None for d, _, p in weeks)]
    print(f"PMMS weeks {weeks[0][0]} to {weeks[-1][0]} ({len(weeks)}); rate weeks per year 1972 to 2025: "
          f"{min(rate_weeks.values())} to {max(rate_weeks.values())}")
    print(f"  points weeks per year: {', '.join(f'{y} {n}' for y, n in point_weeks.items() if n != 52)} (others 52)")
    print(f"  last week with points {max(d for d, _, p in weeks if p is not None)}; months 1972 to 2025 without "
          f"points: {months_without[:3]} ... {months_without[-1]} ({len(months_without)})")
    print(f"  months 1972 to 2025 without a rate week: "
          f"{[(y, m) for y in years for m in range(1, 13) if not any(d[:2] == (y, m) for d, _, _ in weeks)]}")
    print(f"  weeks with points dated 2018 to 2022 (p_fix): {sum(point_weeks[y] for y in range(2018, 2023))}")

    dlm = read_dlm()
    print(f"DLM column F: {span(dlm)}; 1972Q1 {dlm[(1972, 1)]:.6f}, 2018Q2 {dlm[(2018, 2)]:.6f}")
    at, po = read_fhfa_at(), read_fhfa_po()
    print(f"FHFA all-transactions USA: {span(at)}; 1975Q1 {at[(1975, 1)]}, 2025Q4 {at[(2025, 4)]}")
    print(f"FHFA purchase-only USA: {span(po)}; 1991Q1 {po[(1991, 1)]}, 2018Q2 {po[(2018, 2)]}, 2025Q4 {po[(2025, 4)]}")
    cq = read_new_house_index()
    print(f"Census new-house index: {span(cq)}; 1971 to 1975: {[cq[y] for y in range(1971, 1976)]}")

    z1 = read_z1()
    for code, d in z1.items():
        full = [y for y in range(1970, 2026) if all((y, q) in d for q in (1, 2, 3, 4))]
        print(f"Z.1 {code}: {span(d)}; years 1970 to 2025 with four quarter-ends: {len(full)}")
    nipa = read_nipa()
    for code, d in nipa.items():
        print(f"NIPA {code}: {span(d)}; 1972 {d.get(1972)}, 2025 {d.get(2025)}")
    fa, book = read_fa(), read_fa_book()
    for code, d in fa.items():
        same = [y for y in d if book[code].get(y) == d[y]]
        print(f"FA {code} ({FA_SERIES[code]}): {span(d)}; flat file equals the workbook in {len(same)} of {len(d)} years")
    print(f"  owner-occupied over private, year-end: 1972 {fa['k1r53101esoo'][1972] / fa['k1r53101es00'][1972]:.4f}, "
          f"2023 {fa['k1r53101esoo'][2023] / fa['k1r53101es00'][2023]:.4f} (2024 and 2025 hold 2023's, A2)")

    french, rights = read_french()
    print(f"French monthly: {span(french)}; {rights}")
    ici = read_ici()
    print(f"ICI index equity asset-weighted: {span(ici)}; 1996 {ici[1996]}, 2025 {ici[2025]}")
    cpi = read_cpi()
    for code, d in cpi.items():
        missing = [k for k, v in d.items() if v is None]
        print(f"CPI {code}: {span(d)}; unpublished months {missing}")
    rs = read_rcpiurs()
    eleven = [v for v in rs[2025]["months"] if isinstance(v, (int, float))]
    print(f"R-CPI-U-RS AVG: {span(rs)}; 1996 {rs[1996]['avg']}, 2025 {rs[2025]['avg']} as stored (R14) against "
          f"{sum(eleven) / len(eleven):.4f}, the mean of the {len(eleven)} published 2025 months")
    print(f"Census median value of specified owner-occupied homes: {read_census_value()}")

    acs = read_acs()
    print(f"ACS cells read from acs_positions.csv: {len(acs)}")
    print("R7a cross-check (A2), 2010 to 2019: ACS aggregate ratio B25090/B25082 | ratio of medians B25103/B25077")
    medians = ("B25103_001", "B25077_001")
    unpinned = [f"{y} {c}" for y in range(2010, 2020) for c in medians if (y, c) not in acs]
    for y in list(range(2010, 2020)) + [2025]:
        agg = acs[(y, "B25090_001")] / acs[(y, "B25082_001")]
        lost = [c for c in medians if (y, c) not in acs]
        med = f"{acs[(y, medians[0])] / acs[(y, medians[1])]:.5f}" if not lost else f"not pinned: {', '.join(lost)}"
        print(f"  {y}: {agg:.5f} | {med}")
    print(f"  B25103_001 is pinned for {[y for y, c in acs if c == 'B25103_001']}; B25077_001 for "
          f"{[y for y, c in acs if c == 'B25077_001']}")

    ahs = read_ahs_values()
    for name in sorted({n for n, _ in ahs}):
        print(f"AHS {name}: {[(y, ahs[(n, y)]) for n, y in sorted(ahs) if n == name]}")
    costs = read_cost_values()
    for name in sorted({n for n, _ in costs}):
        print(f"cost {name}: {[(y, costs[(n, y)]) for n, y in sorted(costs) if n == name]}")
    forms = sum(costs[(f"naic_premium_{f}", 2023)] for f in ("ho1", "ho2", "ho3", "ho5", "ho8"))
    total = costs[("naic_premium_total_dw_and_owner_forms", 2023)] - costs[("naic_premium_dw", 2023)]
    print(f"NAIC 2023 HO-1 + HO-2 + HO-3 + HO-5 + HO-8 = {forms:,.0f}; Total less DW = {total:,.0f} (R15.5)")

    lm, fl = z1["LM155035015"], z1["FL155035013"]
    for y in (1972, 1980, 1990, 2000, 2010, 2025):
        base_b = sum(fl[(y, q)] for q in (1, 2, 3, 4)) / 4
        base_scope = sum(lm[(y, q)] for q in (1, 2, 3, 4)) / 4
        print(f"R3 level B {y}: DOSTRC/FL155035013 {nipa['DOSTRC'][y] / base_b:.5f}; scope check DOWNRC/LM155035015 "
              f"{nipa['DOWNRC'][y] / base_scope:.5f}")
    if unpinned:
        raise SystemExit(f"R7a (A2): the 2010 to 2019 check needs both measures; no pinned ACS value for "
                         f"{', '.join(unpinned)}")


if __name__ == "__main__":
    main()
