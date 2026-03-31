from flask import Flask, render_template_string, send_file, request
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz
import io

app = Flask(__name__)

def get_fractal_resistance(df):
    if len(df) < 6: return None
    for i in range(len(df) - 4, 2, -1):
        if (df['High'].iloc[i] > df['High'].iloc[i-1] and 
            df['High'].iloc[i] > df['High'].iloc[i-2] and 
            df['High'].iloc[i] > df['High'].iloc[i+1] and 
            df['High'].iloc[i] > df['High'].iloc[i+2]):
            return df['High'].iloc[i]
    return None

def cek_breakout(simbol):
    try:
        ticker = yf.Ticker(simbol)
        # Ambil data lebih sedikit untuk efisiensi (1mo cukup)
        df = ticker.history(period="1mo", interval="1d")
        if df.empty or len(df) < 6: return None
        
        resistance = get_fractal_resistance(df)
        if resistance is None: return None
        
        high_hari_ini = df['High'].iloc[-1]
        close_hari_ini = df['Close'].iloc[-1]
        close_kemarin = df['Close'].iloc[-2]
        volume_hari_ini = df['Volume'].iloc[-1]
        high_kemarin = df['High'].iloc[-2]

        # Hitung % Perubahan Harga vs Closing Kemarin
        change_pct = ((close_hari_ini - close_kemarin) / close_kemarin) * 100

        if high_hari_ini > resistance and high_kemarin <= resistance:
            if volume_hari_ini > 5000000:
                status = "CLOSE ABOVE" if close_hari_ini > resistance else "HIGH ONLY"
                return {
                    "simbol": simbol.replace('.JK', ''), 
                    "status": status, 
                    "price": close_hari_ini,
                    "change": change_pct,
                    "vol": volume_hari_ini, 
                    "res": resistance
                }
        return None
    except Exception as e:
        return None

