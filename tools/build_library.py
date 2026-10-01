"""Single source of truth for the material library. Run: python build_library.py -> materials/*.yaml"""
from pathlib import Path
import yaml, numpy as np
OUT = Path(__file__).resolve().parents[1] / "src" / "materials_library" / "materials"
C = 2.99792458e10
EV = 8065.544005  # cm^-1 per eV

# ------------------------------------------------------------------ references
R = {
 'Olmon2012': dict(citation='R. L. Olmon et al., Optical dielectric function of gold, Phys. Rev. B 86, 235147 (2012)', doi='10.1103/PhysRevB.86.235147'),
 'Yang2015': dict(citation="H. U. Yang et al., Optical dielectric function of silver, Phys. Rev. B 91, 235137 (2015)", doi='10.1103/PhysRevB.91.235137', url='https://nano-optics.colorado.edu/wp-content/uploads/2020/06/Yang_PhysRevB_15_MainText.pdf'),
 'Derkachova2016': dict(citation='A. Derkachova, K. Kolwas, I. Demchenko, Plasmonics 11, 941 (2016)', doi='10.1007/s11468-015-0128-7'),
 'ChandlerHorowitz2005': dict(citation='D. Chandler-Horowitz, P. M. Amirtharaj, J. Appl. Phys. 97, 123526 (2005)', doi='10.1063/1.1923612'),
 'Li1980': dict(citation='H. H. Li, Refractive index of silicon and germanium..., J. Phys. Chem. Ref. Data 9, 561 (1980)', doi='10.1063/1.555624'),
 'Li1980b': dict(citation='H. H. Li, Refractive index of alkaline earth halides..., J. Phys. Chem. Ref. Data 9, 161 (1980)'),
 'Li1976': dict(citation='H. H. Li, Refractive index of alkali halides..., J. Phys. Chem. Ref. Data 5, 329 (1976)'),
 'Dore1998': dict(citation='P. Dore et al., Appl. Opt. 37, 5731 (1998) (CVD diamond)', doi='10.1364/AO.37.005731'),
 'Stephens1952': dict(citation='R. E. Stephens, I. H. Malitson, J. Res. Natl. Bur. Stand. 49, 249 (1952)'),
 'Jasperse1966': dict(citation='J. R. Jasperse et al., Phys. Rev. 146, 526 (1966) (MgO, LiF infrared dispersion) — NOT OPENED', doi='10.1103/PhysRev.146.526'),
 'Tiwald1999_doi': dict(citation='T. E. Tiwald et al., Phys. Rev. B 60, 11464 (1999)', doi='10.1103/PhysRevB.60.11464'),
 'Franta2016': dict(citation='D. Franta et al., Proc. SPIE 9890, 989014 (2016) (fused silica)', doi='10.1117/12.2227580'),
 'Kischkat2012': dict(citation='J. Kischkat et al., Mid-infrared optical properties of thin films of Al2O3, TiO2, SiO2, AlN and Si3N4, Appl. Opt. 51, 6789 (2012)', doi='10.1364/AO.51.006789'),
 'Popova1972': dict(citation='S. Popova, T. Tolstykh, V. Vorobev, Opt. Spectrosc. 33, 444 (1972) (amorphous quartz)'),
 'Querry1985': dict(citation='M. R. Querry, Optical constants, Contractor Report CRDC-CR-85034 (1985)'),
 'Querry1987': dict(citation='M. R. Querry, Optical constants of minerals and other materials..., CRDEC-CR-88009 (1987)'),
 'Rodney1956': dict(citation='W. S. Rodney, I. H. Malitson, J. Opt. Soc. Am. 46, 956 (1956) (KRS-5)', doi='10.1364/JOSA.46.000956'),
 'Skauli2003': dict(citation='T. Skauli et al., J. Appl. Phys. 94, 6447 (2003) (GaAs)'),
 'Lorimor1965': dict(citation='O. G. Lorimor, W. G. Spitzer, J. Appl. Phys. 36, 1841 (1965) (InAs)'),
 'Kaiser1962': dict(citation='W. Kaiser, W. G. Spitzer, R. H. Kaiser, L. E. Howarth, Phys. Rev. 127, 1950 (1962)', doi='10.1103/PhysRev.127.1950', url='https://github.com/polyanskiy/refractiveindex.info-scripts'),
 'Tsuda2018': dict(citation='S. Tsuda et al., Opt. Express 26, 6899 (2018) (PMMA Lorentz–Drude fit)', url='https://github.com/polyanskiy/refractiveindex.info-scripts'),
 'Beaini2020': dict(citation='R. Beaini et al., Sol. Energy Mater. Sol. Cells 205, 110260 (2020) (70 nm VO2 film on SiO2)'),
 'Frantz2023': dict(citation='J. A. Frantz et al., Opt. Mater. Express 13, 3631 (2023) (Ge2Sb2Te5)'),
 'Schubert2000': dict(citation='M. Schubert, T. E. Tiwald, C. M. Herzinger, Phys. Rev. B 61, 8187 (2000) (sapphire)', doi='10.1103/PhysRevB.61.8187', url='https://www.academia.edu/28131084/Infrared_dielectric_anisotropy_and_phonon_modes_of_sapphire'),
 'Schubert2016_preprint': dict(citation='Schubert et al., arXiv:1512.08590, earlier preprint fit (x parallel c)', url='https://arxiv.org/pdf/1512.08590'),
 'Schubert2016_published': dict(citation='Schubert et al., Phys. Rev. B 93, 125209 (2016), revised published fit (x parallel a); comparison only', doi='10.1103/PhysRevB.93.125209', url='https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.93.125209/fulltext'),
 'Mock2017': dict(citation='A. Mock et al., Phys. Rev. B 95, 165202 (2017) (CdWO4), Tables II and III', doi='10.1103/PhysRevB.95.165202', url='https://arxiv.org/abs/1701.00813'),
 'AlvarezPerez2020': dict(citation='G. Álvarez-Pérez et al., Adv. Mater. 32, 1908176 (2020) (alpha-MoO3), Table 1', doi='10.1002/adma.201908176', url='https://arxiv.org/abs/1912.06267'),
 'TaboadaGutierrez2020': dict(citation='J. Taboada-Gutiérrez et al., Nat. Mater. (2020) (alpha-V2O5), Methods section of the arXiv version', doi='10.1038/s41563-020-0665-0', url='https://arxiv.org/abs/2501.08705'),
 'Giles2018': dict(citation='A. J. Giles et al., Nat. Mater. 17, 134 (2018) (hBN isotopes), SI Table S4', doi='10.1038/nmat5047', url='https://fogler.physics.ucsd.edu/bib/Gilles2018ULP.pdf'),
 'GervaisPiriou1975': dict(citation='F. Gervais, B. Piriou, Phys. Rev. B 11, 3944 (1975) (alpha-quartz) — NOT OPENED; values as transcribed in hyperbolic_optics (MIT) material_params.json', doi='10.1103/PhysRevB.11.3944', url='https://github.com/MarkCunningham0410/hyperbolic_optics'),
 'Winta2019': dict(citation='C. J. Winta et al., Low-temperature infrared dielectric function of hyperbolic alpha-quartz, arXiv:1902.03072 (2019), Tables I-II', url='https://arxiv.org/abs/1902.03072'),
 'Lane1999': dict(citation='M. D. Lane, J. Geophys. Res. Planets 104, 14099 (1999) (calcite) — NOT OPENED; cited by Ma et al. Nature 596, 362 (2021)', doi='10.1029/1999JE900025'),
 'HyperbolicOptics': dict(citation='M. Cunningham, hyperbolic_optics, material_params.json (MIT licence), secondary transcription', url='https://github.com/MarkCunningham0410/hyperbolic_optics'),
 'Ioffe': dict(citation='Ioffe Institute NSM archive, semiconductor properties', url='https://www.ioffe.ru/SVA/NSM/Semicond/'),
 'PatrickChoyke1970': dict(citation='L. Patrick, W. J. Choyke (1970) — via Ioffe NSM', url='https://www.ioffe.ru/SVA/NSM/Semicond/SiC/optic.html'),
 'Mutschke1999': dict(citation='H. Mutschke et al., A&A 345, 187 (1999) (SiC polytypes), Table 1', url='https://arxiv.org/abs/astro-ph/9903031'),
 'Pitman2008': dict(citation='K. M. Pitman et al., A&A 483, 661 (2008) (3C-SiC)', url='https://arxiv.org/abs/0803.1210'),
 'Olego1982': dict(citation='D. Olego et al. (1982), Raman — via Ioffe NSM'),
 'Tiwald1999': dict(citation='T. E. Tiwald et al., Phys. Rev. B 60, 11464 (1999) — NOT OPENED; TO/LO quoted in Phys. Rev. B 93, 085205 (2016)', url='https://link.aps.org/accepted/10.1103/PhysRevB.93.085205'),
 'Barker1973': dict(citation='A. S. Barker, M. Ilegems, Phys. Rev. B 7, 743 (1973) (GaN) — Sellmeier-phonon fit via refractiveindex.info', doi='10.1103/PhysRevB.7.743'),
 'Ratchford2019': dict(citation='D. C. Ratchford et al., ACS Nano 13, 6730 (2019), quoting Azuhata 1995 and McNeil 1993 (Raman)', url='https://arxiv.org/abs/1806.06792'),
 'Goldberg2001': dict(citation='Yu. Goldberg, in Properties of Advanced Semiconductor Materials (Wiley 2001) — via Ioffe NSM (AlN)', url='https://www.ioffe.ru/SVA/NSM/Semicond/AlN/optic.html'),
 'Davydov1999': dict(citation='V. Yu. Davydov et al. (1999) — via Ioffe NSM (InN)', url='https://www.ioffe.ru/SVA/NSM/Semicond/InN/optic.html'),
 'Tansley1994': dict(citation='T. L. Tansley (1994), eps_inf of InN from LST — via Ioffe NSM', url='https://www.ioffe.ru/SVA/NSM/Semicond/InN/optic.html'),
 'Kasic2002': dict(citation='A. Kasic, M. Schubert, Y. Saito, Y. Nanishi, G. Wagner, Effective electron mass and phonon modes in n-type hexagonal InN, Phys. Rev. B 65, 115206 (2002)', doi='10.1103/PhysRevB.65.115206'),
 'Reparaz2018': dict(citation='J. S. Reparaz et al., Comparative study of the pressure dependence of optical-phonon transverse-effective charges and linewidths in wurtzite InN, Phys. Rev. B 98, 165204 (2018)', doi='10.1103/PhysRevB.98.165204'),
 'Falkovsky2008': dict(citation='L. A. Falkovsky, Optical properties of graphene, J. Phys.: Conf. Ser. 129, 012004 (2008)', url='https://arxiv.org/abs/0806.3663'),
 'Low2014': dict(citation='T. Low et al., Plasmons and screening in monolayer and multilayer black phosphorus, Phys. Rev. Lett. 113, 106802 (2014)', url='https://arxiv.org/abs/1404.4035'),
 'pyGTM': dict(citation='pyGTM Permittivities.py @7a228b7 (M. Jeannin, GPL-3.0) — value carried over, no primary source identified', url='https://github.com/pyMatJ/pyGTM'),
}
def refs(*keys, used=None):
    out = []
    for k in keys:
        d = dict(key=k, **R[k])
        if used and k in used: d['used_for'] = used[k]
        out.append(d)
    return out

