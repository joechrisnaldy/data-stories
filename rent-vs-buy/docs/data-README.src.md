# Data for Post 30

The data files are not committed. Each file in `data/` is frozen by its sha256, which `profile_data.py` checks before the build reads anything; a file that does not match stops the build. A fresh download may differ and then needs a new vet.

`docs/provenance-audit.md` records the definition behind each variable from its defining document. Its Appendix A lists each file below with its size, address, transport and retrieval time, and its Appendix B does the same for each stored document in `sources/`, which are not committed either. The blocks below are generated from Appendix A. Where a file came through the Internet Archive, the block gives the original address and the capture's.

## Home values

- **FHFA House Price Index**, United States, quarterly: the all-transactions index, not seasonally adjusted, for the home's value; the purchase-only index, seasonally adjusted, for rent level A after the Davis, Lehnert and Martin workbook ends; and the purchase-only index, not seasonally adjusted, for the purchase-only run. FHFA's notice: This product uses FHFA data but is neither endorsed nor certified by FHFA.
- **New houses, before the FHFA index starts.** U.S. Census Bureau and U.S. Department of Housing and Urban Development, Survey of Construction: the constant-quality (Laspeyres) price index of new single-family houses sold.

```
data/fhfa_hpi_at_us_and_census.csv    580d761c3488f3e9a6f25074bdace5de96f476f579c06eeb7144835e8f52deba
  https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_at_us_and_census.csv
data/fhfa_hpi_po_us_and_census.txt    4776cd3261d1a5ba71701d2fd7c934184d86494b7b2332ba6b20afa63fae1fea
  https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_us_and_census.txt
data/census_nrs_price_sold_cust.xlsx  9b48bfe97fa5e6c9b654eea90017b7d29502dc660f15db0d15d41cd3aa6bcfd3
  https://www.census.gov/construction/nrs/xls/price_sold_cust.xlsx
```

## Mortgage rates and loan costs