@app.route('/')
def home():
    # Contoh list diperpendek (Gunakan list lengkap Anda di sini)
    saham_pilihan = ['AALI.JK', 'ABBA.JK', 'ABDA.JK', 'ABMM.JK', 'ACES.JK', 'ACST.JK', 'ADES.JK', 'ADHI.JK', 'AISA.JK', 'AKKU.JK', 'AKPI.JK', 'AKRA.JK', 'AKSI.JK', 'ALDO.JK', 'ALKA.JK', 'ALMI.JK', 'ALTO.JK', 'AMAG.JK', 'AMFG.JK', 'AMIN.JK', 'AMRT.JK', 'ANJT.JK', 'ANTM.JK', 'APEX.JK', 'APIC.JK', 'APII.JK', 'APLI.JK', 'APLN.JK', 'ARGO.JK', 'ARII.JK', 'ARNA.JK', 'ARTA.JK', 'ARTI.JK', 'ARTO.JK', 'ASBI.JK', 'ASDM.JK', 'ASGR.JK', 'ASII.JK', 'ASJT.JK', 'ASMI.JK', 'ASRI.JK', 'ASRM.JK', 'ASSA.JK', 'ATIC.JK', 'AUTO.JK', 'BABP.JK', 'BACA.JK', 'BAJA.JK', 'BALI.JK', 'BAPA.JK', 'BATA.JK', 'BAYU.JK', 'BBCA.JK', 'BBHI.JK', 'BBKP.JK', 'BBLD.JK', 'BBMD.JK', 'BBNI.JK', 'BBRI.JK', 'BBRM.JK', 'BBTN.JK', 'BBYB.JK', 'BCAP.JK', 'BCIC.JK', 'BCIP.JK', 'BDMN.JK', 'BEKS.JK', 'BEST.JK', 'BFIN.JK', 'BGTG.JK', 'BHIT.JK', 'BIKA.JK', 'BIMA.JK', 'BINA.JK', 'BIPI.JK', 'BIPP.JK', 'BIRD.JK', 'BISI.JK', 'BJBR.JK', 'BJTM.JK', 'BKDP.JK', 'BKSL.JK', 'BKSW.JK', 'BLTA.JK', 'BLTZ.JK', 'BMAS.JK', 'BMRI.JK', 'BMSR.JK', 'BMTR.JK', 'BNBA.JK', 'BNBR.JK', 'BNGA.JK', 'BNII.JK', 'BNLI.JK', 'BOLT.JK', 'BPFI.JK', 'BPII.JK', 'BRAM.JK', 'BRMS.JK', 'BRNA.JK', 'BRPT.JK', 'BSDE.JK', 'BSIM.JK', 'BSSR.JK', 'BSWD.JK', 'BTEK.JK', 'BTEL.JK', 'BTON.JK', 'BTPN.JK', 'BUDI.JK', 'BUKK.JK', 'BULL.JK', 'BUMI.JK', 'BUVA.JK', 'BVIC.JK', 'BWPT.JK', 'BYAN.JK', 'CANI.JK', 'CASS.JK', 'CEKA.JK', 'CENT.JK', 'CFIN.JK', 'CINT.JK', 'CITA.JK', 'CLPI.JK', 'CMNP.JK', 'CMPP.JK', 'CNKO.JK', 'CNTX.JK', 'COWL.JK', 'CPIN.JK', 'CPRO.JK', 'CSAP.JK', 'CTBN.JK', 'CTRA.JK', 'CTTH.JK', 'DART.JK', 'DEFI.JK', 'DEWA.JK', 'DGIK.JK', 'DILD.JK', 'DKFT.JK', 'DLTA.JK', 'DMAS.JK', 'DNAR.JK', 'DNET.JK', 'DOID.JK', 'DPNS.JK', 'DSFI.JK', 'DSNG.JK', 'DSSA.JK', 'DUTI.JK', 'DVLA.JK', 'DYAN.JK', 'ECII.JK', 'EKAD.JK', 'ELSA.JK', 'ELTY.JK', 'EMDE.JK', 'EMTK.JK', 'ENRG.JK', 'EPMT.JK', 'ERAA.JK', 'ERTX.JK', 'ESSA.JK', 'ESTI.JK', 'ETWA.JK', 'EXCL.JK', 'FAST.JK', 'FASW.JK', 'FISH.JK', 'FMII.JK', 'FORU.JK', 'FPNI.JK', 'GAMA.JK', 'GDST.JK', 'GDYR.JK', 'GEMA.JK', 'GEMS.JK', 'GGRM.JK', 'GIAA.JK', 'GJTL.JK', 'GLOB.JK', 'GMTD.JK', 'GOLD.JK', 'GOLL.JK', 'GPRA.JK', 'GSMF.JK', 'GTBO.JK', 'GWSA.JK', 'GZCO.JK', 'HADE.JK', 'HDFA.JK', 'HERO.JK', 'HEXA.JK', 'HITS.JK', 'HMSP.JK', 'HOME.JK', 'HOTL.JK', 'HRUM.JK', 'IATA.JK', 'IBFN.JK', 'IBST.JK', 'ICBP.JK', 'ICON.JK', 'IGAR.JK', 'IIKP.JK', 'IKAI.JK', 'IKBI.JK', 'IMAS.JK', 'IMJS.JK', 'IMPC.JK', 'INAF.JK', 'INAI.JK', 'INCI.JK', 'INCO.JK', 'INDF.JK', 'INDR.JK', 'INDS.JK', 'INDX.JK', 'INDY.JK', 'INKP.JK', 'INPC.JK', 'INPP.JK', 'INRU.JK', 'INTA.JK', 'INTD.JK', 'INTP.JK', 'IPOL.JK', 'ISAT.JK', 'ISSP.JK', 'ITMA.JK', 'ITMG.JK', 'JAWA.JK', 'JECC.JK', 'JIHD.JK', 'JKON.JK', 'JPFA.JK', 'JRPT.JK', 'JSMR.JK', 'JSPT.JK', 'JTPE.JK', 'KAEF.JK', 'KARW.JK', 'KBLI.JK', 'KBLM.JK', 'KBLV.JK', 'KBRI.JK', 'KDSI.JK', 'KIAS.JK', 'KICI.JK', 'KIJA.JK', 'KKGI.JK', 'KLBF.JK', 'KOBX.JK', 'KOIN.JK', 'KONI.JK', 'KOPI.JK', 'KPIG.JK', 'KRAS.JK', 'KREN.JK', 'LAPD.JK', 'LCGP.JK', 'LEAD.JK', 'LINK.JK', 'LION.JK', 'LMAS.JK', 'LMPI.JK', 'LMSH.JK', 'LPCK.JK', 'LPGI.JK', 'LPIN.JK', 'LPKR.JK', 'LPLI.JK', 'LPPF.JK', 'LPPS.JK', 'LRNA.JK', 'LSIP.JK', 'LTLS.JK', 'MAGP.JK', 'MAIN.JK', 'MAPI.JK', 'MAYA.JK', 'MBAP.JK', 'MBSS.JK', 'MBTO.JK', 'MCOR.JK', 'MDIA.JK', 'MDKA.JK', 'MDLN.JK', 'MDRN.JK', 'MEDC.JK', 'MEGA.JK', 'MERK.JK', 'META.JK', 'MFMI.JK', 'MGNA.JK', 'MICE.JK', 'MIDI.JK', 'MIKA.JK', 'MIRA.JK', 'MITI.JK', 'MKPI.JK', 'MLBI.JK', 'MLIA.JK', 'MLPL.JK', 'MLPT.JK', 'MMLP.JK', 'MNCN.JK', 'MPMX.JK', 'MPPA.JK', 'MRAT.JK', 'MREI.JK', 'MSKY.JK', 'MTDL.JK', 'MTFN.JK', 'MTLA.JK', 'MTSM.JK', 'MYOH.JK', 'MYOR.JK', 'MYTX.JK', 'NELY.JK', 'NIKL.JK', 'NIRO.JK', 'NISP.JK', 'NOBU.JK', 'NRCA.JK', 'OCAP.JK', 'OKAS.JK', 'OMRE.JK', 'PADI.JK', 'PALM.JK', 'PANR.JK', 'PANS.JK', 'PBRX.JK', 'PDES.JK', 'PEGE.JK', 'PGAS.JK', 'PGLI.JK', 'PICO.JK', 'PJAA.JK', 'PKPK.JK', 'PLAS.JK', 'PLIN.JK', 'PNBN.JK', 'PNBS.JK', 'PNIN.JK', 'PNLF.JK', 'PSAB.JK', 'PSDN.JK', 'PSKT.JK', 'PTBA.JK', 'PTIS.JK', 'PTPP.JK', 'PTRO.JK', 'PTSN.JK', 'PTSP.JK', 'PUDP.JK', 'PWON.JK', 'PYFA.JK', 'RAJA.JK', 'RALS.JK', 'RANC.JK', 'RBMS.JK', 'RDTX.JK', 'RELI.JK', 'RICY.JK', 'RIGS.JK', 'RIMO.JK', 'RODA.JK', 'ROTI.JK', 'RUIS.JK', 'SAFE.JK', 'SAME.JK', 'SCCO.JK', 'SCMA.JK', 'SCPI.JK', 'SDMU.JK', 'SDPC.JK', 'SDRA.JK', 'SGRO.JK', 'SHID.JK', 'SIDO.JK', 'SILO.JK', 'SIMA.JK', 'SIMP.JK', 'SIPD.JK', 'SKBM.JK', 'SKLT.JK', 'SKYB.JK', 'SMAR.JK', 'SMBR.JK', 'SMCB.JK', 'SMDM.JK', 'SMDR.JK', 'SMGR.JK', 'SMMA.JK', 'SMMT.JK', 'SMRA.JK', 'SMRU.JK', 'SMSM.JK', 'SOCI.JK', 'SONA.JK', 'SPMA.JK', 'SQMI.JK', 'SRAJ.JK', 'SRIL.JK', 'SRSN.JK', 'SRTG.JK', 'SSIA.JK', 'SSMS.JK', 'SSTM.JK', 'STAR.JK', 'STTP.JK', 'SUGI.JK', 'SULI.JK', 'SUPR.JK', 'TALF.JK', 'TARA.JK', 'TAXI.JK', 'TBIG.JK', 'TBLA.JK', 'TBMS.JK', 'TCID.JK', 'TELE.JK', 'TFCO.JK', 'TGKA.JK', 'TIFA.JK', 'TINS.JK', 'TIRA.JK', 'TIRT.JK', 'TKIM.JK', 'TLKM.JK', 'TMAS.JK', 'TMPO.JK', 'TOBA.JK', 'TOTL.JK', 'TOTO.JK', 'TOWR.JK', 'TPIA.JK', 'TPMA.JK', 'TRAM.JK', 'TRIL.JK', 'TRIM.JK', 'TRIO.JK', 'TRIS.JK', 'TRST.JK', 'TRUS.JK', 'TSPC.JK', 'ULTJ.JK', 'UNIC.JK', 'UNIT.JK', 'UNSP.JK', 'UNTR.JK', 'UNVR.JK', 'VICO.JK', 'VINS.JK', 'VIVA.JK', 'VOKS.JK', 'VRNA.JK', 'WAPO.JK', 'WEHA.JK', 'WICO.JK', 'WIIM.JK', 'WIKA.JK', 'WINS.JK', 'WOMF.JK', 'WSKT.JK', 'WTON.JK', 'YPAS.JK', 'YULE.JK', 'ZBRA.JK', 'SHIP.JK', 'CASA.JK', 'DAYA.JK', 'DPUM.JK', 'IDPR.JK', 'JGLE.JK', 'KINO.JK', 'MARI.JK', 'MKNT.JK', 'MTRA.JK', 'OASA.JK', 'POWR.JK', 'INCF.JK', 'WSBP.JK', 'PBSA.JK', 'PRDA.JK', 'BOGA.JK', 'BRIS.JK', 'PORT.JK', 'CARS.JK', 'MINA.JK', 'CLEO.JK', 'TAMU.JK', 'CSIS.JK', 'TGRA.JK', 'FIRE.JK', 'TOPS.JK', 'KMTR.JK', 'ARMY.JK', 'MAPB.JK', 'WOOD.JK', 'HRTA.JK', 'MABA.JK', 'HOKI.JK', 'MPOW.JK', 'MARK.JK', 'NASA.JK', 'MDKI.JK', 'BELL.JK', 'KIOS.JK', 'GMFI.JK', 'MTWI.JK', 'ZINC.JK', 'MCAS.JK', 'PPRE.JK', 'WEGE.JK', 'PSSI.JK', 'MORA.JK', 'DWGL.JK', 'PBID.JK', 'JMAS.JK', 'CAMP.JK', 'IPCM.JK', 'PCAR.JK', 'LCKM.JK', 'BOSS.JK', 'HELI.JK', 'JSKY.JK', 'INPS.JK', 'GHON.JK', 'TDPM.JK', 'DFAM.JK', 'NICK.JK', 'BTPS.JK', 'SPTO.JK', 'PRIM.JK', 'HEAL.JK', 'TRUK.JK', 'PZZA.JK', 'TUGU.JK', 'MSIN.JK', 'SWAT.JK', 'TNCA.JK', 'MAPA.JK', 'TCPI.JK', 'IPCC.JK', 'RISE.JK', 'BPTR.JK', 'POLL.JK', 'NFCX.JK', 'MGRO.JK', 'NUSA.JK', 'FILM.JK', 'ANDI.JK', 'LAND.JK', 'MOLI.JK', 'PANI.JK', 'DIGI.JK', 'CITY.JK', 'SAPX.JK', 'SURE.JK', 'HKMU.JK', 'MPRO.JK', 'DUCK.JK', 'GOOD.JK', 'SKRN.JK', 'YELO.JK', 'CAKK.JK', 'SATU.JK', 'SOSS.JK', 'DEAL.JK', 'POLA.JK', 'DIVA.JK', 'LUCK.JK', 'URBN.JK', 'SOTS.JK', 'ZONE.JK', 'PEHA.JK', 'FOOD.JK', 'BEEF.JK', 'POLI.JK', 'CLAY.JK', 'NATO.JK', 'JAYA.JK', 'COCO.JK', 'MTPS.JK', 'CPRI.JK', 'HRME.JK', 'POSA.JK', 'JAST.JK', 'FITT.JK', 'BOLA.JK', 'CCSI.JK', 'SFAN.JK', 'POLU.JK', 'KJEN.JK', 'KAYU.JK', 'ITIC.JK', 'PAMG.JK', 'IPTV.JK', 'BLUE.JK', 'ENVY.JK', 'EAST.JK', 'LIFE.JK', 'FUJI.JK', 'KOTA.JK', 'INOV.JK', 'ARKA.JK', 'SMKL.JK', 'HDIT.JK', 'KEEN.JK', 'BAPI.JK', 'TFAS.JK', 'GGRP.JK', 'OPMS.JK', 'NZIA.JK', 'SLIS.JK', 'PURE.JK', 'IRRA.JK', 'DMMX.JK', 'SINI.JK', 'WOWS.JK', 'ESIP.JK', 'TEBE.JK', 'KEJU.JK', 'PSGO.JK', 'AGAR.JK', 'IFSH.JK', 'REAL.JK', 'IFII.JK', 'PMJS.JK', 'UCID.JK', 'GLVA.JK', 'PGJO.JK', 'AMAR.JK', 'CSRA.JK', 'INDO.JK', 'AMOR.JK', 'TRIN.JK', 'DMND.JK', 'PURA.JK', 'PTPW.JK', 'TAMA.JK', 'IKAN.JK', 'SAMF.JK', 'SBAT.JK', 'KBAG.JK', 'CBMF.JK', 'RONY.JK', 'CSMI.JK', 'BBSS.JK', 'BHAT.JK', 'CASH.JK', 'TECH.JK', 'EPAC.JK', 'UANG.JK', 'PGUN.JK', 'SOFA.JK', 'PPGL.JK', 'TOYS.JK', 'SGER.JK', 'TRJA.JK', 'PNGO.JK', 'SCNP.JK', 'BBSI.JK', 'KMDS.JK', 'PURI.JK', 'SOHO.JK', 'HOMI.JK', 'ROCK.JK', 'ENZO.JK', 'PLAN.JK', 'PTDU.JK', 'ATAP.JK', 'VICI.JK', 'PMMP.JK', 'BANK.JK', 'WMUU.JK', 'EDGE.JK', 'UNIQ.JK', 'BEBS.JK', 'SNLK.JK', 'ZYRX.JK', 'LFLO.JK', 'FIMP.JK', 'TAPG.JK', 'NPGF.JK', 'LUCY.JK', 'ADCP.JK', 'HOPE.JK', 'MGLV.JK', 'TRUE.JK', 'LABA.JK', 'ARCI.JK', 'IPAC.JK', 'MASB.JK', 'BMHS.JK', 'FLMC.JK', 'NICL.JK', 'UVCR.JK', 'BUKA.JK', 'HAIS.JK', 'OILS.JK', 'GPSO.JK', 'MCOL.JK', 'RSGK.JK', 'RUNS.JK', 'SBMA.JK', 'CMNT.JK', 'GTSI.JK', 'IDEA.JK', 'KUAS.JK', 'BOBA.JK', 'MTEL.JK', 'DEPO.JK', 'BINO.JK', 'CMRY.JK', 'WGSH.JK', 'TAYS.JK', 'WMPP.JK', 'RMKE.JK', 'OBMD.JK', 'AVIA.JK', 'IPPE.JK', 'NASI.JK', 'BSML.JK', 'DRMA.JK', 'ADMR.JK', 'SEMA.JK', 'ASLC.JK', 'NETV.JK', 'BAUT.JK', 'ENAK.JK', 'NTBK.JK', 'SMKM.JK', 'STAA.JK', 'NANO.JK', 'BIKE.JK', 'WIRG.JK', 'SICO.JK', 'GOTO.JK', 'TLDN.JK', 'MTMH.JK', 'WINR.JK', 'IBOS.JK', 'OLIV.JK', 'ASHA.JK', 'SWID.JK', 'TRGU.JK', 'ARKO.JK', 'CHEM.JK', 'DEWI.JK', 'AXIO.JK', 'KRYA.JK', 'HATM.JK', 'RCCC.JK', 'GULA.JK', 'JARR.JK', 'AMMS.JK', 'RAFI.JK', 'KKES.JK', 'ELPI.JK', 'EURO.JK', 'KLIN.JK', 'TOOL.JK', 'BUAH.JK', 'CRAB.JK', 'MEDS.JK', 'COAL.JK', 'PRAY.JK', 'CBUT.JK', 'BELI.JK', 'MKTR.JK', 'OMED.JK', 'BSBK.JK', 'PDPP.JK', 'KDTN.JK', 'ZATA.JK', 'NINE.JK', 'MMIX.JK', 'PADA.JK', 'ISAP.JK', 'VTNY.JK', 'SOUL.JK', 'ELIT.JK', 'BEER.JK', 'CBPE.JK', 'SUNI.JK', 'CBRE.JK', 'WINE.JK', 'BMBL.JK', 'PEVE.JK', 'LAJU.JK', 'FWCT.JK', 'NAYZ.JK', 'IRSX.JK', 'PACK.JK', 'VAST.JK', 'CHIP.JK', 'HALO.JK', 'KING.JK', 'PGEO.JK', 'FUTR.JK', 'HILL.JK', 'BDKR.JK', 'PTMP.JK', 'SAGE.JK', 'TRON.JK', 'CUAN.JK', 'NSSS.JK', 'GTRA.JK', 'HAJJ.JK', 'JATI.JK', 'TYRE.JK', 'MPXL.JK', 'SMIL.JK', 'KLAS.JK', 'MAXI.JK', 'VKTR.JK', 'RELF.JK', 'AMMN.JK', 'CRSN.JK', 'GRPM.JK', 'WIDI.JK', 'TGUK.JK', 'INET.JK', 'MAHA.JK', 'RMKO.JK', 'CNMA.JK', 'FOLK.JK', 'HBAT.JK', 'GRIA.JK', 'PPRI.JK', 'ERAL.JK', 'CYBR.JK', 'MUTU.JK', 'LMAX.JK', 'HUMI.JK', 'MSIE.JK', 'RSCH.JK', 'BABY.JK', 'AEGS.JK', 'IOTF.JK', 'KOCI.JK', 'PTPS.JK', 'BREN.JK', 'STRK.JK', 'KOKA.JK', 'LOPI.JK', 'UDNG.JK', 'RGAS.JK', 'MSTI.JK', 'IKPM.JK', 'AYAM.JK', 'SURI.JK', 'ASLI.JK', 'GRPH.JK', 'SMGA.JK', 'UNTD.JK', 'TOSK.JK', 'MPIX.JK', 'ALII.JK', 'MKAP.JK', 'MEJA.JK', 'LIVE.JK', 'HYGN.JK', 'BAIK.JK', 'VISI.JK', 'AREA.JK', 'MHKI.JK', 'ATLA.JK', 'DATA.JK', 'SOLA.JK', 'BATR.JK', 'SPRE.JK', 'PART.JK', 'GOLF.JK', 'ISEA.JK', 'BLES.JK', 'GUNA.JK', 'LABS.JK', 'DOSS.JK', 'NEST.JK', 'PTMR.JK', 'VERN.JK', 'DAAZ.JK', 'BOAT.JK', 'NAIK.JK', 'AADI.JK', 'MDIY.JK', 'KSIX.JK', 'RATU.JK', 'YOII.JK', 'HGII.JK', 'BRRC.JK', 'DGWG.JK', 'CBDK.JK', 'OBAT.JK', 'MINE.JK', 'ASPR.JK', 'PSAT.JK', 'COIN.JK', 'CDIA.JK', 'BLOG.JK', 'MERI.JK', 'CHEK.JK', 'PMUI.JK', 'EMAS.JK', 'PJHB.JK', 'RLCO.JK', 'SUPA.JK', 'KAQI.JK', 'YUPI.JK', 'FORE.JK', 'MDLA.JK', 'DKHH.JK', 'AYLS.JK', 'DADA.JK', 'ASPI.JK', 'ESTA.JK', 'BESS.JK', 'AMAN.JK', 'CARE.JK', 'PIPA.JK', 'NCKL.JK', 'MENN.JK', 'AWAN.JK', 'MBMA.JK', 'RAAM.JK', 'DOOH.JK', 'CGAS.JK', 'NICE.JK', 'MSJA.JK', 'SMLE.JK', 'ACRO.JK', 'MANG.JK', 'WIFI.JK', 'FAPA.JK', 'DCII.JK', 'KETR.JK', 'DGNS.JK', 'UFOE.JK', 'ADMF.JK', 'ADMG.JK', 'ADRO.JK', 'AGII.JK', 'AGRO.JK', 'AGRS.JK', 'AHAP.JK', 'AIMS.JK', 'PNSE.JK', 'POLY.JK', 'POOL.JK', 'PPRO.JK'] 
    
    results = []
    for s in saham_pilihan:
        res = cek_breakout(s)
        if res: results.append(res)

        # Tentukan timezone Jakarta (WIB)
        timezone = pytz.timezone('Asia/Jakarta')
        # Ambil waktu sekarang sesuai timezone tersebut
        now = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S WIB")

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Breakout Scanner</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        </style>
    </head>
    <body class="p-4 md:p-10">
        <div class="max-w-5xl mx-auto">
            <div id="capture-area" class="bg-white p-8 rounded-xl shadow-lg border border-gray-200">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h1 class="text-3xl font-bold text-gray-800">🚀 Fractal Breakout Watchlist</h1>
                        <p class="text-gray-500 mt-1">Bursa Efek Indonesia (IDX)</p>
                    </div>
                    <div class="text-right">
                        <p class="text-sm font-semibold text-gray-400 uppercase tracking-wider">Waktu Screening</p>
                        <p class="text-lg font-mono text-blue-600">{{ timestamp }}</p>
                    </div>
                </div>

                <div class="overflow-hidden rounded-lg border border-gray-200">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase">Ticker</th>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase">Status</th>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase text-right">Price</th>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase text-right">Change (%)</th>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase text-right">Up Fractal</th>
                                <th class="px-6 py-4 text-sm font-semibold text-gray-700 uppercase text-right">Volume</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            {% for r in results %}
                            <tr class="hover:bg-gray-50 transition-colors">
                                <td class="px-6 py-4 font-bold text-gray-900">{{ r.simbol }}</td>
                                <td class="px-6 py-4">
                                    <span class="px-3 py-1 rounded-full text-xs font-bold {{ 'bg-green-100 text-green-700' if r.status == 'CLOSE ABOVE' else 'bg-yellow-100 text-yellow-700' }}">
                                        {{ r.status }}
                                    </span>
                                </td>
                                <td class="px-6 py-4 text-right font-mono">{{ "{:,.0f}".format(r.price) }}</td>
                                <td class="px-6 py-4 text-right font-bold {{ 'text-green-600' if r.change > 0 else 'text-red-600' }}">
                                    {{ "+" if r.change > 0 }}{{ "%.2f"|format(r.change) }}%
                                </td>
                                <td class="px-6 py-4 text-right text-gray-600 font-mono">{{ "{:,.0f}".format(r.res) }}</td>
                                <td class="px-6 py-4 text-right text-gray-600 font-mono">{{ "{:,.0f}".format(r.vol) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                {% if not results %}
                <div class="text-center py-12">
                    <p class="text-gray-400 italic">Tidak ada saham yang memenuhi kriteria breakout saat ini.</p>
                </div>
                {% endif %}

                <div class="mt-6 pt-6 border-t border-gray-100 text-xs text-gray-400 flex justify-between">
                    <span>Screener by MOSYA (https://stockbit.com/mohsyaifudin93)</span>
                    <span>Data provided by Yahoo Finance</span>
                </div>
            </div>

            <div class="mt-8 flex justify-center">
                <button onclick="downloadImage()" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-bold shadow-lg transition-all transform hover:scale-105 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                    Simpan Hasil (JPEG)
                </button>
                <button onclick="downloadExcel()" class="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-full font-bold shadow-lg transition-all transform hover:scale-105 flex items-center gap-2 ml-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd" />
                    </svg>
                    Simpan Excel (.xlsx)
                </button>
            </div>
        </div>

        <script>
            function downloadImage() {
                const element = document.getElementById('capture-area');
                html2canvas(element, {
                    scale: 2, // Kualitas lebih tinggi
                    backgroundColor: "#f3f4f6"
                }).then(canvas => {
                    const link = document.createElement('a');
                    link.download = 'Screening-Saham-' + new Date().getTime() + '.jpg';
                    link.href = canvas.toDataURL('image/jpeg', 0.9);
                    link.click();
                });
            }
            function downloadExcel() {
                // Ambil data results dari Flask (menggunakan Jinja2 filter tojson)
                const data = {{ results|tojson }};
                if (data.length === 0) {
                    alert("Tidak ada data untuk diunduh");
                    return;
                }
                
                // Kirim data ke route /download_excel melalui URL parameter
                const jsonStr = JSON.stringify(data);
                window.location.href = "/download_excel?data=" + encodeURIComponent(jsonStr);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, results=results, timestamp=now)

@app.route('/download_excel')
def download_excel():
    # Mengambil data dari parameter URL (dikirim dari frontend)
    data_json = request.args.get('data')
    import json
    results = json.loads(data_json)
    
    if not results:
        return "No data to download", 400

    # Convert ke DataFrame
    df = pd.DataFrame(results)
    
    # Beri nama kolom yang lebih rapi untuk Excel
    df.columns = ['Ticker', 'Status', 'Price', 'Change (%)', 'Volume', 'Up Fractal']

    # Simpan ke memory buffer (agar tidak perlu simpan file fisik di server Vercel)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Screening_Results')
    output.seek(0)

    # Nama file sesuai waktu sekarang (WIB)
    tz = pytz.timezone('Asia/Jakarta')
    filename = datetime.now(tz).strftime("Screening_%Y-%m-%d_%H%M%S.xlsx")

    return send_file(output, 
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                     as_attachment=True, 
                     download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)