def tab(f): return dict(type='table', file=f'data/{f}.csv')
def tolo(einf, modes, drude=None):
    d = dict(type='tolo', eps_inf=einf, modes=[dict(zip(('to','lo','gamma_to','gamma_lo'), m)) if len(m)==4 else dict(to=m[0], lo=m[1], gamma=m[2]) for m in modes])
    if drude: d['drude'] = drude
    return d
def uni(o, e): return dict(xx=o, yy=o, zz=e)

M = {}
def add(name, **kw): M[name] = dict(name=name, **kw)

# ============================================================= isotropic / tabulated
add('vacuum', tensor='isotropic', status='verified', axes=dict(iso=dict(type='constant', eps=1.0)), valid_range_cm1=[0, 1e9], references=[])
add('KRS5', tensor='isotropic', status='verified', axes=dict(iso=tab('KRS5_Rodney1956')), valid_range_cm1=[254, 17331],
    references=refs('Rodney1956'), notes=['Same values as the old pyGTM table (which had no citation); k = 0.'])
add('Au', tensor='isotropic', status='verified', axes=dict(iso=tab('Au_Olmon2012_evap')), valid_range_cm1=[401, 33333],
    alternatives=dict(drude_Derkachova2016=dict(type='drude', eps_inf=9.84, wp=round(9.010*EV,1), gamma=round(0.072*EV,1),
                      note='omega_p = 9.010 eV, gamma = 0.072 eV; fitted on visible data, over-damped in the mid-IR (Im eps +60% vs Olmon at 1000 cm-1).')),
    references=refs('Olmon2012', 'Derkachova2016'), notes=['Evaporated film. Replaces pyGTM Johnson&Christy (<1.93 um) + Drude switch, which had a discontinuity at 5180 cm-1.'])
add('Ag', tensor='isotropic', status='verified', axes=dict(iso=tab('Ag_Yang2015')), valid_range_cm1=[401, 37037],
    alternatives=dict(drude_Yang2015=dict(type='drude', eps_inf=5.0, wp=round(8.9*EV,1), gamma=round(1/(2*np.pi*C*17e-15),1),
                      note='omega_p = 8.9 eV, tau = 17 fs -> gamma = 1/(2 pi c tau) = 312 cm-1. pyGTM used 1/tau as if in Hz (6.3x too lossy).')),
    references=refs('Yang2015'), notes=['Tabulated data now used over the full 0.27-25 um range (pyGTM used it only below 1.93 um).'])
add('Si', tensor='isotropic', status='verified', axes=dict(iso=tab('Si_ChandlerHorowitz2005')), valid_range_cm1=[430, 4000],
    references=refs('ChandlerHorowitz2005'), notes=['Intrinsic Si, eps ~ 11.68 at 1000 cm-1 (old constant 13.0 was 11% high). Doped wafers require a specimen-specific Drude contribution; no doping option is exposed by the evaluator.'])
add('Ge', tensor='isotropic', status='verified', axes=dict(iso=tab('Ge_Li1980_293K')), valid_range_cm1=[556, 5263], references=refs('Li1980'))
add('Diamond', tensor='isotropic', status='verified', axes=dict(iso=tab('Diamond_Dore1998_CVD')), valid_range_cm1=[20, 4000], references=refs('Dore1998'),
    notes=['Polycrystalline CVD diamond. eps = 5.65 in the LWIR; the 2.5-3 um region reaches 6.08; retain the source data and assess specimen dependence before replacing it.'])
add('MgO', tensor='isotropic', status='partial', axes=dict(iso=tab('MgO_Stephens1952')), valid_range_cm1=[1852, 27778],
    references=refs('Stephens1952', 'Jasperse1966'),
    notes=['Only the transparent range is sourced. The reststrahlen band (TO ~ 400 cm-1) needs the Jasperse 1966 oscillator fit, not yet extracted.'])
