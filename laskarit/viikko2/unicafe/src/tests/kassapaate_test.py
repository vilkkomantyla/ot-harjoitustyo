import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    def test_rahamaara_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    
    def test_myytyjen_lounaiden_maara_oikea(self):
        self.assertEqual(self.kassapaate.edulliset + self.kassapaate.maukkaat, 0)

    def test_edullisen_toimivuus_jos_rahamaara_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(250)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_edullisen_toimivuus_jos_rahamaara_ei_riittava(self):
        self.kassapaate.syo_edullisesti_kateisella(230)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullisen_kateisen_vaihtoraha_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(250) == 10
        self.kassapaate.syo_edullisesti_kateisella(230) == 230
    
    def test_maukkaan_toimivuus_jos_rahamaara_riittava(self):
        self.kassapaate.syo_maukkaasti_kateisella(410)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_maukkaan_toimivuus_jos_rahamaara_ei_riittava(self):
        self.kassapaate.syo_maukkaasti_kateisella(390)
        
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukkaan_kateisen_vaihtoraha_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(410) == 10
        self.kassapaate.syo_maukkaasti_kateisella(390) == 390
    
    def test_korttiosto_toimii_edullisen_kanssa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        
        self.maksukortti.saldo == 1000-240
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.kassapaate.kassassa_rahaa == 100000
    
    def test_korttiosto_toimii_maukkaan_kanssa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        
        self.maksukortti.saldo == 1000-400
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.kassapaate.kassassa_rahaa == 100000
    
    def test_korttiosto_palauttaa_truen_jos_arvo_riittää(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti) == True
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti) == True
    
    def test_korttiosto_toimii_oikein_edullisen_kanssa_jos_ei_tarpeeksi_rahaa(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        
        kortti.saldo == 100
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.kassapaate.kassassa_rahaa == 100000

    def test_korttiosto_toimii_oikein_maukkaan_kanssa_jos_ei_tarpeeksi_rahaa(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        
        kortti.saldo == 100
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.kassapaate.kassassa_rahaa == 100000
    
    def test_korttiosto_palauttaa_falsen_jos_arvo_ei_riita(self):
        kortti = Maksukortti(100)
        
        self.kassapaate.syo_maukkaasti_kortilla(kortti) == False
        self.kassapaate.syo_edullisesti_kortilla(kortti) == False
    
    def test_rahaa_ladattaessa_kortin_ja_kassan_saldot_muuttuu(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 200)

        self.assertEqual(self.maksukortti.saldo, 1200)
        self.kassapaate.kassassa_rahaa == 100200
    
    def test_rahaa_ladatessa_ei_tapahdu_mitaan_jos_arvo_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1) == None