- **Freddie Mac, Primary Mortgage Market Survey**, weekly: the 30-year fixed rate, and its fees and points until Freddie Mac stopped publishing them. Freddie Mac's site terms keep its data to internal or personal use and bar automated access, so I downloaded this file by hand in a browser. The survey's file and page allow use with attribution, and the file is not redistributed. To rebuild, download it from the survey page (https://www.freddiemac.com/pmms) and check its hash.
- **Consumer Financial Protection Bureau**, 2023 Mortgage Market Activity and Trends: median total loan costs and median loan amounts, for the loan's other costs.

```
data/freddiemac_pmms_historicalweeklydata.xlsx                        3066c422d5b7ec93038a60078871d4b43c51c9df268afa9a0ac363b18c7e292a
  https://www.freddiemac.com/pmms/docs/historicalweeklydata.xlsx
  the owner's hand download in a browser; not redistributed
data/costs/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf  7aaeadcd06a98abfff9c6c5f957493d2783f19a85752f618efea562867271c58
  https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf
```

## Rent of the same home

- **Level A.** The rent-price ratio of Davis, Lehnert and Martin (2008) for the aggregate stock of owner-occupied housing, quarterly, with data from the AEI Housing Center; no relationship with AEI is implied. I downloaded the workbook by hand in a browser. AEI's housing terms give no licence to re-host it, so it is not redistributed; download it from the address below and check its hash. After the workbook ends, level A continues with BLS owners' equivalent rent of primary residence over FHFA's purchase-only index.
- **Level B.** BEA imputed rental of owner-occupied stationary homes, from the national income and product accounts, over the Federal Reserve's Financial Accounts of the United States value of households' owner-occupied real estate. The Z.1 package holds a very large file, so `extract_z1.py` streams it once and writes `data/z1_owner_occupied_extract.csv`.

```
data/aei_dlm_rent_price_ratio_2018q2.xlsx           eba71363889d5207a140c1600c3395fc847b2f04bbc148bb45978190207efb9e
  https://www.aei.org/wp-content/uploads/2018/10/RENT-PRICE-RATIO.2018q2.xlsx
  the same bytes are in Internet Archive capture https://web.archive.org/web/20200229184452id_/https://www.aei.org/wp-content/uploads/2018/10/RENT-PRICE-RATIO.2018q2.xlsx
  the owner's hand download in a browser; not redistributed
data/bls_cu_data_12_ushousing_ia20261029154324.txt  b2ecc4021ea612ee9acf3629f2cbcfc7e1b063338ee5ede5ae10d74512019704
  https://download.bls.gov/pub/time.series/cu/cu.data.12.USHousing
  Internet Archive capture: https://web.archive.org/web/20261029154324id_/https://download.bls.gov/pub/time.series/cu/cu.data.12.USHousing
data/bea_nipadataa_ia20261020095433.txt             9f8e96bb72181d14d7b555f3e1b09c71e900fb8de4c305dc9217424de4757f27
  https://apps.bea.gov/national/Release/TXT/NipaDataA.txt
  Internet Archive capture: https://web.archive.org/web/20261020095433id_/https://apps.bea.gov/national/Release/TXT/NipaDataA.txt
data/frb_z1_csv_2026-09-11.zip                      83b8eded0bc7f9b74c0269ef503a863cee88312460fd7eef076284b98fc28c06
  https://www.federalreserve.gov/releases/z1/data/FRB_Z1_csv.zip
data/z1_owner_occupied_extract.csv                  6148186b68d2d404e32ac425689eca0c130fa3282c989616f9bec225ae1efab2
  written by extract_z1.py from data/frb_z1_csv_2026-09-11.zip
```

## Property tax

- **Annual Housing Survey and American Housing Survey**, U.S. Census Bureau, national volumes of Current Housing Reports Series H150: real estate taxes as a share of value. The older volumes are scans with no text layer. The values read from them are in `data/ahs/ahs_values.csv`; each was read from a page image by independent readers and an adjudicator (`docs/provenance-audit.md`, section on property tax).
- **American Community Survey**, U.S. Census Bureau, the yearly summary files for the United States: real estate taxes paid and home values. The cells read are named in `data/acs/acs_positions.csv`.

```
data/ahs/ahs2005_tab3-13.xls  c01b2c412da2bb532ee296661249c3311fff1610384b618a97bc8e566f0e988e
  https://www2.census.gov/programs-surveys/ahs/2005/tables/tab3-13.xls
data/ahs/ahs_values.csv       bd053dbc9ed39abee158f94fb97871515af66f2b6e92f0ecd3808ffa53d987c3
  written when the data were gathered; docs/provenance-audit.md records how
data/ahs/h150-01.pdf          3acb2a1f3256312388ae0a6a1e6832e0ae1a608a0e74e4e475d1d80a71777e4b
  https://www.census.gov/content/dam/Census/library/publications/2002/demo/h150-01.pdf
data/ahs/h150-03.pdf          7290bc7aa4ac7cc50ff6681fd44400142a3a14edcf080c29abd47abb3bb54952
  https://www.census.gov/content/dam/Census/library/publications/2004/demo/h150-03.pdf
data/ahs/h150-05.pdf          0d650398c6f27bef6bee719fd0f0211e275fcae5b035ba46d3fd43ebff9ba6d4
  https://www.census.gov/content/dam/Census/library/publications/2006/demo/h150-05.pdf
data/ahs/h150-73C.pdf         3b09ae95f37928c8902f02e248793f8e04bcd09cc7e442e610dfdb9881b6ea58
  https://www2.census.gov/prod2/ahsscan/h150-73C.pdf
data/ahs/h150-74C.pdf         5b5ca1889104e9b5c80b48b3512e70deaaf3185853b43db9623e554c8d615c96
  https://www2.census.gov/prod2/ahsscan/h150-74C.pdf
data/ahs/h150-75c.pdf         4a78e44e102e4ba0dbb9ee4fd13becc7368616d92c22b0e7c5084bb0982d93df
  https://www2.census.gov/prod2/ahsscan/h150-75c.pdf
data/ahs/h150-76c.pdf         70821d0e3dfb36cc0e34b2436a8b2da9d1ed86be15c2a5d9a19dd844aa37d0a8
  https://www2.census.gov/prod2/ahsscan/h150-76c.pdf
data/ahs/h150-77c.pdf         67fa042e80b7cc8efcd18a906bd7ac61de722a46ac1f05473e51d41449e47683
  https://www2.census.gov/prod2/ahsscan/h150-77c.pdf
data/ahs/h150-78c.pdf         de5df29505654408a3a434a4f2f286eae2f442a453910d66156554ffcd377cc2
  https://www2.census.gov/prod2/ahsscan/h150-78c.pdf
data/ahs/h150-79c.pdf         9c0b86f639ed575d01511373dc22f70b885088316f11a2b80e961acf112a12bc
  https://www2.census.gov/prod2/ahsscan/h150-79c.pdf
data/ahs/h150-80c.pdf         edee8daca928aad50bb23fac6da138ddb2a12b679d49163f650f047ea85d9e2b
  https://www2.census.gov/prod2/ahsscan/h150-80c.pdf
data/ahs/h150-81c.pdf         a8de836a79740dc2f63f1336108b03988cdeee7821eca9466eee67840ab04f7e
  https://www2.census.gov/prod2/ahsscan/h150-81c.pdf
data/ahs/h150-83c.pdf         e812976483cfccc9cb1deb0b1138f4eff3ef361c7bf2275d21f2ac9c483ec474
  https://www2.census.gov/prod2/ahsscan/h150-83c.pdf
data/ahs/h150-85.pdf          ce594322f219f8c25ec7545d0d744e7d8cc4022937c80c2fcf107a07efcfaa26
  https://www2.census.gov/prod2/ahsscan/h150-85.pdf
data/ahs/h150-87.pdf          4aa9a964223b2f5433d8be483f8451f656f727f9f163281bb86b1cc4fb601202
  https://www2.census.gov/prod2/ahsscan/h150-87.pdf
data/ahs/h150-89.pdf          f5ae55204c086dfa148b90ac1ea602400c5ea959b1ce1c895c47a8ed172bc34f
  https://www2.census.gov/prod2/ahsscan/h150-89.pdf
data/ahs/h150-91.pdf          a4e901e877bbd86838aeae3b157ae177c69e8acdda6dd5fb040de5c8d245d360
  https://www2.census.gov/prod2/ahsscan/h150-91.pdf
data/ahs/h150-97.pdf          db3f5afeffaa6fa78388985f7548f25b444f3ae2a1110d5c31c713af7393284a
  https://www.census.gov/content/dam/Census/library/publications/1999/demo/h150-97.pdf
data/ahs/h150-99-rv.pdf       c2ed3215a035ff58a344bee30c84595e1565cd5011c378fbeb5d60e3e56fa4d1
  https://www.census.gov/content/dam/Census/library/publications/2003/demo/h150-99-rv.pdf
data/ahs/h150_93.pdf          cc886645197b8bfdd25a51a7ef477d0ae742454f7579078647a586451c4d7d7d
  https://www.census.gov/content/dam/Census/library/publications/1995/demo/h150_93.pdf
data/ahs/h150_95rv.pdf        f7e74b356a35b500b7e9df09005e213793bf5129f8b9c8382a638f4faa7d7e45
  https://www.census.gov/content/dam/Census/library/publications/1997/demo/h150_95rv.pdf
```

```
data/acs/20061us0130000.zip      b2abf6e8c4034530b0c85f8fa136023030c2b50ee0388c6865c501810708e112
  https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0130000.zip
data/acs/20061us0131000.zip      be2e87784dd23dc9335393d4b6e7afa7303b7c004436d8eca656f8da2c4c62de
  https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0131000.zip
data/acs/20071us0135000.zip      315ffe752f8f2d1769924a3d50556bccddfcc982360665200d8143a2f5ce5b96
  https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0135000.zip
data/acs/20071us0136000.zip      79a1c945f67390d9c77d62f255cd49d9306111270b910aa6f304f73b30c13105
  https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0136000.zip
data/acs/20081us0139000.zip      81e6eabd821ab564daffc1d5967e2485178a3f51219bb9daabe8f7a0ae197d61
  https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0139000.zip
data/acs/20081us0140000.zip      620d1ada604d712e02a564694738e6268232dd6a89577daab0bf1bcb8becb5cc
  https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0140000.zip
data/acs/20091us0150000.zip      b1a434da8bfcaad9141cf4fe030f14c7bba35c32aed5c51ea0bf5f221922b95b
  https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0150000.zip
data/acs/20091us0151000.zip      af4d1ed4e0c89758aabd473e5de9f24ea42e09098e9305c62f177f2419920106
  https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0151000.zip
data/acs/20101us0150000.zip      83f7c3296fab5298e6b2d01547e2f0b9af38a93097e8fcc74b379b0da13563c2
  https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0150000.zip
data/acs/20101us0151000.zip      cacefb40b20545dec4a1e643ebdf05f36d5208a703242c07806835be9e2f076c
  https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0151000.zip
data/acs/20111us0156000.zip      09ffcd907b358561e9e49339045c143b6d2ca4ea583ad2268825a9b179a8ed85
  https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0156000.zip
data/acs/20111us0158000.zip      725aad4877332153011a101df4721404c0a07a893a33c1c243e686345da63552
  https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0158000.zip
data/acs/20121us0156000.zip      ad004a2a781e091bc52f6e1aba48708ad42727c037c7908f8e908e376967736c
  https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0156000.zip
data/acs/20121us0158000.zip      219b9f798a5b51704c552d8dad4ab6bd1bfabd6c23bd8fbcbe2da644125e80cc
  https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0158000.zip
data/acs/20131us0147000.zip      6cfb4cddb45f7d66274a1c4f428233043c2f216d2fb50d0bbebc60fce89f161d
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0147000.zip
data/acs/20131us0148000.zip      cb496701d7a356726cd03ffaacb104532f0bd26efd5570ae597c96803ad5979f
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0148000.zip
data/acs/20131us0149000.zip      0de206de2028ae1faaa19812d82dead69aaaa17bb9dbcf19113a3c1dfbc71b1e
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0149000.zip
data/acs/20141us0142000.zip      d07a2433845a3d77cdcfc3ac0a4f4e25f05fc5546eace082528b7dfb928d40bb
  https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0142000.zip
data/acs/20141us0144000.zip      cb516aa038db9e411067f715ca8f0eb85d450f5c3c20bed41f97a7d8b64a0b21
  https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0144000.zip
data/acs/20151us0142000.zip      6a1a37f7cd281f2605d7546eae62d0b0ce51cae723f19b727c6c094dd330e497
  https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0142000.zip
data/acs/20151us0144000.zip      d24a0abb3bfb2b0023212fe6f056283e2418ebef535fa4ec5493e15e847e49b7
  https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0144000.zip
data/acs/20161us0143000.zip      eac638abfa4d6cdd604108b52d015f714329124fc0dcc250f2b5b00d01db6b22
  https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0143000.zip
data/acs/20161us0145000.zip      ccf69d66d113b99f83a61b750fbbe3ab084cbb1919d71af0bfdaf5de185629ba
  https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0145000.zip
data/acs/20171us0143000.zip      48acf6545a2dcdf280abcc84bb3a7285a8f4c505fdc1e7445277c611a310462b
  https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0143000.zip
data/acs/20171us0145000.zip      d731127fb98bb05c1b7e49efa96d908b3f53d52a481265d1a6957fa5b3262586
  https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0145000.zip
data/acs/20181us0152000.zip      34572a5d5979222c9bba567f57bf913ad5abcaf663b243b7c11c0653311e2b6b
  https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0152000.zip
data/acs/20181us0154000.zip      89965287fa62b2e62d01061b2bf92ff0d909dd7fc5cc988c1662e0b3a5fd0f6c
  https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0154000.zip
data/acs/20191us0151000.zip      9b5836dc0b1dbd725ca6c46e8568ac3dff1e14842459ed7b2f62729308c27b18
  https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0151000.zip
data/acs/20191us0153000.zip      b000aa74d49ceac807e1faace6f4d8154c1d8e115485d1a34fd0716869faa466
  https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0153000.zip
data/acs/Geos20211YR.txt         f24e9ac0d255cf38d20c0c23ebed6b6874b181f462f417b522304047a03286ea
  https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/documentation/Geos20211YR.txt
data/acs/Geos20221YR.txt         f29667153e72ac95a5a76b87725cf1e509b53bd5611802432a04f06806e8b63f
  https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/documentation/Geos20221YR.txt
data/acs/Geos20231YR.txt         d0e8ca5b28243016f89cb20588675ff6ace83cac503cf0273ec3f2ee7f9fcb62
  https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/documentation/Geos20231YR.txt
data/acs/Geos20241YR.txt         2155acb3c81672eee9b0bd971cca60cd77d8b66222b34973928f57c087ea4afe
  https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/documentation/Geos20241YR.txt
data/acs/Geos20251YR.txt         c8e9250ae8d2632bff4c9e800e5880722ea2cbd899a81c3ef071165fea13e387
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/documentation/Geos20251YR.txt
data/acs/acs_positions.csv       03d07a97de59164c51c1aa76f1b737c9fc4c2841d365f019d74b0e434bf8242a
  written when the data were gathered; docs/provenance-audit.md records how
data/acs/acsdt1y2021-b25077.dat  0bc6d61db91997024c5cdfa07b43c692ffbe8f417dcdf9853db83f1ad21d5e40
  https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25077.dat
data/acs/acsdt1y2021-b25082.dat  997448ed26bcc1741c5cfcc86a66433df6482865087ce46330679800c76deb93
  https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25082.dat
data/acs/acsdt1y2021-b25090.dat  f56d8908d9743a75de1d657e4b044824a01c6ff303c6edfdc7dbcb82b16d7737
  https://www2.census.gov/programs-surveys/acs/summary_file/2021/table-based-SF/data/1YRData/acsdt1y2021-b25090.dat
data/acs/acsdt1y2022-b25077.dat  2ce7a81314c8290186972e1675f3fbea3bfd19dab53cd8f206c2964130a40eb5
  https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25077.dat
data/acs/acsdt1y2022-b25082.dat  28a4407f22248834a64d624d0786775eaa6d18bd62502f862f6894a9334f8bc6
  https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25082.dat
data/acs/acsdt1y2022-b25090.dat  8327d702e247c98d705174d07eb9d39ebe289c13121c3f15bb9394e72bc518e7
  https://www2.census.gov/programs-surveys/acs/summary_file/2022/table-based-SF/data/1YRData/acsdt1y2022-b25090.dat
data/acs/acsdt1y2023-b25077.dat  c39987ce683bc4ac8d5831ac9fb67cbcdfaa9bbb81193bc3af4582ad97353723
  https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25077.dat
data/acs/acsdt1y2023-b25082.dat  302624aa5a8374f126a686ba948bca4b508b13e17efeeb882f175275d123303c
  https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25082.dat
data/acs/acsdt1y2023-b25090.dat  4cf509db1f0379673ed44c666b842211523504bf9a2bc76d6ff6b77ca7c2c433
  https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b25090.dat
data/acs/acsdt1y2024-b25082.dat  7b35e18067f951a57338d88bb31a16f59f4a1d607f632a9a11e39b1462950b2f
  https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/1YRData/acsdt1y2024-b25082.dat
data/acs/acsdt1y2024-b25090.dat  60f95c0745c34d9bd9d4dfca86d09947f463ef61c76d0e525b0b4b80a018810b
  https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/1YRData/acsdt1y2024-b25090.dat
data/acs/acsdt1y2025-b25077.dat  7ab895b182348af2e79cb31e45717be5fdcc38ab1e1ad959cb4e0e7e9393b772
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25077.dat
data/acs/acsdt1y2025-b25082.dat  4db69c6f29eee4d7fe117c5c9dc054be8c1bf7f64cfb6ab29c8a6065b0b9a3c7
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25082.dat
data/acs/acsdt1y2025-b25090.dat  de416cf2b861cfe14e30ce1278a87d813fa30693450d7f6415e8e1b555a5ecd0
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25090.dat
data/acs/acsdt1y2025-b25103.dat  4f3ee59fbf3149db9a06cb1f5a4e3170dc19668d6c69f33f5123127e63c068b3
  https://www2.census.gov/programs-surveys/acs/summary_file/2025/table-based-SF/data/1YRData/acsdt1y2025-b25103.dat
data/acs/e20061us0130000.txt     e6d7c16c7a80ff4657383e9926d03498baa696dc473cc41aabcd5ede115fa519
  https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0130000.zip
data/acs/e20061us0131000.txt     88114192d147aa8553e696717fb2ed9fa452cb44547ae4174cc97286b265b907
  https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/20061us0131000.zip
data/acs/e20071us0135000.txt     6c635a50710b0c36ce623cac9bd01c7265ea2d81dd2ad11e5f9ec59cdbd598a6
  https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0135000.zip
data/acs/e20071us0136000.txt     00549c1f8a72736ad463018cd41529526886a1df9470b9a7b47a07c596bbd281
  https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/20071us0136000.zip
data/acs/e20081us0139000.txt     639a6a60b8067e99424d6b54356f80cfbad99a9b016b4331ef78b09386d7b352
  https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0139000.zip
data/acs/e20081us0140000.txt     13eaeacd3e1fd77c76ede695a6493817c7b2ec3c16d2b1a61a9a87dfc6059d00
  https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/20081us0140000.zip
data/acs/e20091us0150000.txt     4662d04733325728e21704570c21c46387c8e7a7a0e338df45c89682816dd573
  https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0150000.zip
data/acs/e20091us0151000.txt     f58b1aacdc398b42f899f36f32f058a3d31c7b65c01dff590fd09aaa3422977a
  https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/20091us0151000.zip
data/acs/e20101us0150000.txt     7d8f4ab67c41f527488a3795f7e1b1e966ae6eaac021357ad5a436bdf9514b25
  https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0150000.zip
data/acs/e20101us0151000.txt     f53205c5efb1ec10c4a803e0678ef1525b8dff89d1571376ab846808d3f9c05a
  https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/20101us0151000.zip
data/acs/e20111us0156000.txt     50bf52bd064307d940d2b4f7ec44971371de92c1cbd9eac87c4460fe2988c49d
  https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0156000.zip
data/acs/e20111us0158000.txt     73879742f9bc6137f7db076f08fa4e369c051ab965ae6e2d432cd6be424500af
  https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/20111us0158000.zip
data/acs/e20121us0156000.txt     fb52e05f835faa69639bc3b77a81de43f57d16c6db253de2d100c60137c90790
  https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0156000.zip
data/acs/e20121us0158000.txt     912df931e195c60aa65e6a50e2e65e35ecdd2198b99aead8d5875b10035d04bb
  https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/20121us0158000.zip
data/acs/e20131us0147000.txt     28cfe09295507016b5293eef51cd8441b5e8c3ccc3c881ae12213468f922bd31
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0147000.zip
data/acs/e20131us0148000.txt     2738c276973199440e7e044b54e8dbcf37aafe74d2cb8825c46888eed63e875b
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0148000.zip
data/acs/e20131us0149000.txt     6c6a170125c9364c6503c1222f9c095bcdd5552c306c1767e66ab67cf7103156
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/20131us0149000.zip
data/acs/e20141us0142000.txt     a5bb4d346f17b471258edf521d3c4aa6f36e60c42c1e223c7c05711573450b53
  https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0142000.zip
data/acs/e20141us0144000.txt     73e5d351a39588f0a6a1c0fecfc15abb4254fbd96ae3310ce186bee19c0ac3ce
  https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/20141us0144000.zip
data/acs/e20151us0142000.txt     31b17e35a546887c98acbc8dbac1f24a11e798a097cebf5a20ae018dcea9e1b6
  https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0142000.zip
data/acs/e20151us0144000.txt     1aba27110677e45b19454ca3679d876aa9dace8e05f93e75b07add18923a9492
  https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/20151us0144000.zip
data/acs/e20161us0143000.txt     74b5d1e575b4fd0c370ac4052f1f7bc0b77ef35b661c0fa1e90f78bc943daed1
  https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0143000.zip
data/acs/e20161us0145000.txt     f3257a271f9a266cefa028e78e3352e13edbe94e36e78ca43afd63b1d6d41664
  https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/20161us0145000.zip
data/acs/e20171us0143000.txt     d1f21c574e54f7bc2a8af2675c9a4c0e21a8a1bb80e2afc98fe1e4d44282ba9d
  https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0143000.zip
data/acs/e20171us0145000.txt     7321f29445167f1ba3f936e34acd0c34658f7149d3d4d3ab48c422dcf2e969fc
  https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/20171us0145000.zip
data/acs/e20181us0152000.txt     cf27883c0fd5eb47bcc4f7c8735ba00941d4d638ec96a348d4636cafcb10f929
  https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0152000.zip
data/acs/e20181us0154000.txt     b48d93a94d86425b6a3f8dbe0cbe917d119f97ee0bf8de482fd0579de5adc1e3
  https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/20181us0154000.zip
data/acs/e20191us0151000.txt     27f8d7f196e17ffe6e2ca04928b65a59c6c1093f797703a22c1112ef4bb13382
  https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0151000.zip
data/acs/e20191us0153000.txt     0c94948f7cd7898aaecd029ec334e8971022a09f90e010b65832d795dca05e86
  https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/20191us0153000.zip
data/acs/g20061us.txt            f1c042bbbfa9ec5b2d5092908807ed619c182cc71107a93c3cdd46c44d952054
  https://www2.census.gov/programs-surveys/acs/summary_file/2006/data/UnitedStates/g20061us.txt
data/acs/g20071us.txt            aaf411a7d3b8dce3199cb888d8b0825f8fcacbd0ae4fbdf597f002bf0b1efdbc
  https://www2.census.gov/programs-surveys/acs/summary_file/2007/data/1_year/UnitedStates/g20071us.txt
data/acs/g20081us.txt            a3c98376dee89be5c550e79320bfbef0b464e69f233c3385a40488b85159e7c3
  https://www2.census.gov/programs-surveys/acs/summary_file/2008/data/1_year/UnitedStates/g20081us.txt
data/acs/g20091us.txt            a9ff9999965571f4b3bdf0beab7517ac3325601acbba902984ce7773203fbb0c
  https://www2.census.gov/programs-surveys/acs/summary_file/2009/data/1_year_seq_by_state/US/g20091us.txt
data/acs/g20101us.csv            ff65f55adc0ee315f47b46f52dde4f2ebb43bdc640d9df2671562dafc64eb070
  https://www2.census.gov/programs-surveys/acs/summary_file/2010/data/1_year_seq_by_state/UnitedStates/g20101us.csv
data/acs/g20111us.csv            d8d030ca15ccf0c9cc70af5ff6790a8fc075dde9d21fc81af1c8a98bbc5a04f4
  https://www2.census.gov/programs-surveys/acs/summary_file/2011/data/1_year_seq_by_state/UnitedStates/g20111us.csv
data/acs/g20121us.csv            223a2b16ba94e530cf1ce40bb69f8eff6835acf4f39e37d92aec2eee5c08736f
  https://www2.census.gov/programs-surveys/acs/summary_file/2012/data/1_year_seq_by_state/UnitedStates/g20121us.csv
data/acs/g20131us.csv            43437cbe1a45c8267557c249810583ea8e7fd4e01c7f2fed754d7d800dd791b5
  https://www2.census.gov/programs-surveys/acs/summary_file/2013/data/1_year_seq_by_state/UnitedStates/g20131us.csv
data/acs/g20141us.csv            dc53d7e85e4498a9a2fa9dc7d4c2539ac53e7d5a21d1e675f0d48a31535bc846
  https://www2.census.gov/programs-surveys/acs/summary_file/2014/data/1_year_seq_by_state/UnitedStates/g20141us.csv
data/acs/g20151us.csv            6639a6c9e28ae3bedd3afd6011c1e657519fac07b9a7d3d2b051d6fcf8726f45
  https://www2.census.gov/programs-surveys/acs/summary_file/2015/data/1_year_seq_by_state/UnitedStates/g20151us.csv
data/acs/g20161us.csv            40d2be3d5f62daf1c2884a0cc02cc91df7f20e582ae8c1c90820744b50438b97
  https://www2.census.gov/programs-surveys/acs/summary_file/2016/data/1_year_seq_by_state/UnitedStates/g20161us.csv
data/acs/g20171us.csv            0a6123de31cb6f16ee3c07ea5b3c9688f3cec63526e903018b4a2928e7666a65
  https://www2.census.gov/programs-surveys/acs/summary_file/2017/data/1_year_seq_by_state/UnitedStates/g20171us.csv
data/acs/g20181us.csv            b1fc6c533d3845290dace40990081a19c1dfa6927d6b95c7129b5965bc4ebde2
  https://www2.census.gov/programs-surveys/acs/summary_file/2018/data/1_year_seq_by_state/UnitedStates/g20181us.csv
data/acs/g20191us.csv            50a9f92f62fc816741f2a6b83b7660385442aa952da392e6bea6134b96a27af2
  https://www2.census.gov/programs-surveys/acs/summary_file/2019/data/1_year_seq_by_state/UnitedStates/g20191us.csv
data/acs/us0000131.2005-1yr.zip  e54d1b1665fba6adb09f63437f515539df2d59842a525a9f487acbadf193e857
  https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000131.2005-1yr.zip
data/acs/us0000131e.2005-1yr     3f7330b8b6510c72db25cac7c2c5deacac53fc5057c7c1ed4e3bfadce663edeb
  https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000131.2005-1yr.zip
data/acs/us0000132.2005-1yr.zip  54bd413d0376865cd1fe1b106c560918276af58df5857300f6b27c5e1dde9b57
  https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000132.2005-1yr.zip
data/acs/us0000132e.2005-1yr     1c887775b63b2995cc832f7ebdb7cef5a227a6ee64728858a989f9e5abf3786b
  https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/us0000132.2005-1yr.zip
data/acs/usgeo.2005-1yr          b31eb15ca45a56eda05b76a52d7e54b79e2c468c4dab63ca336f2cca53560513
  https://www2.census.gov/programs-surveys/acs/summary_file/2005/data/0UnitedStates/usgeo.2005-1yr
```

## Insurance and upkeep

- **Insurance.** The National Association of Insurance Commissioners' homeowners insurance reports, Internet Archive copies, with the American Housing Survey's median property insurance payment. NAIC's individual figures are cited; no NAIC table is reproduced.
- **Upkeep.** BEA's national accounts (owner-occupied housing's intermediate inputs and residential improvements) and fixed assets (the owner-occupied share of residential assets), over the Financial Accounts value. In the lower owner-costs run, upkeep is instead the American Housing Survey's routine maintenance costs over its mean value, from the table specifications file below. The values the build reads from the cost reports are in `data/costs/cost_values.csv`.