add('aSiO2', aliases=['SiO2', 'fused_silica'], tensor='isotropic', status='verified', axes=dict(iso=tab('aSiO2_Franta2016_fused')), valid_range_cm1=[80, 403000],
    alternatives=dict(film_Kischkat2012=tab('aSiO2_Kischkat2012_film'), Popova1972=tab('aSiO2_Popova1972')),
    references=refs('Franta2016', 'Kischkat2012', 'Popova1972'), notes=['Bulk fused silica. Sputtered films (Kischkat) differ by ~20% near the 1080 cm-1 band.'])
add('BaF2', tensor='isotropic', status='verified', axes=dict(iso=tab('BaF2_Querry1987')), valid_range_cm1=[60, 45455],
    alternatives=dict(lorentz_Kaiser1962=dict(type='lorentz', eps_inf=2.16, oscillators=[dict(w0=184., strength=4.50, gamma=round(0.020*184,2)), dict(w0=278., strength=0.07, gamma=round(0.30*278,1))])),
    references=refs('Querry1987', 'Kaiser1962'))
add('CaF2', tensor='isotropic', status='verified', axes=dict(iso=dict(type='lorentz', eps_inf=2.045, oscillators=[dict(w0=257., strength=4.20, gamma=round(0.018*257,2)), dict(w0=328., strength=0.40, gamma=round(0.35*328,1))])),
    valid_range_cm1=[125, 1000], alternatives=dict(Li1980=tab('CaF2_Li1980')), references=refs('Kaiser1962', 'Li1980b'),
    notes=['Kaiser oscillator model for the phonon region; use the Li 1980 table above 833 cm-1 (transparent range).', 'Exists in pyGTM but was not exposed in the old catalog.'])
add('KBr', tensor='isotropic', status='verified', axes=dict(iso=tab('KBr_Li1976')), valid_range_cm1=[238, 50000], references=refs('Li1976'),
    notes=['IR window; transparent above ~ 240 cm-1 (TO phonon ~ 113 cm-1 not modelled).'])
add('ZnSe', tensor='isotropic', status='verified', axes=dict(iso=tab('ZnSe_Querry1987')), valid_range_cm1=[460, 20000], references=refs('Querry1987'))
add('Si3N4_film', aliases=['SiNx'], tensor='isotropic', status='verified', axes=dict(iso=tab('Si3N4_Kischkat2012_film')), valid_range_cm1=[700, 6500],
    references=refs('Kischkat2012'), notes=['437 nm sputtered film on Si. LPCVD/PECVD SiNx varies strongly with stoichiometry; pyGTM eps_SiN (Cataldo et al., Opt. Lett. 37, 4200 (2012)) is an alternative for low-stress PECVD SiNx.'])
add('GaAs', tensor='isotropic', status='partial', axes=dict(iso=tolo(10.9, [(267.8, 291.2, 0.8)])), valid_range_cm1=[100, 5000],
    alternatives=dict(table_Skauli2003=tab('GaAs_Skauli2003')), references=refs('Ioffe', 'Skauli2003', 'pyGTM'),
    notes=['TO/LO = 33.2/36.1 meV at 300 K and eps_inf = n^2 = 10.9 from Ioffe; gamma = 0.8 cm-1 carried over from pyGTM (unverified, Lockwood et al. SSC 136, 404 (2005) not accessible).'])
add('GaP', tensor='isotropic', status='partial', axes=dict(iso=tolo(9.11, [(366.3, 402.0, 1.1)])), valid_range_cm1=[100, 5000], references=refs('Ioffe', 'pyGTM'),
    notes=['eps_inf = 9.11 (Ioffe). TO/LO/gamma from pyGTM, not traced to a primary source.'])
add('InAs', tensor='isotropic', status='partial', axes=dict(iso=tolo(12.3, [(218.0, 243.0, 2.5)])), valid_range_cm1=[100, 3000],
    alternatives=dict(table_Lorimor1965=tab('InAs_Lorimor1965')), references=refs('Ioffe', 'Lorimor1965', 'pyGTM'),
    notes=['eps_inf = n^2 = 3.51^2 = 12.3 (Ioffe; old value 12.9 was 7% high vs Lorimor). TO/LO/gamma from pyGTM (LO consistent with LST for eps_DC = 15.15).'])
add('ZnO_pellet', tensor='isotropic', status='partial', axes=dict(iso=tab('ZnO_Querry1985_pellet')), valid_range_cm1=[180, 47619], references=refs('Querry1985'),
    notes=['Pressed-pellet (effective isotropic) data. Anisotropic wurtzite parameters (Ashkenov et al., J. Appl. Phys. 93, 126 (2003)) still to be extracted.'])
add('PMMA', tensor='isotropic', status='verified', valid_range_cm1=[550, 4000], references=refs('Tsuda2018'),
    axes=dict(iso=dict(type='lorentz', eps_inf=2.162, oscillators=[dict(w0=w0, strength=s, gamma=g) for w0, s, g in zip(
        [752.25, 808.09, 825.19, 843.16, 913.82, 965.31, 989.60, 1066.27, 1149.37, 1190.32, 1241.23, 1269.59, 1361.50, 1387.61, 1434.77, 1450.59, 1481.89, 1730.18, 2840.98, 2920.93, 2950.55, 2997.71, 3440.07],
        [3.18E-03, 6.94E-04, 1.13E-04, 2.86E-03, 1.68E-03, 3.94E-03, 2.79E-03, 1.10E-03, 2.92E-02, 1.04E-02, 6.64E-03, 5.49E-03, 1.09E-03, 1.07E-03, 1.34E-03, 4.11E-03, 2.12E-03, 1.56E-02, 6.66E-05, 8.42E-04, 6.60E-04, 9.53E-04, 4.15E-05],
        [13.65, 15.51, 4.21, 23.09, 32.50, 26.70, 14.68, 13.56, 31.12, 22.12, 21.38, 24.66, 41.97, 15.80, 10.56, 25.15, 19.17, 9.40, 15.32, 60.94, 18.80, 36.68, 33.89])])),
    notes=['Standard nano-FTIR test sample; C=O stretch at 1730 cm-1.'])
add('VO2_insulating', tensor='isotropic', status='verified', axes=dict(iso=tab('VO2_Beaini2020_25C_film')), valid_range_cm1=[400, 20000], references=refs('Beaini2020'),
    notes=['70 nm film, 25 C (monoclinic insulating phase). Data digitised from a figure by refractiveindex.info.'])
add('VO2_metallic', tensor='isotropic', status='verified', axes=dict(iso=tab('VO2_Beaini2020_100C_film')), valid_range_cm1=[400, 20000], references=refs('Beaini2020'),
    notes=['Same film at 100 C (rutile metallic phase).'])
add('GST_amorphous', tensor='isotropic', status='verified', axes=dict(iso=tab('GST_Frantz2023_amorphous')), valid_range_cm1=[338, 28549], references=refs('Frantz2023'))
add('GST_crystalline', tensor='isotropic', status='verified', axes=dict(iso=tab('GST_Frantz2023_crystal')), valid_range_cm1=[309, 28549], references=refs('Frantz2023'))

