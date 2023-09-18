import streamlit as st
import pandas as pd
from csv import writer
st.write("Analyse bien immobilier")

with st.expander("infos bien") :
    nom_bien=st.text_input("Bien")
    link_annonce=st.text_input("Lien de l'annonce")
    localisation=st.text_input("Adresse du bien")
    surface=st.number_input("Surface",min_value=0,step=10)
    prix_affiché=st.number_input("Prix affiché",min_value=0,step=1000)

    if surface ==0:
        surface=1

    prixm2=prix_affiché/surface
    st.write("Prix de base au m² : " +str(prixm2)+" €")

with st.expander("Travaux"):
    montant_tvx=st.number_input("Montant Travaux",min_value=0,step=1000)
    gestion_tvx=round(montant_tvx*0.03,2)
    st.text("Gestion travaux : "+str(gestion_tvx))
    total_tvx=montant_tvx+gestion_tvx
    st.text("total travaux : "+str(total_tvx))


with st.expander("Financement") :
    taux_nego=st.number_input("Taux de négociation %",min_value=0,step=1)
    nego=prix_affiché*taux_nego/100
    st.text("négociation : " + str(nego) )
    taux_notaire=8
    prix_acquisition = prix_affiché-nego
    frais_notaire =prix_acquisition*taux_notaire/100
    st.text("pris acquisition : "+ str(prix_acquisition))
    st.text("Frais de notaire : "+str(frais_notaire))

    apport=st.number_input("Apport",min_value=0,step=1000)
    pret_brut=prix_acquisition+total_tvx
    frais_bq=0.01*(pret_brut)
    st.text("frais bancaires : "+str(frais_bq))
    pret_net=pret_brut+frais_notaire+frais_bq-apport
    st.text("montant total du crédit : "+str(pret_net))
    duree_pret=20
    taux_pret=5.94
    mens_pret_m=round((pret_net*taux_pret/100/12)/(1-pow(1+(taux_pret/100)/12,-duree_pret*12)),2)
    mens_pret_a=mens_pret_m*12

    st.text("Mensualité prêt : "+str(mens_pret_m))
    st.text("Mensualités annuelles : "+str(mens_pret_a))


with st.expander("Rentabilité"):
    revenu_loc_classique=st.number_input("Revenus location classique")
    taxe_fonciere=st.number_input("Taxe fonciere")
    charge_copro=st.number_input("charges de copropriété")
    assurance_pno=st.number_input("assurance")
    frais_gestion=st.number_input("frais de gestion")
    frais_conciergerie=st.number_input("frais de conciergerie")
    frais_compta=st.number_input("frais de comptabilité")
    impôt=st.number_input("impôt")
    autre_frais=st.number_input("autres frais")

    total_charges=taxe_fonciere+charge_copro+assurance_pno+frais_gestion+frais_conciergerie+frais_compta+impôt+autre_frais

    if prix_acquisition==0:
        prix_acquisition=1

    rdmt_brut=revenu_loc_classique/prix_acquisition
    rdmt_net=(revenu_loc_classique-charge_copro)/(prix_acquisition+total_tvx)

    cash_annuel=revenu_loc_classique-total_charges-mens_pret_a
    cash_mensuel=cash_annuel/12

    st.text("Total charges : "+str(total_charges))
    st.text("Rendement brut : "+str(rdmt_brut))
    st.text("Rendement net : " + str(rdmt_net))
    st.text("cashflow annuel : "+str(cash_annuel))
    st.text("cashflow mensuel : "+str(cash_mensuel))

with st.expander("Enrichissement latent"):
    annee=5
    taux_progr_marche=1.5
    def capital_rembourse(annee):
        round(pret_net*(pow(1+taux_pret/100/12,annee*12)-1)/(pow(1+taux_pret/100/12,duree_pret*12)-1),2)
        return

    def total_cashflow(annee):
        round(cash_annuel*annee,2)
        return

    def plus_value_potentielle(annee):
        round((pret_net+apport)*pow(1+taux_progr_marche/100,annee)-(pret_net+apport),2)
        return


    st.text("a 5 ans  : capital rembourse : "+str(capital_rembourse) +" cashflow :"+str(total_cashflow)+" PV :"+ str(plus_value_potentielle) )

    table=list(range(1,duree_pret+1))
    df=pd.DataFrame(table, columns=["Années d'amortissement"])

    #st.write(df)

    #df["capital"]=df["Années d'amortissement"].apply(capital_rembourse)
    #df["cashflow"]=df["Années d'amortissement"].apply(total_cashflow)
    #df["PV"]=df["Années d'amortissement"].apply(plus_value_potentielle)

    st.write(df)


with st.expander("Questions"):
    a=[1,2,3]
    z=[]
    for i in a:
        x=st.checkbox(str(i))
        st.write(x)
        z.append(x)
    st.write(z)





if st.button("enregistrer"):
    with open("./data.csv","a") as f_object:
        writer_object=writer(f_object)
        writer_object.writerow([nom_bien,link_annonce,localisation,surface,prix_affiché,prixm2,montant_tvx,gestion_tvx,total_tvx,taux_nego,nego,taux_notaire,prix_acquisition,frais_notaire,apport,pret_brut,frais_bq,pret_net,duree_pret,taux_pret,mens_pret_m,mens_pret_a,revenu_loc_classique,taxe_fonciere,charge_copro,assurance_pno,frais_gestion,frais_conciergerie,frais_compta,impôt,autre_frais,total_charges,rdmt_brut,rdmt_net,cash_annuel,cash_mensuel,
])
        f_object.close()
        st.write("enregistré")

st.write(pd.read_csv("./data.csv",sep=",",encoding="latin-1"))