```
data/costs/naic_homeowners_report_dy2021_ia20240217020958.pdf  b1c98f9c1753730593a0c9329f23d6e44168aa0459ba2c020867a94b5d57c638
  https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
  Internet Archive capture: https://web.archive.org/web/20240217020958id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
data/costs/naic_homeowners_report_dy2022_ia20250706013631.pdf  369718e3f64767077c1639902d8a053c42b3110a2dd0c3cf802ca4658ca69858
  https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
  Internet Archive capture: https://web.archive.org/web/20250706013631id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
data/costs/naic_homeowners_report_dy2023_ia20261011104807.pdf  b157866e6656e17041416665557867f4effe77b7b124656a747d2833ea9f4739
  https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
  Internet Archive capture: https://web.archive.org/web/20261011104807id_/https://content.naic.org/sites/default/files/publication-hmr-zu-homeowners-report.pdf
data/costs/census_ahs2023_table_specs_puf_estimates.xlsx       f94af71db86b11562252823f64ffad919e88ec0f6802a9d91dd8c8732b9b9b0e
  https://www2.census.gov/programs-surveys/ahs/2023/AHS%202023%20Table%20Specifications%20and%20PUF%20Estimates%20for%20User%20Verification.xlsx
data/costs/cost_values.csv                                     9b5767862bad96824aa0d608867a8f2e42bc9a04a43831c0ba728c97d267974e
  written when the data were gathered; docs/provenance-audit.md records how
data/bea/bea_fa_section5all_ia20250202204948.xlsx              afb5988f9cebac83bfc0bd30ca5c0921c5c024363d92231711815058b785844d
  https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx
  Internet Archive capture: https://web.archive.org/web/20250202204948id_/https://apps.bea.gov/national/FixedAssets/Release/XLS/Section5All_xls.xlsx
data/bea/bea_fa_seriesregister_ia20250207173438.txt            fc902fc813dfeea585df24435b4a3ea689429d28c366bef6e97925a215b89d4a
  https://apps.bea.gov/national/FixedAssets/Release/TXT/SeriesRegister.txt
  Internet Archive capture: https://web.archive.org/web/20250207173438id_/https://apps.bea.gov/national/FixedAssets/Release/TXT/SeriesRegister.txt
data/bea/bea_fixedassets_ia20250202204946.txt                  d880b8dfb5eb92e541f066ba8445a85d0df568bd1e7642a1c9790772ca5721fe
  https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt
  Internet Archive capture: https://web.archive.org/web/20250202204946id_/https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt
```