# ============================================================= polar crystals (TO-LO)
add('SiC3C', tensor='isotropic', status='verified', axes=dict(iso=tolo(6.52, [(796.2, 972.2, 3.0)])), valid_range_cm1=[100, 5000],
    references=refs('PatrickChoyke1970', 'Olego1982', 'Mutschke1999', 'Pitman2008'),
    notes=['LST check: 6.52*(972.2/796.2)^2 = 9.72 = measured eps_DC.', 'gamma = 3 cm-1 is a modelling choice. Mutschke discusses ad hoc narrow damping; Pitman reports widths around 5-6 cm-1 also for crystals. Damping depends on specimen and convention.'])
add('SiC4H', tensor='uniaxial', status='partial', axes=uni(tolo(6.52, [(797.0, 970.0, 3.75)]), tolo(6.70, [(788.0, 964.0, 3.75)])), valid_range_cm1=[100, 5000],
    references=refs('Tiwald1999', 'PatrickChoyke1970', 'pyGTM'),
    notes=['perp TO/LO from Tiwald 1999 (as quoted); parallel TO/LO and gamma carried over from the old repo definition (unverified).', 'eps_inf: Ioffe recommends the 6H values for 4H.'])
add('SiC6H', tensor='uniaxial', status='partial', axes=uni(tolo(6.52, [(794.78, 967.93, 2.535)]), tolo(6.70, [(783.67, 962.0, 5.07)])), valid_range_cm1=[100, 5000],
    references=refs('PatrickChoyke1970', 'pyGTM'),
    notes=['Replaces pyGTM eps_SiC6Hz, whose eps_3phonon formula returned ~2*eps_inf (upper reststrahlen edge at 875 instead of 962 cm-1). Weak modes at 881/886 cm-1 dropped.', 'eps_inf updated to Patrick & Choyke 6.52/6.70 (old 6.56/6.78).'])
add('AlN', tensor='uniaxial', status='partial', axes=uni(tolo(4.6, [(673.0, 916.0, 2.2)]), tolo(4.6, [(614.0, 893.0, 2.2)])), valid_range_cm1=[100, 5000],
    alternatives=dict(film_Kischkat2012=tab('AlN_Kischkat2012_film')), references=refs('Ratchford2019', 'Goldberg2001', 'Kischkat2012', 'pyGTM'),
    notes=['Bulk wurtzite. LST check perp: 4.6*(916/673)^2 = 8.52 vs eps_DC 8.5 (Goldberg).', 'Sputtered films have eps_inf ~ 4.0 (Kischkat table).', 'gamma = 2.2 cm-1 from pyGTM (unverified).'])
add('GaN', tensor='uniaxial', status='partial', axes=uni(tolo(5.35, [(561.0, 743.0, 4.0)]), tolo(5.35, [(533.0, 735.0, 4.0)])), valid_range_cm1=[100, 5000],
    references=refs('Barker1973', 'Ratchford2019', 'Ioffe', 'pyGTM'),
    notes=['eps_inf = 5.35 (Barker & Ilegems; old 5.04/5.01). TO/LO from Raman (Azuhata/McNeil via Ratchford 2019). gamma = 4 cm-1 from pyGTM (unverified).'])
add('InN', tensor='uniaxial', status='verified', axes=uni(tolo(6.7, [(477.1, 601.4, 4.4)]), tolo(6.7, [(450.5, 588.1, 4.4)])), valid_range_cm1=[100, 5000],
    references=refs('Kasic2002', 'Reparaz2018'),
    notes=['E_inf = 6.7 +/- 0.1, E1(TO) = 477.1 +/- 0.6 cm-1, and gamma = 4.4 +/- 1.0 cm-1 from Kasic et al. 2002; the measured gamma is used on both axes.',
           'A1(TO) = 450.5, E1(LO) = 601.4, and A1(LO) = 588.1 cm-1 from Reparaz et al. 2018.'])
for iso, (eo, to, lo, go, ee, te, le, ge) in {
        'natural': (4.9, 1360, 1614, 7, 2.95, 760, 825, 3),
        '11B':     (5.32, 1359.8, 1608.7, 2.1, 3.15, 755, 814, 1),
        '10B':     (5.1, 1394.5, 1650, 1.8, 2.5, 785, 845, 1)}.items():
    add(f'hBN_{iso}' if iso != 'natural' else 'hBN', tensor='uniaxial', status='verified',
        axes=uni(tolo(eo, [(to, lo, go)]), tolo(ee, [(te, le, ge)])), valid_range_cm1=[100, 5000], references=refs('Giles2018'),
        frame=dict(z='c axis (out of plane of a flake)'), notes=[f'{iso} isotopic composition, Giles 2018 SI Table S4.'])
add('Al2O3', aliases=['sapphire'], tensor='uniaxial', status='verified', valid_range_cm1=[100, 5000], references=refs('Schubert2000', 'Querry1985'),
    axes=uni(tolo(3.077, [(384.96, 387.60, 3.3, 3.1), (439.10, 481.68, 3.1, 1.9), (569.00, 629.50, 4.7, 5.9), (633.63, 906.6, 5.0, 14.7)]),
             tolo(3.072, [(397.52, 510.87, 5.3, 1.1), (582.41, 881.1, 3.0, 15.4)])),
    frame=dict(z='c axis'), notes=['Unrounded Schubert values; fixes the gamma_TO/gamma_LO mix-up of the old extraordinary axis.', 'Above the last LO (> 950 cm-1) the model under-estimates multiphonon absorption: Im eps 0.06 vs 0.17 (Querry) at 1000 cm-1.'])
add('MoO3', tensor='biaxial', status='verified', valid_range_cm1=[400, 1200], references=refs('AlvarezPerez2020'),
    frame=dict(x='[100]', y='[001]', z='[010] (van der Waals stacking axis)'),
    axes=dict(xx=tolo(5.78, [(506.7, 534.3, 49.1), (821.4, 963.0, 6.0), (998.7, 999.2, 0.35)]),
              yy=tolo(6.07, [(544.6, 850.1, 9.5)]), zz=tolo(4.47, [(956.7, 1006.9, 1.5)])))
add('V2O5', tensor='biaxial', status='verified', valid_range_cm1=[400, 1200], references=refs('TaboadaGutierrez2020'),
    frame=dict(x='[100]', y='[001]', z='[010] (van der Waals stacking axis)'),
    axes=dict(xx=tolo(6.6, [(765, 952, 40)]), yy=tolo(6.1, [(506, 842, 19)]), zz=tolo(3.9, [(976, 1037, 2.0)])),
    notes=['z gamma: paper gives 2.0 (1.5 gives a slightly better fit).'])
add('alpha_quartz', aliases=['quartz'], tensor='uniaxial', status='secondary', valid_range_cm1=[300, 1600], references=refs('GervaisPiriou1975', 'Winta2019', 'HyperbolicOptics'),
    frame=dict(z='c (optic) axis'),
    axes=uni(tolo(2.356, [(393.5, 403.0, 2.1, 2.8), (450.0, 507.0, 4.5, 3.5), (695.0, 697.6, 13.0, 13.0), (797.0, 810.0, 6.9, 6.9), (1065.0, 1226.0, 7.2, 12.5), (1158.0, 1155.0, 9.3, 9.3)]),
             tolo(2.383, [(363.5, 386.7, 4.8, 7.0), (487.5, 550.0, 4.0, 3.2), (777.0, 790.0, 6.7, 6.7), (1071.0, 1229.0, 6.8, 12.0)])),
    notes=['Room-temperature set attributed to Gervais & Piriou 1975; cross-checked against Winta 2019 (T <= 200 K): all modes agree within 5 cm-1.', 'Low-frequency E modes (128, 265 cm-1) omitted.'])
