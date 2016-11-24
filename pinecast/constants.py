# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.utils.translation import ugettext_lazy

MILESTONES = [1, 100, 250, 500, 1000, 2000, 5000, 7500, 10000, 15000, 20000,
              50000, 100000, 150000, 250000, 500000, 1000000, 2000000, 5000000,
              10000000, float('inf')]

# This is the list of iOS locales. Probably not complete but good enough.
# https://gist.github.com/jacobbubu/1836273
locales = {
    'af_NA': ugettext_lazy(u'Afrikaans (Namibia)'),
    'af_ZA': ugettext_lazy(u'Afrikaans (South Africa)'),
    'af': ugettext_lazy(u'Afrikaans'),
    'ak_GH': ugettext_lazy(u'Akan (Ghana)'),
    'ak': ugettext_lazy(u'Akan'),
    'sq_AL': ugettext_lazy(u'Albanian (Albania)'),
    'sq': ugettext_lazy(u'Albanian'),
    'am_ET': ugettext_lazy(u'Amharic (Ethiopia)'),
    'am': ugettext_lazy(u'Amharic'),
    'ar_DZ': ugettext_lazy(u'Arabic (Algeria)'),
    'ar_BH': ugettext_lazy(u'Arabic (Bahrain)'),
    'ar_EG': ugettext_lazy(u'Arabic (Egypt)'),
    'ar_IQ': ugettext_lazy(u'Arabic (Iraq)'),
    'ar_JO': ugettext_lazy(u'Arabic (Jordan)'),
    'ar_KW': ugettext_lazy(u'Arabic (Kuwait)'),
    'ar_LB': ugettext_lazy(u'Arabic (Lebanon)'),
    'ar_LY': ugettext_lazy(u'Arabic (Libya)'),
    'ar_MA': ugettext_lazy(u'Arabic (Morocco)'),
    'ar_OM': ugettext_lazy(u'Arabic (Oman)'),
    'ar_QA': ugettext_lazy(u'Arabic (Qatar)'),
    'ar_SA': ugettext_lazy(u'Arabic (Saudi Arabia)'),
    'ar_SD': ugettext_lazy(u'Arabic (Sudan)'),
    'ar_SY': ugettext_lazy(u'Arabic (Syria)'),
    'ar_TN': ugettext_lazy(u'Arabic (Tunisia)'),
    'ar_AE': ugettext_lazy(u'Arabic (United Arab Emirates)'),
    'ar_YE': ugettext_lazy(u'Arabic (Yemen)'),
    'ar': ugettext_lazy(u'Arabic'),
    'hy_AM': ugettext_lazy(u'Armenian (Armenia)'),
    'hy': ugettext_lazy(u'Armenian'),
    'as_IN': ugettext_lazy(u'Assamese (India)'),
    'as': ugettext_lazy(u'Assamese'),
    'asa_TZ': ugettext_lazy(u'Asu (Tanzania)'),
    'asa': ugettext_lazy(u'Asu'),
    'az_Cyrl': ugettext_lazy(u'Azerbaijani (Cyrillic)'),
    'az_Cyrl_AZ': ugettext_lazy(u'Azerbaijani (Cyrillic, Azerbaijan)'),
    'az_Latn': ugettext_lazy(u'Azerbaijani (Latin)'),
    'az_Latn_AZ': ugettext_lazy(u'Azerbaijani (Latin, Azerbaijan)'),
    'az': ugettext_lazy(u'Azerbaijani'),
    'bm_ML': ugettext_lazy(u'Bambara (Mali)'),
    'bm': ugettext_lazy(u'Bambara'),
    'eu_ES': ugettext_lazy(u'Basque (Spain)'),
    'eu': ugettext_lazy(u'Basque'),
    'be_BY': ugettext_lazy(u'Belarusian (Belarus)'),
    'be': ugettext_lazy(u'Belarusian'),
    'bem_ZM': ugettext_lazy(u'Bemba (Zambia)'),
    'bem': ugettext_lazy(u'Bemba'),
    'bez_TZ': ugettext_lazy(u'Bena (Tanzania)'),
    'bez': ugettext_lazy(u'Bena'),
    'bn_BD': ugettext_lazy(u'Bengali (Bangladesh)'),
    'bn_IN': ugettext_lazy(u'Bengali (India)'),
    'bn': ugettext_lazy(u'Bengali'),
    'bs_BA': ugettext_lazy(u'Bosnian (Bosnia and Herzegovina)'),
    'bs': ugettext_lazy(u'Bosnian'),
    'bg_BG': ugettext_lazy(u'Bulgarian (Bulgaria)'),
    'bg': ugettext_lazy(u'Bulgarian'),
    'my_MM': ugettext_lazy(u'Burmese (Myanmar [Burma])'),
    'my': ugettext_lazy(u'Burmese'),
    'ca_ES': ugettext_lazy(u'Catalan (Spain)'),
    'ca': ugettext_lazy(u'Catalan'),
    'tzm_Latn': ugettext_lazy(u'Central Morocco Tamazight (Latin)'),
    'tzm_Latn_MA': ugettext_lazy(u'Central Morocco Tamazight (Latin, Morocco)'),
    'tzm': ugettext_lazy(u'Central Morocco Tamazight'),
    'chr_US': ugettext_lazy(u'Cherokee (United States)'),
    'chr': ugettext_lazy(u'Cherokee'),
    'cgg_UG': ugettext_lazy(u'Chiga (Uganda)'),
    'cgg': ugettext_lazy(u'Chiga'),
    'zh_Hans': ugettext_lazy(u'Chinese (Simplified Han)'),
    'zh_Hans_CN': ugettext_lazy(u'Chinese (Simplified Han, China)'),
    'zh_Hans_HK': ugettext_lazy(u'Chinese (Simplified Han, Hong Kong SAR China)'),
    'zh_Hans_MO': ugettext_lazy(u'Chinese (Simplified Han, Macau SAR China)'),
    'zh_Hans_SG': ugettext_lazy(u'Chinese (Simplified Han, Singapore)'),
    'zh_Hant': ugettext_lazy(u'Chinese (Traditional Han)'),
    'zh_Hant_HK': ugettext_lazy(u'Chinese (Traditional Han, Hong Kong SAR China)'),
    'zh_Hant_MO': ugettext_lazy(u'Chinese (Traditional Han, Macau SAR China)'),
    'zh_Hant_TW': ugettext_lazy(u'Chinese (Traditional Han, Taiwan)'),
    'zh': ugettext_lazy(u'Chinese'),
    'kw_GB': ugettext_lazy(u'Cornish (United Kingdom)'),
    'kw': ugettext_lazy(u'Cornish'),
    'hr_HR': ugettext_lazy(u'Croatian (Croatia)'),
    'hr': ugettext_lazy(u'Croatian'),
    'cs_CZ': ugettext_lazy(u'Czech (Czech Republic)'),
    'cs': ugettext_lazy(u'Czech'),
    'da_DK': ugettext_lazy(u'Danish (Denmark)'),
    'da': ugettext_lazy(u'Danish'),
    'nl_BE': ugettext_lazy(u'Dutch (Belgium)'),
    'nl_NL': ugettext_lazy(u'Dutch (Netherlands)'),
    'nl': ugettext_lazy(u'Dutch'),
    'ebu_KE': ugettext_lazy(u'Embu (Kenya)'),
    'ebu': ugettext_lazy(u'Embu'),
    'en_AS': ugettext_lazy(u'English (American Samoa)'),
    'en_AU': ugettext_lazy(u'English (Australia)'),
    'en_BE': ugettext_lazy(u'English (Belgium)'),
    'en_BZ': ugettext_lazy(u'English (Belize)'),
    'en_BW': ugettext_lazy(u'English (Botswana)'),
    'en_CA': ugettext_lazy(u'English (Canada)'),
    'en_GU': ugettext_lazy(u'English (Guam)'),
    'en_HK': ugettext_lazy(u'English (Hong Kong SAR China)'),
    'en_IN': ugettext_lazy(u'English (India)'),
    'en_IE': ugettext_lazy(u'English (Ireland)'),
    'en_JM': ugettext_lazy(u'English (Jamaica)'),
    'en_MT': ugettext_lazy(u'English (Malta)'),
    'en_MH': ugettext_lazy(u'English (Marshall Islands)'),
    'en_MU': ugettext_lazy(u'English (Mauritius)'),
    'en_NA': ugettext_lazy(u'English (Namibia)'),
    'en_NZ': ugettext_lazy(u'English (New Zealand)'),
    'en_MP': ugettext_lazy(u'English (Northern Mariana Islands)'),
    'en_PK': ugettext_lazy(u'English (Pakistan)'),
    'en_PH': ugettext_lazy(u'English (Philippines)'),
    'en_SG': ugettext_lazy(u'English (Singapore)'),
    'en_ZA': ugettext_lazy(u'English (South Africa)'),
    'en_TT': ugettext_lazy(u'English (Trinidad and Tobago)'),
    'en_UM': ugettext_lazy(u'English (U.S. Minor Outlying Islands)'),
    'en_VI': ugettext_lazy(u'English (U.S. Virgin Islands)'),
    'en_GB': ugettext_lazy(u'English (United Kingdom)'),
    'en_US': ugettext_lazy(u'English (United States)'),
    'en_ZW': ugettext_lazy(u'English (Zimbabwe)'),
    'en': ugettext_lazy(u'English'),
    'eo': ugettext_lazy(u'Esperanto'),
    'et_EE': ugettext_lazy(u'Estonian (Estonia)'),
    'et': ugettext_lazy(u'Estonian'),
    'ee_GH': ugettext_lazy(u'Ewe (Ghana)'),
    'ee_TG': ugettext_lazy(u'Ewe (Togo)'),
    'ee': ugettext_lazy(u'Ewe'),
    'fo_FO': ugettext_lazy(u'Faroese (Faroe Islands)'),
    'fo': ugettext_lazy(u'Faroese'),
    'fil_PH': ugettext_lazy(u'Filipino (Philippines)'),
    'fil': ugettext_lazy(u'Filipino'),
    'fi_FI': ugettext_lazy(u'Finnish (Finland)'),
    'fi': ugettext_lazy(u'Finnish'),
    'fr_BE': ugettext_lazy(u'French (Belgium)'),
    'fr_BJ': ugettext_lazy(u'French (Benin)'),
    'fr_BF': ugettext_lazy(u'French (Burkina Faso)'),
    'fr_BI': ugettext_lazy(u'French (Burundi)'),
    'fr_CM': ugettext_lazy(u'French (Cameroon)'),
    'fr_CA': ugettext_lazy(u'French (Canada)'),
    'fr_CF': ugettext_lazy(u'French (Central African Republic)'),
    'fr_TD': ugettext_lazy(u'French (Chad)'),
    'fr_KM': ugettext_lazy(u'French (Comoros)'),
    'fr_CG': ugettext_lazy(u'French (Congo - Brazzaville)'),
    'fr_CD': ugettext_lazy(u'French (Congo - Kinshasa)'),
    'fr_CI': ugettext_lazy(u'French (Côte d’Ivoire)'),
    'fr_DJ': ugettext_lazy(u'French (Djibouti)'),
    'fr_GQ': ugettext_lazy(u'French (Equatorial Guinea)'),
    'fr_FR': ugettext_lazy(u'French (France)'),
    'fr_GA': ugettext_lazy(u'French (Gabon)'),
    'fr_GP': ugettext_lazy(u'French (Guadeloupe)'),
    'fr_GN': ugettext_lazy(u'French (Guinea)'),
    'fr_LU': ugettext_lazy(u'French (Luxembourg)'),
    'fr_MG': ugettext_lazy(u'French (Madagascar)'),
    'fr_ML': ugettext_lazy(u'French (Mali)'),
    'fr_MQ': ugettext_lazy(u'French (Martinique)'),
    'fr_MC': ugettext_lazy(u'French (Monaco)'),
    'fr_NE': ugettext_lazy(u'French (Niger)'),
    'fr_RW': ugettext_lazy(u'French (Rwanda)'),
    'fr_RE': ugettext_lazy(u'French (Réunion)'),
    'fr_BL': ugettext_lazy(u'French (Saint Barthélemy)'),
    'fr_MF': ugettext_lazy(u'French (Saint Martin)'),
    'fr_SN': ugettext_lazy(u'French (Senegal)'),
    'fr_CH': ugettext_lazy(u'French (Switzerland)'),
    'fr_TG': ugettext_lazy(u'French (Togo)'),
    'fr': ugettext_lazy(u'French'),
    'ff_SN': ugettext_lazy(u'Fulah (Senegal)'),
    'ff': ugettext_lazy(u'Fulah'),
    'gl_ES': ugettext_lazy(u'Galician (Spain)'),
    'gl': ugettext_lazy(u'Galician'),
    'lg_UG': ugettext_lazy(u'Ganda (Uganda)'),
    'lg': ugettext_lazy(u'Ganda'),
    'ka_GE': ugettext_lazy(u'Georgian (Georgia)'),
    'ka': ugettext_lazy(u'Georgian'),
    'de_AT': ugettext_lazy(u'German (Austria)'),
    'de_BE': ugettext_lazy(u'German (Belgium)'),
    'de_DE': ugettext_lazy(u'German (Germany)'),
    'de_LI': ugettext_lazy(u'German (Liechtenstein)'),
    'de_LU': ugettext_lazy(u'German (Luxembourg)'),
    'de_CH': ugettext_lazy(u'German (Switzerland)'),
    'de': ugettext_lazy(u'German'),
    'el_CY': ugettext_lazy(u'Greek (Cyprus)'),
    'el_GR': ugettext_lazy(u'Greek (Greece)'),
    'el': ugettext_lazy(u'Greek'),
    'gu_IN': ugettext_lazy(u'Gujarati (India)'),
    'gu': ugettext_lazy(u'Gujarati'),
    'guz_KE': ugettext_lazy(u'Gusii (Kenya)'),
    'guz': ugettext_lazy(u'Gusii'),
    'ha_Latn': ugettext_lazy(u'Hausa (Latin)'),
    'ha_Latn_GH': ugettext_lazy(u'Hausa (Latin, Ghana)'),
    'ha_Latn_NE': ugettext_lazy(u'Hausa (Latin, Niger)'),
    'ha_Latn_NG': ugettext_lazy(u'Hausa (Latin, Nigeria)'),
    'ha': ugettext_lazy(u'Hausa'),
    'haw_US': ugettext_lazy(u'Hawaiian (United States)'),
    'haw': ugettext_lazy(u'Hawaiian'),
    'he_IL': ugettext_lazy(u'Hebrew (Israel)'),
    'he': ugettext_lazy(u'Hebrew'),
    'hi_IN': ugettext_lazy(u'Hindi (India)'),
    'hi': ugettext_lazy(u'Hindi'),
    'hu_HU': ugettext_lazy(u'Hungarian (Hungary)'),
    'hu': ugettext_lazy(u'Hungarian'),
    'is_IS': ugettext_lazy(u'Icelandic (Iceland)'),
    'is': ugettext_lazy(u'Icelandic'),
    'ig_NG': ugettext_lazy(u'Igbo (Nigeria)'),
    'ig': ugettext_lazy(u'Igbo'),
    'id_ID': ugettext_lazy(u'Indonesian (Indonesia)'),
    'id': ugettext_lazy(u'Indonesian'),
    'ga_IE': ugettext_lazy(u'Irish (Ireland)'),
    'ga': ugettext_lazy(u'Irish'),
    'it_IT': ugettext_lazy(u'Italian (Italy)'),
    'it_CH': ugettext_lazy(u'Italian (Switzerland)'),
    'it': ugettext_lazy(u'Italian'),
    'ja_JP': ugettext_lazy(u'Japanese (Japan)'),
    'ja': ugettext_lazy(u'Japanese'),
    'kea_CV': ugettext_lazy(u'Kabuverdianu (Cape Verde)'),
    'kea': ugettext_lazy(u'Kabuverdianu'),
    'kab_DZ': ugettext_lazy(u'Kabyle (Algeria)'),
    'kab': ugettext_lazy(u'Kabyle'),
    'kl_GL': ugettext_lazy(u'Kalaallisut (Greenland)'),
    'kl': ugettext_lazy(u'Kalaallisut'),
    'kln_KE': ugettext_lazy(u'Kalenjin (Kenya)'),
    'kln': ugettext_lazy(u'Kalenjin'),
    'kam_KE': ugettext_lazy(u'Kamba (Kenya)'),
    'kam': ugettext_lazy(u'Kamba'),
    'kn_IN': ugettext_lazy(u'Kannada (India)'),
    'kn': ugettext_lazy(u'Kannada'),
    'kk_Cyrl': ugettext_lazy(u'Kazakh (Cyrillic)'),
    'kk_Cyrl_KZ': ugettext_lazy(u'Kazakh (Cyrillic, Kazakhstan)'),
    'kk': ugettext_lazy(u'Kazakh'),
    'km_KH': ugettext_lazy(u'Khmer (Cambodia)'),
    'km': ugettext_lazy(u'Khmer'),
    'ki_KE': ugettext_lazy(u'Kikuyu (Kenya)'),
    'ki': ugettext_lazy(u'Kikuyu'),
    'rw_RW': ugettext_lazy(u'Kinyarwanda (Rwanda)'),
    'rw': ugettext_lazy(u'Kinyarwanda'),
    'kok_IN': ugettext_lazy(u'Konkani (India)'),
    'kok': ugettext_lazy(u'Konkani'),
    'ko_KR': ugettext_lazy(u'Korean (South Korea)'),
    'ko': ugettext_lazy(u'Korean'),
    'khq_ML': ugettext_lazy(u'Koyra Chiini (Mali)'),
    'khq': ugettext_lazy(u'Koyra Chiini'),
    'ses_ML': ugettext_lazy(u'Koyraboro Senni (Mali)'),
    'ses': ugettext_lazy(u'Koyraboro Senni'),
    'lag_TZ': ugettext_lazy(u'Langi (Tanzania)'),
    'lag': ugettext_lazy(u'Langi'),
    'lv_LV': ugettext_lazy(u'Latvian (Latvia)'),
    'lv': ugettext_lazy(u'Latvian'),
    'lt_LT': ugettext_lazy(u'Lithuanian (Lithuania)'),
    'lt': ugettext_lazy(u'Lithuanian'),
    'luo_KE': ugettext_lazy(u'Luo (Kenya)'),
    'luo': ugettext_lazy(u'Luo'),
    'luy_KE': ugettext_lazy(u'Luyia (Kenya)'),
    'luy': ugettext_lazy(u'Luyia'),
    'mk_MK': ugettext_lazy(u'Macedonian (Macedonia)'),
    'mk': ugettext_lazy(u'Macedonian'),
    'jmc_TZ': ugettext_lazy(u'Machame (Tanzania)'),
    'jmc': ugettext_lazy(u'Machame'),
    'kde_TZ': ugettext_lazy(u'Makonde (Tanzania)'),
    'kde': ugettext_lazy(u'Makonde'),
    'mg_MG': ugettext_lazy(u'Malagasy (Madagascar)'),
    'mg': ugettext_lazy(u'Malagasy'),
    'ms_BN': ugettext_lazy(u'Malay (Brunei)'),
    'ms_MY': ugettext_lazy(u'Malay (Malaysia)'),
    'ms': ugettext_lazy(u'Malay'),
    'ml_IN': ugettext_lazy(u'Malayalam (India)'),
    'ml': ugettext_lazy(u'Malayalam'),
    'mt_MT': ugettext_lazy(u'Maltese (Malta)'),
    'mt': ugettext_lazy(u'Maltese'),
    'gv_GB': ugettext_lazy(u'Manx (United Kingdom)'),
    'gv': ugettext_lazy(u'Manx'),
    'mr_IN': ugettext_lazy(u'Marathi (India)'),
    'mr': ugettext_lazy(u'Marathi'),
    'mas_KE': ugettext_lazy(u'Masai (Kenya)'),
    'mas_TZ': ugettext_lazy(u'Masai (Tanzania)'),
    'mas': ugettext_lazy(u'Masai'),
    'mer_KE': ugettext_lazy(u'Meru (Kenya)'),
    'mer': ugettext_lazy(u'Meru'),
    'mfe_MU': ugettext_lazy(u'Morisyen (Mauritius)'),
    'mfe': ugettext_lazy(u'Morisyen'),
    'naq_NA': ugettext_lazy(u'Nama (Namibia)'),
    'naq': ugettext_lazy(u'Nama'),
    'ne_IN': ugettext_lazy(u'Nepali (India)'),
    'ne_NP': ugettext_lazy(u'Nepali (Nepal)'),
    'ne': ugettext_lazy(u'Nepali'),
    'nd_ZW': ugettext_lazy(u'North Ndebele (Zimbabwe)'),
    'nd': ugettext_lazy(u'North Ndebele'),
    'nb_NO': ugettext_lazy(u'Norwegian Bokmål (Norway)'),
    'nb': ugettext_lazy(u'Norwegian Bokmål'),
    'nn_NO': ugettext_lazy(u'Norwegian Nynorsk (Norway)'),
    'nn': ugettext_lazy(u'Norwegian Nynorsk'),
    'nyn_UG': ugettext_lazy(u'Nyankole (Uganda)'),
    'nyn': ugettext_lazy(u'Nyankole'),
    'or_IN': ugettext_lazy(u'Oriya (India)'),
    'or': ugettext_lazy(u'Oriya'),
    'om_ET': ugettext_lazy(u'Oromo (Ethiopia)'),
    'om_KE': ugettext_lazy(u'Oromo (Kenya)'),
    'om': ugettext_lazy(u'Oromo'),
    'ps_AF': ugettext_lazy(u'Pashto (Afghanistan)'),
    'ps': ugettext_lazy(u'Pashto'),
    'fa_AF': ugettext_lazy(u'Persian (Afghanistan)'),
    'fa_IR': ugettext_lazy(u'Persian (Iran)'),
    'fa': ugettext_lazy(u'Persian'),
    'pl_PL': ugettext_lazy(u'Polish (Poland)'),
    'pl': ugettext_lazy(u'Polish'),
    'pt_BR': ugettext_lazy(u'Portuguese (Brazil)'),
    'pt_GW': ugettext_lazy(u'Portuguese (Guinea-Bissau)'),
    'pt_MZ': ugettext_lazy(u'Portuguese (Mozambique)'),
    'pt_PT': ugettext_lazy(u'Portuguese (Portugal)'),
    'pt': ugettext_lazy(u'Portuguese'),
    'pa_Arab': ugettext_lazy(u'Punjabi (Arabic)'),
    'pa_Arab_PK': ugettext_lazy(u'Punjabi (Arabic, Pakistan)'),
    'pa_Guru': ugettext_lazy(u'Punjabi (Gurmukhi)'),
    'pa_Guru_IN': ugettext_lazy(u'Punjabi (Gurmukhi, India)'),
    'pa': ugettext_lazy(u'Punjabi'),
    'ro_MD': ugettext_lazy(u'Romanian (Moldova)'),
    'ro_RO': ugettext_lazy(u'Romanian (Romania)'),
    'ro': ugettext_lazy(u'Romanian'),
    'rm_CH': ugettext_lazy(u'Romansh (Switzerland)'),
    'rm': ugettext_lazy(u'Romansh'),
    'rof_TZ': ugettext_lazy(u'Rombo (Tanzania)'),
    'rof': ugettext_lazy(u'Rombo'),
    'ru_MD': ugettext_lazy(u'Russian (Moldova)'),
    'ru_RU': ugettext_lazy(u'Russian (Russia)'),
    'ru_UA': ugettext_lazy(u'Russian (Ukraine)'),
    'ru': ugettext_lazy(u'Russian'),
    'rwk_TZ': ugettext_lazy(u'Rwa (Tanzania)'),
    'rwk': ugettext_lazy(u'Rwa'),
    'saq_KE': ugettext_lazy(u'Samburu (Kenya)'),
    'saq': ugettext_lazy(u'Samburu'),
    'sg_CF': ugettext_lazy(u'Sango (Central African Republic)'),
    'sg': ugettext_lazy(u'Sango'),
    'seh_MZ': ugettext_lazy(u'Sena (Mozambique)'),
    'seh': ugettext_lazy(u'Sena'),
    'sr_Cyrl': ugettext_lazy(u'Serbian (Cyrillic)'),
    'sr_Cyrl_BA': ugettext_lazy(u'Serbian (Cyrillic, Bosnia and Herzegovina)'),
    'sr_Cyrl_ME': ugettext_lazy(u'Serbian (Cyrillic, Montenegro)'),
    'sr_Cyrl_RS': ugettext_lazy(u'Serbian (Cyrillic, Serbia)'),
    'sr_Latn': ugettext_lazy(u'Serbian (Latin)'),
    'sr_Latn_BA': ugettext_lazy(u'Serbian (Latin, Bosnia and Herzegovina)'),
    'sr_Latn_ME': ugettext_lazy(u'Serbian (Latin, Montenegro)'),
    'sr_Latn_RS': ugettext_lazy(u'Serbian (Latin, Serbia)'),
    'sr': ugettext_lazy(u'Serbian'),
    'sn_ZW': ugettext_lazy(u'Shona (Zimbabwe)'),
    'sn': ugettext_lazy(u'Shona'),
    'ii_CN': ugettext_lazy(u'Sichuan Yi (China)'),
    'ii': ugettext_lazy(u'Sichuan Yi'),
    'si_LK': ugettext_lazy(u'Sinhala (Sri Lanka)'),
    'si': ugettext_lazy(u'Sinhala'),
    'sk_SK': ugettext_lazy(u'Slovak (Slovakia)'),
    'sk': ugettext_lazy(u'Slovak'),
    'sl_SI': ugettext_lazy(u'Slovenian (Slovenia)'),
    'sl': ugettext_lazy(u'Slovenian'),
    'xog_UG': ugettext_lazy(u'Soga (Uganda)'),
    'xog': ugettext_lazy(u'Soga'),
    'so_DJ': ugettext_lazy(u'Somali (Djibouti)'),
    'so_ET': ugettext_lazy(u'Somali (Ethiopia)'),
    'so_KE': ugettext_lazy(u'Somali (Kenya)'),
    'so_SO': ugettext_lazy(u'Somali (Somalia)'),
    'so': ugettext_lazy(u'Somali'),
    'es_AR': ugettext_lazy(u'Spanish (Argentina)'),
    'es_BO': ugettext_lazy(u'Spanish (Bolivia)'),
    'es_CL': ugettext_lazy(u'Spanish (Chile)'),
    'es_CO': ugettext_lazy(u'Spanish (Colombia)'),
    'es_CR': ugettext_lazy(u'Spanish (Costa Rica)'),
    'es_DO': ugettext_lazy(u'Spanish (Dominican Republic)'),
    'es_EC': ugettext_lazy(u'Spanish (Ecuador)'),
    'es_SV': ugettext_lazy(u'Spanish (El Salvador)'),
    'es_GQ': ugettext_lazy(u'Spanish (Equatorial Guinea)'),
    'es_GT': ugettext_lazy(u'Spanish (Guatemala)'),
    'es_HN': ugettext_lazy(u'Spanish (Honduras)'),
    'es_419': ugettext_lazy(u'Spanish (Latin America)'),
    'es_MX': ugettext_lazy(u'Spanish (Mexico)'),
    'es_NI': ugettext_lazy(u'Spanish (Nicaragua)'),
    'es_PA': ugettext_lazy(u'Spanish (Panama)'),
    'es_PY': ugettext_lazy(u'Spanish (Paraguay)'),
    'es_PE': ugettext_lazy(u'Spanish (Peru)'),
    'es_PR': ugettext_lazy(u'Spanish (Puerto Rico)'),
    'es_ES': ugettext_lazy(u'Spanish (Spain)'),
    'es_US': ugettext_lazy(u'Spanish (United States)'),
    'es_UY': ugettext_lazy(u'Spanish (Uruguay)'),
    'es_VE': ugettext_lazy(u'Spanish (Venezuela)'),
    'es': ugettext_lazy(u'Spanish'),
    'sw_KE': ugettext_lazy(u'Swahili (Kenya)'),
    'sw_TZ': ugettext_lazy(u'Swahili (Tanzania)'),
    'sw': ugettext_lazy(u'Swahili'),
    'sv_FI': ugettext_lazy(u'Swedish (Finland)'),
    'sv_SE': ugettext_lazy(u'Swedish (Sweden)'),
    'sv': ugettext_lazy(u'Swedish'),
    'gsw_CH': ugettext_lazy(u'Swiss German (Switzerland)'),
    'gsw': ugettext_lazy(u'Swiss German'),
    'shi_Latn': ugettext_lazy(u'Tachelhit (Latin)'),
    'shi_Latn_MA': ugettext_lazy(u'Tachelhit (Latin, Morocco)'),
    'shi_Tfng': ugettext_lazy(u'Tachelhit (Tifinagh)'),
    'shi_Tfng_MA': ugettext_lazy(u'Tachelhit (Tifinagh, Morocco)'),
    'shi': ugettext_lazy(u'Tachelhit'),
    'dav_KE': ugettext_lazy(u'Taita (Kenya)'),
    'dav': ugettext_lazy(u'Taita'),
    'ta_IN': ugettext_lazy(u'Tamil (India)'),
    'ta_LK': ugettext_lazy(u'Tamil (Sri Lanka)'),
    'ta': ugettext_lazy(u'Tamil'),
    'te_IN': ugettext_lazy(u'Telugu (India)'),
    'te': ugettext_lazy(u'Telugu'),
    'teo_KE': ugettext_lazy(u'Teso (Kenya)'),
    'teo_UG': ugettext_lazy(u'Teso (Uganda)'),
    'teo': ugettext_lazy(u'Teso'),
    'th_TH': ugettext_lazy(u'Thai (Thailand)'),
    'th': ugettext_lazy(u'Thai'),
    'bo_CN': ugettext_lazy(u'Tibetan (China)'),
    'bo_IN': ugettext_lazy(u'Tibetan (India)'),
    'bo': ugettext_lazy(u'Tibetan'),
    'ti_ER': ugettext_lazy(u'Tigrinya (Eritrea)'),
    'ti_ET': ugettext_lazy(u'Tigrinya (Ethiopia)'),
    'ti': ugettext_lazy(u'Tigrinya'),
    'to_TO': ugettext_lazy(u'Tonga (Tonga)'),
    'to': ugettext_lazy(u'Tonga'),
    'tr_TR': ugettext_lazy(u'Turkish (Turkey)'),
    'tr': ugettext_lazy(u'Turkish'),
    'uk_UA': ugettext_lazy(u'Ukrainian (Ukraine)'),
    'uk': ugettext_lazy(u'Ukrainian'),
    'ur_IN': ugettext_lazy(u'Urdu (India)'),
    'ur_PK': ugettext_lazy(u'Urdu (Pakistan)'),
    'ur': ugettext_lazy(u'Urdu'),
    'uz_Arab': ugettext_lazy(u'Uzbek (Arabic)'),
    'uz_Arab_AF': ugettext_lazy(u'Uzbek (Arabic, Afghanistan)'),
    'uz_Cyrl': ugettext_lazy(u'Uzbek (Cyrillic)'),
    'uz_Cyrl_UZ': ugettext_lazy(u'Uzbek (Cyrillic, Uzbekistan)'),
    'uz_Latn': ugettext_lazy(u'Uzbek (Latin)'),
    'uz_Latn_UZ': ugettext_lazy(u'Uzbek (Latin, Uzbekistan)'),
    'uz': ugettext_lazy(u'Uzbek'),
    'vi_VN': ugettext_lazy(u'Vietnamese (Vietnam)'),
    'vi': ugettext_lazy(u'Vietnamese'),
    'vun_TZ': ugettext_lazy(u'Vunjo (Tanzania)'),
    'vun': ugettext_lazy(u'Vunjo'),
    'cy_GB': ugettext_lazy(u'Welsh (United Kingdom)'),
    'cy': ugettext_lazy(u'Welsh'),
    'yo_NG': ugettext_lazy(u'Yoruba (Nigeria)'),
    'yo': ugettext_lazy(u'Yoruba'),
    'zu_ZA': ugettext_lazy(u'Zulu (South Africa)'),
    'zu': ugettext_lazy(u'Zulu'),
}