## Stocks and the fund fee

- **Kenneth R. French Data Library**, Fama/French 3 factors, monthly: the market return is Mkt-RF plus RF, with dividends reinvested. The file's last line is its copyright line, Copyright {{inputs.french_copyright.year:year}} Eugene F. Fama and Kenneth R. French, which the post repeats. The raw file is not redistributed.
- **Investment Company Institute**, Trends in the Expenses and Fees of Funds: the asset-weighted average expense ratio of index equity mutual funds. ICI's values are cited with attribution (www.ici.org); no ICI table or chart is reproduced, and ICI says its averages are not meant as a benchmark for a single investor's fees.

```
data/french_ff_factors_csv_2026-09-update.zip  593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66
  https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/Historical_Archives/09%202026%20Update/ftp/F-F_Research_Data_Factors_CSV.zip
data/ici_per32_01_data.xlsx                    d6fd8052b5621288194a79665d8e2d74cb977922a6628f03b849c64a3f5c2d70
  https://www.ici.org/files/2026/per32-01-data.xlsx
  Internet Archive capture: https://web.archive.org/web/20260325214944id_/https://www.ici.org/files/2026/per32-01-data.xlsx
```

## Dollars for the {{household.start:year}} household

- **Home value.** U.S. Census Bureau, historical census of housing tables: the median value of specified owner-occupied homes in {{household.census_year:year}}.
- **Prices.** U.S. Bureau of Labor Statistics, the consumer price index retroactive series using current methods, R-CPI-U-RS, annual averages.