add('calcite', aliases=['CaCO3'], tensor='uniaxial', status='secondary', valid_range_cm1=[80, 1700], references=refs('Lane1999', 'HyperbolicOptics'),
    frame=dict(z='c (optic) axis'),
    axes=uni(tolo(2.7, [(712, 715, 5.0), (1410, 1550, 10.0), (297, 381, 14.4), (223, 239, 11.4), (102, 123, 5.7)]),
             tolo(2.4, [(871, 890, 3.0), (303, 387, 9.1), (92, 136, 5.6)])),
    notes=['Values from hyperbolic_optics; primary source (Lane 1999, used by Ma et al. 2021 for ghost polaritons) not opened. VERIFY before quantitative use.',
           'eps_inf check: visible n_o^2 = 2.75, n_e^2 = 2.21 (Ghosh), so eps_inf_e = 2.4 looks high.'])
# ============================================================= monoclinic (rank-1 oscillator sum)
def mono_osc(A, to, g, alpha=None, G=0.0, sym='Bu'):
    e = [alpha, 0.0, 0.0] if alpha is not None else [0.0, 90.0, 90.0]
    d = dict(symmetry=sym, amplitude=A, to=to, gamma=g, euler_deg=e)
    if G: d['anharmonic_paper'] = G   # not read by matlib; rename to `anharmonic` to enable (non-passive)
    return d
ga_bu = [mono_osc(A, t, g, a) for A, t, g, a in zip([256.45, 426.87, 820.36, 792.85, 358.37, 161.7, 485.67, 520.75],
                                                   [743.55, 692.44, 572.53, 432.56, 356.81, 279.15, 262.38, 213.79],
                                                   [10.4, 6.44, 12.32, 10.05, 3.79, 1.85, 1.75, 1.98],
                                                   [48.7, 5.4, 106.0, 21.0, 144.0, 0.0, 158.5, 80.9])]
ga_au = [mono_osc(A, t, g, sym='Au') for A, t, g in zip([542, 718, 579, 72], [663.22, 448.65, 296.64, 154.85], [3.23, 10.28, 14.31, 2.1])]
add('Ga2O3_beta', tensor='monoclinic', status='verified', valid_range_cm1=[150, 1200], references=refs('Schubert2016_preprint', 'Schubert2016_published'),
    frame=dict(x='crystal c axis', y='perpendicular to b and c (in the a-c plane)', z='crystal b axis (monoclinic 2-fold axis)'),
    model=dict(eps_inf=[[3.89, 0, 0], [0, 2.90, 0], [0, 0, 3.87]], oscillators=ga_bu + ga_au,
               lo_modes=dict(Bu=[817.0, 778.1, 719.1, 579.3, 391.8, 307.5, 286.5, 271.2], Au=[770.3, 558.9, 344.7, 156.0])),
    notes=['rho_l = A^2/(w_TO^2 - w^2 - i gamma w); eps = eps_inf + sum rho_l * R(euler) diag(1,0,0) R^T.',
           'Bu alpha (paper) is measured from x (= c) towards y; Euler = (alpha, 0, 0). Au modes lie along z = b: Euler = (0, 90, 90).',
           'Check: eps_DC reproduced as xx 11.51, yy 11.90, zz 11.12, xy -0.05 vs paper 11.51, 11.89, 11.15, -0.05.',
           'eps_inf column order (xx 3.89, yy 2.90, zz 3.87) confirmed by that LST check; the paper text has a typo.',
           'The published PRB fit has eps_inf xx 3.75, yy 3.21, zz 3.71, xy -0.08 and revised oscillators in x parallel a. This default follows the earlier preprint in x parallel c; do not mix their coefficients or frames.'])
cd_bu = [mono_osc(A, t, g, a, G) for A, t, g, a, G in zip([908, 1018, 279, 645, 326, 236, 294, 236], [779.5, 549.0, 450.6, 276.3, 265.2, 227.3, 149.1, 98.1],
                                                         [15.0, 15.3, 12.5, 11.3, 12.0, 5.0, 5.7, 3.5], [24.3, -66.9, 180.8, 65.6, -98.1, -52.4, 145.1, 18.9],
                                                         [31, -22, -17, -67, 88, 7, -27, 70])]
cd_au = [mono_osc(A, t, g, G=G, sym='Au') for A, t, g, G in zip([392, 679, 445, 299, 364, 93, 226], [866.6, 653.7, 501.0, 400.3, 341.2, 285.5, 121.8],
                                                               [7.5, 15.8, 15.1, 10.2, 3.4, 17, 2.0], [8.6, 14, -29, -24, -16, 57, -9.4])]
add('CdWO4', tensor='monoclinic', status='partial', valid_range_cm1=[80, 1200], references=refs('Mock2017'),
    frame=dict(x='crystal a axis', y='c* (perpendicular to a in the a-c plane)', z='crystal b axis (monoclinic 2-fold axis)'),
    model=dict(eps_inf=[[4.46, 0.086, 0], [0.086, 4.81, 0], [0, 0, 4.25]], oscillators=cd_bu + cd_au,
               lo_modes=dict(Bu=[901.4, 754.4, 466.5, 369.8, 269.1, 243.5, 180.0, 117.0], Au=[904.0, 742.4, 532.8, 418.0, 360.2, 286.8, 144.0])),
    notes=['Anharmonic oscillator: rho_l = (A^2 - i Gamma w)/(w_TO^2 - w^2 - i gamma w) (Mock 2017 Eq. 4); alpha measured from a.',
           'Check: eps_DC zz = 11.57 (paper 11.56), xy = 1.048 (1.05), xx+yy = 32.16 (32.17) but xx 15.66 / yy 16.51 vs paper 16.16 / 16.01: the xx/yy labels of Table III may be swapped in the paper or in text extraction. VERIFY against the PDF.',
           'Passivity: with the anharmonic Gamma terms Im(eps_zz) goes slightly negative (min -0.67 near 271 cm-1). Set every `anharmonic` to 0 for a strictly passive (harmonic) model; that version stays passive everywhere.'])

# ============================================================= 2D sheets
add('graphene', tensor='sheet', status='verified', valid_range_cm1=[10, 20000], references=refs('Falkovsky2008'),
    model=dict(type='graphene_falkovsky', defaults=dict(mu_eV=0.3, T_K=300, tau_fs=100),
               formula='sigma = sigma_intra + sigma_inter; sigma_intra = 2 i e^2 k_B T /(pi hbar^2 (omega + i/tau)) ln[2 cosh(mu/2k_BT)]; '
                       'sigma_inter = e^2/(4 hbar) [theta(hbar omega - 2mu) - (i/2pi) ln((hbar omega+2mu)^2/((hbar omega-2mu)^2 + (2k_BT)^2))]'),
    notes=['Needs a 2D-conductivity boundary condition in the engine (not a bulk eps). Defaults are illustrative; mu and tau are sample parameters.',
           'Common bulk surrogate: eps = 1 + i sigma/(eps0 omega t) with t = 0.335 nm.'])
add('black_phosphorus', tensor='sheet', status='verified', valid_range_cm1=[10, 5000], references=refs('Low2014'),
    frame=dict(x='armchair', y='zigzag'),
    model=dict(type='bp_drude', defaults=dict(n_cm2=1e13, eta_meV=10, m_x=0.15, m_y=0.7),
               masses=dict(bulk=dict(m_cx=0.08, m_vx=0.08, m_cy=0.7, m_vy=1.0, m_cz=0.2, m_vz=0.4), monolayer=dict(m_cx=0.15, m_vx=0.15)),
               formula='sigma_jj = i D_j / (pi (omega + i eta/hbar)),  D_j = pi e^2 n / m_j  (intraband Drude, Low 2014 Eq. 10-11)'),
    notes=['Masses in units of m0. Intraband only; interband edge (gap ~2 eV monolayer, 0.3 eV bulk) not included.'])


