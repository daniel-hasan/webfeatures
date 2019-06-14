# -*- coding: utf-8 -*-

'''
Created on 8 de ago de 2017
Entidades basicas para serem usadas
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''
from datetime import datetime
from enum import Enum, IntEnum


class CheckTime(object):
    def __init__(self):
        self.time = datetime.now()
        
    def finishTime(self):
        delta = datetime.now()-self.time
        self.time = datetime.now()
        return delta
    def printDelta(self,task):
        delta = self.finishTime()
        print(task+" done in "+str(delta.total_seconds()))
class FeatureTimePerDocumentEnum(Enum):
    '''
    Created on 8 de ago de 2017
    Tempo médio para extrair uma determinada feature no documento
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
    '''
    MICROSECONDS = "microseconds"
    MILLISECONDS = "milliseconds"
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"

    def is_higher_than(self,timePerDocumentFeature):
        '''
        Created on 17 de ago de 2017
        Verifica se o objeto corrente representa uma velocidade maior do que o objeto passado como argumento
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
        '''
        #ve o indice do enum corrente
        int_curr_idx = self._check_velocity_index()
        #ve o indice do enum passado como parametro
        int_arg_idx = timePerDocumentFeature._check_velocity_index()
        return int_curr_idx>int_arg_idx 
    def _check_velocity_index(self):
        ARR_ORDER_PER_VELOCITY = [FeatureTimePerDocumentEnum.MICROSECONDS,
                                  FeatureTimePerDocumentEnum.MILLISECONDS,
                                  FeatureTimePerDocumentEnum.SECONDS,
                                  FeatureTimePerDocumentEnum.MINUTES,
                                  FeatureTimePerDocumentEnum.HOURS]
        for int_i,enum in enumerate(ARR_ORDER_PER_VELOCITY):
            if(self == enum):
                return int_i
        raise Exception("Não foi possível encontrar este enum num array ARR_ORDER_PER_VELOCITY")
    
class FormatEnum(Enum):
    text_plain = "Text-Plain"
    HTML = "HTML"
    #mark_down = "Mark-Down" Nao impleentado ainda
    
class LanguageEnum(Enum):

    
    gv = "Manx"
    gu = "Gujarati"
    gd = "Scottish Gaelic; Gaelic"
    ga = "Irish"
    gn = "Guaraní"
    gl = "Galician"
    ty = "Tahitian"
    tw = "Twi"
    tt = "Tatar"
    tr = "Turkish"
    ts = "Tsonga"
    tn = "Tswana"
    to = "Tonga (Tonga Islands)"
    tl = "Tagalog"
    tk = "Turkmen"
    th = "Thai"
    ti = "Tigrinya"
    tg = "Tajik"
    te = "Telugu"
    ta = "Tamil"
    de = "German"
    da = "Danish"
    dv = "Divehi; Dhivehi; Maldivian;"
    qu = "Quechua"
    zh = "Chinese"
    za = "Zhuang, Chuang"
    wa = "Walloon"
    wo = "Wolof"
    jv = "Javanese"
    ja = "Japanese"
    ch = "Chamorro"
    co = "Corsican"
    ca = "Catalan; Valencian"
    ce = "Chechen"
    cy = "Welsh"
    cs = "Czech"
    cr = "Cree"
    cv = "Chuvash"
    cu = "Old Church Slavonic, Church Slavic, Church Slavonic, Old Bulgarian, Old Slavonic"
    ps = "Pashto, Pushto"
    pt = "Portuguese"
    pa = "Panjabi, Punjabi"
    pi = "Pāli"
    pl = "Polish"
    mg = "Malagasy"
    ml = "Malayalam"
    mn = "Mongolian"
    mi = "Māori"
    mh = "Marshallese"
    mk = "Macedonian"
    mt = "Maltese"
    ms = "Malay"
    mr = "Marathi (Marāṭhī)"
    my = "Burmese"
    ve = "Venda"
    vi = "Vietnamese"
    is_ = "Icelandic"
    iu = "Inuktitut"
    it = "Italian"
    vo = "Volapük"
    ii = "Nuosu"
    ik = "Inupiaq"
    io = "Ido"
    ia = "Interlingua"
    ie = "Interlingue"
    id = "Indonesian"
    ig = "Igbo"
    fr = "French"
    fy = "Western Frisian"
    fa = "Persian"
    ff = "Fula; Fulah; Pulaar; Pular"
    fi = "Finnish"
    fj = "Fijian"
    fo = "Faroese"
    ss = "Swati"
    sr = "Serbian"
    sq = "Albanian"
    sw = "Swahili"
    sv = "Swedish"
    su = "Sundanese"
    st = "Southern Sotho"
    sk = "Slovak"
    si = "Sinhala, Sinhalese"
    so = "Somali"
    sn = "Shona"
    sm = "Samoan"
    sl = "Slovene"
    sc = "Sardinian"
    sa = "Sanskrit (Saṁskṛta)"
    sg = "Sango"
    se = "Northern Sami"
    sd = "Sindhi"
    lg = "Luganda"
    lb = "Luxembourgish, Letzeburgesch"
    la = "Latin"
    ln = "Lingala"
    lo = "Lao"
    li = "Limburgish, Limburgan, Limburger"
    lv = "Latvian"
    lt = "Lithuanian"
    lu = "Luba-Katanga"
    yi = "Yiddish"
    yo = "Yoruba"
    el = "Greek, Modern"
    eo = "Esperanto"
    en = "English"
    ee = "Ewe"
    eu = "Basque"
    et = "Estonian"
    es = "Spanish; Castilian"
    ru = "Russian"
    rw = "Kinyarwanda"
    rm = "Romansh"
    rn = "Kirundi"
    ro = "Romanian, Moldavian, Moldovan"
    be = "Belarusian"
    bg = "Bulgarian"
    ba = "Bashkir"
    bm = "Bambara"
    bn = "Bengali"
    bo = "Tibetan Standard, Tibetan, Central"
    bh = "Bihari"
    bi = "Bislama"
    br = "Breton"
    bs = "Bosnian"
    om = "Oromo"
    oj = "Ojibwe, Ojibwa"
    oc = "Occitan"
    os = "Ossetian, Ossetic"
    or_ = "Oriya"
    xh = "Xhosa"
    hz = "Herero"
    hy = "Armenian"
    hr = "Croatian"
    ht = "Haitian; Haitian Creole"
    hu = "Hungarian"
    hi = "Hindi"
    ho = "Hiri Motu"
    ha = "Hausa"
    he = "Hebrew (modern)"
    uz = "Uzbek"
    ur = "Urdu"
    uk = "Ukrainian"
    ug = "Uighur, Uyghur"
    aa = "Afar"
    ab = "Abkhaz"
    ae = "Avestan"
    af = "Afrikaans"
    ak = "Akan"
    am = "Amharic"
    an = "Aragonese"
    as_ = "Assamese"
    ar = "Arabic"
    av = "Avaric"
    ay = "Aymara"
    az = "Azerbaijani"
    nl = "Dutch"
    nn = "Norwegian Nynorsk"
    no = "Norwegian"
    na = "Nauru"
    nb = "Norwegian Bokmål"
    nd = "North Ndebele"
    ne = "Nepali"
    ng = "Ndonga"
    ny = "Chichewa; Chewa; Nyanja"
    nr = "South Ndebele"
    nv = "Navajo, Navaho"
    ka = "Georgian"
    kg = "Kongo"
    kk = "Kazakh"
    kj = "Kwanyama, Kuanyama"
    ki = "Kikuyu, Gikuyu"
    ko = "Korean"
    kn = "Kannada"
    km = "Khmer"
    kl = "Kalaallisut, Greenlandic"
    ks = "Kashmiri"
    kr = "Kanuri"
    kw = "Cornish"
    kv = "Komi"
    ku = "Kurdish"
    ky = "Kirghiz, Kyrgyz"
