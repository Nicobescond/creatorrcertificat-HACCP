import streamlit as st
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Certificat HACCP",
    page_icon="🏆",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .certificate-container {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 2rem;
        background: white;
        font-family: Arial, sans-serif;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .cert-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .company-name {
        font-size: 1.5em;
        font-weight: bold;
        margin: 1rem 0;
        text-align: center;
        color: #333;
    }
    
    .cert-details {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: left;
    }
    
    .signature-section {
        text-align: right;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
    
    .calculated-dates {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .cert-info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin: 20px 0;
        font-size: 0.9em;
        text-align: left;
    }
    
    .cert-info-full {
        grid-column: 1/-1;
    }
    
    @media (max-width: 768px) {
        .cert-info-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
def calculate_dates(audit_date):
    """Calcule les dates selon les règles IFS Food"""
    if not audit_date:
        return None, None, None
    
    # Date d'expiration: Date d'audit + 1 an + 8 semaines - 1 jour
    expiry_date = audit_date + timedelta(days=365) + timedelta(weeks=8) - timedelta(days=1)
    
    # Fenêtre d'audit de recertification
    audit_anniversary = audit_date + timedelta(days=365)
    audit_window_start = audit_anniversary - timedelta(weeks=8)
    audit_window_end = audit_anniversary + timedelta(weeks=2)
    
    return expiry_date, audit_window_start, audit_window_end

def format_date(date, format_type="fr"):
    """Formate les dates selon le type demandé"""
    if not date:
        return "-"
    
    if format_type == "fr":
        return date.strftime("%d/%m/%Y")
    else:  # format UK pour le certificat
        return date.strftime("%d/%m/%Y")

def generate_certificate_html(company_name, address, audit_scope, audit_date, issue_date, 
                            certificate_number, expiry_date, audit_window_start, audit_window_end):
    """Génère le HTML du certificat"""
    
    certificate_html = f"""
    <div class="certificate-container">
        <div class="cert-header">
            <div style="font-size: 0.8em; color: #666; text-align: left;">F-HACCP-04</div>
            <div style="font-size: 0.7em; color: #666; margin: 10px 0; line-height: 1.4;">
                ECOCERT Environnement SAS – Capital 37.000 € – 36 Boulevard de la Bastille, 75012 Paris<br>
                SIREN 409 982 709 RCS PARIS - Tél. +33 (0)1 53 44 74 44– www.ecocert.com
            </div>
            
            <div style="font-size: 2em; font-weight: bold; color: #333; margin: 1rem 0;">
                ENVIRONNEMENT 🌿<br>
                <span style="font-size: 1.2em;">ECOCERT</span>
            </div>
            
            <div style="font-size: 1.5em; font-weight: bold; color: #333; margin: 1rem 0; text-transform: uppercase; letter-spacing: 2px;">
                CERTIFICATE OF CONFORMITY<br>HACCP
            </div>
        </div>

        <div style="text-align: center; line-height: 1.6;">
            <p>By this letter, Ecocert Environnement SAS, as a Control Body, certifies that:</p>
            
            <div class="company-name">
                {company_name}
            </div>
            
            <div style="margin: 15px 0; line-height: 1.4;">
                {address.replace(chr(10), '<br>')}
            </div>

            <div class="cert-details">
                <strong>For the audit scope:</strong><br><br>
                {audit_scope.replace(chr(10), '<br>')}
            </div>

            <p style="margin: 20px 0; text-align: justify;">
                Comply with the recommendations described in the Codex Alimentarius GENERAL PRINCIPLES 
                OF FOOD HYGIENE Guide, No. CAC/RCP 1-1969, Rev. 6 (2022) according to the program 
                requirements defined by Ecocert in the F-HACCP-01 audit checklist and the C-HACCP-01 audit 
                process.
            </p>

            <div class="cert-info-grid">
                <div><strong>Certificate No.:</strong> {certificate_number}</div>
                <div><strong>Audit Date:</strong> {format_date(audit_date, "uk")}</div>
                <div><strong>Date of issue:</strong> {format_date(issue_date, "uk")}</div>
                <div><strong>End date of validity:</strong> {format_date(expiry_date, "uk")}</div>
                <div class="cert-info-full"><strong>Next audit period:</strong> {format_date(audit_window_start, "uk")} – {format_date(audit_window_end, "uk")}</div>
            </div>

            <div class="signature-section">
                <div style="margin-top: 30px;">
                    <div style="border-bottom: 1px solid #333; width: 200px; margin-left: auto;"></div>
                    <div style="margin-top: 10px;">
                        <strong>Nicolas BESCOND</strong><br>
                        Head of Department<br>
                        Food Quality and Safety
                    </div>
                </div>
            </div>

            <div style="font-size: 0.7em; color: #666; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                This document is the property of Ecocert Environnement SAS. It must be returned on request. Only the signed original is valid.<br><br>
                ECOCERT Environnement SAS – Capital 37.000 € – 36 Boulevard de la Bastille, 75012 Paris<br>
                SIREN 409 982 709 RCS PARIS - Tél. +33 (0)1 53 44 74 44– www.ecocert.com
            </div>
        </div>
    </div>
    """
    
    return certificate_html

# Interface principale
st.markdown("""
<div class="main-header">
    <h1>🏆 Générateur de Certificat HACCP</h1>
    <p>Conforme aux standards Ecocert Environnement</p>
</div>
""", unsafe_allow_html=True)

# Colonnes pour l'interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Informations de l'entreprise")
    
    company_name = st.text_input(
        "Nom de l'entreprise *", 
        value="JUICING EXPERTS SAC",
        help="Nom complet de l'entreprise à certifier"
    )
    
    address = st.text_area(
        "Adresse complète *", 
        value="CENTRO INDUSTRIAL\nLAS PRADERAS DE LURIN\nMZ A LT 14-LURIN\nLIMA-PERÚ",
        help="Adresse complète avec ville et pays",
        height=100
    )
    
    audit_scope = st.text_area(
        "Périmètre d'audit *", 
        value="Pasteurized and frozen juices of ginger, turmeric, pineapple,\nlemon & passion fruit and by-products (starch and sediments of ginger and\nturmeric)\npacked in bulk and in polythene bags and in buckets or cylinders",
        help="Description détaillée des produits et processus audités",
        height=120
    )
    
    st.header("📅 Dates et certification")
    
    audit_date = st.date_input(
        "Date d'audit initial *",
        value=datetime(2025, 1, 21),
        help="Date du premier jour de l'audit initial"
    )
    
    issue_date = st.date_input(
        "Date d'émission du certificat *",
        value=datetime.now(),
        help="Date d'émission du certificat"
    )
    
    certificate_number = st.text_input(
        "Numéro de certificat *",
        value="25HACCP001",
        help="Numéro unique du certificat"
    )
    
    # Calcul automatique des dates
    if audit_date:
        expiry_date, audit_window_start, audit_window_end = calculate_dates(audit_date)
        
        st.markdown("""
        <div class="calculated-dates">
            <h3>📊 Dates calculées automatiquement :</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col_exp, col_audit = st.columns(2)
        with col_exp:
            st.metric("Date d'expiration", format_date(expiry_date))
        with col_audit:
            st.info(f"**Période audit de recertification:**\n\n{format_date(audit_window_start)} – {format_date(audit_window_end)}")

with col2:
    st.header("📄 Aperçu du certificat")
    
    # Validation des champs obligatoires
    if all([company_name, address, audit_scope, audit_date, issue_date, certificate_number]):
        
        # Génération du certificat
        certificate_html = generate_certificate_html(
            company_name, address, audit_scope, audit_date, issue_date,
            certificate_number, expiry_date, audit_window_start, audit_window_end
        )
        
        # Affichage du certificat
        st.markdown(certificate_html, unsafe_allow_html=True)
        
        # Bouton de téléchargement
        st.markdown("---")
        
        # Création du fichier HTML pour téléchargement
        full_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certificat HACCP - {company_name}</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 20px; 
            background: white;
        }}
        .certificate-container {{ 
            border: 2px solid #ddd; 
            padding: 2rem; 
            background: white; 
            max-width: 800px;
            margin: 0 auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .company-name {{ 
            font-size: 1.5em; 
            font-weight: bold; 
            margin: 1rem 0; 
            text-align: center; 
            color: #333;
        }}
        .cert-details {{ 
            background: #f8f9fa; 
            padding: 1rem; 
            border-radius: 8px; 
            margin: 1rem 0; 
            text-align: left;
        }}
        .signature-section {{ 
            text-align: right; 
            margin-top: 2rem; 
            padding-top: 1rem; 
            border-top: 1px solid #ddd; 
        }}
        .cert-info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
            font-size: 0.9em;
            text-align: left;
        }}
        .cert-info-full {{
            grid-column: 1/-1;
        }}
        @media print {{
            body {{ margin: 0; }}
            .certificate-container {{ 
                border: none; 
                box-shadow: none; 
                margin: 0;
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    {certificate_html}
</body>
</html>"""
        
        # Bouton de téléchargement HTML
        st.download_button(
            label="📥 Télécharger le certificat (HTML)",
            data=full_html,
            file_name=f"Certificat_HACCP_{certificate_number}_{company_name.replace(' ', '_').replace('/', '_')}.html",
            mime="text/html",
            use_container_width=True
        )
        
        # Bouton de génération PDF (simulation)
        if st.button("🖨️ Imprimer le certificat", use_container_width=True):
            st.success("💡 **Astuce :** Pour imprimer en PDF, téléchargez le fichier HTML puis ouvrez-le dans votre navigateur et utilisez Ctrl+P → 'Enregistrer au format PDF'")
        
    else:
        st.warning("⚠️ Veuillez remplir tous les champs obligatoires pour générer le certificat.")
        st.info("Les champs marqués d'un astérisque (*) sont obligatoires.")

# Instructions d'utilisation
st.markdown("---")
with st.expander("ℹ️ Instructions d'utilisation"):
    st.markdown("""
    ### Comment utiliser ce générateur :
    
    1. **Remplissez les informations de l'entreprise** dans la colonne de gauche
    2. **Saisissez la date d'audit initial** - les autres dates seront calculées automatiquement selon les règles IFS Food
    3. **Ajustez la date d'émission** si nécessaire
    4. **Le certificat se génère automatiquement** dans la colonne de droite
    5. **Téléchargez le fichier HTML** que vous pouvez imprimer ou convertir en PDF
    
    ### Règles de calcul des dates :
    - **Date d'expiration** : Date d'audit + 1 an + 8 semaines - 1 jour
    - **Fenêtre de recertification** : 8 semaines avant à 2 semaines après la date anniversaire de l'audit
    
    ### Pour convertir en PDF :
    1. Téléchargez le fichier HTML
    2. Ouvrez-le dans votre navigateur
    3. Appuyez sur **Ctrl+P** (ou Cmd+P sur Mac)
    4. Sélectionnez **"Enregistrer au format PDF"**
    5. Ajustez les marges si nécessaire
    """)

# Footer
st.markdown("---")
st.markdown("*Générateur de Certificat HACCP - Conforme aux standards Ecocert Environnement*")
st.markdown("*Développé par Nicolas Bescond - Version 1.0*")