# ============================================================= UPDATES from primary sources supplied by the user (2026-09-28)
R.update({
 'Kasic2000': dict(citation='A. Kasic, M. Schubert, S. Einfeldt, D. Hommel, T. E. Tiwald, Phys. Rev. B 62, 7365 (2000), Tables I-III (sample A)', doi='10.1103/PhysRevB.62.7365'),
 'Barker1973': dict(citation='A. S. Barker, M. Ilegems, Phys. Rev. B 7, 743 (1973), Tables I-II', doi='10.1103/PhysRevB.7.743'),
 'Moore2005': dict(citation='W. J. Moore, J. A. Freitas, R. T. Holm, O. Kovalenkov, V. Dmitriev, Appl. Phys. Lett. 86, 141912 (2005), Table I', doi='10.1063/1.1899233'),
 'Tiwald1999': dict(citation='T. E. Tiwald, J. A. Woollam, S. Zollner et al., Phys. Rev. B 60, 11464 (1999), Table I', doi='10.1103/PhysRevB.60.11464'),
 'GervaisPiriou1975': dict(citation='F. Gervais, B. Piriou, Phys. Rev. B 11, 3944 (1975), Tables I-II (T = 295 K rows)', doi='10.1103/PhysRevB.11.3944'),
 'Lane1999': dict(citation='M. D. Lane, J. Geophys. Res. Planets 104, 14099 (1999), Table 1', doi='10.1029/1999JE900025'),
 'Ma2021': dict(citation='W. Ma et al., Ghost hyperbolic surface polaritons in bulk anisotropic crystals, Nature 596, 362 (2021), Methods Eq. 4 (values from Hellwege et al. 1970)', doi='10.1038/s41586-021-03755-1'),
 'Lockwood2005': dict(citation='D. J. Lockwood, G. Yu, N. L. Rowell, Solid State Commun. 136, 404 (2005), Table 2 (293 K)', doi='10.1016/j.ssc.2005.08.030'),
 'Ashkenov2003': dict(citation='N. Ashkenov et al., J. Appl. Phys. 93, 126 (2003), Tables I-II', doi='10.1063/1.1526935'),
 'Jasperse1966': dict(citation='J. R. Jasperse, A. Kahan, J. N. Plendl, S. S. Mitra, Phys. Rev. 146, 526 (1966), Tables I-II (295 K)', doi='10.1103/PhysRev.146.526'),
 'Mock2017': dict(citation='A. Mock, R. Korlacki, S. Knight, M. Schubert, Phys. Rev. B 95, 165202 (2017), Tables II-IV', doi='10.1103/PhysRevB.95.165202'),
})
def sk(eps_inf, osc):
    """Spitzer-Kleinman classical oscillators: eps_inf + sum 4pi rho nu^2/(nu^2 - w^2 - i (g/nu) nu w); osc = (nu, 4pi rho, g/nu)."""
    return dict(type='lorentz', eps_inf=eps_inf, oscillators=[dict(w0=n, strength=f, gamma=round(g * n, 4)) for n, f, g in osc])

# --- GaN: Kasic 2000 sample A (the unnamed source of the old pyGTM values) --------------------------
add('GaN', tensor='uniaxial', status='verified', valid_range_cm1=[100, 5000], references=refs('Kasic2000', 'Barker1973'),
    frame=dict(z='c axis'),
    axes=uni(tolo(5.04, [(560.1, 742.1, 3.8, 6.9)]), tolo(5.01, [(537.0, 732.5, 4.0, 6.0)])),
    alternatives=dict(Barker1973=dict(xx=tolo(5.35, [(560.0, 746.0, 17.0)]), zz=tolo(5.35, [(533.0, 744.0, 17.0)]),
                      note='Older film data: eps_inf 5.35 from an index fit, Gamma = 17 cm-1 (lower-quality 1973 films).')),
    notes=['Kasic sample A (lowest free-carrier density, 7.8e16 cm-3). gamma_LO values are the LPP broadenings ~gamma_LO at this low density.',
           'A1(TO) = 537 cm-1 and gamma_TO,par = 4 cm-1 were fixed from Raman / assumed in the paper (not fitted).',
           'The old pyGTM GaN values are exactly this sample (source had not been cited).'])
# --- AlN: Moore 2005 (the unnamed source of the old values; damping convention fixed) ------------------
_alN = lambda einf, eip, edc, ngap, nto, gg, g2, gt: dict(type='lorentz', eps_inf=1.0, oscillators=[
    dict(w0=ngap, strength=round(einf - 1, 4), gamma=2 * gg), dict(w0=2 * nto, strength=round(eip - einf, 4), gamma=2 * g2), dict(w0=nto, strength=round(edc - eip, 4), gamma=2 * gt)])
add('AlN', tensor='uniaxial', status='verified', valid_range_cm1=[50, 14000], references=refs('Moore2005', 'Kischkat2012'),
    frame=dict(z='c axis'),
    axes=uni(_alN(4.160, 4.175, 7.76, 74300, 667.2, 1, 3, 2.2), _alN(4.350, 4.366, 9.32, 73000, 608.5, 1, 3, 2.2)),
    alternatives=dict(film_Kischkat2012=tab('AlN_Kischkat2012_film')),
    notes=['Moore Eq. 1: eps = 1 + sum (eps_j - eps_(j-1)) nu_j^2 / (nu_j^2 - nu^2 + 2 i nu Gamma_j): gap oscillator, two-phonon term at 2 nu_TO, one-phonon term at nu_TO.',
           'Converted to exp(-i w t): damping gamma = 2 Gamma, so the one-phonon gamma is 4.4 cm-1. pyGTM used 2.2 (half).',
           'LO (reference only): 909.6 / 888.9 cm-1; LST: 4.175*(909.6/667.2)^2 = 7.76 = eps_DC.', 'E||c values were modelled in the paper, not fitted.',
           'The old pyGTM AlN values are these (source had not been cited).'])
# --- SiC 4H / 6H: Tiwald 1999 Table I, lowest-doping samples ----------------------------------------
add('SiC4H', tensor='uniaxial', status='verified', valid_range_cm1=[100, 5000], references=refs('Tiwald1999'),
    frame=dict(z='c axis'), axes=uni(tolo(6.6, [(797.0, 970.0, 1.4)]), tolo(6.9, [(782.0, 964.0, 1.4)])),
    notes=['Tiwald Table I sample 9, undoped 4H epilayer (N ~ 0): eps_inf 6.6/6.9, TO 797/782 (fixed), LO 970/964, Gamma 1.4 cm-1.',
           'Tiwald Eq. 3: eps_inf [1 + (w_LO^2 - w_TO^2)/(w_TO^2 - w^2 - i w Gamma)] = TO-LO form with gamma_TO = gamma_LO = Gamma.',
           'The old repo values (797/970, 788/964) are Tiwald\'s quoted literature values for 6H, not 4H.'])
add('SiC6H', tensor='uniaxial', status='verified', valid_range_cm1=[100, 5000], references=refs('Tiwald1999', 'PatrickChoyke1970'),
    frame=dict(z='c axis'), axes=uni(tolo(6.6, [(797.0, 972.0, 2.7)]), tolo(6.8, [(788.0, 967.0, 2.7)])),
    notes=['Tiwald Table I sample 7 (6H, N = 0.2e18 cm-3, the lowest-doped 6H): eps_inf 6.6/6.8, TO 797/788, LO 972/967, Gamma 2.7 cm-1.',
           'Replaces pyGTM eps_SiC6Hz, whose eps_3phonon formula returned ~2 eps_inf.'])