```
data/census_coh_values_unadj.txt           5fbabee6743983f4f39b61c6e42cc9a5727c2266173344ec3fc0381b06a221b6
  https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-values/values-unadj.txt
data/bls_rcpiurs_allitems_ia20260819.xlsx  355ea8a14a6d07d777a17a1ddad526b8a199390a7c1bb8c7b58e2dec1a2544d8
  https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx
  Internet Archive capture: https://web.archive.org/web/20260819055403id_/https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx
```

## Files written from the others

These files in `data/` are written from the files above and pinned like them. `data/z1_owner_occupied_extract.csv` is written by `extract_z1.py`. `data/acs/acs_positions.csv`, `data/ahs/ahs_values.csv` and `data/costs/cost_values.csv` were written when the data were gathered, and `docs/provenance-audit.md` records how each value in them was read and checked; the scripts that wrote them are not in this folder.

## Licences and credits

- BLS, the Census Bureau, BEA, the Federal Reserve Board and CFPB publish these data as public domain; each is cited.
- FHFA: the notice above, and the credit Source: FHFA HPI®, all-transactions, not seasonally adjusted, nominal (home values); FHFA HPI®, purchase-only, seasonally adjusted, nominal (rent level A after the Davis, Lehnert and Martin workbook ends); FHFA HPI®, purchase-only, not seasonally adjusted, nominal (the purchase-only run).
- Freddie Mac: used with attribution; the file is not redistributed.
- AEI Housing Center: named as the data source, with no relationship implied; the workbook is not redistributed.
- Kenneth R. French Data Library: credited with the file's copyright line.
- ICI and NAIC: values cited with attribution; no table reproduced.
- Internet Archive: named for each file retrieved through it. Its terms ask research that uses its collections to list the archive in the bibliography, and the post does.
- The post is non-commercial, and no publisher of these data endorses it.

## Rebuild

With the files above in place, from the post folder:

```bash
pip install -r requirements.txt
python3 -m unittest test_rentbuy
python3 -I extract_z1.py
python3 -I profile_data.py
python3 -I build_analysis.py
python3 -I make_charts.py
```
