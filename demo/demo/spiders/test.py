urls= []
u = [("https://www.falabella.com.pe/s/browse/v1/listing/pe?page=", "&categoryId=cat40584&categoryName=Electrohogar&pgid=2&pid=b57d6999-0f3a-41e2-9828-ef706d47852d&zones=912_SANTIAGO_DE_SURCO_1%2C150140%2C912_SANTIAGO_DE_SURCO_6%2COLVAA_81%2CLIMA_URB1_DIRECTO%2C912_SANTIAGO_DE_SURCO_2%2CURBANO_83%2C912_SANTIAGO_DE_SURCO_3%2CIBIS_19%2C912_SANTIAGO_DE_SURCO_4%2C912_SANTIAGO_DE_SURCO_5%2CPERF_TEST%2C150000"),
    ("https://www.falabella.com.pe/s/browse/v1/listing/pe?page=", "&categoryId=cat40793&categoryName=Tecnologia&pgid=2&pid=16501f55-5411-4554-8ccc-79e9c14d600f&zones=OLVAA_81%2C150122%2CURBANO_83%2CIBIS_19%2C912_MIRAFLORES_3%2C912_MIRAFLORES_4%2C912_MIRAFLORES_1%2C912_MIRAFLORES_2%2CPERF_TEST%2C150000")
]



for i,v in enumerate (u):

 for e in range (200):
    urls.append(v[0]+str(e+1)+v[1])
    # for e in range (200):
    #     web  = v[i][0]+str(e+1)+v[i][1]
    #     urls.append(web)

print(urls)