# --- alpha-quartz: Gervais & Piriou 1975, 295 K --------------------------------------------------------
add('alpha_quartz', aliases=['quartz'], tensor='uniaxial', status='verified', valid_range_cm1=[300, 1600], references=refs('GervaisPiriou1975', 'Winta2019'),
    frame=dict(z='c (optic) axis'),
    axes=uni(tolo(2.356, [(393.5, 402.0, 2.8, 2.8), (450.0, 510.0, 4.5, 4.1), (695.0, 697.6, 13.0, 13.0), (797.0, 810.0, 6.9, 6.9), (1065.0, 1226.0, 7.2, 12.5), (1158.0, 1155.0, 9.3, 9.3)]),
             tolo(2.383, [(363.5, 386.7, 4.8, 4.8), (495.0, 551.5, 5.2, 5.8), (509.0, 507.5, 14.0, 14.0), (777.0, 790.0, 6.7, 6.7), (1071.0, 1229.0, 6.8, 12.0)])),
    notes=['FPSQ (four-parameter semi-quantum) product form, T1 = 295 K rows of Tables I (A2, E||c) and II (E, E perp c).',
           'Includes the weak A2 oscillator 509/507.5 cm-1 (LO in parentheses in the paper). Low-frequency E modes 1-2 (<300 cm-1) not in these tables.',
           'Supersedes the hyperbolic_optics transcription, which had several errors (e.g. E LO 507 vs 510, A2 TO 487.5 vs 495, A2 gamma_LO 7.0 vs 4.8).'])
# --- calcite: Lane 1999 (default) + Ma 2021 alternative ----------------------------------------------
add('calcite', aliases=['CaCO3'], tensor='uniaxial', status='verified', valid_range_cm1=[50, 2000], references=refs('Lane1999', 'Ma2021'),
    frame=dict(z='c (optic) axis'),
    axes=uni(sk(2.749, [(1404, 0.58, 0.0061), (891, 0.001, 0.004), (712, 0.016, 0.0065), (380, 0.13, 0.6), (298, 1.7, 0.035), (223, 1.0, 0.05), (102, 3.4, 0.06)]),
             sk(2.208, [(871, 0.08, 0.0017), (848, 0.004, 0.007), (305, 1.36, 0.031), (95, 4.6, 0.07)])),
    alternatives=dict(Ma2021=dict(
        xx=dict(type='lorentz', eps_inf=2.7, oscillators=[dict(w0=712, strength=round(2.7 * (715**2 - 712**2) / 712**2, 6), gamma=5), dict(w0=1410, strength=round(2.7 * (1550**2 - 1410**2) / 1410**2, 6), gamma=10)]),
        zz=dict(type='lorentz', eps_inf=2.4, oscillators=[dict(w0=871, strength=round(2.4 * (890**2 - 871**2) / 871**2, 6), gamma=3)]),
        note='Ma et al. Methods Eq. 4: eps = eps_inf [1 + sum (w_LO^2 - w_TO^2)/(w_TO^2 - w^2 - i w Gamma)]; perp 712/715 G5, 1410/1550 G10, eps_inf 2.7; par 871/890 G3, eps_inf 2.4 (from Hellwege 1970). Mid-IR only; used for the ghost-polariton simulations.')),
    notes=['Lane Table 1 classical oscillators: strength = 4 pi rho, damping gamma_j = (tabulated gamma) x nu_j, eps_inf from Chang et al. 1996.',
           'Dispersion form assumed to be the Spitzer-Kleinman convention eps_inf + sum 4pi rho nu_j^2/(nu_j^2 - nu^2 - i gamma nu_j nu) cited by Lane; the paper does not print the formula.',
           'The hyperbolic_optics set mixed Ma 2021 (mid-IR) with unidentified far-IR modes.'])
# --- CdWO4: published tables confirm the arXiv values ------------------------------------------------
M['CdWO4']['status'] = 'verified'
M['CdWO4']['references'] = refs('Mock2017')
M['CdWO4']['notes'] = [
    'Anharmonic oscillator: rho_l = (A^2 - i Gamma w)/(w_TO^2 - w^2 - i gamma w) (Mock 2017 Eq. 4); alpha measured from a. Published frame: x = a, -z = b, y = c* (sign of z irrelevant for rank-1 terms).',
    'Published Table II lists alpha_TO = 24.3, 113.1, 0.8, 65.6, 81.9, 127.6, 145.1, 18.9 deg; the arXiv values used here differ by 180 deg for modes 2, 3, 5, 6, which is the same dipole direction.',
    'Check: model eps_DC zz 11.57 (paper 11.56), xy 1.048 (1.05); xx/yy 15.66/16.51 vs 16.16/16.01. The paper states eps_DC was extrapolated from the wavelength-by-wavelength data, not computed from the model; det(eps_DC) agrees to 0.1%, which is what the S-LST relation tests.',
    'Default is the harmonic (passive) model: the paper\'s anharmonic broadenings are stored as `anharmonic_paper` and ignored by matlib. Renaming them to `anharmonic` reproduces Eq. 4 exactly, but Im(eps_zz) then goes slightly negative (min -0.67 near 271 cm-1).']
# --- III-V semiconductors: Lockwood 2005 Table 2 (293 K) -----------------------------------------------
for nm, (einf, lo, glo, to, gto) in {'GaAs': (10.86, 292.01, 2.33, 268.41, 2.51), 'GaP': (9.236, 402.50, 1.18, 366.33, 2.59), 'InAs': (11.91, 240.20, 2.01, 217.36, 8.67),
                                     'InP': (9.563, 345.32, 0.95, 303.62, 2.80), 'InSb': (15.55, 192.11, 3.37, 179.95, 4.45), 'AlAs': (8.167, 399.59, 3.03, 360.04, 4.44)}.items():
    alt = dict(Lockwood2005_exact=tolo(einf, [(to, lo, gto, glo)]))
    alt['Lockwood2005_exact']['note'] = f'Exact Table 2 values (gamma_TO = {gto}, gamma_LO = {glo}). gamma_LO < gamma_TO violates the Lowndes condition, so Im(eps) turns slightly negative above the LO frequency (gain artefact in thick layers).'
    if nm == 'GaAs': alt['table_Skauli2003'] = tab('GaAs_Skauli2003')
    if nm == 'InAs': alt['table_Lorimor1965'] = tab('InAs_Lorimor1965')
    add(nm, tensor='isotropic', status='verified', valid_range_cm1=[50, 5000], references=refs('Lockwood2005'),
        axes=dict(iso=tolo(einf, [(to, lo, gto)])), alternatives=alt,
        notes=['Semi-insulating / low-doped bulk, 293 K. TO, LO and eps_inf (LST value, Lockwood column eps_inf^b) from Table 2.',
               f'Default uses one damping gamma = gamma_TO = {gto} cm-1 for TO and LO so the model stays passive; the paper\'s separate gamma_LO = {glo} cm-1 is kept under alternatives.Lockwood2005_exact.'])
