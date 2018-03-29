
text="coordinated by Prof. Shervin Shirmohammadi from Computer Science and  Engineering Department of \u015eEH\u0130R, is composed of University of Pannonia-Hungary, University of Maribor-Slovenia, ZGURA-M Ltd.-Bulgaria PhoenixKM-Belgium, Ubited-Turkey,  4flyy Ltd.-Turkey and Onda Dokuz Education Services-Turkey. 36 months-project will help to improve the quality, attractiveness and accessibility of the opportunities for lifelong learning available by developing interactive mobile games and 3D stimulations by user generated scenarios for acquiring  transversal competencies  such as social  "
n=0
for a in range(len(text)/70):
    text2 = ""
    for i in range(70):
        text2+=text[i+(a*70)]
    print text2