# --- ZnO: Ashkenov 2003 bulk (default) + film ------------------------------------------------------------
add('ZnO', tensor='uniaxial', status='verified', valid_range_cm1=[100, 5000], references=refs('Ashkenov2003', 'Querry1985'),
    frame=dict(z='c axis'), axes=uni(tolo(3.70, [(408.2, 592.1, 13.0)]), tolo(3.78, [(379.0, 577.1, 13.0)])),
    alternatives=dict(film_Ashkenov2003=dict(xx=tolo(3.61, [(409.1, 588.3, 10.0)]), zz=tolo(3.76, [(380.0, 574.5, 10.0)]), note='PLD film on c-sapphire'),
                      pellet_Querry1985=tab('ZnO_Querry1985_pellet')),
    notes=['Bulk sample: E1 TO/LO 408.2/592.1 (IRSE), A1 TO 379 (Raman), A1 LO 577.1 (IRSE), eps_inf 3.70/3.78 from LST with measured eps_0 7.77/8.91, gamma 13 cm-1 (single Lorentzian broadening).'])
del M['ZnO_pellet']
# --- MgO and LiF: Jasperse 1966, 295 K ----------------------------------------------------------------
add('MgO', tensor='isotropic', status='verified', valid_range_cm1=[100, 27778], references=refs('Jasperse1966', 'Stephens1952'),
    axes=dict(iso=sk(3.01, [(401, 6.60, 0.0190), (640, 0.045, 0.160)])), alternatives=dict(transparent_Stephens1952=tab('MgO_Stephens1952')),
    notes=['Two-oscillator fit at 295 K (main + weak secondary resonance); eps_inf = 3.01 held temperature independent in the paper.', 'eps\' = 0 at 725 cm-1 (LO).',
           'Above ~2000 cm-1 the Stephens & Malitson table (eps 2.6-2.97) is more accurate than the constant eps_inf.'])
add('LiF', tensor='isotropic', status='verified', valid_range_cm1=[100, 5000], references=refs('Jasperse1966'),
    axes=dict(iso=sk(1.90, [(306, 6.80, 0.0600), (503, 0.110, 0.180)])), notes=['295 K row of Jasperse Table I.'])
# --- Corrections from the 2026-10-01 literature and numerical audit -----------------
# Preserve the packaged broader-loss 4H model; expose the narrow experimental fit explicitly.
M['SiC4H']['alternatives'] = dict(Tiwald1999_sample9=dict(
    **uni(tolo(6.6, [(797.0, 970.0, 1.4)]), tolo(6.9, [(782.0, 964.0, 1.4)])),
    valid_range_cm1=[700, 4000], note='Sample 9 lattice fit, Gamma = 1.4 cm-1, carrier density fixed to zero. Multiphonon absorption is omitted.'))
M['SiC4H']['axes'] = uni(tolo(6.6, [(797.0, 970.0, 6.0)]), tolo(6.9, [(782.0, 964.0, 6.0)]))
M['SiC4H']['notes'].insert(0, 'Default Gamma = 6 cm-1 is a broader-loss modelling assumption, not the Tiwald sample-9 measurement. The exact narrow lattice fit is an alternative.')
for nm in ('SiC4H', 'SiC6H'):
    M[nm]['valid_range_cm1'] = [700, 4000]
    M[nm]['notes'].append('Lattice-only approximation in the source measurement band; carriers and multiphonon absorption are omitted. This is not the full measured dielectric response.')
M['SiC3C']['alternatives'] = dict(gamma6_sensitivity=dict(
    **tolo(6.52, [(796.2, 972.2, 6.0)]), note='Broader-loss sensitivity model, not an exact Pitman experimental fit.'))
M['GaN']['valid_range_cm1'] = [300, 1200]
M['GaN']['notes'].append('Conservative phonon modelling band. Separate TO/LO damping gives negative loss below approximately 153 cm-1; do not extrapolate this fit there. Carrier response is omitted.')
M['MgO']['valid_range_cm1'] = [100, 2000]
for nm in ('SiC3C', 'SiC4H', 'SiC6H', 'GaN', 'CdWO4', 'AlAs', 'GaP', 'GaAs', 'InP', 'InAs', 'InSb'):
    M[nm]['status'] = 'modified'
for nm in ('AlN', 'InN', 'graphene', 'black_phosphorus'):
    if nm in M: M[nm]['status'] = 'modelled'
M['InN']['notes'].append('Composite lattice model: the shared Gamma = 4.4 cm-1 is not an independently measured extraordinary-axis damping. Carrier response is omitted.')
M['calcite']['status'] = 'partial'
M['V2O5']['status'] = 'partial'
M['V2O5']['notes'].append('Constants transcribed from the source, but its printed frequency-weighted damping formula is dimensionally ambiguous with the quoted cm-1 units. The evaluator uses the conventional TO-LO form; full curve validation remains pending.')
M['V2O5']['alternatives'] = dict(gamma_z_1p5=dict(
    xx=M['V2O5']['axes']['xx'], yy=M['V2O5']['axes']['yy'], zz=tolo(3.9, [(976, 1037, 1.5)]),
    note='Source-mentioned z-axis damping alternative; the formula ambiguity also applies here.'))
M['Ga2O3_beta']['status'] = 'preprint'
M['Ga2O3_beta']['references'] = refs('Schubert2016_preprint', 'Schubert2016_published')
M['Ga2O3_beta']['notes'].append('Default contains the preprint lattice response only; the source samples also have free-carrier contributions.')
M['GaAs']['references'] += refs('Skauli2003')
M['InAs']['references'] += refs('Lorimor1965')
# Table bounds are actual data coverage; zero entries do not establish an absorption floor.
for material in M.values():
    tables = [axis for axis in material.get('axes', {}).values() if axis.get('type') == 'table']
    for spec in tables + [alt for alt in material.get('alternatives', {}).values() if alt.get('type') == 'table']:
        data = np.loadtxt(OUT.parent / spec['file'], delimiter=',', comments='#')
        spec['valid_range_cm1'] = [float(data[0, 0]), float(data[-1, 0])]
        if np.any(data[:, 2] == 0):
            spec['note'] = 'Zero-loss rows reflect absent k data or source zeros; they do not establish a measured absorption floor.'
    if tables:
        lo, hi = material['valid_range_cm1']
        material['valid_range_cm1'] = [max(lo, *(t['valid_range_cm1'][0] for t in tables)), min(hi, *(t['valid_range_cm1'][1] for t in tables))]

# ------------------------------------------------------------------ Euler / tensor helpers written into YAML
def principal(eps2):
    a, b, c = eps2[0][0], eps2[0][1], eps2[1][1]
    th = 0.5 * np.degrees(np.arctan2(2 * b, a - c)); ev = np.linalg.eigvalsh(np.array([[a, b], [b, c]]))
    return round(float(th), 3), [round(float(v), 4) for v in ev[::-1]]
for n in ('Ga2O3_beta', 'CdWO4'):
    e = M[n]['model']['eps_inf']; th, ev = principal(e)
    M[n]['model']['eps_inf_as_rotated_diagonal'] = dict(diagonal=[ev[0], ev[1], e[2][2]], euler_deg=[th, 0.0, 0.0],
        note='eps_inf = R(euler) diag(...) R^T, rotation about z (= b).')

class NoAlias(yaml.SafeDumper):
    def ignore_aliases(self, data): return True

if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.glob("*.yaml"):
        path.unlink()
    order = ['name', 'aliases', 'status', 'tensor', 'frame', 'valid_range_cm1', 'axes', 'model', 'recipe', 'alternatives', 'notes', 'references']
    for n, d in M.items():
        dd = {k: d[k] for k in order if k in d}
        with (OUT / f"{n}.yaml").open("w", encoding="utf-8") as fh:
            fh.write(f'# {n} — generated by tools/build_library.py; edit there, not here.\n')
            yaml.dump(dd, fh, Dumper=NoAlias, sort_keys=False, allow_unicode=True, width=160, default_flow_style=None)
    print(len(M), 'materials written')
